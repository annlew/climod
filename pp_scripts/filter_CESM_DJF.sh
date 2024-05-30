#!/bin/sh


###############################################
# Requires input:
#  ./run.sh exp_name variable 
###############################################

rm filelist_stat.txt 2&> /dev/null

# Adjust path to your output location
f="/proj/climod/users/"${USER}"/CESM/archive/"$1"/atm/hist/"

   for g in $(ls $f | grep -E '(20[5-9]|21[0-9])' | grep -E '\-(01|02|12)' )

   do echo "'"$f$g"'" >> filelist_stat.txt

      cdo cat -selvar,$2 $f$g temp1.nc

   done

   cdo yearmean -shifttime,-16days temp1.nc temp12.nc
   cdo timmean temp12.nc tmean_$1_$2_DJF.nc
   cdo timstd temp12.nc tstd_$1_$2_DJF.nc

rm temp*

echo "done"
