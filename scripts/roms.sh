#! /bin/bash

rm -rf converted_roms_files/ 

for i in {18985..19233}
    do
        FILENAME="/panfs/storage.local/coaps/home/todd/ROMS-exp/ngi/output/exp30layers/CFSR/2010/ngi_his_00$i.nc"
        PARAMFILE="/panfs/storage.local/coaps/home/ndc08/code/converter/parameter_files/roms.param"
        c2v $FILENAME $PARAMFILE
    done
