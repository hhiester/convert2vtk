#! /bin/bash

# Remove the generated files before creating new ones. Other wise the file
# indexing in the generated vtk files will begin at the highest value of the
# current folder!
rm -rf converted_gulf_files

# An example of a simple for loop in bash to create many vtk files to be read
# in as a database. for U and V vector data!
for i in 002
    do
        FILENAME_U="./hycom_data/gulf_of_mexico/022GOMl0.04-1992_${i}_00_u.nc"
        FILENAME_V="./hycom_data/gulf_of_mexico/022GOMl0.04-1992_${i}_00_v.nc"
        c2v -v $FILENAME_U $FILENAME_V ./parameter_files/gulf.param
    done
