import pandas as pd
from sklearn.model_selection import GridSearchCV
import numpy as np
import pickle
from sklearn.metrics import precision_score, recall_score, accuracy_score

import sys, getopt

def help_and_exit():
    print('test.py -m <model_name> -d <train/test>')
    sys.exit(2)

def main(argv):
    model = ''
    dataset = ''
    try:
        opts, args = getopt.getopt(argv,"hm:d:",["model=","dataset="])
    except getopt.GetoptError:
        help_and_exit()
    for opt, arg in opts:
        if opt == '-h':
            help_and_exit()
        elif opt in ("-m", "--model"):
            model = arg
        elif opt in ("-d", "--dataset"):
            dataset = arg
    print('Model is ' + model)
    print('Dataset is ' + dataset)

    print('Reading Datasets')
    X_test = pd.read_csv('output/X_'+ dataset + '_60.csv')
    y_test = pd.read_csv('output/y_'+ dataset + '_60.csv')
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
    file = open('output/' + model + '.sav', 'rb')

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


if __name__ == "__main__":
   main(sys.argv[1:])
   


