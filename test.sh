#!/bin/sh

###### 合并 N 个数据库  
dir_out=King-SR-001
table_out=${dir_out}/TABLE

######## 1.  King_ASR_358: 
######## DEVICE01-03  SESSION01-02
#king=King-ASR-358
#king_out=${king}_out
#rm -rf  ${king_out}
#python2.7 rrr_358.py  >  ${king}.log 
#
##### 排序 
#for file in "SAMPSTAT.txt" "SESSION.txt"  "SPEAKER.txt";do 
#    file=${king_out}/TABLE/${file}
#    head -1 ${file} > ttt
#    tail -n +2  ${file}  | sort -k1  >> ttt
#    mv   ttt  ${file}
#
#done
#
#### 修改所有的script文件中的 <SSS/>
#find ${king_out}/DATA  -iname "*.txt"|while read file
#do
#    sed -i 's/<[A-Z]\+\/>//g' $file
#done
#
#
#
#
#### 2.  king_asr_429:
##### DEVICE04-07  SESSION03-04
#king=King-ASR-429
#king_out=${king}_out
#dos2unix ${king}/TABLE/*
#rm -rf ${king}_ou*
#python2.7 rrr_429.py  > ${king}.log 
#
##### 排序 
#for file in "SAMPSTAT.txt" "SESSION.txt"  "SPEAKER.txt";do 
#    file=${king_out}/TABLE/${file}
#    head -1 ${file} > ttt
#    tail -n +2  ${file}  | sort -k1  >> ttt
#    mv   ttt  ${file}
#
#done
#### 修改所有的script文件中的 <SSS/>
#find  ${king_out}/DATA  -iname "*.txt"|while read file
#do
#    sed -i 's/<[A-Z]\+\/>//g' $file
#done
#
#
#
##### 3.  king_asr_052:
###### DEVICE08-10  SESSION04-10
#king=King-ASR-052
#king_out=${king}_out
#dos2unix ${king}/TABLE/*
#rm -rf ${king}_ou*
#python2.7 rrr_052.py  > ${king}.log 
#
#
###### 排序 
#for file in "SAMPSTAT.txt" "SESSION.txt"  "SPEAKER.txt";do 
#    file=${king_out}/TABLE/${file}
#    head -1 ${file} > ttt
#    tail -n +2  ${file}  | sort -k1  >> ttt
#    mv   ttt  ${file}
#
#done
#
##### 修改所有的script文件中的 <SSS/>
#find  ${king_out}/DATA  -iname "*.txt"|while read file
#do
#    sed -i 's/<[A-Z]\+\/>//g' $file
#    sed -i 's/\t \+/\t/g' $file
#done
#
#
#

#rm -rf ${dir_out}  &&  mkdir -p ${dir_out}/DATA
#rm -rf ${table_out}  &&  mkdir -p ${table_out}
#for king in "King-ASR-358_out" "King-ASR-429_out" "King-ASR-052_out";do
#
#    cp -r ${king}/DATA/DEVICE*  ${dir_out}/DATA/
#
#    for file in "SAMPSTAT.txt" "SESSION.txt"  "SPEAKER.txt";do 
#
#        file_in=${king}/TABLE/${file}
#        file_out=${dir_out}/TABLE/${file}
#        echo "${file_in}   ---->   ${file_out}"
#
#        if [ ! -f ${file_out} ];then
#            head -1 ${file_in} > ttt
#            tail -n +2  ${file_in}  | sort -k1  >> ttt
#            mv ttt ${file_out}
#        else
#            tail -n +2  ${file_in}  | sort -k1  >> ${file_out}
#        fi
#    done
#    
#done
####### 排序 
#for file in "SAMPSTAT.txt" "SESSION.txt"  "SPEAKER.txt";do 
#    file=${dir_out}/TABLE/${file}
#    head -1 ${file} > ttt
#    tail -n +2  ${file}  | sort -k1  >> ttt
#    mv   ttt  ${file}
#
#done
#
#### 处理方言区标签中的 , 
#sed -i 's/,$//g'  ${dir_out}/TABLE/SPEAKER.txt
#
#python2.7  statistic_table.py  > ${dir_out}.log
#
#
#
###### 质检后  格式处理 
#find  ${dir_out}/DATA -name "*.TXT" |while read txt
#do
#    ### 每一个txt文件  UTF-8 带BOM头   dos格式
#    python Add_BOM_Dir.py  ${txt}  ${txt}.bom
#    unix2dos ${txt}.bom
#    mv ${txt}.bom   ${txt}
#
#done
#
#
###### 质检后  格式处理 
#find  ${dir_out}/TABLE -name "*.txt" |while read txt
#do
#    ### 每一个txt文件  UTF-8 带BOM头   dos格式
#    python Add_BOM_Dir.py  ${txt}  ${txt}.bom
#    unix2dos ${txt}.bom
#    mv ${txt}.bom   ${txt}
#
#done

### Heilongjinag
sed -i 's/Heilongjinag/Heilongjiang/g'  King-SR-001/TABLE/SPEAKER.txt   


