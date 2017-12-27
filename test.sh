#!/bin/sh

### king_asr_429:
dos2unix king_429_test/TABLE/*
rm -rf king_429_test_ou*
python2.7 rrr.py  > king_429_test.log 




####  King_ASR_358: 
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

### 统一命名规则 



