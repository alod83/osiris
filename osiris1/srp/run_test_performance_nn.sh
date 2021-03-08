#!/bin/bash

dataset_size=(2000 4000 8000)

for i in "${dataset_size[@]}" 
do
   echo $i
   cd ../manage
   python build_reduced_dataset.py -n $i
   cd ../srp
   python train-nn.py
   mkdir data/mlp-$i
   mv data/*mlp*.pkl data/mlp-$i
   mv data/*mlp*.txt data/mlp-$i
   
   # discretize
   python train-nn.py -d
   mkdir data/mlp-$i-discretize
   mv data/*mlp*.pkl data/mlp-$i-discretize
   mv data/*mlp*.txt data/mlp-$i-discretize
done
