import chardet
import happybase
from database.hbaseHelper import hbaseconfig

#hbase连接对象
class HBaseConnect():
    def __init__(self):
        self.host = hbaseconfig.HBASE_HOST
        self.port = hbaseconfig.HBASE_PORT
        self.timeout = hbaseconfig.HBASE_TIMEOUT
        self.connection = happybase.Connection(host=self.host, autoconnect=False,port=self.port,timeout=self.timeout)
    def getConnect(self):
        return self.connection

_hbaseManager = HBaseConnect()

def getConn():
    """ 获取数据库连接 """
    return _hbaseManager.getConnect()

#获得表  要记得关闭连接
def getTable(tableName):
    connect = getConn()
    connect.open()
    table = happybase.Table(tableName,connect)
    return table

#获得单行
def getRow(tableName,rowkey):
    # 创建实例
    connect = getConn()
    connect.open()
    table = happybase.Table(tableName, connect)
    row = table.row(row=rowkey)
    connect.close()
    if row == None or not row:
        return row
    row = changeEncode(row)
    return row

#获得多行
def getRows(tableName,rowkeys):
    connect = getConn()
    connect.open()
    table = happybase.Table(tableName, connect)
    rows = table.rows(rows=rowkeys)
    connect.close()
    new_rows = []
    for row in rows:
        new_row = changeEncode(row)
        new_rows.append(new_row)
    return new_rows


#改变字典编码
def changeEncode(row):
    dicts = {}
    for rowKey in row.keys():
        keyDetRes = chardet.detect(rowKey)  # 返回编码结果
        keyCharset = keyDetRes["encoding"]
        strRowKey = rowKey.decode(keyCharset, "ignore")
        #修改内容的编码
        valueDetRes = chardet.detect(row[rowKey])  # 返回编码结果
        valueCharset = valueDetRes["encoding"]
        dicts[strRowKey] = row[rowKey].decode(valueCharset, "ignore")
    return dicts

if __name__ == '__main__':
    row = getRow(tableName="po_data",rowkey='18102ee4ebbf556a227b3c8f01c1a2b765d1')
    print(row)
