#!/usr/bin/env python
# coding: utf-8

# # Discretize and Scale Features
# 
# The following features are discretized:
# * speed
# * course
# * class
# 
# Simple Scaling is used for all the features.
# 
# **INPUT**
# * `resources/ais_data_clean.csv`
# 
# **OUPTUT**
# * `resources/ais_data_discretized.csv`
# * `model/scaler_course.pkl`
# * `model/scaler_speed.pkl`

# In[2]:


import pandas as pd
df = pd.read_csv('resources/ais_data_clean.csv')


# In[3]:


#df.columns


# In[4]:


df.drop(columns=['Unnamed: 0'], axis=1,inplace=True)


# In[5]:


#df.head()


# In[6]:


df['date_time'] = pd.to_datetime(df['date_time'])


# In[7]:


#df['date_time'].min()


# In[8]:


#df['date_time'].max()


# In[6]:


#df.head(10)


# In[15]:


#df.describe()


# ## Speed

# In[9]:


def get_discretized_speed(speed):
    # speed class
    sc = 0 # slow - speed between 0.5 and 3
    if speed > 3 and speed <= 14:
        sc = 1 # medium
    elif speed > 14 and speed <= 23:
        sc = 2 # high
    elif speed > 23 and speed <= 60:
        sc = 3 # very high
    elif speed > 60:
        sc = 4 # exception
    return sc 


# In[1]:


df['speed'] = df['speed'].apply(get_discretized_speed)


# ## Course

# In[10]:


def get_discretized_course(course):
    # course class
    cc = 0 # nord 337.5 - 22.5
    if course > 22.5 and course <= 67.5:
        cc = 1
    elif course > 67.5 and course <= 112.5:
        cc = 2
    elif course > 112.5 and course <= 157.5:
        cc = 3
    elif course > 157.5 and course <= 202.5:
        cc = 4
    elif course > 202.5 and course <= 247.5:
        cc = 5
    elif course > 247.5 and course <= 292.5:
        cc = 6
    elif course > 292.5 and course <= 337.5:
        cc = 7
    return cc


# In[ ]:


df['course'] = df['course'].apply(get_discretized_course)


# ## Basic Class

# In[11]:


def get_basic_class(length):
    small_ship_length = 50.0 
    small_ship_width = 6.0 # 6-8
    big_ship_length = 51.0
    big_ship_width = 15.0
    if length <= small_ship_length:
        return 0 # small ship class 0
    if length >= big_ship_length:
        return 1 # big ship class 2
    return 2 # medium ship class 1


# In[16]:


df['length'] = abs(df['b'] + df['a'])


# In[17]:


df['width'] = abs(df['c'] + df['d'])


# In[18]:


df['class'] = df['length'].apply(get_basic_class)


# In[19]:


df.drop(columns=['a', 'b','c','d'], axis=1,inplace=True)


# In[20]:


df.drop(columns=['width', 'length'], axis=1,inplace=True)


# In[68]:


#df.head(10)


# ## Scaling

# In[ ]:


from sklearn.preprocessing import MaxAbsScaler
from sklearn.externals import joblib

columns = ['course', 'speed']
for column in columns:
    feature = np.array(df[column]).reshape(-1,1)
    scaler = MaxAbsScaler()
    scaler.fit(feature)
    feature_scaled = scaler.transform(feature)
    df[column] = feature_scaled.reshape(1,-1)[0]
    
    # save scaler
    joblib.dump(scaler, 'model/scaler_' + column + '.pkl')


# In[21]:


#df['course'] = df['course']/df['course'].max()


# In[22]:


#df['speed'] = df['speed']/df['speed'].max()


# In[24]:


#df.head(10)


# In[23]:


df.to_csv('resources/ais_data_discretized.csv')


# In[ ]:




