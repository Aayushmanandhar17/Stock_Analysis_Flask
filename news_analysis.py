import visual as vc
import text_filter as tf
import requests
import pandas as pd
import numpy as np

yahoo_data=vc.visual_class()
filter=tf.news_filter()
class news_data:
    def __init__(self):
        self.finnhub_api='c0c76rn48v6u6kubfclg'
        self.news_json=None

    def news(self,symbol='TSLA'):
        start,end=yahoo_data.get_start_end_date(2)
        r = requests.get(f'https://finnhub.io/api/v1/company-news?symbol={symbol}&from={start}&to={end}&token={self.finnhub_api}')
        data=r.json()
        self.news_json=data
        return data

    def news_attribute(self,attribute='headline'):
        result=[]
        for i in range(len(self.news_json)):
            head=self.news_json[i][f'{attribute}']
            result.append(head)
        return result

    def metrics(self,symbol,attribute):
        pass



data=news_data()
news=data.news()
headline=data.news_attribute('headline')
merged_data=filter.clean_data(headline)
sen=filter.getSubjectivity()
pol=filter.getPolarity()
SIA=filter.getSIA()

stock_price=yahoo_data.today_yahoo_data()

data={'Open':stock_price['Open'],
      'High':stock_price['High'],
      'Low':stock_price['Low'],
      'Volume':stock_price['Volume'],
      'Subjectivity':sen,
      'Polarity':pol,
      'Negative':SIA['neg'],
      'Positive':SIA['pos'],
      'Neutral':SIA['neu'],
      'Compound':SIA['compound']
      }
# Create the pandas DataFrame
df = pd.DataFrame(data)
df.reset_index(drop=True,inplace=True)
print(df)
