import visual as vc
import text_filter as tf
import requests

data=vc.visual_class()
filter=tf.news_filter()
class news_data:
    def __init__(self):
        self.finnhub_api='c0c76rn48v6u6kubfclg'
        self.news_json=None

    def news(self,symbol='TSLA'):
        r = requests.get(f'https://finnhub.io/api/v1/company-news?symbol={symbol}&from=2020-04-30&to=2020-05-01&token={self.finnhub_api}')
        data=r.json()
        self.news_json=data
        return data

    def news_attribute(self,attribute='headline'):
        result=[]
        for i in range(len(self.news_json)):
            head=self.news_json[i][f'{attribute}']
            result.append(head)
        return result


data=news_data()
news=data.news()
headline=data.news_attribute('headline')
#print(headline)
merged_data=filter.clean_data(headline)
print(merged_data)
