# -*- coding: utf-8 -*-
import os, sys
import MySQLdb
from MySQLdb.cursors import DictCursor
from DBUtils.PooledDB import PooledDB

sys.path.append(os.path.abspath(os.path.dirname(os.path.abspath(__file__))+'/mysql'))
sys.path.append(os.path.abspath(os.path.dirname(os.path.abspath(__file__))+'/log'))
import mysqlConfig
from log import Log


class MysqlModel(object):
    _pool = {}
    _config = ''
    _conn = None  # 当前数据库连接
    _cursor = None  # 当前数据库游标
    _log = None

    def __init__(self, db):
        self._config = db if db is not None else 'master'
        self._conn = self.getConn(db)
        self._cursor = self._conn.cursor()

        if self._log is None:
            self._log = Log()

    """
        @summary: 静态方法，从连接池中取出连接
        @return MySQLdb.connection
    """
    @staticmethod
    def getConn(db):
        if MysqlModel._pool.get(db, None) is None:
            config = mysqlConfig.config[db]
            MysqlModel._pool[db] = PooledDB(creator=MySQLdb, mincached=1, maxcached=20, host=config['HOST'],
                                                      port=config['PORT'], user=config['USER'], passwd=config['PASSWD'],
                                                      db=config['DBNAME'], use_unicode=False, charset=config['CHARSET'],
                                                      cursorclass=DictCursor)
        return MysqlModel._pool[db].connection()

    """
        @summary: 执行查询，并取出所有结果集
        @param sql:查询SQL，如果有查询条件，请只指定条件列表，并将条件值使用参数[param]传递进来
        @param param: 可选参数，条件列表值（元组/列表）
        @return: result list(字典对象)/boolean 查询到的结果集
    """
    def query(self, sql, params=None):
        result = False
        try:
            if params is None:
                result = self._cursor.execute(sql)
            else:
                result = self._cursor.execute(sql, params)

            self._conn.commit()
        except MySQLdb.MySQLError as e:
            self._log.write('error', {'reason': e})
        return result

    def getAll(self, sql, params=None):
        query = self.query(sql=sql, params=params)
        if query > 0:
            result = self._cursor.fetchall()
        else:
            result = []
        return result

    def getOne(self, sql, params):
        query = self.query(sql=sql, params=params)
        if query > 0:
            result = self._cursor.fetchone()
        else:
            result = {}
        return result

    """
        @summary: 向数据表插入一条记录
        @param sql: 要插入的SQL格式
        @param value: 要插入的记录数据tuple/list
        @return: 受影响的行数
    """
    def insert(self, sql, value):
        result = 0
        try:
            result = self._cursor.execute(sql, value)
            self._conn.commit()
        except MySQLdb.MySQLError as e:
            self._log.write('error', {'reason': e})
        return result

    def update(self, sql, param=None):
        return self.query(sql, param)

    def delete(self, sql, param=None):
        return self.query(sql, param)

    """
        @summary: 开启事务
    """
    def begin(self):
        self._conn.autocommit(0)

    """
        @summary: 结束事务
    """
    def end(self, option='commit'):
        if option == 'commit':
            self._conn.commit()
        else:
            self._conn.rollback()

    """
        @summary: 释放连接池资源
    """
    def dispose(self, config=None):
        if config is None:
            self._cursor.close()
            self._conn.close()
            MysqlModel._pool[self._config] = None
        else:
            MysqlModel._pool[config] = None

        return True


# print(MysqlModel('master').getAll('show tables;'))
