import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

pd.set_option('display.max_rows', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

hindi_tweets_data=pd.read_csv('/content/drive/My Drive/hindi_total.csv')
only_hindi_tokenized=pd.read_csv('/content/drive/My Drive/only_hindi_tokenized.csv')

list_form = []
for i in only_hindi_tokenized["only_hindi_tokenized"]:
    i = i.strip("]'[").split("', '")
    list_form.append(i)
only_hindi_tokenized["list_form"] = list_form

date = []
for i in only_hindi_tokenized["index_in_whole_data"]:
    date.append(hindi_tweets_data["date"][i])
only_hindi_tokenized["date"] = date

only_hindi_tokenized['date'] = pd.to_datetime(only_hindi_tokenized['date'])

# select phase number
phase_number=1

if phase_number == 1:
    df=only_hindi_tokenized.loc[(only_hindi_tokenized['date'] >= '2020-01-1') & (only_hindi_tokenized['date'] <= '2020-02-01' )]
elif phase_number == 2:
    df=only_hindi_tokenized.loc[(only_hindi_tokenized['date'] >= '2020-02-02') & (only_hindi_tokenized['date'] <= '2020-03-04' )]
elif phase_number == 3:
    df=only_hindi_tokenized.loc[(only_hindi_tokenized['date'] >= '2020-03-05') & (only_hindi_tokenized['date'] <= '2020-03-13' )]
elif phase_number == 4:
    df=only_hindi_tokenized.loc[(only_hindi_tokenized['date'] >= '2020-03-14') & (only_hindi_tokenized['date'] <= '2020-03-21' )]
else:
    df=only_hindi_tokenized.loc[(only_hindi_tokenized['date'] >= '2020-03-22') & (only_hindi_tokenized['date'] <= '2020-03-31' )]

s = df['mentions'].tolist()
for i in range(len(df['mentions'])):
    s[i] = s[i].strip("]'[").split("', '")

edgelist = []
nodelist = df['username'].tolist()
for i in range(len(df['mentions'])):
    if ((len(s[i])) > 0):
        for j in range(len(s[i])):
            if ((len(s[i][j])) > 1):
                edgelist.append((df['username'].iloc[i], s[i][j]))

G = nx.DiGraph()
GG = nx.DiGraph()
G.add_edges_from(edgelist)
GG.add_edges_from(edgelist)
GG.add_nodes_from(nodelist)

distinct=set(df.username.tolist())
print("number of tweets in this phase:",len(df))
print("distinct tweeting usernames in this phase:",len(distinct))

"counting tweets per day and per user"
tweet_count=df.groupby('username').count().rename(columns={"date": "no_of_tweets_per_user"})
tweet_count.reset_index(inplace=True)
tweet_count=tweet_count[["username","no_of_tweets_per_user"]]

date_count=df.groupby('date').count().rename(columns={"username": "no_of_tweets_per_day"})
date_count.reset_index(inplace=True)
date_count=date_count[["date","no_of_tweets_per_day"]]

date_count.plot(kind='bar', x='date', y='no_of_tweets_per_day',figsize=(16,8))
plt.show()

sorted_dates=date_count.sort_values(by='no_of_tweets_per_day', ascending=False)
print("top 10 days with highest number of tweets:")
print(sorted_dates)

"calculation of the degree distribution"
in_degree=list(G.in_degree())
out_degree=list(G.out_degree())
in_degree.sort(key=lambda x: x[1], reverse=True)
out_degree.sort(key=lambda x: x[1], reverse=True)
in_degree2 = []
out_degree2 = []

for i in range(len(in_degree)):
    in_degree2.append(in_degree[i][1])

for i in range(len(out_degree)):
    out_degree2.append(out_degree[i][1])

in_dist = []
in_degree_max = max(in_degree2)
in_degree_min = min(in_degree2)
in_degree_range = in_degree_max - in_degree_min + 1
for i in range(in_degree_range):
    cnt = in_degree2.count(in_degree_max - i)
    if ((cnt != 0) and (in_degree_max - i) !=0):
        in_dist.append((in_degree_max - i, cnt))

in_degree_dataframe = pd.DataFrame(in_degree, columns=['username', 'in_Degree'])

out_dist = []
out_degree_max = max(out_degree2)
out_degree_min = min(out_degree2)
out_degree_range = out_degree_max - out_degree_min + 1
for i in range(out_degree_range):
    cnt = out_degree2.count(out_degree_max - i)
    if ((cnt != 0) and (out_degree_max - i) !=0):
        out_dist.append((out_degree_max - i, cnt))

out_degree_dataframe = pd.DataFrame(out_degree, columns=['username', 'out_Degree'])

out_degree_dataframe['in_degree'] = out_degree_dataframe['username'].map(dict(G.in_degree()))
in_degree_dataframe['out_degree'] = in_degree_dataframe['username'].map(dict(G.out_degree()))

out_degree_dataframe=out_degree_dataframe.merge(tweet_count, on='username', how='outer')
in_degree_dataframe=in_degree_dataframe.merge(tweet_count, on='username', how='outer')

out_degree_dataframe=out_degree_dataframe.fillna(0)
in_degree_dataframe=in_degree_dataframe.fillna(0)

print("top 10 highest out-degree nodes:")
print(out_degree_dataframe.head(10))
print("top 10 highest in-degree nodes:")
print(in_degree_dataframe.head(10))

d1 = pd.DataFrame(in_dist, columns=['k', 'N(k)'])
d1.plot(kind='scatter', x='k', y='N(k)',figsize=(8,8))

plt.yscale("log")
plt.xscale("log")

plt.show()

d2 = pd.DataFrame(out_dist, columns=['k', 'N(k)'])
d2.plot(kind='scatter', x='k', y='N(k)',figsize=(8,8))

plt.yscale("log")
plt.xscale("log")

plt.show()

"fitting for the power law and finding its coefficient"
def power_law(x, a, b):
    return a * np.power(x, b)

from scipy.optimize import curve_fit

pars1, cov = curve_fit(f=power_law, xdata=d1['k'], ydata=d1['N(k)'], p0=[0, 0])

pars2, cov = curve_fit(f=power_law, xdata=d2['k'], ydata=d2['N(k)'], p0=[0, 0])

print("in degree distribution power law values:",pars1)
print("out degree distribution power law values:",pars2)

"other properties of the network"
network_properties = {'number of nodes': len(GG), 'number of edges': len(G.edges()),
                      'number of isolated nodes': (len(GG) - len(G))}

d_5 = pd.DataFrame([network_properties])
print("network_properties")
print(d_5)

"clustering coefficient of each node"
in_degree=list(G.in_degree())
out_degree=list(G.out_degree())

cc = nx.clustering(G)

d_2 = pd.DataFrame(list(in_degree), columns=['username', 'in_degree'])
d_2['clustering coefficient'] = d_2['username'].map(cc)

d_2[d_2['clustering coefficient'] != 0]
d_2.plot(kind='scatter', x='in_degree', y='clustering coefficient',figsize=(8,8))
plt.title('CC of each node vs in degree')
plt.show()

d_3 = pd.DataFrame(list(out_degree), columns=['username', 'out_degree'])
d_3['clustering coefficient'] = d_2['username'].map(cc)
d_3[d_3['clustering coefficient'] != 0]
d_3.plot(kind='scatter', x='out_degree', y='clustering coefficient',figsize=(8,8))
plt.title('CC of each node vs out degree')
plt.show()
