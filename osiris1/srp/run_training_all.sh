#!/bin/bash

#n=430000
#n_list=(20000 50000 100000 200000 300000 400000)
n_list=(430000)
algo_list=("knn" "one-vs-rest" "gaussian-nb" "bernoulli-nb" "decision-tree" "linear-svm" "sgd" "kernel-approx")
# completare con one-vs-rest e linear-svm
#algo_list=("knn" "gaussian-nb" "bernoulli-nb" "decision-tree" "sgd" "kernel-approx")

#algo_list=("sgd" "kernel-approx")
#algo_list=("gaussian-nb")

for n in "${n_list[@]}"; do
	echo "n: $n"
	#mkdir data/$n
	#mkdir data/$n/balanced
	#python balance.py -n $n -b 100
	for i in "${algo_list[@]}"; do
    	echo "algorithm: $i"
    	python train.py -a $i -n $n -b 100 &
    	#python train-balance.py -a $i -n $n &
    done
done
