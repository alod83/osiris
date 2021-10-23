import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import GridSearchCV
import numpy as np
import pickle
from sklearn.metrics import precision_score, recall_score, accuracy_score


#df = pd.read_csv('source/dataset_60_balanced.csv')
print('Reading Datasets')
X_test = pd.read_csv('output/X_train_60.csv')
y_test = pd.read_csv('output/y_train_60.csv')
print('Done')
columns = ['class', 'course','speed','row','column','hour_sin','hour_cos','day_sin','day_cos']
#X = df[columns]
#Y = df['target']

X_test = X_test[columns]
y_test = y_test['0']

import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve

# open a file, where you stored the pickled data
print('Open Model')
file = open('output/dt.sav', 'rb')

# dump information to that file
loaded_model = pickle.load(file)
print('Done')

# In[133]:



y_pred = loaded_model.predict(X_test)
precision = precision_score(y_test.values.ravel(),y_pred, average='macro')
recall = recall_score(y_test.values.ravel(),y_pred, average='macro')
accuracy = accuracy_score(y_test.values.ravel(),y_pred)
print('Precision: ' , precision)
print('Recall: ' , recall)
print('Accuracy: ' , accuracy)


