import flask
from flask import render_template, jsonify,json
import pandas as pd
import numpy as np
import datetime
import pandas_datareader.data as web
import requests
import os

class visual_class:
    company_name="TSLA"
    close_price=0
    stock=0
    model=0

    def __init__(self):

        self.alpha_vintage="4X4XP17E6TN4ULP5"
        self.stock=self.dual_moving_average(self.company_name)
        self.buy,self.sell=self.buy_sell(self.stock)
        print("Constructor created")


    def get_start_end_date(self,range):
        now = datetime.datetime.now()
        end_time=now.strftime("%Y-%m-%d")
        start_time=pd.date_range(end = end_time, periods = range).to_pydatetime().tolist()
        start_time=start_time[0].strftime("%Y-%m-%d")
        return start_time,end_time


    def stock_data(self,name=company_name):
        start,end=self.get_start_end_date(30)
        STOCK=web.DataReader(name,'yahoo',start,end)
        result = STOCK['Close']
        return result


    def convert_json(self,data):
        new_result=data.to_json(orient="values")
        parsed = json.loads(new_result)
        x=json.dumps(parsed, indent=4)
        y=json.loads(x)
        return y

    def company_description(self,name):
        data=requests.get(f"https://www.alphavantage.co/query?function=OVERVIEW&symbol={name}&apikey={self.alpha_vintage}")
        data=data.json()
        description=data['Description']
        sector=data['Sector']
        dividend=data['DividendPerShare']
        EPS=data['EPS']
        capital=data['MarketCapitalization']
        Name=data['Name']
        exchange=data['Exchange']
        peratio=data['PERatio']


        return Name, description,sector,dividend,EPS,capital,exchange,peratio

    def dual_moving_average(self,name):
        now = datetime.datetime.now()
        end_time=now.strftime("%Y-%m-%d")
        start=datetime.datetime(2013,10,18)
        STOCK=web.DataReader(name,'yahoo',start,end_time)
        STOCK['MA30']=STOCK['Close'].rolling(30).mean()
        STOCK['MA100']=STOCK['Close'].rolling(100).mean()
        STOCK.reset_index(inplace=True)
        return STOCK

    def buy_sell(self,data):

        sigBuy=[]
        sigSell=[]
        flag=-1

        for i in range(len(data)):
            if data['MA30'][i]>data['MA100'][i]:
                if flag!=1:
                    sigBuy.append(data['Close'][i])
                    sigSell.append(np.nan)
                    flag=1
                else:
                    sigBuy.append(np.nan)
                    sigSell.append(np.nan)

            elif data['MA30'][i]<data['MA100'][i]:
                if flag!=-1:
                    sigBuy.append(np.nan)
                    sigSell.append(data['Close'][i])
                    flag=-1
                else:
                    sigBuy.append(np.nan)
                    sigSell.append(np.nan)
            else:
                sigBuy.append(np.nan)
                sigSell.append(np.nan)

        return(sigBuy,sigSell)
