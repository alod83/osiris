import argparse
from datetime import datetime
from ship_status import ShipStatus
import pickle
import pandas as pd
from geojson import Feature, Polygon, FeatureCollection, dumps

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
		with open(output, 'ab') as fh:
			fh.write(result)


parser = argparse.ArgumentParser(description='Ship Route Preditction')
parser.add_argument('-l', '--latitude', help='define current latitude',type=float,required=True)
parser.add_argument('-n', '--longitude', help='define current longitude',type=float,required=True)
parser.add_argument('-s', '--speed',help='define current speed',required=True)
parser.add_argument('-c', '--course',help='define current course',required=True)
parser.add_argument('-b', '--basic_class',help='define basic class (0 = small ship, 1 = big ship)',required=True)
parser.add_argument('-t', '--date_time',help='define datetime format YYYY-MM-DD HH:MM:SS',required=True)
parser.add_argument('-f', '--no_feature_collection',action='store_true',help='set output without feature collection',required=False)
parser.add_argument('-v', '--verbose',action='store_true',help='set verbosity to TRUE. Default is FALSE',required=False)
parser.add_argument('-o', '--output',help='specify output file name',required=False)

args = parser.parse_args()

startTime = datetime.now()

verbose = False
if args.verbose:
    verbose = True

no_feature_collection = False
if args.no_feature_collection:
    no_feature_collection = True

ship_status = ShipStatus(args.latitude,args.longitude,args.course,args.speed,args.basic_class,args.date_time)
cstatus = ship_status.get_status()
cx = ship_status.get_cx()

# restore the model
file = open('source/knn.sav', 'rb')
model = pickle.load(file)
prob = model.predict_proba([cstatus]).tolist()


# restore the classes
df_classes = pd.read_csv('source/classes.csv')
n_classes = len(prob[0])

prop = {}
polygons = {}
features = []



for i in range(0,n_classes):
    
	#ith_class = df_classes['target'][i]

	nz_prob = float("{0:.2f}".format(prob[0][i]))
	if nz_prob > 0:
		x = df_classes['next_status_60_column'][i]
		y = df_classes['next_status_60_row'][i]
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


