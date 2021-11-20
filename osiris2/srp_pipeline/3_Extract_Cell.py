#!/usr/bin/env python
# coding: utf-8

# # Extract Cell (row, column) from Position
# 
# **INPUT**
# * `resources/ais_data_discretized.csv`
# 
# **OUTPUT**
# * `resources/ais_data_discretized_0.1.csv` with 0.1 equal to the default cell size

# In[1]:


cx = 0.1 # cell size


# In[ ]:


import pandas as pd

df = pd.read_csv('resources/ais_data_discretized.csv')


# In[89]:


from math import floor
from math import copysign

def get_position(x,ctype,cx):
    if cx > 0:
        if ctype == "lng":
            xg = floor(copysign((abs(x)%180),x)/cx)
            if xg == -0:
                xg = 0 
        else:
            xg = floor(x/cx)
    else:
        xg = -1
    return xg


# In[ ]:


df['row'] = df.apply(lambda x: get_position(x['latitude'],'lat',cx), axis=1)
df['column'] = df.apply(lambda x: get_position(x['longitude'],'lng',cx), axis=1)


# In[90]:


df.drop(columns=['longitude', 'latitude'], axis=1,inplace=True)


# In[92]:


df.to_csv('resources/ais_data_discretized_' + str(cx) + '.csv')

