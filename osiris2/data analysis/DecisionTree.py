# coding: utf-8

# # Import Dataset

# In[1]:


import pandas as pd
# from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import GridSearchCV
import numpy as np
import pickle
from sklearn.metrics import precision_score, recall_score, accuracy_score


#df = pd.read_csv('source/dataset_60_balanced.csv')
print('Reading Datasets')
X_train = pd.read_csv('output/X_train_60.csv')
X_test = pd.read_csv('output/X_test_60.csv')
y_train = pd.read_csv('output/y_train_60.csv')
y_test = pd.read_csv('output/y_test_60.csv')
print('Done')
columns = ['class', 'course','speed','row','column','hour_sin','hour_cos','day_sin','day_cos']
#X = df[columns]
#Y = df['target']
X_train = X_train[columns]
y_train = y_train['0']

X_test = X_test[columns]
y_test = y_test['0']



#n_classes = len(Y.unique())


# # Split Train and Test

# In[111]:


#burst = 1000
#i = 1
#N = 100 # test size per class
#cursor = burst
#y_train = pd.DataFrame()
#y_test =  pd.DataFrame()
#X_train = pd.DataFrame()
#X_test =  pd.DataFrame()
#for c in range(0, n_classes):
#    for i in range(0,burst):
#        if i < burst - N:
#            y_train = y_train.append([Y.loc[burst*c + i]])
#            X_train = X_train.append(X.loc[burst*c + i])
#        else:
#            X_test = X_test.append(X.loc[burst*c + i])
#            y_test = y_test.append([Y.loc[burst*c + i]])


#X_train.to_csv('output/X_train_60.csv')
#X_test.to_csv('output/X_test_60.csv')
#y_train.to_csv('output/y_train_60.csv')
#y_test.to_csv('output/y_test_60.csv')


# In[118]:



print('Training')
classifier = DecisionTreeClassifier()
parameters = {  'criterion'       : [ 'gini', 'entropy'],
                'splitter'        : [ 'best', 'random'],
                'max_depth'       : np.arange(1,10) # a great number may generate overfitting
                }
clf = GridSearchCV(classifier, parameters, cv = 5, n_jobs = 3)
clf.fit(X_train, y_train.values.ravel())
print('Done')




# # Save the Model

# In[120]:


print('Saving')
pickle.dump(clf.best_estimator_, open("output/dt.sav", 'wb'))
print('Done')

# # Load the saved model

# In[121]:


# open a file, where you stored the pickled data
print('Open Model')
file = open('output/dt.sav', 'rb')

# dump information to that file
loaded_model = pickle.load(file)
print('Done')

# # Predict Unseen

# In[122]:


y_score = loaded_model.predict_proba(X_test)



import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve



# In[133]:



y_pred = loaded_model.predict(X_test)
precision = precision_score(y_test.values.ravel(),y_pred, average='weighted')
recall = recall_score(y_test.values.ravel(),y_pred, average='weighted')
accuracy = accuracy_score(y_test.values.ravel(),y_pred)
print('Precision: ' , precision)
print('Recall: ' , recall)
print('Accuracy: ' , accuracy)


# In[ ]:




