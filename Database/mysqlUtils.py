# coding:utf8
import os
import sys

__author__ = 'ITTC-Jayvee'

import sqlite3 as sqlite

project_path = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
data_path = '%s/data' % (project_path)
sys.path.append(project_path)

# # conn.execute('''CREATE TABLE COMPANY
# # (ID      INT PRIMARY KEY     NOT NULL,
# # NAME    TEXT                NOT NULL,
# # AGE     INT                 NOT NULL,
# #  ADDRESS CHAR(50),
# #  SALARY  REAL);''')
#
# te = conn.execute('''SELECT "NAME" WHERE "AGE">0''')
# print te.next()

# table = '123123123123'
# sqltext = 'insert %s into %s' % ('ddddd', str(table))
# print sqltext


def initDatabase():
    conn = sqlite.connect('%s/Database/data/PhoneSales.db' % project_path)
    sqlcursor = conn.cursor()
    sqltext = '''create table PhoneRemains (
    phone_name  TEXT NOT NULL,
    remains INT(10) NOT NULL,
    record_id INTEGER primary key  autoincrement
);'''
    sqlcursor.execute(sqltext)


def insertData(connect, table, data):
    cur = connect.cursor()
    # 组织sql
    keytext = '(phone_name,remains)'
    valuetext = '(\'%s\',%s)' % (data['phone_name'], data['remains'])
    # for key in data.keys():
    # keytext += ', %s=%s' % (key, data[key])
    # valuetext +=''
    # datatext = datatext[1:]
    sqltext = 'insert into %s %s values %s;' % (str(table), keytext, valuetext)
    cur.execute(sqltext)
    connect.commit()


if __name__ == '__main__':
    # initDatabase()
    data = {}
    data['phone_name'] = 'xiaomi'
    # data['phone_id'] = 'iphone'
    data['remains'] = 2
    conn = sqlite.connect('%s/Database/data/PhoneSales.db' % project_path)
    insertData(conn, 'PhoneRemains', data)