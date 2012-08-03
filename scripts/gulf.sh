#! /bin/bash

rm -rf converted_gulf_files

for i in 002
    do
        FILENAME_U="./hycom_data/gulf_of_mexico/022GOMl0.04-1992_${i}_00_u.nc"
        FILENAME_V="./hycom_data/gulf_of_mexico/022GOMl0.04-1992_${i}_00_v.nc"
        c2v -v $FILENAME_U $FILENAME_V ./parameter_files/gulf.param
    done
