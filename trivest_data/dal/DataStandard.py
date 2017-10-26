# -*- coding: utf-8 -*-
import json

import datetime

from scrapy import Selector

from trivest_spider import getTableByName


def getDetailList(pageIndex):
    table = getTableByName('baike_citiao_detail')
    return table.select().paginate(pageIndex, 100)


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
    for item in dataList:
        detailName = item.detail_name
        summary = item.summary
        baseInfo = item.base_info
        baseInfoObj = json.loads(baseInfo)
        # 毕业院校： 毕业于***
        # 去世日期： 没活过1971年4月29日
        # 职业：职业是***
        # 代表作品： 代表作品有
        # 出生地： 出生于 **
        # 主要成就： **
        # 星座： **
        # 别名：别名**
        # 又名：也叫**
        # 主要荣誉：
        # 发明者： **发明了它
        # 跆拳道精神： 跆拳道精神是***
        # 创始人：	创始人是**
        # 创建人： 创建人是**
        # 建立时间：建成于**
        # 地理位置： 位于**
        # 所在地： 位于**
        # 遗产级别：是**
        # 遗产编号： 遗产编号是
        # 车牌代码： 车牌代码是**
        # 临床表现： 	临床表现有**
        # 景区等级：是***景区

        replys = []

        words = [
            {'key': u'毕业院校：','valueContent': u'TA毕业于{**}'},
            {'key': u'去世日期：', 'valueContent': u'TA没活过{**}这天'},
            {'key': u'职业：', 'valueContent': u'TA的职业是{**}'},
            {'key': u'代表作品：', 'valueContent': u'TA的代表作品有{**}'},
            {'key': u'出生地：', 'valueContent': u'TA出生于{**}'},
            {'key': u'主要成就：', 'valueContent': u'TA主要成就有{**}'},
            {'key': u'星座：', 'valueContent': u'TA的星座是{**}'},
            {'key': u'别名：', 'valueContent': u'TA也叫{**}'},
            {'key': u'又名：', 'valueContent': u'TA也叫{**}'},
            {'key': u'主要荣誉：', 'valueContent': u'TA主要荣誉有{**}'},
            {'key': u'发明者：', 'valueContent': u'{**}发明了它'},
            {'key': u'创始人：', 'valueContent': u'创始人是{**}'},
            {'key': u'创建人：', 'valueContent': u'创建人是{**}'},
            {'key': u'建立时间：', 'valueContent': u'建成于{**}'},
            {'key': u'地理位置：', 'valueContent': u'位于{**}'},
            {'key': u'所在地：', 'valueContent': u'位于{**}'},
            {'key': u'遗产级别：', 'valueContent': u'是{**}'},
            {'key': u'遗产编号：', 'valueContent': u'遗产编号是{**}'},
            {'key': u'车牌代码：', 'valueContent': u'车牌代码是{**}'},
            {'key': u'临床表现：', 'valueContent': u'临床表现有{**}'},
            {'key': u'景区等级：', 'valueContent': u'是{**}景区'},
        ]

        for word in words:
            key = word['key']
            valueContent = word['valueContent']
            value = baseInfoObj.get('key')
            if value:
                valueNew = valueContent.replace('{**}', value)
                replys.append(valueNew)

        # 处理summary
        if not summary or u'请用一段简单的话描述' in summary:
            pass
        else:
            # 取第一句
            if len(summary) > 30:
                summarys = summary.split(u'。')
                replys.append(summarys[0] + u'。')
            else:
                replys.append(summary)
                pass

        for reply in replys:
            print u'问: ', detailName
            print u'回答: ', reply
            print ''


if __name__ == '__main__':
    circleRun(operate)
