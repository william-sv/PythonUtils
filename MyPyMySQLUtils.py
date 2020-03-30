# -*- coding: utf-8 -*-

import pymysql
import time


class DB:
    def __init__(self, host, user, password, database, port=3306):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.port = port
        try:
            self.__conn = pymysql.connect(host=self.host, user=self.user, password=self.password,
                                          database=self.database, port=self.port, use_unicode=True,
                                          charset="utf8mb4", cursorclass=pymysql.cursors.DictCursor)
            self.__cursor = self.__conn.cursor()
            self.__cursor.execute('SET NAMES utf8mb4;')
            self.__cursor.execute('SET CHARACTER SET utf8mb4;')
            self.__cursor.execute('SET character_set_connection=utf8mb4;')
        except pymysql.Error as e:
            print(e)

    def find(self, table, id):
        result = None
        try:
            sql = "SELECT * FROM { table } WHERE id={ id }".format(table=table, id=id)
            self.__cursor.execute(sql)
            result = self.__cursor.fetchone()
        except pymysql.Error as e:
            self.__conn.rollback()
            print(e)
        if result:
            result = result
        return result

    def find_many(self, table, query_conditions, field='*'):
        result = None
        try:
            sql = "SELECT { field } FROM { table } WHERE { query_conditions }".format(field=field, table=table,
                                                                                      query_conditions=query_conditions)
            self.__cursor.execute(sql)
            result = self.__cursor.fetchall()
        except pymysql.Error as e:
            print(e)
        if result:
            result = result
        return result

    def find_by_sql(self, sql):
        result = None
        try:
            self.__cursor.execute(sql)
            result = self.__cursor.fetchall()
        except pymysql.Error as e:
            self.__conn.rollback()
            print(e)
        if result:
            result = result
        return result

    def insert(self, table, data):
        insert_id = None
        sql_start = "INSERT INTO " + table + " ("
        sql_end = ") VALUES ("
        try:
            for key,value in data.items():
                sql_start += key + ','
                sql_end += value + ','
            sql = sql_start[:-1] + sql_end[:-1] + ')'
            self.__cursor.execute(sql)
            self.__conn.commit()
            insert_id = self.__conn.insert_id()
        except pymysql.Error as e:
            self.__conn.rollback()
            print(e)
        return insert_id

    def update_many(self, table, column_data, value_data):
        # 批量更新的前提条件是，值中有 primaryKey键 或 有 unique 键
        column = ''
        column_type = ''
        keys = ''
        sql_start = "INSERT INTO " + table + " ("
        sql_end = ") VALUES ("
        for item in column_data:
            column += item + ','
            keys += item + '=VALUES(' + item + ')' + ','
            column_type += '%s' + ','
        try:
            sql = sql_start + column[:-1] + sql_end + column_type[:-1] + ') ON DUPLICATE KEY UPDATE ' \
                  + keys[:-1]
            self.__cursor.executemany(sql, value_data)
            self.__conn.commit()
            self.__conn.insert_id()
        except pymysql.Error as e:
            self.__conn.rollback()
            print(e)
        return insert_id

    def close_db(self):
        try:
            self.__cursor.close()
            self.__conn.close()
        except pymysql.Error as e:
            print(e)

    def __del__(self):
        self.close_db()

