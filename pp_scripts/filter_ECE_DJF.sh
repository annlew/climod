#!/bin/sh

#SBATCH -A snic
#SBATCH -n 1
#SBATCH -t 02:00:00


#rm filelist_stat.txt

mkdir -p /scratch/local/${USER}
cd /scratch/local/${USER}

#f="/proj/climod/users/"${USER}"/ec_out/"$1"/output/ifs/"
#echo "'"$f"'" 

for g in $(ls $f)

    do
#    regular expressions: match 1870         match GG       match + four digits followed by 01, 02 or 12 e.g. +199001        
     for h in $(ls $f$g | grep -E '(1870)' | grep -E 'GG' | grep -E '\+[0-9]{4}(01|02|12)')
     do
        echo "'"$f$g/$h"'"  >> filelist_stat.txt 

      #cdo cat -selvar,$2 $f$g/$h temp1.nc




     done

     #make an average here e.g. cdo timmean
done

mv final_output /proj/climod/users/${USER}/somewhere

#rm temp1.nc
