# -*- coding: utf-8 -*-
import json

import datetime
import re

from scrapy import Selector

from trivest_spider import getTableByName


def getDetailList(pageIndex):
    table = getTableByName('baike_citiao_detail')
    return table.select().where(table.id > 131572).paginate(pageIndex, 1000)


def circleRun(operate):
    pageIndex = 13
    while True:
        if operate(pageIndex):
            print 'end', pageIndex
            break
        print 'pageIndex', pageIndex
        pageIndex += 1


def operate(pageIndex):
    dataList = getDetailList(pageIndex)
    # if not dataList:
    #     return True
    if pageIndex > 26:
        return True
    for item in dataList:
        name = item.name
        detailName = item.detail_name.replace(' ', '').strip()
        summary = item.summary
        open_type = item.open_type
        baseInfo = item.base_info
        baseInfoObj = json.loads(baseInfo)
        # 毕业院校： 毕业于***
        # 去世日期： 没活过1971年4月29日
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
            {'key': u'含义：', 'valueContent': [u'{**}']},
            {'key': u'完整说法：', 'valueContent': [u'{**}']},
            {'key': u'帖子标题：', 'valueContent': [u'{**}']},
            {'key': u'释义：', 'valueContent': [u'{**}']},
            {'key': u'毕业院校：', 'valueContent': [u'Ta毕业于{**}']},
            {'key': u'代表作品：', 'valueContent': [u'Ta的代表作品有{**}']},
            {'key': u'出生地：', 'valueContent': [u'Ta出生于{**}']},
            {'key': u'主要成就：', 'valueContent': [u'Ta主要成就有{**}']},
            {'key': u'星座：', 'valueContent': [u'Ta的星座是{**}']},
            {'key': u'别名：', 'valueContent': [u'Ta也叫{**}', u'你也可以叫Ta{**}']},
            {'key': u'又名：', 'valueContent': [u'Ta也叫{**}', u'你也可以叫Ta{**}']},
            {'key': u'主要荣誉：', 'valueContent': [u'TA主要荣誉有{**}']},
            {'key': u'发明者：', 'valueContent': [u'{**}发明了它']},
            {'key': u'创始人：', 'valueContent': [u'Ta的创始人是{**}']},
            {'key': u'创建人：', 'valueContent': [u'Ta的创建人是{**}']},
            {'key': u'建立时间：', 'valueContent': [u'建成于{**}']},
            {'key': u'地理位置：', 'valueContent': [u'位于{**}']},
            {'key': u'所在地：', 'valueContent': [u'位于{**}']},
            {'key': u'遗产级别：', 'valueContent': [u'是{**}']},
            {'key': u'遗产编号：', 'valueContent': [u'遗产编号是{**}']},
            {'key': u'车牌代码：', 'valueContent': [u'车牌代码是{**}']},
            {'key': u'临床表现：', 'valueContent': [u'临床表现有{**}']},
            {'key': u'景区等级：', 'valueContent': [u'是{**}景区']},
        ]

        typeRemoves = [
            u'中华人民共和国领导人',
            u'中国共产党员',
            u'政治人物',
            u'官员',
            u'各国政治人物',
            u'中国政治人物',
            u'国家元首',
            u'总理',
            u'中国共产党',
            u'政党',
            u'政府组织',
            u'政治',
            u'政治组织',
            u'书籍',  # 书籍去掉
        ]

        # 去掉不要的类型
        # 科学家
        # 科技产品
        # 政治人物
        # 社会
        # 体育设施
        # 饮食
        # 健康
        # 时尚
        # 社会科学人物
        # 自然科学人物

        removeCiTiaoTypes = [
            u'科学家',
            u'科技产品',
            u'政治人物',
            u'自然科学人物',
            u'社会科学人物',
            u'饮食',
            u'健康',
            u'时尚',
            u'社会',
            u'体育设施',
        ]
        ciTiaoTable = getTableByName('baike_citiao')
        ciTiaoResults = ciTiaoTable.select().where(ciTiaoTable.name == name)
        isNeedRemoveCiTiao = False
        if ciTiaoResults:
            type_name = ciTiaoResults[0].type_name
            if type_name in removeCiTiaoTypes:
                print u'移除不要的分类', type_name, detailName, open_type
                isNeedRemoveCiTiao = True
            else:
                typeTable = getTableByName('baike_type')
                typeResults = typeTable.select().where(typeTable.name == type_name)
                if typeResults:
                    parents = typeResults[0].parent.split('-')
                    for parent in parents:
                        if parent in removeCiTiaoTypes:
                            isNeedRemoveCiTiao = True
                            print u'移除不要的分类', type_name, parent, detailName, open_type
                            break
        if isNeedRemoveCiTiao:
            continue


        # 包含数字，或者字母的去掉
        def isNotChinese(checkValue):
            return any(char.isdigit() or char.isalpha() for char in checkValue)

        if isNotChinese(detailName.encode('utf8')):
            print u'移除', u'带有字母数字', detailName, open_type
            continue

        # 书籍去掉 《》
        if detailName.startswith(u'《') or detailName.endswith(u'》'):
            print u'移除', u'书籍', detailName, open_type
            continue

        needRemove = False
        for typeRemove in typeRemoves:
            if typeRemove in open_type:
                print u'移除', typeRemove, detailName, open_type
                needRemove = True
                break
        if needRemove:
            continue

        for word in words:
            key = word['key']
            valueContent = word['valueContent']
            value = baseInfoObj.get(key)
            if value:
                for valueReplace in valueContent:
                    valueNew = valueReplace.replace('{**}', value)
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
        print '========', detailName, '========== start'
        for reply in replys:
            print u'问: ', detailName
            print u'回答: ', reply
            print 'E'
            saveFile(detailName, reply)
        print '========', detailName, '========== end'
        print ''


def saveFile(ask, reply):
    ask = ask.encode('utf8')
    reply = reply.encode('utf8')
    with open('baike_ask_reply2.txt', 'a') as loadF:
        loadF.write('E' + '\n')
        loadF.write('M ' + ask + '\n')
        loadF.write('M ' + reply + '\n')
        loadF.close()


if __name__ == '__main__':
    circleRun(operate)
    # def isChinese(checkValue):
    #     return not any(char.isdigit() or char.isalpha() for char in checkValue)
    #
    #
    # print isChinese(u'你好'.encode('utf8'))
    # print getDetailList(1)[0].name