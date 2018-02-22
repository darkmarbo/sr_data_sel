#-*- coding: utf-8 -*-

import os
import sys
import string
import shutil

'''
    所有table 都是标准格式 

'''

king="King-SR-001"
king_table="%s/TABLE"%(king)
king_data="%s/DATA"%(king)


##    读取 SPEAKER.txt
##    SCD     SEX     AGE     ACC
##    0000    F       45      China, Jilin
##    0010    M       33      China, Shandong
##
##    到一个map中 
##    map[0000] = {};
##        map[0000][SEX] = F
##        map[0000][AGE] = 45
##        map[0000][ACC] = China_Jilin
##
##    note:
##        key1=1 第1列 必须独立唯一 不重复  
def load_table_1(dir_file, map_tab, key1):

    vec_row = [];
    num_row = 0;
    flag_1 = 0;

    for line in open(dir_file, 'r').readlines():

        line=line.strip();
        vec_line=line.split("\t");

        ### 第一行 
        if flag_1 == 0 and len(vec_line)>0:
            num_row = len(vec_line);
            vec_row=vec_line;
            flag_1 = 1;
            continue;

        ### 读取数据行 
        map_tab[vec_line[key1-1]] ={};
        for ii in range(0, num_row):
            map_tab[vec_line[key1-1]][vec_row[ii]] = vec_line[ii];

### 输出map_spk等信息 
def out_table_1(map_tab):
    items = map_tab.items();
    items.sort();
    for key,value in items:
        print("%s\t"%(key)),
        print(map_tab[key]);





###    统计某个table 中 某一列 AGE 的：
###        分类个数
###        各个分类的比例
###
###    map[0000] = {};
###        map[0000][SEX] = F
###        map[0000][AGE] = 45
###        map[0000][ACC] = China_Jilin
def count_rate_1(map_tab, key):
    items = map_tab.items();
    items.sort();
    map_count={};
    for key_tmp,value_tmp in items:
        value=map_tab[key_tmp][key]; ### map[0000][AGE] = 45
        if map_count.has_key(value):
            map_count[value] += 1;
        else:
            map_count[value] = 1;

    items = map_count.items();
    items.sort()
    print("\n\nstatistic: %s\tnum:"%(key));
    for kk,vv in items:
        print("%s\t%d"%(kk,map_count[kk]))
        
### 计算某一列(DUR) 的所有元素的 数值和 
def sum_1(map_tab, key):
    items = map_tab.items();
    items.sort();
    sum=0.0
    for key_tmp,value_tmp in items:
        value=map_tab[key_tmp][key]; ### map[UTTID][TOTDUR] = 3.45
        sum += float(value);

    sum = sum/60/60;
    print("\n%s all sum = %.4f 小时"%(key, sum));


## 统计tabel 文件  某一列对应数值的均值和总和 
## key_num: 表示第几列
def stat_file_1(dir_file, key_num):

    flag_1 =0;
    sum = 0.0;
    num = 0;
    for line in open(dir_file, 'r').readlines():

        line=line.strip();
        vec_line=line.split("\t");

        ### 第一行 
        if flag_1 == 0 and len(vec_line)>0:
            num_row = len(vec_line);
            vec_row=vec_line;
            flag_1 = 1;
            continue;

        num += 1;
        sum += float(vec_line[key_num-1]);

    print("\n%s \t row=%d \t all_num=%.4f\t num=%d\tav=%.4f"%(\
                    dir_file, key_num, sum, num, sum/num ));



## 同一个spk 可能对应2个 DEVICE 或者 SESSION
## 我们想统计 某一列 DEVICE|SESSION 每个分类 包含多少个spk 
## key_num: 表示第几列
def stat_file_2(dir_file, key_num):

    flag_1 =0;
    sum = 0.0;
    map_ccc={};
    for line in open(dir_file, 'r').readlines():

        line=line.strip();
        vec_line=line.split("\t");

        ### 第一行 
        if flag_1 == 0 and len(vec_line)>0:
            num_row = len(vec_line);
            vec_row=vec_line;
            flag_1 = 1;
            continue;

        ccc = vec_line[key_num-1];
        if map_ccc.has_key(ccc):
            map_ccc[ccc] += 1;
        else:
            map_ccc[ccc] = 1;

    print("\n%s row=%d: statistic"%(dir_file, key_num));
    items = map_ccc.items();
    items.sort()
    for key, value in items:
        print("%s\t%d"%(key, map_ccc[key]));


## 统计最终的 tabel 文件(都有独立唯一的key了)
## key_num: 表示第几列是 主key
## vec_key: ['SEX','AGE']
def statistic_table(file_in, key_num, vec_key):
    map_tmp={};
    load_table_1(file_in, map_tmp, key_num);
    for kk in vec_key:
        ## 随机取一个 spk  就是为了得到map_tmp 对应的列
        count_rate_1(map_tmp, kk)
    
    
##    SESSION.txt
##    一个 SPEAKER  对应 CHN=0123
##    
##    SES	SCD	CHN	DVC	REP	ENV	NSC	UTN	CAR
##    0	0000	0	SHURE WH30	China	car	noisy	220	Honda Accord
##    0	0010	0	SHURE WH30	China	car	noisy	220	Toyota Corolla
##
##    0	0000	1	Sennheiser ME104	China	car	noisy	220	Honda Accord
##    0	0010	1	Sennheiser ME104	China	car	noisy	220	Toyota Corolla
##
##    map[0000] = {}
##    map[0000][0] = {} map[0000][1] = {}
##    map[0000][0][DVC] = "SHURE WH30"
##
##    key1 表示第1个key 所在的列  = 2  SCD 
##    key2 表示第2个key 所在的列  = 3  CHN 
def load_table_2(dir_file, map_tab, key1, key2):
    vec_row = [];
    num_row = 0;
    flag_1 = 0;

    for line in open(dir_file).xreadlines():

        line=line.strip();
        vec_line=line.split("\t");

        ### 第一行 
        if flag_1 == 0 and len(vec_line)>0:
            num_row = len(vec_line);
            vec_row=vec_line;
            flag_1 = 1;
            continue;

        ### 读取数据行 
        key1_line = vec_line[key1-1];   ### SCD
        key2_line = vec_line[key2-1];   ### CHN 

        if not map_tab.has_key(key1_line):
            map_tab[key1_line] ={};

        if not map_tab[key1_line].has_key(key2_line):
            map_tab[key1_line][key2_line] ={};

        for ii in range(0, num_row):
            map_tab[key1_line][key2_line][vec_row[ii]] = vec_line[ii];


    return 0;


### 输出 map_ses 的信息 
def out_table_2(map_tab):
    items = map_tab.items();
    items.sort();
    for key,value in items:
        print("%s"%(key))

        items_2 = map_tab[key].items();
        items_2.sort();
        for key_2,value_2 in items_2:
            print("\t%s\t"%(key_2)),
            print(map_tab[key][key_2]);

##    统计某个table 中 某一列 的：
##        分类个数
##        各个分类的比例
##
##    map[0000] = {}
##    map[0000][0] = {} map[0000][1] = {}
##    map[0000][0][DVC] = "SHURE WH30"
def count_rate_2(map_tab, key):
    map_count={};

    for k1 in map_tab.keys():
        for k2 in map_tab[k1].keys():
            value=map_tab[k1][k2][key]; ### map[0000][0][DVC] = "SHURE WH30"
            if map_count.has_key(value):
                map_count[value] += 1;
            else:
                map_count[value] = 1;

    items = map_count.items();
    items.sort()
    print("\n%s\tnum"%(key));
    for kk,vv in items:
        print("%s\t%d"%(kk,map_count[kk]))


### 年龄段映射 
def age2str(age):
    age=int(age)
    return 0;
    #if age>0 and age<=10:
    #    return 1;
    #elif age>10 and age<=20:
    #    return 2;
    #elif age>20 and age<=30:
    #    return 3;
    #elif age>30 and age<=40:
    #    return 4;
    #elif age>40 and age<=50:
    #    return 5;
    #elif age>50 and age<=60:
    #    return 6;
    #elif age>60:
    #    return 7;
    #else:
    #    return 0;

### 方言区 映射 
def acc2str(acc):
    str="";



#### 获取map中某一列的所有元素的种类list
#### map_spk 中 sex列 得到: F M
def get_class_1(map_tab, key):
    vec_out=[];
    for kk in map_tab.keys():
        vv = map_tab[kk][key];
        if vv not in vec_out:
            vec_out.append(vv);

    return vec_out;


###  获取map 中 指定某些spk  对应的 sex列
###  SEX=map_spk[SPK]['SEX']
def get_row_1(map_tab, vec_spk, key):
    vec_out=[];
    for spk in vec_spk:
        value=map_tab[spk][key];
        vec_out.append(value);

    return vec_out;



### 获取map_ses 中key1=SPEAKER  chn=channel  key='DVC'
### 获取对应通道的50人的所有dvc类型 
def get_row_2(map_tab, vec_spk, chn, key):
    vec_out=[];
    map_count={};
    for kk in vec_spk:
        vv=map_tab[kk][chn][key]
        vec_out.append(vv);

    return vec_out;



### 统计某个vector中所有元素的种类 和 比例
### [F M F F F M]: F   4   M   2   
def count_rate_3(vec_in):
    num_all = 0;
    map_count={};
    for value in vec_in:
        num_all += 1;
        if map_count.has_key(value):
            map_count[value] += 1;
        else:
            map_count[value] = 1;

    items = map_count.items();
    items.sort()
    print("\nrate:");
    for kk,vv in items:
        print("%s\t%d\t%.2f"%(kk,map_count[kk], 100.0*map_count[kk]/num_all))





if __name__ == '__main__':
    #if len(sys.argv)<3:
    #    print("usage: %s in_file out_file "%(sys.argv[0]));
    #    sys.exit(0)


    ##   1. 载入table 表格 
    ##  map[0000][SEX] = F
    ## SPKID	SEX	AGE	ACC
    ## SPEAKER0001	M	20	China, Jiangxi
    map_spk={}
    load_table_1("%s/SPEAKER.txt"%(king_table), map_spk, 1);
    ##out_table_1(map_spk);
    count_rate_1(map_spk, 'SEX')
    count_rate_1(map_spk, 'AGE')
    count_rate_1(map_spk, 'ACC')

    ## map_smp[UTTID][SPKRID] = '0001'
    ## SPKID	SESID	UTTID	SAMPRATE	BITS	DUR	SNR
    ## SPEAKER0001	SESSION02	01_0001_02_0001	16000	16	4.618	27.535
    map_smp={}
    load_table_1("%s/SAMPSTAT.txt"%(king_table), map_smp, 3);
    #out_table_1(map_smp);
    count_rate_1(map_smp, 'SAMPRATE')
    count_rate_1(map_smp, 'BITS')
    sum_1(map_smp, 'DUR');


    ## SESSION.txt 
    ## DVCID	SPKID	SESID	NSC	UTN	TOTDUR	MINDUR	MAXDUR	AVEDUR
    ## DEVICE01	SPEAKER0001	SESSION02	noisy	220	744.57	1.67	7.74	3.38
    ## DEVICE02	SPEAKER0001	SESSION05	noisy	220	744.57	1.67	7.74	3.38

    ### 文件第6列 的总和 平均值 个数 
    stat_file_1("%s/SESSION.txt"%(king_table), 5);
    stat_file_1("%s/SESSION.txt"%(king_table), 6);

    ## 同一个spk 可能对应2个 DEVICE 或者 SESSION
    ## 我们想统计 某一列 DEVICE|SESSION 每个分类 包含多少个spk 
    stat_file_2("%s/SESSION.txt"%(king_table), 1);
    stat_file_2("%s/SESSION.txt"%(king_table), 3);
    ## map[spk][device][session][key] = xxx;
    #map_ses={}
    #load_table_1("%s/SESSION.txt"%(king_table), map_ses, 2);
    ##out_table_1(map_ses);
    #count_rate_1(map_ses, 'DVC')
    #count_rate_1(map_ses, 'NSC')


    ##print("\n\n最终数据库的统计信息:");
    ##### 对于最终生成的库   统计 DEVICE  SESSION AGE SEX ACC 等比例 
    ##### SPKID	SEX	AGE	ACC
    #vec_tmp=('SEX','AGE','ACC');
    #statistic_table("%s/SPEAKER.txt"%(king_table), 1, vec_tmp);

    #vec_tmp=('SESID','DVCID');
    #statistic_table("%s/SESSION.txt"%(king_table), 2, vec_tmp);



    sys.exit(0);









