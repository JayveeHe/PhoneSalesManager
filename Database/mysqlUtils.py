# coding:utf8
import os
from string import strip
import sys
import time

__author__ = 'ITTC-Jayvee'

import sqlite3 as sqlite

project_path = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
data_path = '%s/data' % project_path
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
    conn = sqlite.connect('%s/Database/data/Data.sqlite' % project_path)
    sqlcursor = conn.cursor()
    # 创建销售记录表
    sqltext = '''create table SalesRecords (
    item_type TEXT NOT NULL,
    item_name TEXT NOT NULL,
    price float not null ,
    sale_pos int(2) not null,
    sale_time timestamp not null,
    record_id INTEGER primary key  autoincrement);'''
    sqlcursor.execute(sqltext)
    # 创建库存记录表
    sqltext = '''create table RemainsRecords (
    item_type TEXT NOT NULL,
    item_name TEXT not null ,
    sale_pos int(2) not null,
    remains int(10) not null ,
    record_id INTEGER primary key  autoincrement);'''
    sqlcursor.execute(sqltext)
    conn.commit()
    sqlcursor.close()


def insertSalesRecord(connect, insert_data, table='SalesRecords'):
    cur = connect.cursor()
    # 组织sql
    keytext = '(item_type,item_name,price,sale_pos,sale_time)'
    valuetext = '(\'%s\',\'%s\',%s,%s,%s)' % \
                (insert_data['item_type'], insert_data['item_name'], insert_data['price'], insert_data['sale_pos'],
                 insert_data['sale_time'])
    # for key in data.keys():
    # keytext += ', %s=%s' % (key, data[key])
    # valuetext +=''
    # datatext = datatext[1:]
    sqltext = 'insert into %s %s values %s;' % (str(table), keytext, valuetext)
    cur.execute(sqltext)
    connect.commit()
    cur.close()


def updateSalesData(connect, record_id, update_data, table='SalesRecords'):
    cur = connect.cursor()
    # print type(remains)
    sqltext = '''update %s set item_type = \'%s\', item_name = \'%s\', price = %s, sale_pos = %s, sale_time = %s where record_id=%s;''' % (
        table, update_data['item_type'], update_data['item_name'], update_data['price'], update_data['sale_pos'],
        update_data['sale_time'], record_id)
    cur.execute(sqltext)
    # print remains
    connect.commit()
    cur.close()


def insertRemainsRecord(connect, insert_data, table='RemainsRecords'):
    cur = connect.cursor()
    # 组织sql
    keytext = '(item_type,item_name,sale_pos,remains)'
    valuetext = '(\'%s\',\'%s\',%s,%s)' % \
                (insert_data['item_type'], insert_data['item_name'], insert_data['sale_pos'], insert_data['remains'])
    sqltext = 'insert into %s %s values %s;' % (str(table), keytext, valuetext)
    cur.execute(sqltext)
    connect.commit()
    cur.close()


def updateRemainsData(connect, update_data, table='RemainsRecords'):
    cur = connect.cursor()
    cur.execute('''select remains,record_id from %s where item_type=\'%s\' and item_name=\'%s\' and sale_pos=%s;''' % (
        table, update_data['item_type'], update_data['item_name'], update_data['sale_pos']))
    result = cur.fetchall()[0]
    remains = result[0]
    record_id = result[1]
    # print type(remains)
    remains += update_data['update_count']
    cur.execute(
        '''update %s set remains = %s where item_type=\'%s\' and item_name=\'%s\' and sale_pos=%s and record_id=%s;''' % (
            table, remains, update_data['item_type'], update_data['item_name'], update_data['sale_pos'], record_id))
    # print remains
    connect.commit()
    cur.close()


def showData(connect, table):
    cur = connect.cursor()
    sqltext = 'select * from %s;' % table
    cur.execute(sqltext)
    root = []
    # 获取表的列名
    col_names = [key[0] for key in cur.description]
    for tup in cur.fetchall():
        show_data = {}
        for x in range(len(col_names)):
            show_data[col_names[x]] = str(tup[x])
        root.append(show_data)
    cur.close()
    return root


def getDBconnect(dbName):
    return sqlite.connect('%s/Database/data/%s.sqlite' % (project_path, dbName))


if __name__ == '__main__':
    # initDatabase()
    data = {}
    data['item_type'] = 'phone'
    data['item_name'] = 'xiaomi'
    data['sale_pos'] = 1
    data['remains'] = 10
    data['update_count'] = 2
    # data['phone_name'] = u'华为'
    # data['remains'] = 21
    # # data['phone_id'] = 'iphone'
    conn = sqlite.connect('%s/Database/data/Data.sqlite' % project_path)
    # insertRemainsRecord(conn, data)
    # updateRemainsData(conn, data)

    insertSalesRecord(conn, {'item_name': "pingguo", 'item_type': 'shouji', 'price': 1234, 'sale_pos': 2,
                             'sale_time': time.time()})
    saledata = {'item_name': "pingguo", 'item_type': 'shouji', 'price': 122224, 'sale_pos': 1,
                'sale_time': time.time()}
    updateSalesData(conn, 1, saledata)

    # # insertPhoneData(conn, 'PhoneRemains', data)
    #
    # print showData(conn, 'PhoneRemains')
    # print showData(conn, 'PhoneSales')
