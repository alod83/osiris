#!/bin/bash

#n=430000
n=100000
algo_list=("knn" "one-vs-rest" "gaussian-nb" "bernoulli-nb" "decision-tree" "linear-svm" "sgd" "kernel-approx")
#algo_list=("sgd" "kernel-approx")
#algo_list=("gaussian-nb")

for i in "${algo_list[@]}"; do
    echo "algorithm: $i"
    python train.py -a $i -n $n -b 100
    #python train-balance.py -a $i
done
