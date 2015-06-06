# coding:utf8
import os
from string import strip
import sys
import time

__author__ = 'ITTC-Jayvee'

import sqlite3 as sqlite

project_path = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
data_path = '%s/data' % project_path
reload(sys)
sys.setdefaultencoding('utf8')
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
    item_name TEXT NOT NULL unique,
    item_id text not null,
    price float not null ,
    sale_pos text not null,
    sale_time timestamp not null,
    ps_info text,
    record_id INTEGER primary key  autoincrement);'''
    sqlcursor.execute(sqltext)
    # 创建库存记录表
    sqltext = '''create table RemainsRecords (
    item_type TEXT NOT NULL,
    item_name TEXT not null unique ,
    item_id text not null,
    sale_pos text not null,
    remains int(10) not null ,
    record_id INTEGER primary key  autoincrement);'''
    sqlcursor.execute(sqltext)

    sqltext = '''create table PasswordsRecords (
    username TEXT NOT NULL unique,
    password TEXT not null ,
    pos TEXT not null ,
    power int(2) not null,
    record_id INTEGER primary key  autoincrement);'''
    sqlcursor.execute(sqltext)

    conn.commit()
    sqlcursor.close()


'''
Password part
'''


def insertPassword(connect, insert_data, table='PasswordsRecords'):
    cur = connect.cursor()
    sqltext = 'insert into %s %s values (\'%s\',\'%s\',\'%s\',%s);' % (
        str(table), '(username,password,pos,power)', insert_data['username'],
        insert_data['password'], insert_data['pos'], 0)
    try:
        cur.execute(sqltext)
        connect.commit()
    except:
        return None

    cur.close()
    return 'ok'


def checkPassword(connect, username, password, table='PasswordsRecords'):
    cur = connect.cursor()
    sqltext = 'select password,pos,power from %s where username = \'%s\';' % (table, username)
    cur.execute(sqltext)
    for tup in cur.fetchall():
        if tup[0] == password:
            return tup[1], tup[2]
        else:
            return None


'''
SalesRecords part
'''


def insertSalesRecord(connect, insert_data, isBasedOnRemains=False, table='SalesRecords'):
    """
    :arg isBasedOnRemains  是否与库存记录相联系
    """
    cur = connect.cursor()
    # 组织sql
    keytext = '(item_type,item_name,item_id,ps_info,price,sale_pos,sale_time)'
    valuetext = '(\'%s\',\'%s\',\'%s\',\'%s\',%s,\'%s\',%s)' % \
                (insert_data['item_type'], insert_data['item_name'],
                 insert_data['item_id'],
                 insert_data['ps_info'],
                 insert_data['price'], insert_data['sale_pos'],
                 insert_data['sale_time'])
    sqltext = 'insert into %s %s values %s;' % (str(table), keytext, valuetext)
    if isBasedOnRemains:
        fetchRemainsText = 'select remains from RemainsRecords where item_name = \'%s\' and item_type=\'%s\' and item_id=\'%s\' and sale_pos=\'%s\';' % (
            insert_data['item_name'], insert_data['item_type'], insert_data['item_id'], insert_data['sale_pos'])
        cur.execute(fetchRemainsText)
        remains = cur.fetchone()
        if remains is not None and remains > 0:
            remains_count = remains[0]
            remains_count -= 1
            remainsSQLtext = 'update %s set remains = %s where item_name = \'%s\' and item_type =\'%s\' and item_id=\'%s\';' % (
                'RemainsRecords', remains_count, insert_data['item_name'], insert_data['item_type'],
                insert_data['item_id'])
            cur.execute(sqltext)
            cur.execute(remainsSQLtext)
            connect.commit()
            cur.close()
            return 'ok'
        return '没有足够的库存'
    else:
        cur.execute(sqltext)
    connect.commit()
    cur.close()


def updateSalesData(connect, record_id, update_data, table='SalesRecords'):
    cur = connect.cursor()
    # print type(remains)
    sqltext = '''update %s set item_type = \'%s\', item_name = \'%s\',item_id=\'%s\',ps_info=\'%s\', price = %s, sale_pos = \'%s\' where record_id=%s;''' % (
        table, update_data['item_type'], update_data['item_name'], update_data['item_id'], update_data['ps_info'],
        update_data['price'], update_data['sale_pos'],
        record_id)
    cur.execute(sqltext)
    # print remains
    connect.commit()
    cur.close()


def removeSalesData(connect, record_id):
    cur = connect.cursor()
    # print type(remains)
    sqltext = '''delete from SalesRecords where record_id=%s;''' % (record_id)
    cur.execute(sqltext)
    # print remains
    connect.commit()
    cur.close()


def removeRemainsData(connect, record_id):
    cur = connect.cursor()
    # print type(remains)
    sqltext = '''delete from RemainsRecords where record_id=%s;''' % (record_id)
    cur.execute(sqltext)
    # print remains
    connect.commit()
    cur.close()


'''
RemainsRecords part
'''


def insertRemainsRecord(connect, insert_data, table='RemainsRecords'):
    cur = connect.cursor()
    # 组织sql
    keytext = '(item_type,item_name,item_id,sale_pos,remains)'
    valuetext = '(\'%s\',\'%s\',\'%s\',\'%s\',%s)' % \
                (insert_data['item_type'], insert_data['item_name'], insert_data['item_id'], insert_data['sale_pos'],
                 insert_data['remains'])
    sqltext = 'insert into %s %s values %s;' % (str(table), keytext, valuetext)
    cur.execute(sqltext)
    connect.commit()
    cur.close()


def updateRemainsData(connect, record_id, update_data, table='RemainsRecords'):
    cur = connect.cursor()
    # cur.execute('''select remains,record_id from %s where item_type=\'%s\' and item_name=\'%s\' and sale_pos=%s;''' % (
    # table, update_data['item_type'], update_data['item_name'], update_data['sale_pos']))
    # result = cur.fetchall()[0]
    # remains = result[0]
    # record_id = result[1]
    # print type(remains)
    # remains += update_data['update_count']
    cur.execute(
        '''update %s set remains = %s , item_type=\'%s\' , item_name=\'%s\' ,item_id=\'%s\' sale_pos=\'%s\' where record_id=%s;''' % (
            table, update_data['remains'], update_data['item_type'], update_data['item_name'], update_data['item_id'],
            update_data['sale_pos'],
            record_id))
    # print remains
    connect.commit()
    cur.close()


def showData(connect, table, pos, power=0):
    cur = connect.cursor()
    if power == 1:
        sqltext = 'select * from %s;' % (table)
    else:
        sqltext = 'select * from %s where sale_pos=\'%s\';' % (table, pos)
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
    initDatabase()
    # data = {}
    # data['item_type'] = 'phone'
    # data['item_name'] = 'xiaomi'
    # data['sale_pos'] = 1
    # data['remains'] = 10
    # data['update_count'] = 2
    # data['phone_name'] = u'华为'
    # data['remains'] = 21
    # # data['phone_id'] = 'iphone'
    # conn = sqlite.connect('%s/Database/data/Data.sqlite' % project_path)
    # insertRemainsRecord(conn, data)
    # updateRemainsData(conn, data)
    # print time.time()
    # localtime = time.localtime(time.time()*1000)
    # print "Local current time :", localtime
    # insertSalesRecord(conn, {'item_name': "pingguo", 'item_type': 'shouji', 'price': 1234, 'sale_pos': 2,
    # 'sale_time': time.time()})

    # saledata = {'item_name': "pingguo", 'item_type': 'shouji', 'price': 122224, 'sale_pos': 1,
    # 'sale_time': time.time()}
    # updateSalesData(conn, 1, saledata)

    # # insertPhoneData(conn, 'PhoneRemains', data)
    #
    # print showData(conn, 'PhoneRemains')
    # print showData(conn, 'PhoneSales')
