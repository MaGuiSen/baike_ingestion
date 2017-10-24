# -*- coding: utf-8 -*-
import json

import scrapy

from base_spider import BaseSpider
from trivest_data.dal.trivest_spider import getTableByName


class BaiKeCiTiaoSpider(BaseSpider):
    handle_httpstatus_list = [204, 206, 301, 400, 403, 404, 500] # 错误码中302是处理重定向的，可以不写，因为写了可能导致404无法回掉，写在外部
    name = 'bai_ke_ci_tiao'
    custom_settings = {
        'download_delay': 2.5,
        'ITEM_PIPELINES': {
            'trivest_spider.pipelines.BaiKeCiTiaoPipeline': 50,
        },
    }

    def __init__(self, name=None, **kwargs):
        super(BaiKeCiTiaoSpider, self).__init__(name=None, **kwargs)
        self.existCiTiao = []

    def close(self, reason):
        # 做一些操作
        self.afterClose()

    def start_requests(self):
        # 做一些操作
        self.beforeRequest()

        if not self.wait_utils_env_ok():
            self.logWarn(u'环境不可行，退出当前抓取')
            return

        # 得到type
        types = getTableByName('baike_type').select()
        for type in types:
            url = 'http://fenlei.baike.com/%s/list/' % type.name
            self.logInfo(u"开始抓取列表：" + url)
            yield scrapy.Request(url=url,
                                 meta={
                                     'request_type': self.name,
                                     'typeName': type.name
                                 },
                                 callback=self.parseDetail, dont_filter=True)

    def parseDetail(self, response):
        typeName = response.meta['typeName']
        list = response.xpath('//div[@class="content"]//dd/a')
        for item in list:
            name = item.xpath('./text()').extract_first('')
            if name and name not in self.existCiTiao:
                self.existCiTiao.append(name)
                content = {
                    'name': name,
                    'url': '',
                    'type_name': typeName,
                    'catch_status': ''
                }
                yield content
        pass
