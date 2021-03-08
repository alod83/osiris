import numpy as np
from imblearn.over_sampling import SMOTE, ADASYN
from imblearn.under_sampling import RandomUnderSampler
from imblearn.under_sampling import NeighbourhoodCleaningRule
from imblearn.under_sampling import NearMiss
from collections import Counter
# classifiers
from sklearn.model_selection import train_test_split
import dill
from sklearn.externals import joblib
import os.path

base_path = "/home/angelica/Git/osiris/srp/"
import os
import sys
config_path = base_path + "utilities/"
sys.path.append(os.path.abspath(config_path))
from MyAPI import MyAPI
from utilities import concatenate
from utilities import get_keys_by_value

import argparse

parser = argparse.ArgumentParser(description='Train')
parser.add_argument('-a', '--algorithm', help='SMOTE,ADASYN',required=False)
parser.add_argument('-n', '--number', help='number of records',required=True)
parser.add_argument('-b', '--burst', help='burst size',required=False)

args = parser.parse_args()

algorithm = "SMOTE"
if args.algorithm is not None:
	algorithm = args.algorithm

burst = 100
if args.burst:
	int(args.burst)
		
nr = int(args.number)

api = MyAPI()
ps = [30]
        
for psi in range(0,len(ps)):
	print ps[psi]
	out_file = open(base_path + "data/" + str(nr) + "/balance-statistics-" + algorithm + '-' + str(ps[psi]) + '.txt',"w")

	start_index = 1 
	end_index = start_index + burst
	X = []
	Y = []
	while end_index <= nr:
		X_temp, Y_temp = api.get_dataset(psi, start_index=start_index,end_index=end_index, nr=nr)
		if len(X_temp) > 0:
			X = concatenate(X,X_temp)
			Y = concatenate(Y,Y_temp)
    
		start_index = end_index + 1
		end_index = start_index + burst - 1
		if end_index > nr:
			end_index = nr
		if start_index > nr:
			end_index = nr+1
        
	print("Number of total samples " + str(len(X)))
	test_size = 0.20
	X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=test_size, random_state=42)

	np.savetxt('data/' + str(nr) + '/original_X_train-'  + algorithm + '-' +  str(ps[psi]) + '.csv', X_train, delimiter=',')
	np.savetxt('data/' + str(nr) + '/original_Y_train-' + algorithm + '-' + str(ps[psi]) + '.csv', Y_train, delimiter=',',fmt='%s')
	np.savetxt('data/' + str(nr) + '/original_X_test-' + algorithm + '-' +  str(ps[psi]) + '.csv', X_test, delimiter=',')
	np.savetxt('data/' + str(nr) + '/original_Y_test-' + algorithm + '-' + str(ps[psi]) + '.csv', Y_test, delimiter=',',fmt='%s')
  
	# filter all the classes with number of samples < 10
	out_file.write("Number of Classes " + str(len(Counter(Y_train))) + "\n")
	filtered_classes = get_keys_by_value(Counter(Y_train), 1)
	filtered_classes.extend(get_keys_by_value(Counter(Y_train), 2))
	filtered_classes.extend(get_keys_by_value(Counter(Y_train), 3))
	filtered_classes.extend(get_keys_by_value(Counter(Y_train), 4))
	filtered_classes.extend(get_keys_by_value(Counter(Y_train), 5))
	filtered_classes.extend(get_keys_by_value(Counter(Y_train), 6))
    
	#print(sorted(filtered_classes))
	out_file.write("Number of Classes to be filtered " + str(len(filtered_classes)) + "\n")

	index_list = []
	out_file.write("Number of samples before filter " + str(len(X_train)) + "\n")
	for i in range(0, len(Y_train)):
		if Y_train[i] in filtered_classes:
			index_list.append(i)

	temp_X = []
	temp_Y = []
	for i in range(0, len(X_train)):
		if i not in index_list:
			if len(temp_X) == 0:
				temp_X = np.array(X_train[i])
				temp_Y = Y_train[i]
			else:
				temp_X = np.vstack((temp_X, X_train[i]))
				temp_Y = np.append(temp_Y, Y_train[i])
    
	X_train = temp_X
	Y_train = temp_Y 

	out_file.write("Number of samples after filter " + str(len(X_train)) + "\n")
	out_file.write("Number of Classes after filter " + str(len(Counter(Y_train))) + "\n")
	classes_to_undersample = {'358_145' : 1000, '358_146' : 1000, '359_148' : 1000, '359_146' : 1000, '358_147' : 1000, '357_146' : 1000, '359_145' : 1000, '358_148' : 1000, '357_145' : 1000, '359_147' : 1000, '359_149' : 1000, '360_148' : 1000, '360_147' : 1000, '357_148' : 1000, '358_149' : 1000, '358_150' : 1000, '339_126' : 1000, '360_143' : 1000, '359_151' : 1000, '357_147' : 1000, '359_150' : 1000, '358_151' : 1000, '360_149' : 1000, '359_143' : 1000, '357_149' : 1000, '360_146' : 1000, '357_144' : 1000, '359_152' : 1000, '357_143' : 1000, '357_152' : 1000, '359_144' : 1000, '357_150' : 1000, '358_152' : 1000, '359_155' : 1000, '360_150' : 1000, '359_154' : 1000, '359_140' : 1000, '359_153' : 1000, '358_142' : 1000, '360_145' : 1000, '360_151' : 1000, '360_152' : 1000, '358_141' : 1000, '360_153' : 1000, '356_152' : 1000, '360_155' : 1000, '359_156' : 1000, '358_128' : 1000, '359_139' : 1000, '360_144' : 1000, '360_154' : 1000, '358_153' : 1000, '357_151' : 1000}
	rus = NeighbourhoodCleaningRule(random_state=42,sampling_strategy=classes_to_undersample)
	X_train, Y_train = rus.fit_resample(X_train, Y_train)
	
	out_file.write("Number of samples after undersample " + str(len(X_train)) + "\n")
	if algorithm == 'SMOTE':
		X_train, Y_train = SMOTE(k_neighbors=5).fit_resample(X_train, Y_train)
	elif algorithm == 'ADASYN':
		X_train, Y_train = SMOTE(k_neighbors=5).fit_resample(X_train, Y_train)

	out_file.write("Number of samples after balancing " + str(len(X_train)) + "\n")
    
	np.savetxt('data/' + str(nr) + '/X_train-'  + algorithm + '-' +  str(ps[psi]) + '.csv', X_train, delimiter=',')
	np.savetxt('data/' + str(nr) + '/Y_train-' + algorithm + '-' + str(ps[psi]) + '.csv', Y_train, delimiter=',',fmt='%s')
	np.savetxt('data/' + str(nr) + '/X_test-' + algorithm + '-' +  str(ps[psi]) + '.csv', X_test, delimiter=',')
	np.savetxt('data/' + str(nr) + '/Y_test-' + algorithm + '-' + str(ps[psi]) + '.csv', Y_test, delimiter=',',fmt='%s')

        

