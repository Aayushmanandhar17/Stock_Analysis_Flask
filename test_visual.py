import visual
import datetime
import pandas as pd
test=visual.visual_class()

now = datetime.datetime.now()
end_time=now.strftime("%Y-%m-%d")
start_time=pd.date_range(end = end_time, periods = 15).to_pydatetime().tolist()
start_time=start_time[0].strftime("%Y-%m-%d")

data=test.stock_data()
text,pol,sub=test.news()
print(data)
print(sub)
