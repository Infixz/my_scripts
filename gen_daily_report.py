# coding: utf-8
__doc__ = "gen target .xls file conveniently"
__author__ = "Jonathan Wong"
__date__ = "2016-08-02"

import xlwt


class Xls_generator(object):
    """hehe"""
    def __init__(self, file_name, sheet_name, headline_name, position_set, data):
        self._handler = xlwt.Workbook(encoding='utf-8')
        self._file_name = file_name
        self._sheet1 = self._handler.add_sheet(sheet_name)
        self._headline = headline_name
        self._position = position_set
        self._data = data
        self._row_size = len(data)
        for i in range(len(self._headline)):
            self._sheet1.write(0, i, self._headline[i])
    
    def write_one_row(self, datum, col_no):
        for key in datum.keys():
            if not key in self._position:
                continue
            content = datum[key]
            try:
                content = content.encode('utf8')
            except AttributeError, e:
                pass
            self._sheet1.write(col_no, self._position[key]-1, content)
        print 'write one row'

    def data_to_xls(self):
        for i in range(self._row_size):
            self.write_one_row(self._data[i], i+1)
        
    def export(self):
        self.data_to_xls()
        self._handler.save('%s.xls' % self._file_name)
        

if __name__ == '__main__':
    import requests
    # sample data
    resp = requests.get(r'http://115.28.79.197:9090/TroubleReport').json()
    data = resp['data']
    # position_set
    content_position = {
        'Id':1,
        'TroubleStatus':2,
        'CarSignedNo':3,
        'PlateNo':4,
        'MobilePhoneNo':5,
        'LineName':6,
        'LineProperty':7,
        'ReportContent':8,
        'TroubleType':9,
        'CreateTime':10,
        'Register':11,
        'Handler':12,
        'Exec_time':13,
        'Frequency':14,
        'LastTime':15
    }
    # headline_set
    headline_name = [
        '序号',
        '状态',
        '车签号',
        '车牌号',
        '联系电话',
        '线路名称',
        '线路属性',
        '情况说明',
        '情况类型',
        '创建时间',
        '登记人',
        '处理人',
        '处理时间',
        '延误次数',
        '延误总时长'
    ]
    # gen a "TroubleReport" instance
    trouble_report_xls = Xls_generator('trouble_report_date-x-x', 'date_of_xx', headline_name, content_position, data)
    trouble_report_xls.export()
    
