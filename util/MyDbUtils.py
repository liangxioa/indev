# -*- coding: UTF-8 -*-
"""
1、执行带参数的ＳＱＬ时，请先用sql语句指定需要输入的条件列表，然后再用tuple/list进行条件批配
２、在格式ＳＱＬ中不需要使用引号指定数据类型，系统会根据输入参数自动识别
３、在输入的值中不需要使用转意函数，系统会自动处理
"""
import sys

import pymysql
from DBUtils.PooledDB import PooledDB
from config import DB_config

"""
DB_config是一些数据库的配置文件
"""


class Mysql(object):
    """
    MYSQL数据库对象，负责产生数据库连接 , 此类中的连接采用连接池实现获取连接对象：conn = Mysql.getConn()
            释放连接对象;conn.close()或del conn
    """
    # 连接池对象
    __pool = None

    def __init__(self):
        self.open()

    @staticmethod
    def __getConn():
        """
        @summary: 静态方法，从连接池中取出连接
        @return MySQLdb.connection
        """
        if Mysql.__pool is None:
            Mysql.__pool = PooledDB(creator=pymysql, mincached=DB_config.DB_MIN_CACHED,
                                    maxcached=DB_config.DB_MAX_CACHED,
                                    maxshared=DB_config.DB_MAX_SHARED, maxconnections=DB_config.DB_MAX_CONNECYIONS,
                                    blocking=DB_config.DB_BLOCKING, maxusage=DB_config.DB_MAX_USAGE,
                                    setsession=DB_config.DB_SET_SESSION,
                                    host=DB_config.DB_HOST, port=DB_config.DB_PORT,
                                    user=DB_config.DB_USER, passwd=DB_config.DB_PASSWORD,
                                    db=DB_config.DB_DBNAME, use_unicode=False, charset=DB_config.DB_CHARSET)
        return Mysql.__pool.connection()

    def open(self):
        # 数据库构造函数，从连接池中取出连接，并生成操作游标
        self._conn = Mysql.__getConn()
        self._cursor = self._conn.cursor()

    def close(self):
        self._cursor.close()
        self._conn.close()

    def execute(self, sql='', param=(), autoclose=False):
        try:
            self.open()
            if param:
                self._cursor.execute(sql, param)
            else:
                self._cursor.execute(sql)
            self._conn.commit()
            if autoclose:
                self.close()
        except Exception as e:
            print('execute failed========', e.args)

    def executemany(self, paramlist=None):
        """
        执行多条命令
        :type paramlist: object [{"sql":"xxx","param":"xx"}...]
        """
        if paramlist is None:
            paramlist = []
        try:
            self.open()
            for order in paramlist:
                sql = order['sql']
                param = order['param']
                if param:
                    self._cursor.execute(sql, param)
                else:
                    self._cursor.execute(sql)
            self._conn.commit()
            self.close()
            return True
        except Exception as e:
            print('execute failed========', e.args)
            self._conn.rollback()
            self.close()
            return False

    def selectone(self, sql="", param=()):
        try:
            self.execute(sql, param)
            res = self._cursor.fetchone()
            self.close()
            return res
        except Exception as e:
            print('selectone except:', e.args)
            self.close()
            return False

    def selectall(self, sql="", param=()):
        try:
            self.execute(sql, param)
            res = self._cursor.fetchall()
            self.close()
            return res
        except Exception as e:
            print('selectall except:', e.args)
            self.close()
            return False

    def insert(self, sql="", param=()):
        try:
            self.execute(sql, param)
            _id = self._cursor.lastrowid
            self._conn.commit()
            self.close()
            if _id == 0:
                return True
            return _id
        except Exception as e:
            print('insert except:', e.args)
            self._conn.rollback()
            self.close()
            return False

    def insertMany(self, sql, param):
        try:
            self._cursor.executemany(sql, param)
            self._conn.commit()
            self.close()
            return True
        except Exception as e:
            print('insert many except:', e.args)
            self._conn.rollback()
            self.close()
            return False

    def update(self, sql, param=None):
        try:
            self.execute(sql, param)
            self._conn.commit()
            self.close()
            return True
        except Exception as e:
            print('update except:', e.args)
            self._conn.rollback()
            self.close()
            return False

    def delete(self, sql, param=None):
        try:
            self.execute(sql, param)
            self.close()
            return True
        except Exception as e:
            print('delete except:', e.args)
            self._conn.rollback()
            self.close()
            return False
