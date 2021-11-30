#!/bin/bash

n_cores=4
routes=($(cat resources/routes_names.txt))
n_routes=${#routes[@]}
burst=$((n_routes/n_cores))

start=3540 # first 3539 already done
for ((current=0;current<n_routes;current=current+burst));
do
    echo $start
    current_routes=${routes[@]:$start:$burst}
    for route in $current_routes;
    do
	    #printf "Route $route\n"
	    #python3 build_next_status.py -r $route &
    done
    start=$((current + burst))
done



#for route in $(cat resources/routes_names.txt); 
#do
#	printf "Route $route\n"
#	python3 build_next_status.py -r $route
#done