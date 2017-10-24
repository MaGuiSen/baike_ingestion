# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


import datetime

from trivest_data.dal import LogDao
from trivest_data.dal.trivest_spider import getTableByName
from trivest_data.dal.StatusDao import CiTiaoStatusDao

class BasePipeline(object):
    def __init__(self):
        self.belong_to = ''

    def logInfo(self, msg, belong_to='', saveInDB=False):
        belong_to = belong_to or self.belong_to
        LogDao.info(msg, belong_to=belong_to, saveInDB=saveInDB)

    def logWarn(self, msg, belong_to='', saveInDB=True):
        belong_to = belong_to or self.belong_to
        LogDao.warn(msg, belong_to=belong_to, saveInDB=saveInDB)

    def process_item_default(self, item, table, logName):
        try:
            self.logInfo(u'存%s详情：%s' % (logName, item['title']), saveInDB=False)
            # 查重
            results = table.select().where(table.haoyaoshi_id == item.get('haoyaoshi_id')).count()
            if not results:
                item['update_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                table.create(**item)
                self.logInfo(u'存%s详情：%s 成功 haoyaoshi_id：%s' % (logName, item['title'], item['haoyaoshi_id']))
            else:
                self.logInfo(u'%s详情：%s 已经存在 haoyaoshi_id：%s' % (logName, item['title'], item['haoyaoshi_id']))
        except Exception as e:
            self.logWarn(str(e))
            self.logWarn(u'存%s详情：%s失败' % (logName, item['title']))

        return item


class BaiKeTypePipeline(BasePipeline):
    def __init__(self):
        self.belong_to = 'baike_type'
        self.logName = u'百科类型'
        self.Table = getTableByName('baike_type')
        pass

    def process_item(self, item, spider):
        # 如果存储方式和process_item_default方法的相同，则直接调用父类的process_item_default
        try:
            self.logInfo(u'存%s：%s' % (self.logName, item['name']), saveInDB=False)
            # 查重
            results = self.Table.select().where(self.Table.name == item.get('name')).count()
            if not results:
                item['update_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                self.Table.create(**item)
                self.logInfo(u'存%s：%s 成功' % (self.logName, item['name']))
            else:
                self.logInfo(u'%s：%s 已经存在' % (self.logName, item['name']))
        except Exception as e:
            self.logWarn(str(e))
            self.logWarn(u'存%s：%s失败' % (self.logName, item['name']))

        return item

    def close_spider(self, spider):
        pass


class BaiKeCiTiaoPipeline(BasePipeline):
    def __init__(self):
        self.belong_to = 'baike_citiao'
        self.logName = u'百科词条'
        self.Table = getTableByName('baike_citiao')
        pass

    def process_item(self, item, spider):
        # 如果存储方式和process_item_default方法的相同，则直接调用父类的process_item_default
        statusDao = CiTiaoStatusDao()
        try:
            self.logInfo(u'存%s：%s' % (self.logName, item['name']), saveInDB=False)
            # 查重
            results = self.Table.select().where(self.Table.name == item.get('name')).count()
            if not results:
                item['update_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                self.Table.create(**item)
                self.logInfo(u'存%s：%s 成功' % (self.logName, item['name']))
            else:
                self.logInfo(u'%s：%s 已经存在' % (self.logName, item['name']))
            statusDao.updateStatus(item.get('name'), statusDao.Status_save_success)
        except Exception as e:
            self.logWarn(str(e))
            self.logWarn(u'存%s：%s失败' % (self.logName, item['name']))
            statusDao.updateStatus(item.get('name'), statusDao.Status_save_fail)

        return item

    def close_spider(self, spider):
        pass


class BaiKeCiTiaoDetailPipeline(BasePipeline):
    def __init__(self):
        self.belong_to = 'baike_citiao_detail'
        self.logName = u'百科词条详情'
        self.Table = getTableByName('baike_citiao_detail')
        pass

    def process_item(self, item, spider):
        # 如果存储方式和process_item_default方法的相同，则直接调用父类的process_item_default
        try:
            self.logInfo(u'存%s：%s' % (self.logName, item['name']), saveInDB=False)
            # 查重
            results = self.Table.select().where(self.Table.name == item.get('name')).count()
            if not results:
                item['update_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                self.Table.create(**item)
                self.logInfo(u'存%s：%s 成功' % (self.logName, item['name']))
            else:
                self.logInfo(u'%s：%s 已经存在' % (self.logName, item['name']))
        except Exception as e:
            self.logWarn(str(e))
            self.logWarn(u'存%s：%s失败' % (self.logName, item['name']))

        return item

    def close_spider(self, spider):
        pass


