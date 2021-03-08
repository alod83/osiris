#!/usr/bin/python

# This script predicts the grid of probabilities
from sklearn.preprocessing import RobustScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.kernel_approximation import RBFSampler
import numpy as np
import json
import math
from sklearn.externals import joblib
from geojson import Feature, Polygon, FeatureCollection, dumps

import os
import sys
from scipy.odr.odrpack import Output
from matplotlib.backends.backend_ps import ps_backend_helper
config_path = "utilities/"
sys.path.append(os.path.abspath(config_path))

from geo import get_position_in_grid
from geo import get_polygon
from utilities import print_result
from utilities import get_day_of_year
from utilities import get_minutes_from_midnight
from datetime import datetime
from numpy.distutils.misc_util import cxx_ext_match
import json

import argparse
import time
from datetime import datetime

def platt_func(x):
    return 1/(1+np.exp(-x))
    

def parse_features(args):
	
	gp = { 'cx' : 0.1, 'cy' : 0.1}

	clat = float(args.latitude)
	clng = float(args.longitude)
	[x,y] = get_position_in_grid(clng, clat, float(gp['cx']),float(gp['cy']))
	cspeed = float(args.speed)
	
	ccourse = float(args.course)
	ccourse_sin = math.sin(float(args.course))
	ccourse_cos = math.cos(float(args.course))
	cdate = datetime.strptime(args.date_time, '%Y-%m-%d %H:%M:%S')
	
	cday_of_year = get_day_of_year(cdate)
	cminutes_of_day = get_minutes_from_midnight(cdate)
	bc = int(args.basic_class)
	#cstatus_orig = [[int(y),int(x),ccourse_sin,ccourse_cos,cspeed, bc]] 
	cstatus_orig = [[clat,clng,ccourse_sin,ccourse_cos,cspeed, bc, cday_of_year,cminutes_of_day]] 
	
	return cstatus_orig,None

# receive the current position, the speed, the course and time as input

parser = argparse.ArgumentParser(description='Ship Route Preditction')
parser.add_argument('-l', '--latitude', help='define current latitude',type=float,required=True)
parser.add_argument('-n', '--longitude', help='define current longitude',type=float,required=True)
parser.add_argument('-s', '--speed',help='define current speed',required=True)
parser.add_argument('-c', '--course',help='define current course',required=True)
parser.add_argument('-b', '--basic_class',help='define basic class (0 = small ship, 1 = big ship)',required=True)
parser.add_argument('-t', '--date_time',help='define datetime format YYYY-MM-DD HH:MM:SS',required=True)

parser.set_defaults(func=parse_features)

parser.add_argument('-a', '--algorithm',help='select algorithm (default knn). Allowed algorithms are: K-Nearest Neighbor, Decision TreeBernoulli Naive Bayes, Gaussian Naive Bayes, Linear Support Vector Machines, One-vs-Rest, Kernel Approximation, Stochastic Gradient Descent, Multi-layer Perceptron',required=False)
parser.add_argument('-i', '--sdi',help='ship identifier',required=False)
parser.add_argument('-f', '--no_feature_collection',action='store_true',help='set output without feature collection',required=False)
parser.add_argument('-v', '--verbose',action='store_true',help='set verbosity to TRUE. Default is FALSE',required=False)

parser.add_argument('-o', '--output',help='specify output file name',required=False)

args = parser.parse_args()

startTime = datetime.now()

algorithm = "knn"
if args.algorithm is not None:
    algorithm = args.algorithm
    
verbose = False
if args.verbose:
    verbose = True;
    
sdi = None
if args.sdi is not None:
    sdi = args.sdi

no_feature_collection = False
if args.no_feature_collection:
    no_feature_collection = True
    
	
# current position
cstatus_orig,y = args.func(args)
	
prop = {}
polygons = {}

gp = { 'cx' : 0.1, 'cy' : 0.1}
psl = [30,45,60,120]
features = []
for ps in psl:
    
    ps = str(ps)
    
    # restore classifier set from file
    classifier = joblib.load('data/' + algorithm + '-' + ps + '.pkl') 
    
    # restore robust scaler from file
    robust_scaler = joblib.load('data/rs-' + algorithm + '-' + ps + '.pkl') 
    
    # restore classes from file
    classes = joblib.load('data/classes-' + algorithm + '-' + ps + '.pkl') 
    
    
    cstatus = robust_scaler.transform(cstatus_orig)
    
    if algorithm == 'kernel-approx':
        rbf_feature = RBFSampler(gamma=1, random_state=1)
        cstatus = rbf_feature.fit_transform(cstatus)
        
    prob = None
    if algorithm == 'one-vs-rest' or algorithm == 'linear-svm':
        f = np.vectorize(platt_func)
        raw_predictions = classifier.decision_function(cstatus)
        platt_predictions = f(raw_predictions)
        prob = platt_predictions / platt_predictions.sum(axis=1)
        #prob = prob.tolist()
        
    else:
        prob = classifier.predict_proba(cstatus).tolist()
        
    
    for i in range(0,len(classes)):
        
        if algorithm == 'one-vs-rest'  or algorithm == 'linear-svm':
            nz_prob = float("{0:.4f}".format(prob[0][i]))
        else:
            nz_prob = float("{0:.2f}".format(prob[0][i]))
        if nz_prob > 0:
            coord = classes[i].split("_")
            #print coord
            polygons[classes[i]] = get_polygon(int(coord[1]),int(coord[0]),float(gp['cx']),float(gp['cy']))
           
            try:
               prop[classes[i]]['probability_' + ps] = nz_prob
               prop[classes[i]]['row'] = int(coord[0])
               prop[classes[i]]['column'] = int(coord[1])
            except KeyError:
                prop[classes[i]] = {}
                prop[classes[i]]['probability_' + ps] = nz_prob
                prop[classes[i]]['row'] = int(coord[0])
                prop[classes[i]]['column'] = int(coord[1])
                if sdi is not None:
                	prop[classes[i]]['sdi'] = sdi
            	prop[classes[i]]['type'] = "probability"
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
	
if y is not None and no_feature_collection is False:
	prop = {}
	polygon = {}
	for ps in psl:
		ps = str(ps)
		
		if ps in y:
			coord = y[ps][0].split("_")
			label = y[ps][0]
			polygon[label] = get_polygon(int(coord[1]),int(coord[0]),float(gp['cx']),float(gp['cy']))
			try:
				
				prop[label]['row'] = int(coord[0])
				prop[label]['column'] = int(coord[1])
				prop[label]['type'] = "effective"
				prop[label]['delta'].append(ps)
			except KeyError:
				prop[label] = {}
				prop[label]['row'] = int(coord[0])
				prop[label]['column'] = int(coord[1])
				prop[label]['type'] = "effective"
				prop[label]['delta'] = [ps]
	for key in prop:			
		pol = Polygon(polygon[key])
		myprop = prop[key]
		features.append(Feature(geometry=pol,properties=myprop))
	
if no_feature_collection is False:
	result = FeatureCollection(features)
	result = dumps(result)
	print_result(args.output,result)

if verbose:
	seconds = datetime.now() - startTime
	print "Number of seconds to execute the script: " + str(seconds)
