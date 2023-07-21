#!/usr/local/bin/python3
import argparse
from datetime import datetime
from ship_status import ShipStatus
import pickle
#import pandas as pd
from geojson import Feature, Polygon, FeatureCollection, dumps
import csv
import pandas as pd
import joblib

def get_points(x, cx):
    if cx > 0:
        return [float("{0:.2f}".format(x*cx)),float("{0:.2f}".format((x+1)*cx)) ]

def get_polygon(x,y,cx,cy):
    by = get_points(y,cy)
    bx = get_points(x,cx)
    return [[
            (bx[0],by[0]), 
            (bx[0],by[1]), 
            (bx[1],by[1]),
            (bx[1],by[0]),
            (bx[0],by[0])
        ]]

def print_result(output,result):
	if output is None:
		print(result)
	else:
		with open(output, 'a') as fh:
			fh.write(result)


parser = argparse.ArgumentParser(description='Ship Route Preditction')
parser.add_argument('-l', '--latitude', help='define current latitude',type=float,required=True)
parser.add_argument('-n', '--longitude', help='define current longitude',type=float,required=True)
parser.add_argument('-s', '--speed',help='define current speed',required=True)
parser.add_argument('-c', '--course',help='define current course',required=True)
parser.add_argument('-b', '--basic_class',help='define basic class (0 = small ship, 1 = big ship)',required=True)
parser.add_argument('-t', '--date_time',help='define datetime format YYYY-MM-DD HH:MM:SS',required=False)
parser.add_argument('-f', '--no_feature_collection',action='store_true',help='set output without feature collection',required=False)
parser.add_argument('-v', '--verbose',action='store_true',help='set verbosity to TRUE. Default is FALSE',required=False)
parser.add_argument('-o', '--output',help='specify output file name',required=False)
parser.add_argument('-i', '--sdi',help='ship identifier',required=False)
args = parser.parse_args()

startTime = datetime.now()

verbose = False
if args.verbose:
    verbose = True

sdi = None
if args.sdi is not None:
    sdi = args.sdi
print(sdi)

no_feature_collection = False
if args.no_feature_collection:
    no_feature_collection = True
prop = {}
polygons = {}
features = []

use_date = False
if args.date_time:
	use_date = True
	ship_status = ShipStatus(args.latitude,args.longitude,args.course,args.speed,args.basic_class,args.date_time)
else:
	ship_status = ShipStatus(args.latitude,args.longitude,args.course,args.speed,args.basic_class)
cstatus = ship_status.get_status()
print(cstatus)
cx = ship_status.get_cx()
# restore the model
speed = float(args.speed)
if speed < 0.5:
	prop[0] = {}
	prop[0]['probability_60'] = 1.0
	prop[0]['row'] = ship_status.get_row()
	prop[0]['column'] = ship_status.get_column()
	prop[0]['type'] = "probability"
	polygons[0] = get_polygon(ship_status.get_column(),ship_status.get_row(),cx,cx)
	if sdi is not None:
		prop[0]['sdi'] = sdi
elif speed > 60:
	prop[0] = {}
	prop[0]['type'] = "maximum speed exceeded"
	polygons[0] = [[]]
else:
	path = ''
	if use_date:
		file = open(path + 'source/knn.sav', 'rb')
	else:
		file = open(path + 'source/knn_without_date.sav', 'rb')
	model = pickle.load(file)
	prob = model.predict_proba(cstatus).tolist()

	classes = model.classes_
	#y_res = model.predict(cstatus)
	#print(classes)
	#mlb = joblib.load(path + 'model/classes.pkl')
	#status.to_csv('item.csv')
	# restore the classes
	df_classes = pd.read_csv(path + 'source/classes.csv')
	#n_classes = len(prob[0])
	#classes_file =  open('source/classes.csv', 'r')
	#classes = list(csv.DictReader(classes_file))
	#n_classes = len(classes)
	#print(df_classes[df_classes['target'] == y_res[0]]['next_status_60_row'])
	#print(df_classes[df_classes['target'] == y_res[0]]['next_status_60_column'])

	#prop = {}
	#polygons = {}
	#features = []
	for i in range(0,len(prob[0])):
	#for i in range(0,n_classes):
		
		#ith_class = df_classes['target'][i]

		nz_prob = float("{0:.2f}".format(prob[0][i]))
		if nz_prob > 0:
			#target_label = mlb.inverse_transform(i)
			target_index = classes[i] 

			#targets = target_label.split('_')
			#y = float(targets[0])
			#x = float(targets[1])
			#target_label = zip(classes,nz_prob)
			
			#index = df_classes[df_classes['target'] == i].index
			#print(i)
			#y = float(df_classes.iloc[i]['next_status_60_row'])
			#x = float(df_classes.iloc[i]['next_status_60_column'])
			x = float(df_classes[df_classes['target'] == target_index]['next_status_60_column'])
			y = float(df_classes[df_classes['target'] == target_index]['next_status_60_row'])
			#print coord
			polygons[i] = get_polygon(x,y,cx,cx)
			
			try:
				prop[i]['probability_60'] = nz_prob
				prop[i]['row'] = y
				prop[i]['column'] = x
			except KeyError:
				prop[i] = {}
				prop[i]['probability_60'] = nz_prob
				prop[i]['row'] = y
				prop[i]['column'] = x
				prop[i]['type'] = "probability"
				if sdi is not None:
					prop[i]['sdi'] = sdi
i=0    
    
for key in prop:
	pol = Polygon(polygons[key])
	if no_feature_collection is True:
		result = dumps({'type': 'Feature', 'geometry' : pol, "properties" : prop[key]})
		
		print_result(args.output,result)
		if i < len(prop)-1:
			print_result(args.output,",")
	else:
		features.append(Feature(geometry=pol,properties=prop[key]))
	i = i + 1
	

	
if no_feature_collection is False:
	result = FeatureCollection(features)
	result = dumps(result)
	
	print_result(args.output,result)

#if verbose:
#	seconds = datetime.now() - startTime
#	print (f"Number of seconds to execute the script: {seconds}")


