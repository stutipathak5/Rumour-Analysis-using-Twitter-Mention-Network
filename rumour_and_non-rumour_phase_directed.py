import pandas as pd
import networkx as nx

pd.set_option('display.max_rows', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

hindi_tweets_data=pd.read_csv('/Users/stutipathak/Networks/hindi/hindi_total.csv')
only_hindi_tokenized=pd.read_csv('/Users/stutipathak/Networks/hindi/only_hindi_tokenized.csv')

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

h = []
rumour_words = ['गोबर', 'गाय', 'कंडे', 'शुद्ध', 'शाकाहारी', 'प्याज', 'प्याज़', 'गोबर', 'शंख', 'गिलोय', 'थाली', 'ध्वनि',
                'आवाज़', 'आवाज', 'दीपक', 'मोमबत्ती', 'दिया', 'लहसुन', 'मांस', 'जानवर', 'पक्षी', 'पशु', 'मांसाहारी',
                'आध्यात्मिक', 'अध्यात्म', 'परमेश्वर', 'भक्ति']

for i in list(df.index):
    x = df.list_form[i]
    for j in x:
        for l in rumour_words:
            if j == l:
                h.append(df.index_in_whole_data[i])

index_rumours = list(set(h))
rumour_frame = df[df["index_in_whole_data"].isin(index_rumours)]

total_index=df.index_in_whole_data.tolist()
f=set(total_index).symmetric_difference(set(index_rumours))
non_rumour_index=list(f)

non_rumour_frame=df[df["index_in_whole_data"].isin(non_rumour_index)]

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

non_isolated_nodes=list(set(G.nodes))
isolated_nodes=list(set(GG.nodes).symmetric_difference(set(non_isolated_nodes)))

rumour_nodes = list(set(rumour_frame.username.tolist()))
q = list(set(non_rumour_frame.username.tolist()))
intersection = list(set(rumour_nodes) & set(q))
non_rumour_nodes = list(set(q).symmetric_difference(set(intersection)))

s = df['mentions'].tolist()
for i in range(len(df['mentions'])):
    s[i] = s[i].strip("]'[").split("', '")

q1 = []
for i in range(len(df['mentions'])):
    if ((len(s[i])) > 0):
        for j in range(len(s[i])):
            if ((len(s[i][j])) > 1):
                q1.append(s[i][j])

q2 = list(set(q1))
intersection1 = list(set(rumour_nodes) & set(q2))
intersection2 = list(set(non_rumour_nodes) & set(q2))

non_rumour_nodes1 = list(set(q2).symmetric_difference(set(intersection1)))  # mentions
non_rumour_nodes2 = list(set(non_rumour_nodes1).symmetric_difference(set(intersection2)))

i1 = list(set(rumour_nodes) & set(isolated_nodes))
rumour_nodes = list(set(rumour_nodes).symmetric_difference(set(i1)))
i2 = list(set(non_rumour_nodes) & set(isolated_nodes))
non_rumour_nodes = list(set(non_rumour_nodes).symmetric_difference(set(i2)))
i3 = list(set(non_rumour_nodes2) & set(isolated_nodes))
non_rumour_nodes2 = list(set(non_rumour_nodes2).symmetric_difference(set(i3)))

phase_info_whole= {'total_no._of_nodes': len(GG.nodes),
       'total_no._of_isolated_nodes': len(GG) - len(G),
       'total_no._of_edges': len(GG.edges),
       'total_no._of_usernames_who_have_tweeted_rumour': len(rumour_nodes),
       'total_no._of_usernames_who_have_not_tweeted_rumour': len(non_rumour_nodes),
       'total_no._of_usernames_who_have_never_tweeted_and_have_only_been_mentioned': len(non_rumour_nodes2),
       'total_no._of_tweets': len(only_hindi_tokenized),
       'total_no._of_rumour_tweets': len(rumour_frame),
       'total_no._of_non_rumour_tweets': len(non_rumour_frame)}

phase_info_whole= pd.DataFrame([phase_info_whole]).T

print(phase_info_whole)

count = 0
for r in rumour_nodes:
  count = count + len(G.out_edges(r))

f = G.subgraph(rumour_nodes).copy()
rumor_to_rumor_edges = f.number_of_edges()
rumor_to_non_rumor_edges = count - rumor_to_rumor_edges

count2 = 0
for r in rumour_nodes:
  count2 += len(G.in_edges(r))

non_rumor_to_rumor_edges = count2 - rumor_to_rumor_edges
non_rumor_to_non_rumor_edges = G.number_of_edges() - rumor_to_rumor_edges - rumor_to_non_rumor_edges - non_rumor_to_rumor_edges

phase_info_whole_interaction={'no. of connections in between rumour nodes':rumor_to_rumor_edges,
     'no. of connections in between non rumour nodes':non_rumor_to_non_rumor_edges,
     'in degree of rumour nodes from non rumour nodes':non_rumor_to_rumor_edges,
     'out degree of non rumour nodes to rumour nodes':non_rumor_to_rumor_edges,
     'in degree of non rumour nodes from rumour nodes':rumor_to_non_rumor_edges,
     'out degree of rumour nodes to non rumour nodes':rumor_to_non_rumor_edges}

phase_info_whole_interaction=pd.DataFrame([phase_info_whole_interaction]).T

print(phase_info_whole_interaction)
