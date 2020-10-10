import flask
import os
from flask import Flask, render_template, jsonify,json
from jinja2 import Template
from visual import *
import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt
import seaborn as sns

import pandas_datareader.data as web
import pandas_datareader
from flask import Flask, render_template, request, url_for
app=flask.Flask(__name__)

test=visual_class()


@app.route('/form',methods=["POST"])
def search():
    company=request.form.get("symbol")
    test.company_name=company

    ##test.value=y
    return flask.redirect("/")

@app.route('/test')
def testing():
    stock_result=stock_data(test.company_name)

    return render_template('test.html', data=test.company_name, value=stock_result)


def stock_data(name):
    start=datetime.datetime(2020,8,29)
    end=datetime.datetime(2020,9,29)

    STOCK=web.DataReader(test.company_name,'yahoo',start,end)
    result = STOCK['Close']
    return result


def convert_json(data):
    new_result=data.to_json(orient="values")
    parsed = json.loads(new_result)
    x=json.dumps(parsed, indent=4)
    y=json.loads(x)
    return y


@app.route('/')
def index():
    stock_result=stock_data(test.company_name)
    json_data=convert_json(stock_result)
    data.close_price=json_data
    return render_template('chart.html',data=test.company_name, value=json_data)

## Creatign a json object of the Data
@app.route('/data')
def data():
    stock_result=stock_data(test.company_name)
    json_data=convert_json(stock_result)
    return jsonify({'results':json_data })



if __name__=='__main__':
    app.run(debug=True)
