# -*- coding: utf-8 -*-
import json

import datetime
import re

from scrapy import Selector

from trivest_spider import getTableByName


def getDetailList(pageIndex):
    table = getTableByName('baike_citiao_detail_new')
    return table.select(table.name).paginate(pageIndex, 1000)


def circleRun(operate):
    pageIndex = 1
    while True:
        if operate(pageIndex):
            print 'end', pageIndex
            break
        print 'pageIndex', pageIndex
        pageIndex += 1


def operate(pageIndex):
    dataList = getDetailList(pageIndex)
    if not dataList:
        return True
    # if pageIndex > 120:
    #     return True
    for item in dataList:
        name = item.name
        parent_type = ''
        type_name = ''
        ciTiaoTable = getTableByName('baike_citiao')
        ciTiaoResults = ciTiaoTable.select().where(ciTiaoTable.name == name)
        if ciTiaoResults:
            type_name = ciTiaoResults[0].type_name
            typeTable = getTableByName('baike_type')
            typeResults = typeTable.select().where(typeTable.name == type_name)
            if typeResults:
                parent_type = typeResults[0].parent
        detailTable = getTableByName('baike_citiao_detail_new')
        detailTable.update(type_name=type_name, parent_type=parent_type).where(detailTable.name == name).execute()
        print name, type_name, parent_type


if __name__ == '__main__':
    circleRun(operate)
    # def isChinese(checkValue):
    #     return not any(char.isdigit() or char.isalpha() for char in checkValue)
    #
    #
    # print isChinese(u'你好'.encode('utf8'))
