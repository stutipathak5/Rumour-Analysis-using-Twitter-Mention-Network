import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scipy.signal as signal

pd.set_option('display.max_rows', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

hindi_tweets_data=pd.read_csv('/Users/stutipathak/Networks/hindi/hindi_total.csv')

date_data=pd.DataFrame(hindi_tweets_data["date"])
date_data['number_of_tweets'] = 0
date_data['date'] = pd.to_datetime(date_data['date']).dt.date
tweets_each_day=date_data.groupby('date', as_index=False).count()

row=pd.DataFrame({"date": "2020-01-14", "number_of_tweets": 0}, index=[7.5])
tweets_each_day=tweets_each_day.append(row, ignore_index=False).sort_index().reset_index(drop=True).reindex(["date", "number_of_tweets"], axis=1)

tweets_each_day['day'] = np.arange(1,87,1)

number_of_tweets=tweets_each_day["number_of_tweets"].to_numpy()
date=tweets_each_day["date"].to_numpy()

N=1
Wn=0.2
B,A=signal.butter(N,Wn,output='ba')
smoothed_number_of_tweets=signal.filtfilt(B,A,number_of_tweets)
tweets_each_day['smoothed_number_of_tweets']=smoothed_number_of_tweets

firstdiff=np.append([0],np.diff(smoothed_number_of_tweets))
tweets_each_day['velocity']=firstdiff

seconddiff=np.append([0],np.diff(firstdiff))
tweets_each_day['acceleration']=seconddiff

tweets_each_day.plot(x='date',y=['number_of_tweets','smoothed_number_of_tweets'])
plt.xlabel('date')
plt.show()

tweets_each_day.plot(x='date',y=['velocity','acceleration'])
plt.xlabel('date')
plt.show()
