#!/bin/sh


###############################################
# A bash loop demo 
#  ./loop.sh 
###############################################



for g in {1981..2010}

   do echo $g 
   done

echo "done"

year=1981
expname=exp1

mm=01..12
    for fname in ICM{SH,GG}${exp_name}+${year}{01..12}
    do
      echo $fname
    done


