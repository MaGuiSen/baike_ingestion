# -*- coding: utf-8 -*-
import datetime

from trivest_data.dal import LogDao
from trivest_data.dal.trivest_spider import getTableByName


class CiTiaoStatusDao(object):
    Status_start_request = 'start_request'
    Status_save_success = 'save_success'
    Status_save_fail = 'save_fail'
    Status_no_source = '404'
    Status_no_complete_data = 'no_complete_data'
    Status_no_parse_method = 'no_parse_method'
    Status_dont_need_parse = 'dont_need_parse'
    Status_be_forbid = 'be_forbid'

    def __init__(self):
        self.Table = getTableByName('baike_citiao')

    def updateStatus(self, name, status):
        """
        存在更改，不存在则新增
        :param status: start_request, save_success, save_fail, 404, no_complete_data, no_parse_method, dont_need_parse
        :return:
        """
        pass
        try:
            results = self.Table.select().where(self.Table.name == name)
            if len(results):
                for result in results:
                    result.status = status
                    result.update_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    result.save()
        except Exception as e:
            print str(e)
            LogDao.warn(str(e), belong_to='updateStatus')

    def getCatchList(self, pageIndex):
        try:
            existStatus = [self.Status_save_success,
                           self.Status_no_source,
                           self.Status_dont_need_parse,
                           self.Status_no_complete_data,
                           self.Status_no_parse_method,
                           self.Status_be_forbid
                           ]
            results = self.Table.select().where(~(self.Table.status << existStatus))\
                .paginate(pageIndex, 15)
            return results
        except Exception as e:
            print str(e)
            LogDao.warn(str(e), belong_to='getReCatchList')
            return []

if __name__ == '__main__':
    pass
    print CiTiaoStatusDao().getCatchList(1)