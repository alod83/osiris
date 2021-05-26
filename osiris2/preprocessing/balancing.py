# coding: utf-8

# In[2]:


import pandas as pd

df = pd.read_csv('source/dataset_60.csv')
df.head()


# In[3]:


df.shape


# # Drop records where the corresponding class has less than 100 records

# In[4]:


target_classes = df['target'].value_counts() > 100
tc = target_classes[target_classes == True].index


# In[5]:


def myfilter(x):
    return x in tc


# In[6]:


df['delete'] = df['target'].apply(lambda x: myfilter(x))


# In[7]:


dff = df[df['delete']]


# In[8]:


dff.shape


# # Prepare data

# In[75]:


X = dff[['class','course','speed','row','column','hour_sin','hour_cos', 'day_sin', 'day_cos']]
y = dff['target']


# In[77]:


def sampling_strategy(X,y,t='over'):
    n_samples = 1000
    target_classes = ''
    if t == 'under':
        target_classes = y.value_counts() > n_samples
    else:
        target_classes = y.value_counts() < n_samples
    tc = target_classes[target_classes == True].index
    #target_classes_all = y.value_counts().index
    sampling_strategy = {}
    for target in tc:
        sampling_strategy[target] = n_samples
    return sampling_strategy


# # Under Sampling

# In[78]:


import warnings
warnings.filterwarnings('ignore')


# In[79]:


from imblearn.under_sampling import ClusterCentroids
under_sampler = ClusterCentroids(sampling_strategy=sampling_strategy(X,y,t='under'))
X_res, y_res = under_sampler.fit_resample(X, y)


# # Over Sampling

# In[83]:


from imblearn.over_sampling import RandomOverSampler
over_sampler = RandomOverSampler(sampling_strategy=sampling_strategy(X_res, y_res, t='over'))
X_res, y_res = over_sampler.fit_resample(X_res, y_res)


# In[86]:


X_res.to_csv('source/X_balanced_60.csv')
y_res.to_csv('source/y_balanced_60.csv')


# In[88]:





# In[ ]:




