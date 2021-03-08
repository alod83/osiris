#!/bin/bash

ncores=4
#nrows=38017577
nrows=19008788 # gestisco la meta dei record

srows=1
burst=4752198
erows=$burst

for route in $(cat source/routes_names.txt); 
do
	printf "Route $route\n"
	python3.8 build_next_status.py -r $route
done