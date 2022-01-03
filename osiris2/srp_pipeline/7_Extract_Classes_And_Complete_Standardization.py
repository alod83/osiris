#!/usr/bin/env python
# coding: utf-8

# # Class Analysis
# 
# Each output class has the following label: df['next_status_60_row']  + df['next_status_60_column']
# Associate each label a number

# In[1]:


import pandas as pd

df = pd.read_csv('resources/ais_data_next_status_60.csv')


# In[20]:


df.head()


# In[2]:


df.drop(['Unnamed: 0', 'Unnamed: 0.1', 'Unnamed: 0.1.1', 'index'], axis=1, inplace=True)


# In[3]:


df['target_label'] = df['next_status_60_row'].astype(int).astype(str) + '_' +  df['next_status_60_column'].astype(int).astype(str)


# In[4]:


df['target_label'].head()


# ## Drop classes with value_counts <= 100
# 
# WARNINNG: Skip this step for now

# In[11]:



# In[15]:





# # OneHot Encoding

# In[5]:


from sklearn.preprocessing import LabelEncoder

encoder = LabelEncoder()
target = encoder.fit_transform([df['target_label'].tolist()])[0]


# In[6]:


len(encoder.classes_)


# In[8]:


import joblib
joblib.dump(encoder, 'model/classes_encoder.pkl')


# In[ ]:


len(target)


# In[10]:


def get_target(x):
    return encoder.transform([x]).tolist()[0].index(1)


# In[11]:


df['target'] = df['target_label'].apply(lambda x: get_target([x]))


# In[12]:


df['target'].head()


# In[ ]:





# # Standardize Row and Column
# 
# Standardize row and column. Use simple scaling

# In[18]:


from sklearn.preprocessing import MaxAbsScaler
import joblib

columns = ['row', 'column']
for column in columns:
    feature = np.array(df[column]).reshape(-1,1)
    scaler = MaxAbsScaler()
    scaler.fit(feature)
    feature_scaled = scaler.transform(feature)
    df[column] = feature_scaled.reshape(1,-1)[0]
    
    # save scaler
    joblib.dump(scaler, 'model/scaler_' + column + '.pkl')


# # Standardize Date

# In[43]:


import numpy as np

df['date_time'] = pd.to_datetime(df['date_time'])

df['hour_sin'] = np.sin(2 * np.pi * df['date_time'].dt.hour/24.0)
df['hour_cos'] = np.cos(2 * np.pi * df['date_time'].dt.hour/24.0)


# In[44]:


df['month_sin'] = np.sin(2 * np.pi * df['date_time'].dt.month/12.0)
df['month_cos'] = np.cos(2 * np.pi * df['date_time'].dt.month/12.0)


# In[45]:


df['day_sin'] = np.sin(2 * np.pi * df['date_time'].dt.dayofyear/365.0)
df['day_cos'] = np.cos(2 * np.pi * df['date_time'].dt.dayofyear/365.0)


# In[46]:


columns = ['class', 'course', 'speed', 'row','column','hour_sin','hour_cos','day_sin','day_cos', 'month_sin', 'month_cos','target', 'next_status_60_column', 'next_status_60_row']
df.to_csv('resources/dataset_60.csv', columns = columns)


# # Bibliography
# * [Best practice for encoding datetime in machine learning](https://stats.stackexchange.com/questions/311494/best-practice-for-encoding-datetime-in-machine-learning)
# * [What is a good way to transform Cyclic Ordinal attributes?](https://datascience.stackexchange.com/questions/5990/what-is-a-good-way-to-transform-cyclic-ordinal-attributes)

# In[ ]:




