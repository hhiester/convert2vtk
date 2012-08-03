#! /bin/bash

<<<<<<< HEAD
for i in {274..304}
    do
        FILENAME="./hycom_data/arctic/020arc08Nord.2005$i-00s.nc"
        c2v $FILENAME ./parameter_files/arctic.param
        FILENAME="./hycom_data/arctic/020arc08Nord.2005$i-12s.nc"
        c2v $FILENAME ./parameter_files/arctic.param
    done

FILENAME="./hycom_data/arctic/020arc08Nord.2005305-00s.nc"
c2v $FILENAME ./parameter_files/arctic.param
=======
for i in {74..75}
    do
        FILENAME="./hycom_data/020arc08Nord.20052$i-00s.nc"
        c2v $FILENAME ./parameter_files/arctic.param
        FILENAME="./hycom_data/020arc08Nord.20052$i-12s.nc"
        c2v $FILENAME ./parameter_files/arctic.param
    done
>>>>>>> eb0cbca65dcd113bc12fd557fb46327e4756b1ae
