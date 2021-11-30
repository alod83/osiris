#!/bin/bash

index=$1
#echo "Son: $1"


for route in in $(cat resources/routes_names_$index.txt);
    do
	    printf "Route $route\n"
	    python3 build_next_status.py -r $route
    done

