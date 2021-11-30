#!/usr/bin/env python
# coding: utf-8

# # SRP Dataset Analysis
# 
# Dump of DB dati_ais_with_ts on CSV
# `COPY (
# SELECT date_time,mmsi,course,speed,heading,a,b,c,d,ST_X (ST_Transform (geom, 4326)) as longitude, ST_Y (ST_Transform (geom, 4326)) as latitude,source FROM ais_data
# ) TO '/home/angelica/ais_data_small.csv' WITH CSV HEADER DELIMITER ',';`
# This notebook analyses the dataset ais_data_clean contained in the postgres database dati_ais2.

# In[1]:




import pandas as pd
from math import floor
from math import copysign
import argparse

parser = argparse.ArgumentParser(description='Build Next Status')
parser.add_argument('-r', '--route', help='root name',type=int,required=True)

args = parser.parse_args()
route = args.route



df = pd.read_csv('resources/groups/group_' + str(route) + '.csv')
#df.drop(columns=['id'], axis=1,inplace=True)
#df.dropna(inplace=True)
print(df.shape[0])
#df = pd.read_csv('source/ais_data_deduplicated.csv')
#df = pd.read_csv('source/ais_data_discretized.csv')
#df.drop(columns=['Unnamed: 0'], axis=1,inplace=True)
#df.drop_duplicates(subset=['date_time', 'mmsi', 'course', 'speed', 'longitude', 'latitude', 'class'],inplace=True)
#df.to_csv('source/ais_data_deduplicated.csv')
df['date_time'] = pd.to_datetime(df['date_time'])
#print(routes.head(10))
df['next_status_60_date_time'] = 0
df['next_status_60_row'] = 0
df['next_status_60_column'] = 0

from datetime import timedelta
epsilon = 90
ps = 60 * 60
sstep = ps - epsilon
estep = ps + epsilon
result = pd.DataFrame()
#burst = 1
#threshold = burst
header = True
for i in range(0,len(df)):
    ts = df['date_time'].iloc[i]
    #print('CURRENT TS: ' + str(ts))
    next_sdate = ts + timedelta(seconds=sstep)
    #print('NEXT START DATE: ' + str(next_sdate))
    next_edate = ts + timedelta(seconds=estep)
    #print('NEXT END DATE: ' + str(next_edate))
    next_cdate = ts + timedelta(seconds=ps)
    res = df[(df['date_time'] <= next_edate) & (df['date_time'] >= next_sdate)]
    mode = 'w' if header else 'a'
    # if first element is empty, exit and drop group
    if len(res) == 0:
    	result = result.append(df.iloc[i])
    	result.to_csv('resources/next_status/ais_data_next_status_60_' + str(route) + '.csv', mode=mode, header=header)
    	result = pd.DataFrame()
    	header = False
    	continue
    # order by abs asc and take the first
    res['diff'] = abs(res['date_time'] - ts)
    res.sort_values("diff", axis = 0, ascending = True, inplace = True, na_position ='last') 
    res.reset_index(inplace=True)
        
    df.loc[i,'next_status_60_row'] = res['row'][0] 
    df.loc[i,'next_status_60_column'] = res['column'][0]
    df.loc[i,'next_status_60_date_time'] = res['date_time'][0]
    #print(group.loc[i])
    result = result.append(df.iloc[i])
    #nrows = result.shape[0]
    #mode = 'w' if header else 'a'
    #if nrows == threshold:
        #print(nrows)
        #threshold = threshold + burst
    result.to_csv('resources/next_status/ais_data_next_status_60_' + str(route) + '.csv', mode=mode, header=header)
    result = pd.DataFrame()
    header = False
        	
    #result = pd.concat([result, group])
    #print(result)


#result.to_csv('source/ais_data_next_status_60.csv')


