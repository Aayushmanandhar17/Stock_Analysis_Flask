import flask
import visual
import rnn
import news
import io
from flask import Flask, render_template, jsonify,json
from jinja2 import Template
#from visual import *
import matplotlib.pyplot as plt
from flask import Flask, render_template, request, url_for
app=flask.Flask(__name__)

test=visual.visual_class()
ml=rnn.machine_learning()
news_info=news.news_data()
stock_opti=[]


@app.route('/form',methods=["POST"])
def search():
    company=request.form.get("symbol")
    test.company_name=company
    ml.company_name=company
    return flask.redirect("/")

@app.route('/list_opt',methods=["POST"])
def list_company():
    company=request.form.get("symbol")
    stock_opti.append(company)
    return flask.redirect("/opt")


@app.route('/opt')
def opt():
    return render_template('optimize.html',list=stock_opti, sample=news_info.sample)

@app.route('/compute',methods=['GET', 'POST'])
def compute():
    news_info.sample="Hello there how are you"
    return flask.redirect("/opt")



@app.route('/')
def index():
    stock_result=test.stock_data(test.company_name)
    json_data=test.convert_json(stock_result)
    Name, company_description,sector,dividend,eps,capital,exchange,peratio=test.company_description(test.company_name)
    ml.load_trained_model()

    #print("The prediction for next day is: ",ml.single_day)
    print("The bias is ", ml.bias)
    single_day_pred=ml.single_day
    news_data,polarity,subjectivity=news_info.news()
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
    prediction_data=test.convert_json(ml.pred)

    return jsonify({'res':json_data,'pred':prediction_data})



if __name__=='__main__':
    app.run(debug=True,threaded=True)
