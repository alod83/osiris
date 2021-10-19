import pandas as pd
#from sklearn.model_selection import train_test_split

df = pd.read_csv('source/dataset_60_balanced.csv')

columns = ['class', 'course','speed','row','column','hour_sin','hour_cos','day_sin','day_cos']
#X = df[columns]
#Y = df['target']

#X_train, X_test, y_train, y_test = train_test_split(df[columns], df['target'],test_size=0.2)

#gets a random 80% of the entire set
df_train = df.sample(frac=0.8, random_state=1)
#gets the left out portion of the dataset
df_test = df.loc[~df.index.isin(df_train.index)]

X_train = df_train[columns]
X_test = df_test[columns]

y_train = df_train['target']
y_test = df_test['target']

X_train.to_csv('output/X_train_60_random.csv')
X_test.to_csv('output/X_test_60_random.csv')
y_train.to_csv('output/y_train_60_random.csv')
y_test.to_csv('output/y_test_60_random.csv')