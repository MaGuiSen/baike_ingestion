# -*- coding: utf-8 -*-
# 项目唯一标识，分布式，不同的项目思考(规则：项目名称!@项目部署位置!@部署时间!@ 1000-9999的随机数）
projectIdentify = 'baike_spider!@xiamen!@2017-10-19 13:52!@2211'

# key为spider的名称 此配置和数据库：spider_monitor字段一致
spiderDetails = {
    'wei_bai_ke': {
        'table_name': 'baike_detail',
        'table_name_zh': u'百科详情',
        'spider_name': 'wei_bai_ke',
        'spider_name_zh': u'微百科'
    },
    'bai_ke_type': {
        'table_name': 'baike_type',
        'table_name_zh': u'百科分类',
        'spider_name': 'bai_ke_type',
        'spider_name_zh': u'百科分类'
    }
}


def getSpiderDetail(spiderName):
    return spiderDetails.get(spiderName, {})