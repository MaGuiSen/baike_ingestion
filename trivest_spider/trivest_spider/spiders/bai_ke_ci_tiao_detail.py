# -*- coding: utf-8 -*-
import json

import scrapy

from base_spider import BaseSpider
from trivest_data.dal.trivest_spider import getTableByName
from trivest_data.dal.StatusDao import CiTiaoStatusDao


class BaiKeCiTiaoDetailSpider(BaseSpider):
    handle_httpstatus_list = [204, 206, 301, 400, 403, 404, 500] # 错误码中302是处理重定向的，可以不写，因为写了可能导致404无法回掉，写在外部
    name = 'bai_ke_ci_tiao_detail'
    custom_settings = {
        'download_delay': 2.5,
        'ITEM_PIPELINES': {
            'trivest_spider.pipelines.BaiKeCiTiaoDetailPipeline': 50,
        },
    }

    def __init__(self, name=None, **kwargs):
        super(BaiKeCiTiaoDetailSpider,                                                                                                                                                                                                                                                                                                                                             self).__init__(name=None, **kwargs)
        self.existCiTiao = []
        self.ciTiaoStatusDao = CiTiaoStatusDao()

    def close(self, reason):
        # 做一些操作
        self.afterClose()

    def start_requests(self):
        # 做一些操作
        self.beforeRequest()

        if not self.wait_utils_env_ok():
            self.logWarn(u'环境不可行，退出当前抓取')
            return

        # 得到词条
        pageIndex = 1
        while True:
            catchList = self.ciTiaoStatusDao.getCatchList(pageIndex)
            if not len(catchList):
                print 'end'
                break
            for item in catchList:
                ciTiaoName = item.name
                self.ciTiaoStatusDao.updateStatus(ciTiaoName, self.ciTiaoStatusDao.Status_start_request)
                url = 'http://www.baike.com/wiki/%s' % ciTiaoName
                self.logInfo(u"开始抓取：" + url)
                yield scrapy.Request(url=url,
                                     meta={
                                         'request_type': self.name,
                                         'ciTiaoName': ciTiaoName
                                     },
                                     callback=self.parseDetail, dont_filter=True)
            pageIndex += 1

    def parseDetail(self, response):
        ciTiaoName = response.meta['ciTiaoName']

        url = response.url
        status = response.status
        if status == 403:
            self.ciTiaoStatusDao.updateStatus(ciTiaoName, self.ciTiaoStatusDao.Status_be_forbid)
        elif 'so.baike.com' in url:
            self.ciTiaoStatusDao.updateStatus(ciTiaoName, self.ciTiaoStatusDao.Status_no_source)
        else:
            openType = response.xpath('//*[@id="openCatp"]/a/text()').extract()
            openType = ','.join(openType)
            summary = response.xpath('//*[@id="anchor"]//text()').extract()
            summary = ''.join(summary).strip().replace(u'编辑摘要', '')

            baseInfoObj = {}
            baseInfoTable = response.xpath('//*[@id="datamodule"]//td')
            for baseInfo in baseInfoTable:
                key = baseInfo.xpath('./strong//text()').extract()
                key = ''.join(key).replace(' ', '').strip()

                value = baseInfo.xpath('./span//text()').extract()
                value = ''.join(value).replace(' ', '').strip()
                if key and value:
                    baseInfoObj[key] = value
            baseInfo = json.dumps(baseInfoObj, ensure_ascii=False)

            if summary or baseInfo:
                yield {
                    'name': ciTiaoName,
                    'open_type': openType,
                    'summary': summary,
                    'base_info': baseInfo
                }
            else:
                self.ciTiaoStatusDao.updateStatus(ciTiaoName, self.ciTiaoStatusDao.Status_no_complete_data)






