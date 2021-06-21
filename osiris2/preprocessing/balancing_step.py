# coding: utf-8

# In[1]:


import pandas as pd

df = pd.read_csv('source/dataset_60.csv')
df.head()


# In[2]:


df.shape


# # Drop records where the corresponding class has less than 100 records

# In[3]:


target_classes = df['target'].value_counts() > 100
tc = target_classes[target_classes == True].index


# In[4]:


def myfilter(x):
    return x in tc


# In[5]:


df['delete'] = df['target'].apply(lambda x: myfilter(x))


# In[6]:


dff = df[df['delete']]


# In[7]:


dff.shape


# # Prepare data

# In[41]:


X = dff[['class','course','speed','row','column','hour_sin','hour_cos', 'day_sin', 'day_cos']]
y = dff['target']


# In[42]:


y = y.astype(int)


# In[43]:


y.value_counts().count()


# get over balanced classes

# In[44]:


n_samples = 1000
target_classes = y.value_counts() > n_samples
tc = target_classes[target_classes == True].index
tc_1 = tc[len(tc)-1]
tc_2 = tc[len(tc)-2]


# Strategy: for each pair of over balanced classes, perform under sampling
# 
# calculate the number of elements for current target class

# In[22]:


y[y == tc_1].value_counts()


# In[23]:


y[y == tc_2].value_counts()


# In[24]:


idx = y[(y == tc_1) | (y == tc_2)].index
idx.max()


# In[25]:


c_X = X.loc[idx]
c_y = y.loc[idx]


# In[26]:


c_X.shape


# # Under Sampling

# In[28]:


import warnings
warnings.filterwarnings('ignore')


# In[27]:


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


# In[102]:


from imblearn.under_sampling import ClusterCentroids
from imblearn.over_sampling import RandomOverSampler

def balance(X,y,mode='under'):
    n_samples = 1000
    target_classes = None
    X_res = None
    y_res = None
    if mode == 'under':
        target_classes = y.value_counts() > n_samples
    else:
        target_classes = y.value_counts() < n_samples
        
    tc = target_classes[target_classes == True].index
    n = len(tc) -1
    #i = 0
    i = n -1
    while i <= n:
    
        tc_1 = tc[n-i]
        tc_2 = tc[n-i-1]
        print(tc_1)
        print(tc_2)
        idx = None
        if ((n+1) % 2 != 0) and (i == 0):
            tc_3 = tc[n-i-2]
            idx = y[(y == tc_1) | (y == tc_2) | (y == tc_3)].index
        else:
            idx = y[(y == tc_1) | (y == tc_2)].index
        
        c_X = X.loc[idx]
        c_y = y.loc[idx]
        
        X_res = 0
        y_res = 0
        if mode == 'under':
            under_sampler = ClusterCentroids(sampling_strategy=sampling_strategy(c_X,c_y,t='under'))
            X_res, y_res = under_sampler.fit_resample(c_X, c_y)
        else:
            over_sampler = RandomOverSampler(sampling_strategy=sampling_strategy(c_X,c_y, t='over'))
            X_res, y_res = over_sampler.fit_resample(c_X,c_y)
            
        if i == 0:
            X_res.to_csv('source/X_' + mode + '.csv')
            y_res.to_csv('source/y_' + mode + '.csv')
        else:
        	print("saving results")
            X_res.to_csv('source/X_' + mode + '.csv', header=False, mode='a')
            y_res.to_csv('source/y_' + mode + '.csv', header=False, mode='a')
        	
        # do not take the n-1 element if the number of class is odd
        if ((n+1) % 2 != 0) and (i == 0):
            i = i + 3
        else:
            i = i + 2
        


# In[94]:


#balance(X,y,mode='under')


# In[103]:


balance(X,y,mode='over')

