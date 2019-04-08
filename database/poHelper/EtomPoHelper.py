# -*- coding: utf-8 -*-
"""
1、执行带参数的ＳＱＬ时，请先用sql语句指定需要输入的条件列表，然后再用tuple/list进行条件批配
２、在格式ＳＱＬ中不需要使用引号指定数据类型，系统会根据输入参数自动识别
３、在输入的值中不需要使用转意函数，系统会自动处理

PO_JAVA库
"""

import pymysql as MySQLdb
from DBUtils.PooledDB import PooledDB
from database.poHelper import dbconfig


"""
dbconfig是一些数据库的配置文件
"""
class EtomPoHelper:
    def __init__(self):
        connKwargs = {'host': dbconfig.JAVA_DBHOST, 'user': dbconfig.JAVA_DBUSER, 'passwd': dbconfig.JAVA_DBPWD,
                      'db': dbconfig.JAVA_DBNAME, 'charset': dbconfig.DBCHAR,'port':3306}
        self._pool = PooledDB(MySQLdb, mincached=2, maxcached=8, maxshared=5, maxusage=5000,blocking=True, **connKwargs)

    def getConn(self):
        return self._pool.connection()


_dbManager = EtomPoHelper()


def getConn():
    """ 获取数据库连接 """
    return _dbManager.getConn()


def insert(sql, params):
    return __execute(sql, params)


def insertTwo(sql1, sql2, params1, params2):
    return __save(sql1, sql2, params1, params2)


def update( sql, params):
    return __execute(sql, params)


def delete(sql, params):
    return __execute(sql, params)


def __execute(sql, param=[]):
    """ 执行sql语句 """
    try:
        conn = getConn()
        cursor = conn.cursor()
        rowcount = cursor.execute(sql, param)
        cursor.close()
        conn.commit()
        conn.close()
        return rowcount
    except Exception as e:
        print (e)
    finally:
        cursor.close()
        conn.close()


def __save(sql1, sql2,param1=[],params2=[]):
    """ 同时执行两条sql语句 """
    try:
        conn = getConn()
        cursor = conn.cursor()
        rowcount = cursor.execute(sql1, param1)
        cursor.execute(sql2, params2)
        conn.commit()
        cursor.close()
        conn.close()
        return rowcount
    except Exception as e:
        print (e)
    finally:
        cursor.close()
        conn.close()


def fetchone(sql,params=[]):
    """ 获取一条信息 """
    try:
        conn = getConn()
        cursor = conn.cursor()
        rowcount = cursor.execute(sql,params)
        res = cursor.fetchone()
        cursor.close()
        conn.close()
        return res
    except Exception as e:
        cursor.close()
        conn.close()



def fetchall(sql,params):
    """ 获取所有信息 """
    try:
        conn = getConn()
        cursor = conn.cursor()
        rowcount = cursor.execute(sql,params)
        res = cursor.fetchall()
        cursor.close()
        conn.close()
        return res
    except Exception as e:
        cursor.close()
        conn.close()


def executemany(sql,params):
    try:
        conn = getConn()
        cursor = conn.cursor()
        rowcount = cursor.executemany(sql, params)
        conn.commit()
        cursor.close()
        conn.close()
        return rowcount
    except Exception as e:
        print (e)
    finally:
        cursor.close()
        conn.close()

