import flask
from flask import render_template, jsonify,json
import pandas as pd
import numpy as np
import datetime
import pandas_datareader.data as web
import requests
from bs4 import BeautifulSoup

from textblob import TextBlob
#library for the news api
from newsapi import NewsApiClient
import requests

import os
import tensorflow as tf
import keras
from keras import backend as k
from keras import Sequential
from keras.models import load_model
from keras.models import model_from_json

from sklearn.preprocessing import MinMaxScaler


class visual_class:
    company_name="TSLA"
    close_price=0
    stock=0
    model=0
    pred=0
    single_day=0
    scale=0
    def __init__(self):
        self.alpha_vintage="4X4XP17E6TN4ULP5"
        self.newsapi = NewsApiClient(api_key='e0f1e850adbd4b2385bc47eb8ff22685')
        self.stock=self.dual_moving_average(self.company_name)
        self.buy,self.sell=self.buy_sell(self.stock)
        print("Constructor created")

    def news(self):
        # Accessing all the article with the company name
        all_articles = self.newsapi.get_everything(q="Bank",
                                          sources='Bloomberg,the-verge,engadget,financial-post,wired,business-insider',
                                          domains='www.bloomberg.com,techcrunch.com,www.engadget.com,business.financialpost.com,www.wired.com,www.businessinsider.com',
                                          from_param='2020-11-20',
                                          to='2020-11-30',
                                          language='en',
                                          sort_by='relevancy',
                                          page=2)
        unfiltered_news=all_articles['articles']
        total_number_article=len(unfiltered_news)
        filtered_text=[]
        for i in range(total_number_article):
            paragraph=unfiltered_news[i]['title']
            filtered_text.append(paragraph)

        description=[]
        for i in range(total_number_article):
            news_description=unfiltered_news[i]['description']
            description.append(news_description)

        Extracted_paragraph = ' '.join([str(elem) for elem in description])
        obj=TextBlob(Extracted_paragraph)
        polarity=round(obj.sentiment.polarity,2)
        subjectivity=round(obj.sentiment.subjectivity,2)


        return filtered_text,polarity,subjectivity





    def stock_data(self,name):
        start=datetime.datetime(2020,10,30)
        end=datetime.datetime(2020,11,30)

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
        start=datetime.datetime(2013,10,18)
        end=datetime.datetime(2020,11,30)
        STOCK=web.DataReader(name,'yahoo',start,end)
        STOCK['MA30']=STOCK['Close'].rolling(30).mean()
        STOCK['MA100']=STOCK['Close'].rolling(100).mean()
        STOCK.reset_index(inplace=True)


        return STOCK
# Loading the trained model
    def load_trained_model(self,json_file,hfive_file):
        with open(json_file,'r') as f:
            model_json = json.load(f)
        self.model = model_from_json(model_json)
        self.model.load_weights(hfive_file)
        self.prediction('BAC')
        self.prediction_single_day('BAC')


# Predicting the last 60 stock Price
    def prediction(self, name):
        graph=tf.get_default_graph()
        data_frame=self.dual_moving_average(name)
        df=data_frame[['Open','Volume']]

        sixty_day_df=data_frame[-60:]
        sixty_day_df.reset_index(inplace=True)

        Train_60_days=df.tail(120)[:60]
        Test_60_days=df.tail(60)

        sixty_day_price= np.array(df['Open'].tail(60))
        new_df=Train_60_days.append(Test_60_days,ignore_index=True)

        sc=MinMaxScaler(feature_range=(0,1))
        inputs=sc.fit_transform(new_df)

        new_x_test=[]
        new_y_test=[]

        for i in range(60,inputs.shape[0]):
            new_x_test.append(inputs[i-60:i])
            new_y_test.append(inputs[i,0])


        new_x_test=np.array(new_x_test)
        new_y_test=np.array(new_y_test)
        with graph.as_default():
            final_prediction=self.model.predict(new_x_test)
        s=sc.scale_
        self.scale=s
        scaler=(1/s[0])

        final_prediction=final_prediction*scaler
        final_prediction=(final_prediction+22.36)
        final_prediction=final_prediction.flatten()

        predict = np.vstack((final_prediction, sixty_day_price)).T

        sixty_day_df['PREDICT'],sixty_day_df["REAL"]=predict[:,0],predict[:,1]
        self.pred = sixty_day_df[['Date','PREDICT','REAL']]
#Creating a function that lets the user when to buy and sell


    def prediction_single_day(self,name):
        graph=tf.get_default_graph()
        data_frame=self.dual_moving_average(name)
        last_30_days=data_frame[['Open','Volume']][-60:]

        sc=MinMaxScaler(feature_range=(0,1))
        inputs_single=sc.fit_transform(last_30_days)

        Single_data=[]
        for i in range(60,61):
            Single_data.append(inputs_single[i-60:i])
        Single_data=np.array(Single_data)

        Single_final_prediction=self.model.predict(Single_data)
        print(Single_final_prediction)
        s=sc.scale_
        scaler=(1/self.scale[0])

        Single_final_prediction=(Single_final_prediction*scaler)+22.36

        self.single_day= Single_final_prediction



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
