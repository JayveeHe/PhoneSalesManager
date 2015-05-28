# coding=utf-8
import os
from flask import Flask, url_for, redirect, request, make_response
import sys
from Database import mysqlUtils
import json

project_path = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
data_path = '%s/data' % (project_path)
sys.path.append(project_path)
app = Flask(__name__)


@app.route('/')
def hello_world():
    return redirect(url_for('static', filename='web/index.html'))


@app.route('/data/<table>', methods=['GET', 'POST', 'DELETE'])
def getdata(table):
    if request.method == 'GET':
        conn = mysqlUtils.getDBconnect('Data')
        return json.dumps(mysqlUtils.showData(conn, table))


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
            mysqlUtils.updateSalesData(conn, record_id, update_data)
            return "ok!"
        elif table == 'RemainsRecords':
            update_data = {'remains': receive_data['remains'], 'item_type': receive_data['item_type'],
                           'item_name': receive_data['item_name'], 'sale_pos': receive_data['sale_pos']}
            record_id = receive_data['record_id']
            mysqlUtils.updateRemainsData(conn, record_id, update_data)
            return "ok!"
        else:
            return make_response("invalid tablename", 404)


@app.route('/test', methods=['POST'])
def weibo():
    print request.get_data()
    return '服务器收到：' + request.get_data()


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=80)
