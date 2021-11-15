#!/usr/bin/env python
# coding: utf-8

# # Clean Dataset
# 
# Load the original dataset extracted from postgres through the following command:
# 
# `COPY (
# SELECT date_time,mmsi,course,speed,heading,a,b,c,d,ST_X (ST_Transform (geom, 4326)) as longitude, ST_Y (ST_Transform (geom, 4326)) as latitude,source FROM ais_data
# ) TO '/home/angelica/ais_data_small.csv' WITH CSV HEADER DELIMITER ',';`
# 
# Cleaning includes the following operations:
# 
# * speed less than 0.1
# * speed greater than 60 - capire quanti dati sono e se correggere
# * data related to bosforo (date 2015-12-27)
# * course > 360 
# * records where a mmsi is present only once
# * drop duplicates
# * drop NaN values
# 
# **INPUT**
# * `resources/ais_data_small_ts.csv` - extracted from the postgres db
# 
# **OUTPUT**
# * `resources/ais_data_clean.csv` - cleaned dataset

# In[ ]:


#get_ipython().system('ipython --cache-size=5')


# In[ ]:


import pandas as pd

def read_burst(srow,burst,columns,header):
    df = pd.read_csv('resources/ais_data_small_ts.csv', skiprows=srow, nrows=burst, names=columns)
    df['date_time'] = pd.to_datetime(df['date_time'])
    df = df.drop(df[df['speed'] <= 0.1].index)
    df = df.drop(df[df['speed'] >= 60].index)
    df = df.drop(df[df['date_time'] < '2015-12-28'].index)
    df = df.drop(df[df['course'] > 360].index)
    df = df.drop(columns=['source','heading'], axis = 1)
    df = df.groupby(['mmsi']).filter(lambda x : x['date_time'].count() > 1)
    df.to_csv('resources/ais_data_clean_temp.csv', mode='a',header=header)


# In[ ]:


burst =100000
srow = 1
nrows = 187875665
#nrows = 1010
columns = ['date_time','mmsi','course','speed','heading','a','b','c','d','longitude','latitude','source']
header = True
while srow < nrows:
    print('srow: ' + str(srow))
    if srow > 1:
        header = False
    read_burst(srow,burst,columns,header)
    srow = srow + burst

read_burst(srow,nrows,columns,header)   


# ## Drop Duplicates and NaN values

# In[ ]:


df = pd.read_csv('resources/ais_data_clean_temp.csv')
df.drop_duplicates(subset=['date_time', 'mmsi', 'course', 'speed', 'longitude', 'latitude', 'class'],inplace=True)
df.dropna(inplace=True)
df.to_csv('resources/ais_data_clean.csv')

