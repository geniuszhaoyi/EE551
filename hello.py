from flask import Flask
from flask import request
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route('/login')
def login():
    username = request.args.get('username')
    print(username)
    password = request.args.get('password')
    print(password) 
    return 'login'

import project
saved_result = {}

@app.route('/getHL')
def main():
    url = request.args.get('url')
    name = request.args.get('name')
    customerRestaurant(url, name, sys.stdout)
    return ''

@app.route('/html')
def html():
    with open("index.html") as f:
        return f.read()
    Error('no such file')

import json
import os
# import project

@app.route('/get')
def get():
    name = request.args.get('name')
    print(name)
    if name in saved_result:
        return json.dumps(saved_result[name])
    else:
        os.system('python project.py ' + name + ' CustomerRestaurant')
        # with open('fifo', 'w') as fifo:
        #     project.customerRestaurant(name, 'Customer Restaurant', fifo)
        with open('fifo') as fifo:
            read_result(fifo.readlines())
        if 'CustomerRestaurant' in saved_result:
            return json.dumps(saved_result['CustomerRestaurant'])
    return ""

def read_result(ls):
    # print(len(ls))
    for i in range(0, len(ls), 18):
        key = ls[i + 1].strip()
        val = {"name": key, "good": [], "bad": []}
        n = 0
        for j in range(i + 3, i + 16):
            if ls[j] == '' or ls[j] == '\n':
                continue
            if ls[j] == 'What the Guests loved Most: \n':
                n = 0
                continue
            if ls[j] == 'What nedd to be improved: \n':
                n = 1
                continue
            if n == 0:
                val['good'].append(ls[j].strip())
            else:
                val['bad'].append(ls[j].strip())
        saved_result[key] = val

with open('chinese_result.txt') as f:
    read_result(f.readlines())
with open('mexican_result.txt') as f:
    read_result(f.readlines())
with open('italian_result.txt') as f:
    read_result(f.readlines())
