# -*- coding: utf-8 -*-

import scrapy
from base_spider import BaseSpider


class BaiKeTypeSpider(BaseSpider):
    # 错误码中302是处理重定向的，可以不写，因为写了可能导致404无法回掉，写在外部
    handle_httpstatus_list = [204, 206, 301, 400, 403, 404, 500]
    name = 'bai_ke_type'
    custom_settings = {
        'download_delay': 2.5,
        'ITEM_PIPELINES': {
            'trivest_spider.pipelines.BaiKeTypePipeline': 50,
        },
    }

    def __init__(self, name=None, **kwargs):
        super(BaiKeTypeSpider, self).__init__(name=None, **kwargs)

    def close(self, reason):
        # 做一些操作
        self.afterClose()

    def start_requests(self):
        # 做一些操作
        self.beforeRequest()

        if not self.wait_utils_env_ok():
            self.logWarn(u'环境不可行，退出当前抓取')
            return

        url = 'http://fenlei.baike.com/'
        self.logInfo(u"开始抓取列表：" + url)
        yield scrapy.Request(url=url,
                             meta={
                                 'request_type': self.name
                             },
                             callback=self.parseDetail, dont_filter=True)

    def parseDetail(self, response):
        level_first = response.xpath('//*[@class="sort"]/dd/a/text()').extract()
        types = []
        existTypes = []

        def typeIn(name, parent):
            if name and name not in existTypes:
                existTypes.append(name)
                types.append({
                    'name': name,
                    'parent': parent
                })

        for level in level_first:
            typeIn(level, '')

        level_table_rows = response.xpath('//*[@class="bor-e1 table"]')
        for level_table_row in level_table_rows:
            level_first_str = level_table_row.xpath('./div[contains(@class, "td w-39 h")]/text()').extract_first('')
            typeIn(level_first_str, '')

            level_seconds = level_table_row.xpath('./div/dl')
            for level_second in level_seconds:
                level_second_str = level_second.xpath('./dt/a/text()').extract_first('')
                typeIn(level_second_str, level_first_str)

                level_thirds = level_second.xpath('./dd/a/text()').extract()
                for level_third_str in level_thirds:
                    print level_first_str, level_second_str, level_third_str
                    typeIn(level_third_str, level_first_str+'-'+level_second_str)

        for typeItem in types:
            yield typeItem

        pass