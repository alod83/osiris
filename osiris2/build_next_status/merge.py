import pandas as pd

file = open('source/routes_names.txt', 'r')
mmsi_list = file.readlines()
 
output_df = pd.DataFrame()
period = 60
n = 0

for mmsi in mmsi_list:
    mmsi = mmsi[:-1]
    df = pd.read_csv('source/next_status/ais_data_next_status_' + str(period) + '_' + mmsi + '.csv')
    n = n + df.shape[0]
    df = df[df['next_status_' + str(period) + '_row'] > 1]
    df = df[df['next_status_' + str(period) + '_column'] > 1]
    output_df = pd.concat([output_df, df])
output_df.to_csv('source/ais_data_next_status_' + str(period) + '.csv')