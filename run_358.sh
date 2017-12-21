#!/bin/sh

####  检测输入的所有目录 是否存在 
function is_dir(){
    for dir in $*;do
        if [ ! -d ${dir} ];then
            echo "error:dir[${dir}] not exist!"
            exit 0;
        fi
    done
}

####  检测输入的所有文件 是否存在 
function is_file(){
    for dir in $*;do
        if [ ! -f ${dir} ];then
            echo "error:file[${dir}] not exist!"
            exit 0;
        fi
    done
}

if(($#<1));then
    echo "usage: $0 dir_in "
    exit 0
    
fi

dir_king=$1
is_dir $dir_king

dir_data=${dir_king}/DATA
is_dir $dir_data
ls -1 $dir_data |while read chl
do
    ### King-ASR-358/DATA/CHANNEL0/SCRIPT/000200.TXT
    ### King-ASR-358/DATA/CHANNEL0/WAVE/SPEAKER0020/SESSION0/000200001.WAV

    ####    wav name : ABBBBCDDD.wav
    ####    script name: ABBBBC.TXT
    ####    A:channel=0123  BBBB:speaker   C:session=0   DDD:ID 

    C=0

    dir_chl=${dir_data}/${chl}
    echo "log:channel=${dir_chl}"
    A=${dir_chl: -1}

    ### 包含 SCRIPT WAVE 
    dir_scp=${dir_chl}/SCRIPT
    dir_wav=${dir_chl}/WAVE
    is_dir $dir_scp  $dir_wav

    #### 每一个SPEAKER 
    ls -1 ${dir_wav}|while read line
    do
        dir_spk=${dir_wav}/${line}
        BBBB=${line:0-4:4}
        #echo "test1:" $dir_spk $BBBB

        dir_ses=${dir_spk}/SESSION0
        is_dir  $dir_ses
        dir_txt=${dir_scp}/${A}${BBBB}${C}.TXT
        is_file $dir_txt 

#        #### 每一个 ****.wav 
#        ls -1 $dir_ses|while read wav
#        do
#            #echo "test2:" $wav  ${A}${BBBB}${C}
#
#        done
    done

done


#### 检测 TABLE 内文件是否齐全 
#### King-ASR-358/TABLE
dir_table=$dir_king/TABLE
is_dir $dir_table
dos2unix ${dir_table}/*

list_table="CONTENT.TXT SAMPSTAT.TXT SESSION.TXT SPEAKER.TXT"
for file in $list_table;
do
    dir_file=${dir_table}/$file
    echo -e "\nlog: file = $dir_file"
    is_file $dir_file
    head -3 $dir_file
done



