#-*- coding: utf-8 -*-

import os
import sys
import string

"""
    读取 log: file = King-ASR-358/TABLE/SPEAKER.TXT
    SCD     SEX     AGE     ACC
    0000    F       45      China, Jilin
    0010    M       33      China, Shandong

    到一个map中 
    map[0000] = {};
        map[0000][SEX] = F
        map[0000][AGE] = 45
        map[0000][ACC] = China_Jilin

    note:
        key1=1 第1列 必须独立唯一 不重复  
"""
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

def out_tabel_1(map_tab):
    items = map_tab.items();
    items.sort();
    for key,value in items:
        print("%s\t"%(key)),
        print(map_tab[key]);





"""
    统计某个table 中 某一列 AGE 的：
        分类个数
        各个分类的比例

    map[0000] = {};
        map[0000][SEX] = F
        map[0000][AGE] = 45
        map[0000][ACC] = China_Jilin
"""
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
    print("\n%s\tnum"%(key));
    for kk,vv in items:
        print("%s\t%d"%(kk,map_count[kk]))
        
    
"""
    King-ASR-358/TABLE/SESSION.TXT
    一个 SPEAKER  对应 CHN=0123
    
    SES	SCD	CHN	DVC	REP	ENV	NSC	UTN	CAR
    0	0000	0	SHURE WH30	China	car	noisy	220	Honda Accord
    0	0010	0	SHURE WH30	China	car	noisy	220	Toyota Corolla

    0	0000	1	Sennheiser ME104	China	car	noisy	220	Honda Accord
    0	0010	1	Sennheiser ME104	China	car	noisy	220	Toyota Corolla

    map[0000] = {}
    map[0000][0] = {} map[0000][1] = {}
    map[0000][0][DVC] = "SHURE WH30"

    key1 表示第1个key 所在的列  = 2  SCD 
    key2 表示第2个key 所在的列  = 3  CHN 

"""
def loat_table_2(dir_file, map_tab, key1, key2):
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

"""
    统计某个table 中 某一列 的：
        分类个数
        各个分类的比例

    map[0000] = {}
    map[0000][0] = {} map[0000][1] = {}
    map[0000][0][DVC] = "SHURE WH30"
"""
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


def age2str(age):
    age=int(age)
    if age>0 and age<=10:
        return 1;
    elif age>10 and age<=20:
        return 2;
    elif age>20 and age<=30:
        return 3;
    elif age>30 and age<=40:
        return 4;
    elif age>40 and age<=50:
        return 5;
    elif age>50 and age<=60:
        return 6;
    elif age>60:
        return 7;
    else:
        return 0;


def acc2str(acc):
    str="";


#### 测试部分 选取出NUM_SEL个SPEAKER 
###  使得 CHN DVC CAR SEX AGE 平均 
def select_spk(map_spk, map_ses):
    map_sel={}  ### 记录选取出来的SPEAKER 
    num_sel=0
    NUM_SEL=50 ### 选取spk的总数 


    map_count={} ### map_count['0_SHURE WH30_Honda Accord_F_2'] = ['2310', '2820']
    for k1 in map_ses.keys():
        SPK=k1;
        for k2 in map_ses[k1].keys():
            CHN=k2
            DVC = map_ses[k1][k2]['DVC']; ### map[0000][0][DVC] = "SHURE WH30"
            CAR = map_ses[k1][k2]['CAR']; ### map[0000][0][DVC] = "SHURE WH30"
            SEX=map_spk[SPK]['SEX']
            AGE=map_spk[SPK]['AGE']
            AGE=age2str(AGE);
            ACC=map_spk[SPK]['ACC']

            #key = "%s\t%s\t%s\t%s\t%s\t%s"%(CHN,DVC,CAR,SEX,AGE,ACC)
            key = "%s\t%s\t%s\t%s\t%s"%(CHN,DVC,CAR,SEX,AGE)
            if map_count.has_key(key):
                map_count[key].append(SPK);
            else:
                map_count[key]=[];
                map_count[key].append(SPK);

    items = map_count.items();
    items.sort()
    print("=======  组合个数:");
    for kk,vv in items:
        print("%s\t%d:"%(kk,len(map_count[kk]))),
        print(map_count[kk]);
    
    ### 选取说话人
    while(num_sel< NUM_SEL):
        for key in map_count.keys():  ### 每一个组合
            vec_spk=map_count[key]; ###  每一个spk
            for spk_tmp in vec_spk:
                ### 每一个spk  检测其是否 存在于map_sel中 
                if num_sel<50 and (not map_sel.has_key(spk_tmp)):
                    map_sel[spk_tmp] = 1;
                    num_sel += 1;
                    break;

    vec_out_spk=[];
    for key in map_sel:
        vec_out_spk.append(key);
        print(key);


    return vec_out_spk;


#### 获取map中某一列的所有元素的种类list
#### map_spk 中 sex列 得到: F M
def get_class_1(map_tab, key):
    vec_out=[];
    for kk in map_tab.keys():
        vv = map_tab[kk][key];
        if vv not in vec_out:
            vec_out.append(vv);

    return vec_out;




### channel=012 不包括3 中每一类spk个数 必须等于NUM_SEL=50 
### 同时保证其他所有参数尽量平均 
def select_spk_chn(map_spk, map_ses):
    NUM_SEL=50 ### 每个channel 总数  
    map_sel={}  ### 记录选取出来的SPEAKER 
    vec_chn=['0','1','2']

    ### 每一个channel内部  保持参数均衡 
    for k2 in vec_chn:
        num_sel=0
        ### map_count['SHURE WH30_Honda Accord_F_2'] = ['2310', '2820']
        map_count={} 
        ### map[0000][0][DVC] = "SHURE WH30"
        ### 每个人  对应的channel=k2 
        for k1 in map_ses.keys():
            SPK=k1;
            CHN=k2
            DVC = map_ses[k1][k2]['DVC']; 
            CAR = map_ses[k1][k2]['CAR']; ### map[0000][0][DVC] = "SHURE WH30"
            SEX=map_spk[SPK]['SEX']
            AGE=map_spk[SPK]['AGE']
            AGE=age2str(AGE);
            ACC=map_spk[SPK]['ACC']

            #key = "%s\t%s\t%s\t%s\t%s\t%s"%(CHN,DVC,CAR,SEX,AGE,ACC)
            key = "%s\t%s\t%s\t%s"%(DVC,CAR,SEX,AGE)
            if map_count.has_key(key):
                map_count[key].append(SPK);
            else:
                map_count[key]=[];
                map_count[key].append(SPK);


        print("\n=======  组合个数: channel=%s"%(k2));
        items = map_count.items();
        items.sort()
        for kk,vv in items:
            print("%s\t%d:"%(kk,len(map_count[kk]))),
            print(map_count[kk]);
        
        print("\n 选取的说话人: ");
        ### 选取说话人
        vec_spk_chn=[];  ## 记录当前channel 的 50个spk 
        while(num_sel< NUM_SEL):
            for key in map_count.keys():  ### 每一个组合
                vec_spk=map_count[key]; ###  每一个spk
                for spk_tmp in vec_spk:
                    ### 每一个spk  检测其是否 存在于map_sel中 
                    if num_sel<NUM_SEL and (not map_sel.has_key(spk_tmp)):
                        map_sel[spk_tmp] = 1;
                        num_sel += 1;
                        vec_spk_chn.append(spk_tmp);
                        print(spk_tmp);
                        break;

        #### 统计当前chn 对应的 50个spk 的某个分类的比例  
        count_rate_3( get_row_2(map_ses, vec_spk_chn, CHN, 'DVC') );
        count_rate_3( get_row_2(map_ses, vec_spk_chn, CHN, 'CAR') );


    return map_sel.keys();


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


    #map[0000] = {};
    #    map[0000][SEX] = F
    #    map[0000][AGE] = 45
    #    map[0000][ACC] = China_Jilin
    map_spk={}
    load_table_1("King-ASR-358/TABLE/SPEAKER.TXT", map_spk, 1);
    #out_tabel_1(map_spk);
    #count_rate_1(map_spk, 'SEX')
    #count_rate_1(map_spk, 'AGE')
    #count_rate_1(map_spk, 'ACC')

    #log: file = King-ASR-358/TABLE/SAMPSTAT.TXT
    #SPKRID  SESID   UTTID   SAMPRATE   BITS    DUR     SNR     CLP     MAXAMP  MEANAMP
    #0000    0       000000001  16000   16  3.475   22.165  0.000   -11.0708
    #0000    0       000000002  16000   16  2.579   20.348  0.000   -12.6095
    map_smp={}
    load_table_1("King-ASR-358/TABLE/SAMPSTAT.TXT", map_smp, 3);
    #out_tabel_1(map_smp);

    #SCD     SES     UID     TRS
    #0000    0       000000001       打开短程极速赛车二
    #0000    0       000000002       来一首背水姑娘
    map_cnt={}
    load_table_1("King-ASR-358/TABLE/CONTENT.TXT", map_cnt, 3);
    #out_tabel_1(map_cnt);

    map_ses={}
    loat_table_2("King-ASR-358/TABLE/SESSION.TXT", map_ses, 2, 3);
    #out_table_2(map_ses);

    #count_rate_2(map_ses, 'CHN')
    #count_rate_2(map_ses, 'DVC')
    #count_rate_2(map_ses, 'ENV')
    #count_rate_2(map_ses, 'NSC')
    #count_rate_2(map_ses, 'CAR')



    #### 按照一定的标准  选取出NUM_SEL个spk
    #vec_res_spk=select_spk(map_spk, map_ses);
    vec_res_spk=select_spk_chn(map_spk, map_ses);

    #### 获取map_spk 中 ['3550', '3330', '3770', '3380'] 个speaker 对应的所有SEX列
    #### 统计这些spk的各项信息 比例 
    print("\n所有说话人的比例信息");
    count_rate_3( get_row_1(map_spk, vec_res_spk, 'SEX') );
    count_rate_3( get_row_1(map_spk, vec_res_spk, 'AGE') );
    count_rate_3( get_row_1(map_spk, vec_res_spk, 'ACC') );

    #######################################################
    #SESSION:DVC  CAR
    #SPEAKER:SEX   AGE  ACC 


    sys.exit(0);









