import flask
from flask import render_template, jsonify,json
import pandas as pd
import numpy as np
import datetime
import pandas_datareader.data as web
import requests
from bs4 import BeautifulSoup
class visual_class:
    company_name="TSLA"
    close_price=0
    stock=0
    def __init__(self):
        self.alpha_vintage="4X4XP17E6TN4ULP5"
        self.stock=self.dual_moving_average(self.company_name)
        self.buy,self.sell=self.buy_sell(self.stock)
        print("Constructor created")


    def stock_data(self,name):
        start=datetime.datetime(2020,8,29)
        end=datetime.datetime(2020,9,29)

        STOCK=web.DataReader(self.company_name,'yahoo',start,end)
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
        start=datetime.datetime(2015,10,18)
        end=datetime.datetime(2020,10,18)
        STOCK=web.DataReader(name,'yahoo',start,end)

        STOCK['MA30']=STOCK['Close'].rolling(30).mean()
        STOCK['MA100']=STOCK['Close'].rolling(100).mean()
        STOCK.reset_index(inplace=True)

        return STOCK


#Creating a function that lets the user when to buy and sell
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
