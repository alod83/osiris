#!/usr/bin/env python
# coding: utf-8

# # Extract Routes
# This notebook prepares the extraction of next status. For each MMSI, it extracts the list of records, ordered by ascending date.
# 
# **INPUT**
# * `resources/ais_data_discretized_0.1.csv` with 0.1 equal to the default cell size
# 
# **OUTPUT**
# * `resources/routes_names.txt` - the list of all MMSIs
# * `resources/groups/group_<MMSI>.csv` - records for each MMSI, ordered by ascending dates

# In[1]:


import pandas as pd

cx = 0.1

df = pd.read_csv('resources/ais_data_discretized_' + str(cx) + '.csv')
df.shape


# In[4]:


df.drop(columns=['Unnamed: 0'], axis=1,inplace=True)


# In[5]:


df['date_time'] = pd.to_datetime(df['date_time'])


# In[9]:


routes = df.groupby(['mmsi']).apply(lambda x: x.sort_values('date_time'))
routes.head(10)


# In[10]:


routes.shape


# In[17]:


routes['mmsi'].unique()


# In[20]:


for name in routes['mmsi'].unique():
    
    with open("resources/routes_names.txt", 'a') as f:
        f.write(str(name) + "\n")
    group = routes.loc[name]
    group.reset_index(inplace=True)
    group.to_csv('resources/groups/group_' + str(name) + '.csv')


# In[21]:


len(routes['mmsi'].unique())


# In[ ]:




