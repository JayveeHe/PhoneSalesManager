# coding=utf-8
import os
from flask import Flask, url_for, redirect, request
import sys
from Database import mysqlUtils
import json

project_path = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
data_path = '%s/data' % (project_path)
sys.path.append(project_path)
app = Flask(__name__)


@app.route('/')
def hello_world():
    return redirect(url_for('static', filename='web/flatui.html'))


@app.route('/data/<table>', methods=['GET', 'POST', 'DELETE'])
def getdata(table):
    if request.method == 'GET':
        conn = mysqlUtils.getDBconnect('Data')
        return json.dumps(mysqlUtils.showData(conn, table))
    if request.method == 'POST':
        conn=mysqlUtils.getDBconnect('Data')
        request.data


@app.route('/test', methods=['POST'])
def weibo():
    print request.get_data()
    return '服务器收到：' + request.get_data()


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=80)
