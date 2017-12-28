#!/bin/sh




#####  King_ASR_358: 
##### DEVICE01-03  SESSION01-02
#rm -rf King-ASR-358_ou*
#python2.7 read_table.py  > King-ASR-358.log 
#
#### 排序 SAMPRATE.txt
#head -1 King-ASR-358_out2/TABLE/SAMPSTAT.txt > ttt
#tail -n +2 King-ASR-358_out2/TABLE/SAMPSTAT.txt  | sort -k1  >> ttt
#mv  ttt King-ASR-358_out2/TABLE/SAMPSTAT.txt
#
#### 修改所有的script文件中的 <SSS/>
#find King-ASR-358_out2/DATA  -iname "*.txt"|while read file
#do
#    sed -i 's/<[A-Z]\+\/>//g' $file
#done




### king_asr_429:
#### DEVICE04-07  SESSION03-04
king=King-ASR-429
dos2unix ${king}/TABLE/*
rm -rf ${king}_ou*
python2.7 rrr_429.py  > ${king}.log 



