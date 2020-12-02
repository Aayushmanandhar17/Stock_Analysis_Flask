import flask
import os
import io
import base64
from flask import Flask, render_template, jsonify,json
from jinja2 import Template
from visual import *
import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt
import seaborn as sns

import keras
from keras import backend as k
from keras import Sequential
from keras.models import load_model
from keras.models import model_from_json

from sklearn.preprocessing import MinMaxScaler

import pandas_datareader.data as web
import pandas_datareader
from flask import Flask, render_template, request, url_for
app=flask.Flask(__name__)

test=visual_class()


@app.route('/form',methods=["POST"])
def search():
    company=request.form.get("symbol")
    test.company_name=company
    return flask.redirect("/")


@app.route('/')
def index():
    stock_result=test.stock_data(test.company_name)
    json_data=test.convert_json(stock_result)
    Name, company_description,sector,dividend,eps,capital,exchange,peratio=test.company_description(test.company_name)
    test.load_trained_model('BAC_pred.json','BAC_predictor.h5')

    print("The prediction for next day is: ",test.single_day)
    single_day_pred=test.single_day
    news_data,polarity,subjectivity=test.news()
    data.close_price=json_data
    return render_template('chart.html',data=Name,Description=company_description,sector=sector,dividend=dividend,eps=eps,exchange=exchange,peratio=peratio,capital=capital, news=news_data,polar=polarity,subject=subjectivity, single_day=single_day_pred )

## Creatign a json object of the Data
@app.route('/data')
def data():
    stock_result=test.stock_data(test.company_name)
    json_data=test.convert_json(stock_result)
    return jsonify({'results':json_data })

@app.route('/data_strategy')
def data_strategy():

    json_data=test.convert_json(stock)
    return jsonify({'results':json_data})

@app.route('/pipe', methods=["GET", "POST"])
def pipe():
    stock_result=test.dual_moving_average(test.company_name)
    stock_result['Buy_Signal'],stock_result['Sell_Signal']=test.buy_sell(stock_result)
    json_data=test.convert_json(stock_result)
    prediction_data=test.convert_json(test.pred)

    return jsonify({'res':json_data,'pred':prediction_data})



if __name__=='__main__':
    app.run(debug=True,threaded=True)
