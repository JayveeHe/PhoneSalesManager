# coding=utf-8
import base64
import os
from flask import Flask, url_for, redirect, request, make_response, flash, session
import sys
import time

import json

print __file__

print os.path.dirname(__file__)
print os.path.abspath(os.path.dirname(__file__))
project_path = os.path.dirname(__file__)
data_path = '%s/Database/data' % (project_path)
sys.path.append(project_path)
from Database import mysqlUtils
from log.get_logger import logger

app = Flask(__name__)
# 设置密钥，复杂一点：
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'


# 用户登陆管理相关
@app.route('/userinfo')
def getUserInfo():
    if session.has_key('username'):
        info = {'stat': 'ok', 'username': session['username'], 'pos': session['pos'], 'power': session['power']}
        return json.dumps(info)
    else:
        return json.dumps({'stat': 'error'})


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        app.logger.info("post login")
        conn = mysqlUtils.getDBconnect('Data')
        receive_data = request.form
        pwd_hash = base64.encodestring(receive_data['password'])
        result = mysqlUtils.checkPassword(conn, receive_data['username'], pwd_hash)
        if result is not None:
            # 儲存 session
            session['pos'] = result[0]
            session['power'] = result[1]
            session['username'] = receive_data['username']
            logger.info(request.remote_addr + ' 用户 ' + receive_data['username'] + ' 登陆成功')
            app.logger.info(request.remote_addr + ' 用户 ' + receive_data['username'] + ' 登陆成功')
            resp = {'stat': 'ok',
                    're_url': str(url_for('static', filename='web/index.html')),
                    'msg': ''}
            return json.dumps(resp)
        else:
            app.logger.info("密码或用户名错误！")
            logger.info(request.remote_addr + ' 用户 ' + receive_data['username'] + ' 登陆失败')
            app.logger.info(request.remote_addr + ' 用户 ' + receive_data['username'] + ' 登陆失败')
            resp = {'stat': 'error',
                    're_url': str(url_for('static', filename='web/login.html')),
                    'msg': '密码或用户名错误！'}
            return json.dumps(resp)
    if request.method == 'GET':
        app.logger.info("get login")
        return redirect(url_for('static', filename='web/login.html'))


@app.route('/logout', methods=['GET'])
def logout():
    logger.info(request.remote_addr + ' 用户 ' + session['username'] + ' 注销')
    app.logger.info(request.remote_addr + ' 用户 ' + session['username'] + ' 注销')
    session.pop('pos')
    session.pop('power')
    session.pop('username')
    return redirect('/login')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        receive_data = request.form
        # if User.query.filter_by(username=receive_data['username']).first() is None:
        conn = mysqlUtils.getDBconnect('Data')
        insert_data = {'username': receive_data['username'],
                       'password': base64.encodestring(receive_data['password']),
                       'pos': receive_data['pos']}
        result = mysqlUtils.insertPassword(conn, insert_data)
        if result == 'ok':
            logger.info(request.remote_addr + ' 用户 ' + receive_data['username'] + ' 注册成功')
            app.logger.info(request.remote_addr + ' 用户 ' + receive_data['username'] + ' 注册成功')
            return 'ok'
        else:
            logger.info(request.remote_addr + ' 用户 ' + receive_data['username'] + ' 注册失败')
            app.logger.info(request.remote_addr + ' 用户 ' + receive_data['username'] + ' 注册失败')
            return '注册失败'
            # else:
            # return redirect(url_for('static', filename='web/signup.html'))

    print 'get'
    return redirect(url_for('static', filename='web/signup.html'))


# Flask路由相关
@app.route('/')
def hello_world():
    return redirect(url_for('static', filename='web/login.html'))


@app.route('/data/<table>', methods=['GET', 'POST', 'DELETE'])
def getdata(table):
    """
    GET为在网页显示表格，POST为导出CSV
    :param table:
    :return:
    """
    conn = mysqlUtils.getDBconnect('Data')
    pos = session['pos']
    power = session['power']
    if request.method == 'GET':
        return json.dumps(mysqlUtils.showData(conn, table, pos, power=power))
    if request.method == 'POST':
        timestamp = request.form['timestamp']
        dataroot = mysqlUtils.showData(conn, table, pos, power=power)
        output = open('%s/static/csvfiles/' % project_path + timestamp + '.csv', 'w')
        output.write('\xEF\xBB\xBF')
        if table == 'SalesRecords':
            outstr = ''
            outstr += '序号，名称,类型,价格,分店号,销售时间\n'
            output.write('序号,名称,类型,价格,分店号,销售时间\n')
            for row in dataroot:
                timestr = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(float(row['sale_time']) / 1000))
                outstr += '%s,%s,%s,%s,%s,%s\n' % (
                    row['record_id'], row['item_name'], row['item_type'],
                    row['price'], row['sale_pos'], timestr)
                output.write('%s,%s,%s,%s,%s,%s\n' % (
                    row['record_id'], row['item_name'], row['item_type'],
                    row['price'], row['sale_pos'], timestr))
            return redirect(url_for('static', filename='csvfiles/' + timestamp + '.csv'))
            # return outstr
        elif table == 'RemainsRecords':
            outstr = ''
            outstr += '序号,名称,类型,分店号,剩余量\n'
            output.write('序号，名称,类型,分店号,剩余量\n')
            for row in dataroot:
                outstr += '%s,%s,%s,%s,%s\n' % (
                    row['record_id'], row['item_name'], row['item_type'],
                    row['sale_pos'], row['remains'])
                output.write('%s,%s,%s,%s,%s\n' % (
                    row['record_id'], row['item_name'], row['item_type'],
                    row['sale_pos'], row['remains']))
            return redirect(url_for('static', filename='csvfiles/' + timestamp + '.csv'))
            # return outstr
        else:
            return make_response("invalid tablename", 404)


@app.route('/data/<table>/update', methods=['POST'])
def updateTable(table):
    if request.method == 'POST':
        conn = mysqlUtils.getDBconnect('Data')
        receive_data = request.form
        if table == 'SalesRecords':
            update_data = {'item_type': receive_data['item_type'], 'item_name': receive_data['item_name'],
                           'price': receive_data['price'], 'sale_pos': receive_data['sale_pos'],
                           'sale_time': receive_data['sale_time']}
            record_id = receive_data['record_id']
            try:
                mysqlUtils.updateSalesData(conn, record_id, update_data)
                logger.info(request.remote_addr + ' 用户 ' + session['username'] + ' 修改销售记录%s成功' % record_id)
                app.logger.info(request.remote_addr + ' 用户 ' + session['username'] + ' 修改销售记录%s成功' % record_id)
                return "修改成功!"
            except:
                logger.info(request.remote_addr + ' 用户 ' + session['username'] + ' 修改销售记录%s失败' % record_id)
                app.logger.info(request.remote_addr + ' 用户 ' + session['username'] + ' 修改销售记录%s失败' % record_id)
                return '修改失败!'
        elif table == 'RemainsRecords':
            update_data = {'remains': receive_data['remains'], 'item_type': receive_data['item_type'],
                           'item_name': receive_data['item_name'], 'sale_pos': receive_data['sale_pos']}
            record_id = receive_data['record_id']
            try:
                mysqlUtils.updateRemainsData(conn, record_id, update_data)
                logger.info(request.remote_addr + ' 用户 ' + session['username'] + ' 修改库存记录%s成功' % record_id)
                app.logger.info(request.remote_addr + ' 用户 ' + session['username'] + ' 修改库存记录%s成功' % record_id)
                return "修改成功!"
            except:
                logger.info(request.remote_addr + ' 用户 ' + session['username'] + ' 修改库存记录%s失败' % record_id)
                app.logger.info(request.remote_addr + ' 用户 ' + session['username'] + ' 修改库存记录%s失败' % record_id)
                return '修改失败!'
        else:
            return make_response("invalid tablename", 404)


@app.route('/data/<table>/alert', methods=['POST'])
def alertTable(table):
    if request.method == 'POST':
        conn = mysqlUtils.getDBconnect('Data')
        receive_data = request.form
        if table == 'SalesRecords':
            alert_data = {'item_type': receive_data['item_type'], 'item_name': receive_data['item_name'],
                          'price': receive_data['price'], 'sale_pos': session['pos'],
                          'sale_time': receive_data['sale_time']}
            result = mysqlUtils.insertSalesRecord(conn, alert_data, isBasedOnRemains=True)
            logger.info(request.remote_addr + ' 用户 ' + session['username'] + ' 添加销售记录')
            app.logger.info(request.remote_addr + ' 用户 ' + session['username'] + ' 添加销售记录')
            return result
        elif table == 'RemainsRecords':
            alert_data = {'remains': receive_data['remains'], 'item_type': receive_data['item_type'],
                          'item_name': receive_data['item_name'], 'sale_pos': session['pos']}
            mysqlUtils.insertRemainsRecord(conn, alert_data)
            logger.info(request.remote_addr + ' 用户 ' + session['username'] + ' 添加库存记录')
            app.logger.info(request.remote_addr + ' 用户 ' + session['username'] + ' 添加库存记录')
            return "ok!"
        else:
            return make_response("invalid tablename", 404)


@app.route('/data/<table>/remove', methods=['POST'])
def removeData(table):
    if request.method == 'POST':
        conn = mysqlUtils.getDBconnect('Data')
        receive_data = request.form
        record_id = receive_data['record_id']
        if table == 'SalesRecords':
            mysqlUtils.removeSalesData(conn, receive_data['record_id'])
            logger.info(request.remote_addr + ' 用户 ' + session['username'] + ' 删除销售记录%s成功' % record_id)
            app.logger.info(request.remote_addr + ' 用户 ' + session['username'] + ' 删除销售记录%s成功' % record_id)
            return "ok!"
        elif table == 'RemainsRecords':
            mysqlUtils.removeRemainsData(conn, receive_data['record_id'])
            logger.info(request.remote_addr + ' 用户 ' + session['username'] + ' 删除库存记录%s成功' % record_id)
            app.logger.info(request.remote_addr + ' 用户 ' + session['username'] + ' 删除库存记录%s成功' % record_id)
            return "ok!"
        else:
            return make_response("invalid tablename", 404)


@app.route('/test', methods=['POST'])
def weibo():
    print request.get_data()
    return '服务器收到：' + request.get_data()


if __name__ == '__main__':
    app.debug = False
    logger.info('strat')
    app.run(host='0.0.0.0', port=80)
