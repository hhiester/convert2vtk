#! /bin/bash

for i in {74..75}
    do
        FILENAME="./hycom_data/020arc08Nord.20052$i-00s.nc"
        c2v $FILENAME ./parameter_files/arctic.param
        FILENAME="./hycom_data/020arc08Nord.20052$i-12s.nc"
        c2v $FILENAME ./parameter_files/arctic.param
    done
