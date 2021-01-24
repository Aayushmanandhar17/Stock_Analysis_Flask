import visual as vc
from bs4 import BeautifulSoup
from textblob import TextBlob
#library for the news api
from newsapi import NewsApiClient
import requests

data=vc.visual_class()

class news_data:
    def __init__(self):
        self.newsapi = NewsApiClient(api_key='e0f1e850adbd4b2385bc47eb8ff22685')

    def news(self):
        #set start date and end date
        start,end=data.get_start_end_date(15)
        # Accessing all the article with the company name
        all_articles = self.newsapi.get_everything(q="Bank",
                                          sources='Bloomberg,the-verge,engadget,financial-post,wired,business-insider',
                                          domains='www.bloomberg.com,techcrunch.com,www.engadget.com,business.financialpost.com,www.wired.com,www.businessinsider.com',
                                          from_param=start,
                                          to=end,
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
