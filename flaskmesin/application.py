from flask import Flask, request, jsonify, render_template, redirect, url_for
import os
import time
import subprocess
from termcolor import colored
import pymongo
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import codecs

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient['mesin-cnc']
mycol = mydb["machine_status"]

app = Flask(__name__)



@app.route('/mesin', methods = ['GET'])
def details():
    
    cursor_data = mycol.find().sort("_id", -1).limit(4)
    cursor_data_much = mycol.find().sort("_id", -1).limit(20)
    cursor_all = mycol.find()
    tli = []
    time_li = []
    status_li = []
    stat_li = []

    nama_mesin = ''
    lokasi_mesin = ''
    waktu = ''
    status_aktual = 0
    

    for j in cursor_data:
        nama_mesin = j['machine_name']
        lokasi_mesin = j['location']
        waktu = j['time_get_data']
        status_aktual = j['status_mesin']
        tli.append([j['machine_name'],j['lampu_a'],j['lampu_b'],j['status_mesin'],j['time_get_data']])

    side = [nama_mesin, lokasi_mesin, waktu, status_aktual]
    for i in cursor_data_much:
        timesc = i['time_get_data'][5:12]
        time_li.append(timesc)
        status_li.append(i['status_mesin'])
        
    for i in cursor_all:
        stat_li.append(i['status_mesin'])
    
    counter_li = [0,0,0]
    for i in stat_li:
        if i == 0:
            counter_li[0] += 1
        elif i == 1:
            counter_li[1] += 1
        else:
            counter_li[2] += 1    

    return render_template('each.html', listi = tli, a = time_li, b = status_li, donnut = counter_li, side = side)

@app.route('/ui_test')
def ui_test():
    return render_template('ui_tester.html')

if __name__ == '__main__':
    app.run(host='192.168.12.222', port='5001')

    # username admin, password admin, waktu, password user, ssid.