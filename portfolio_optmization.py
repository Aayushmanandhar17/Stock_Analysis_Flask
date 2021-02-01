import pandas as pd
import numpy as np
from pandas_datareader import data as web
from datetime import datetime

stockStartDate='2010-01-01'
today=datetime.today().strftime('%Y-%m-%d')
assets=['BAC','MSFT','AMZN','M']

df=pd.DataFrame()

for stock in assets:
    df[stock]=web.DataReader(stock,data_source='yahoo',start=stockStartDate,end=today)['Adj Close']


from pypfopt.efficient_frontier import efficient_frontier
from pypfopt import risk_models
from pypfopt import expected_returns
