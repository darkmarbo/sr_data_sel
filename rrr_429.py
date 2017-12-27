#-*- coding: utf-8 -*-

import os
import sys
import string
import shutil

'''
    king_asr_429 数据库 
    300个SPEAKER   每个SPEAKER 包含116句
    根据 DVC NSC SEX AGE ACC 均衡 选取总计 200人 

    DVC:
        statistic: DVC	num:
        HTC	65
        Huawei	23
        MIUI	63
        Samsung	149

    NSC:
        noisy	120
        quite	180

    CHN SES REP ENV 都是固定值 没啥用  

'''

## 是否生成wav语音  耗时 
flag_wav=0

### 去掉channel=3 其他012的chn 只要知道设备dvc和spk  就能唯一确定数据

king="king_429_test"
king_table="%s/TABLE"%(king)
king_data="%s/DATA"%(king)

king_out="%s_out"%(king)
king_out_table="%s/TABLE"%(king_out)
king_out_data="%s/DATA"%(king_out)

list_dvc_ori=('CHANNEL0', 'CHANNEL1', 'CHANNEL2'); 

NUM_SEL=200 ### 每个channel 总数  

trans_dvc={"SHURE WH30":"DEVICE01", "Sennheiser ME104":"DEVICE02", "AKG C400BL":"DEVICE03",               "DEVICE01":"SHURE WH30", "DEVICE02":"Sennheiser ME104", "DEVICE03":"AKG C400BL",               "CHANNEL0":"DEVICE01", "CHANNEL1":"DEVICE02", "CHANNEL2":"DEVICE03"}; 

trans_ses={"Honda Accord":"SESSION01", "Toyota Corolla":"SESSION02",  "SESSION01":"Honda Accord", "SESSION02":"Honda Accord"};


### 记录处理过程中  原始speaker 与 新SPEAKER的对应关系 
### 记录了 ori2new 和  new2ori 两种情况  
###  1234  --->   SPEAKER0001
trans_spk={}

## 记录最终的 spk 的所有信息: 
## SPKID	DVCID       SESID	    NSC	    UTN	 SEX AGE ACC TOTDUR	MINDUR	MAXDUR	AVEDUR
## SPEAKER0001	    DEVICE01    SESSION02	noisy	220
map_spk_final={};


"""
    ABBBBCDDD.wav
    ABBBBC.TXT
    A表示通道0123   BBBB说话人  C是session默认0     DDD语音

    CHN对应0123通道 

    SESSION.txt:
    SES	SCD	CHN	DVC	REP	ENV	NSC	UTN	CAR
    0	0000	0	SHURE WH30	China	car	noisy	220	Honda Accord

    SPEAKER.txt:
    SCD	SEX	AGE	ACC
    0000	F	45	China, Jilin

    SAMPSTAT.txt:
    SPKRID	SESID	UTTID	SAMPRATE	BITS	DUR	SNR	CLP	MAXAMP	MEANAMP
    0000	0	000000001	16000	16	3.475	22.165	0.000	-11.070824149477	0

    CONTENT.txt
    SCD	SES	UID	TRS
    0000	0	000000001	打开短程极速赛车二

"""


##    读取 SPEAKER.TXT
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
        

## 统计最终的 tabel 文件(都有独立唯一的key了)
## key_num: 表示第几列是 主key
## vec_key: ['SEX','AGE']
def statistic_table(file_in, key_num, vec_key):
    map_tmp={};
    load_table_1(file_in, map_tmp, key_num);
    for kk in vec_key:
        ## 随机取一个 spk  就是为了得到map_tmp 对应的列
        count_rate_1(map_tmp, kk)
    
    
##    SESSION.TXT
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


### 根据 DVC NSC SEX AGE ACC 均衡 
### 选取总计 200人 
def select_spk_chn(map_spk, map_ses):
    map_sel={}  ### 记录选取出来的SPEAKER 

    ### map_count['DVC NSC SEX AGE ACC'] = ['2310', '2820']
    map_count={} 

    ### map[0000][0][DVC] = "SHURE WH30"
    for SPK in map_ses.keys():
        SEX=map_spk[SPK]['SEX']
        AGE=map_spk[SPK]['AGE']
        AGE=age2str(AGE);
        ACC=map_spk[SPK]['ACC']

        DVC=map_ses[SPK]['DVC']
        NSC=map_ses[SPK]['NSC']

        #key = "%s\t%s\t%s\t%s"%(DVC,NSC,SEX,AGE)
        key = "%s\t%s\t%s\t%s"%(DVC,NSC,SEX,AGE)
        if map_count.has_key(key):
            map_count[key].append(SPK);
        else:
            map_count[key]=[];
            map_count[key].append(SPK);


    print("\n均衡信息记录:");
    items = map_count.items();
    items.sort()
    for kk,vv in items:
        print("%s\t%d:"%(kk,len(map_count[kk]))),
        print(map_count[kk]);
    

    print("\n 最终选取的说话人: ");
    vec_spk_chn=[];  
    num_sel=0
    while(num_sel < NUM_SEL):
        for key in map_count.keys():  ### 每一个组合
            vec_spk=map_count[key]; ###  当前组合中的所有spk
            for spk_tmp in vec_spk:
                ### 每一个spk  检测其是否 存在于map_sel中 
                if num_sel<NUM_SEL and (not map_sel.has_key(spk_tmp)):
                    map_sel[spk_tmp] = 1;
                    num_sel += 1;
                    vec_spk_chn.append(spk_tmp);
                    print(spk_tmp);
                    break;

    #### 统计当前chn 对应的 50个spk 的某个分类的比例  
    count_rate_3( get_row_1(map_spk, vec_spk_chn, 'SEX') );
    count_rate_3( get_row_1(map_spk, vec_spk_chn, 'AGE') );
    count_rate_3( get_row_1(map_spk, vec_spk_chn, 'ACC') );
    count_rate_3( get_row_1(map_ses, vec_spk_chn, 'DVC') );
    count_rate_3( get_row_1(map_ses, vec_spk_chn, 'NSC') );

    #### 拷贝相应的wav和script 到指定目录 
    ### DATA/CHANNEL1/WAVE/SPEAKER0010/SESSION0/100100001.WAV
    ### DATA/CHANNEL1/SCRIPT/100100.TXT
    #for spk in vec_spk_chn:

    #    if flag_wav == 1:
    #        #### 1. wave 
    #        #### DATA/CHANNEL0/WAVE/SPEAKER0830 里面是 SESSION0
    #        dir_wav="%s/DATA/CHANNEL%s/WAVE/SPEAKER%s"%(king, CHN,spk)
    #        print("test:path_dir_wav=%s"%(dir_wav));
    #        if not os.path.isdir(dir_wav):
    #            print("error:path=%s not exist!"%(dir_wav));
    #            sys.exit(0);
    #        dir_wav_out="%s/DATA/CHANNEL%s/WAVE"%(king_out, CHN)
    #        if not os.path.isdir(dir_wav_out):
    #            os.makedirs(dir_wav_out);
    #        shutil.copytree(dir_wav, "%s/SPEAKER%s"%(dir_wav_out,spk));

    #    #### 2. script   ABBBBC.TXT
    #    ### DATA/CHANNEL1/SCRIPT/100100.TXT
    #    file_name="%s%s0"%(CHN,spk)
    #    file_scp="%s/DATA/CHANNEL%s/SCRIPT/%s.TXT"%(king, CHN,file_name)
    #    if not os.path.isfile(file_scp):
    #        print("errror:file=%s not exist!"%(file_scp));
    #        sys.exit(0);
    #    dir_scp_out="%s/DATA/CHANNEL%s/SCRIPT"%(king_out, CHN)
    #    file_scp_out="%s/%s.TXT"%(dir_scp_out, file_name)
    #    if not os.path.isdir(dir_scp_out):
    #        os.makedirs(dir_scp_out);
    #    shutil.copy(file_scp, file_scp_out);

    ### 3. SESSION.TXT
    ##DVCID		SPKID		SESID		NSC		UTN	TOTDUR	MINDUR	MAXDUR	AVEDUR
    ##DEVICE01	SPEAKER0001	SESSION01	quiet	100	xx		xx		xx		xx
    #for spk in vec_spk_chn:
    #    vec_write_ses=[];
    #    vec_write_ses.append(map_ses[spk][CHN]['DVC']);
    #    vec_write_ses.append(map_ses[spk][CHN]['SCD']);
    #    vec_write_ses.append(map_ses[spk][CHN]['CAR']);
    #    vec_write_ses.append('noisy');
    #    vec_write_ses.append(map_ses[spk][CHN]['UTN']);
    #    write_session('SESSION', vec_write_ses);

    ### 4. SAMPSTAT.TXT
    ### 新格式 
    ##SPKID		SESID		UTTID				SAMPRATE	BITS	DUR		SNR	
    ##SPEAKER0001	SESSION01	01_0001_01_0001	44100		16		2.570	55.939

    ### 原始格式 :
    ### SPKRID	SESID	UTTID	SAMPRATE	BITS	DUR	SNR	CLP	MAXAMP	MEANAMP
    ### 0000	0	000000001	16000	16	3.475	22.165	0.000	-11.070824149477	0
    ### 第3列wav的id 是map的key 通过它来查找...
    #for utt in map_smp.keys():
    #    ## 300000001  ABBBBCDDD
    #    utt_chn=utt[0]
    #    utt_spk=utt[1:5]
    #    utt_ses=utt[5]
    #    utt_wav=utt[6:]
    #    ##print("test:%s\t%s\t%s\t%s\t%s"%(utt, utt_chn, utt_spk, utt_ses, utt_wav));
    #    if utt_chn == CHN and utt_spk in vec_spk_chn:
    #        vec_write_ses=[];
    #        vec_write_ses.append(utt_spk);
    #        vec_write_ses.append(map_ses[utt_spk][CHN]['CAR']);
    #        vec_write_ses.append(utt);
    #        vec_write_ses.append(map_smp[utt]['SAMPRATE']);
    #        vec_write_ses.append(map_smp[utt]['BITS']);
    #        vec_write_ses.append(map_smp[utt]['DUR']);
    #        vec_write_ses.append(map_smp[utt]['SNR']);
    #        write_session('SAMPSTAT', vec_write_ses);

    ### 5. SPEAKER.TXT  
    ### SPKID	SEX	AGE	ACC
    ### SPEAKER0001	F	25	China, Wu, Jiangsu
    ### SCD	SEX	AGE	ACC
    ### 0000	F	45	China, Jilin
    #for spk in vec_spk_chn:
    #    vec_write_ses=[];
    #    vec_write_ses.append(spk);
    #    vec_write_ses.append(map_spk[spk]['SEX']);
    #    vec_write_ses.append(map_spk[spk]['AGE']);
    #    vec_write_ses.append(map_spk[spk]['ACC']);
    #    write_session('SPEAKER', vec_write_ses);


    return map_sel.keys();



### flag= SESSION SAMPSTAT SPEAKER LABEL
### 向文件中写入一行: (DVC, SPK, SES, UTN, TOTDUR, MINDUR, MAXDUR, AVEDUR):
### 文件不存在  新建一个  并且写入第一行 
def write_session(flag, vec_in):
    dir_table="%s/TABLE"%(king_out)
    if not os.path.isdir(dir_table):
        os.makedirs(dir_table);
    
    if flag == 'SESSION':
        file_name="%s/SESSION.TXT"%(dir_table)
        if not os.path.isfile(file_name):
            fp=open(file_name,"w");
            fp.write("DVCID\tSPKID\tSESID\tNSC\tUTN\tTOTDUR\tMINDUR\tMAXDUR\tAVEDUR\n");
            fp.close()
        fp=open(file_name,"a+");
        num_tmp=0;
        for line in vec_in:
            if num_tmp == 0:
                fp.write("%s"%(line));
                num_tmp = 1;
            else:
                fp.write("\t%s"%(line));
        fp.write("\n");
        fp.close()

    elif flag == 'SAMPSTAT':
        file_name="%s/SAMPSTAT.TXT"%(dir_table)
        if not os.path.isfile(file_name):
            fp=open(file_name,"w");
            fp.write("SPKID\tSESID\tUTTID\tSAMPRATE\tBITS\tDUR\tSNR\n");
            fp.close()
        fp=open(file_name,"a+");
        num_tmp=0;
        for line in vec_in:
            if num_tmp == 0:
                fp.write("%s"%(line));
                num_tmp = 1;
            else:
                fp.write("\t%s"%(line));
        fp.write("\n");
        fp.close()
    elif flag == 'SPEAKER':
        file_name="%s/SPEAKER.TXT"%(dir_table)
        if not os.path.isfile(file_name):
            fp=open(file_name,"w");
            fp.write("SPKID\tSEX\tAGE\tACC\n");
            fp.close()
        fp=open(file_name,"a+");
        num_tmp=0;
        for line in vec_in:
            if num_tmp == 0:
                fp.write("%s"%(line));
                num_tmp = 1;
            else:
                fp.write("\t%s"%(line));
        fp.write("\n");
        fp.close()

## 转换 010600016  ---->  AA_BBBB_CC_DDDD
def trans_wav(name):

    chn=int(name[0]) + 1;
    spk=trans_spk[name[1:5]][-4:];

    ##ses=int(name[5]);
    ses=int(map_spk_final[trans_spk[name[1:5]]]['SESID'][-2:]);
    wav=int(name[6:])

    name_new="%02d_%s_%02d_%04d"%(chn,spk, ses, wav);

    return name_new;


## 转换 0 1060 0  ---->  AA_BBBB_CC
def trans_scp(name):

    chn=int(name[0]) + 1;
    spk=trans_spk[name[1:5]][-4:];

    ##ses=int(name[5]);
    ses=int(map_spk_final[trans_spk[name[1:5]]]['SESID'][-2:]);

    name_new="%02d_%s_%02d"%(chn,spk, ses);

    return name_new;


"""
    ### 格式固定之后  转换内容 名字等  
    ABBBBCDDD.wav
    ABBBBC.TXT
    A表示通道0123   BBBB说话人  C是session默认0     DDD语音




    需要从script目录下统计  
    CONTENT.txt
    SPKID	SESID	UTTID	    TRS
    0000	0	    000000001	打开短程极速赛车二

"""
def format_table():
    ### DATA/DEVICE01/WAVE/SPEAKER0001/SESSION01



    ## SESSION.txt:
    ## DVCID	    SPKID	SESID	        NSC	    UTN	TOTDUR	MINDUR	MAXDUR	AVEDUR
    ## SHURE WH30	0830	Toyota Corolla	noisy	220
    ## 结果:
    ## DVCID		SPKID		SESID		NSC		UTN	TOTDUR	MINDUR	MAXDUR	AVEDUR
    ## DEVICE01	SPEAKER0001	SESSION01	quiet	100	xx		xx		xx		xx
    #######  1. SESSION.TXT 输入  SESSION.txt 输出 
    fp_ses=open("%s/SESSION.TXT"%(king_out_table));
    fp_ses_out=open("%s/SESSION.txt"%(king_out_table), "w");
    flag=0;
    num_spk=0;

    print("\ntrans_spk: 最终选取的说话人原始ID的转换:");
    print("dvc_ori\tspk_ori\tspk_new\t");
    for line in fp_ses:

        line=line.strip();
        vec_line=line.split("\t");

        if flag == 0:
           fp_ses_out.write("%s\n"%(line)); 
           flag=1;
           continue;
        
        ## 转换 
        dvc = trans_dvc[vec_line[0]];
        ses = trans_ses[vec_line[2]];
        spk_ori = vec_line[1];
        num_spk += 1;
        spk_new = "SPEAKER%04d"%(num_spk);

        ### 记录所有spk的信息  
        ## SPKID    DVCID  SESID	    NSC	    UTN	    TOTDUR	MINDUR	MAXDUR	AVEDUR
        map_spk_final[spk_new]={};
        map_spk_final[spk_new]['DVCID']=dvc;
        map_spk_final[spk_new]['SESID']=ses;

        trans_spk[spk_ori] = spk_new;
        trans_spk[spk_new] = spk_ori;
        print("%s\t%s\t%s"%(vec_line[0],spk_ori, spk_new));

        fp_ses_out.write("%s\t%s\t%s"%(dvc, spk_new, ses));
        for value in vec_line[3:]:
            fp_ses_out.write("\t%s"%(value));
        fp_ses_out.write("\n");
        

    fp_ses.close();
    fp_ses_out.close();

    ### 重新读取新的SESSION.txt 文件  得到map_spk_final 
    ##load_table_1("%s/SESSION.txt"%(king_out_table), map_spk_final, 2);
    

    ## SPEAKER.txt:
    ## SPKID	SEX	AGE	ACC
    ## 0830	M	20	China, Jiangxi
    ## 结果
    ## SPKID		SEX	AGE	ACC
    ## SPEAKER0001	F	25	China, Wu, Jiangsu
    ###################    2. SPEAKER.TXT 
    fp_spk=open("%s/SPEAKER.TXT"%(king_out_table));
    fp_spk_out=open("%s/SPEAKER.txt"%(king_out_table), "w");
    flag=0;
    for line in fp_spk:

        line=line.strip();
        vec_line=line.split("\t");

        if flag == 0:
           fp_spk_out.write("%s\n"%(line)); 
           flag=1;
           continue;
        
        ## 转换 
        spk_new  = trans_spk[vec_line[0]];

        fp_spk_out.write("%s"%(spk_new));
        for value in vec_line[1:]:
            fp_spk_out.write("\t%s"%(value));
        fp_spk_out.write("\n");
        

    fp_spk.close();
    fp_spk_out.close();

    ## SAMPSTAT.txt:
    ## SPKID	SESID	        UTTID	    SAMPRATE	BITS	DUR	    SNR
    ## 1660	Toyota Corolla	016600150	16000	    16	    1.994	28.898
    ## 结果:
    ## SPKID		SESID		UTTID				SAMPRATE	BITS	DUR		SNR	
    ## SPEAKER0001	SESSION01	01_0001_01_0001	44100		16		2.570	55.939
    fp_smp=open("%s/SAMPSTAT.TXT"%(king_out_table));
    fp_smp_out=open("%s/SAMPSTAT.txt"%(king_out_table), "w");
    flag=0;
    for line in fp_smp:

        line=line.strip();
        vec_line=line.split("\t");

        if flag == 0:
           fp_smp_out.write("%s\n"%(line)); 
           flag=1;
           continue;
        
        ## 转换 speaker 
        spk_new  = trans_spk[vec_line[0]];
        fp_smp_out.write("%s"%(spk_new));
        ## 转换 session 
        ses_new  = trans_ses[vec_line[1]];
        fp_smp_out.write("\t%s"%(ses_new));
        ## 转换 UTTID  010600016: ABBBBCDDD.wav
        wav_new=trans_wav(vec_line[2]);
        fp_smp_out.write("\t%s"%(wav_new));

        for value in vec_line[3:]:
            fp_smp_out.write("\t%s"%(value));
        fp_smp_out.write("\n");
        

    fp_smp.close();
    fp_smp_out.close();


    ### todo  使用 sample文件中的 dur信息 重写SESSION文件
    ## SPKID   SESID   UTTID   SAMPRATE    BITS    DUR SNR
    ## SPEAKER0051 SESSION01   00_0051_01_0016 16000   16  3.129   18.305
    fp_smp=open("%s/SAMPSTAT.txt"%(king_out_table));
    fp_ses=open("%s/SESSION.txt"%(king_out_table));
    map_spk_smp={};  ### 记录每个spk对应的: UTN TOTDUR  MINDUR  MAXDUR 
    flag=0;
    for line in fp_smp:

        line=line.strip();
        vec_line=line.split("\t");
        if flag == 0:
           flag=1;
           continue;
        
        spk=vec_line[0];
        dur=float(vec_line[5]);
        if map_spk_smp.has_key(spk):
            map_spk_smp[spk]['UTN'] += 1;
            map_spk_smp[spk]['TOTDUR'] += dur;
            if map_spk_smp[spk]['MINDUR'] > dur:
                map_spk_smp[spk]['MINDUR'] = dur;
            if map_spk_smp[spk]['MAXDUR'] < dur:
                map_spk_smp[spk]['MAXDUR'] = dur;
        else:
            map_spk_smp[spk] = {};
            map_spk_smp[spk]['UTN'] = 1;
            map_spk_smp[spk]['TOTDUR'] = dur;
            map_spk_smp[spk]['MINDUR'] = dur;
            map_spk_smp[spk]['MAXDUR'] = dur;


    ## DVCID	SPKID	SESID	NSC	UTN	TOTDUR	MINDUR	MAXDUR	AVEDUR
    ## DEVICE01	SPEAKER0001	SESSION02	noisy	220
    ### 读 SESSION.txt 中每行 
    fp_ses_out=open("%s/SESSION_out.txt"%(king_out_table), "w");
    flag=0
    for line in fp_ses:

        line=line.strip();
        vec_line=line.split("\t");
        if flag == 0:
           flag=1;
           fp_ses_out.write("%s\n"%(line)); 
           continue;

        for vv in vec_line[0:4]:
           fp_ses_out.write("%s\t"%(vv)); 

        spk = vec_line[1];
        utn=vec_line[4];
        utn_2=map_spk_smp[spk]['UTN'];
        totdur=map_spk_smp[spk]['TOTDUR'];
        mindur=map_spk_smp[spk]['MINDUR'];
        maxdur=map_spk_smp[spk]['MAXDUR'];

        avedur=totdur/utn_2;

        fp_ses_out.write("%d"%(utn_2)); 
        fp_ses_out.write("\t%.2f"%(totdur)); 
        fp_ses_out.write("\t%.2f"%(mindur)); 
        fp_ses_out.write("\t%.2f"%(maxdur)); 
        fp_ses_out.write("\t%.2f\n"%(avedur)); 
        

    fp_smp.close();
    fp_ses.close();
    fp_ses_out.close();
    ###  将 SESSION_out.txt 替换 SESSION.txt

    ##shutil.remove("%s/SESSION.txt"%(king_out_table));
    shutil.move("%s/SESSION_out.txt"%(king_out_table) ,"%s/SESSION.txt"%(king_out_table));


## 生成wav的最终格式  所有wav和目录重命名 
## 原始: DATA/CHANNEL2/WAVE/SPEAKER3010/SESSION0/230100188.WAV
## 新的: DATA/DEVICE02/WAVE/SPEAKER0001/SESSION2/02_0001_02_0188.wav
def rename_data():
    ## ['CHANNEL0', 'CHANNEL1', 'CHANNEL2'] 
    for dvc_ori in list_dvc_ori:

        dvc_new = trans_dvc[dvc_ori];

        ## King-ASR-358_out2/DATA/DEVICE02
        path_dvc_ori = "%s/%s"%(king_out_data, dvc_ori);
        path_dvc_new = "%s/%s"%(king_out_data, dvc_new);


        ## King-ASR-358_out2/DATA/DEVICE02/WAVE
        ## 不同的 speaker 进入到不同的 session 中 
        path_WAVE="%s/WAVE"%(path_dvc_ori)
        list_spk=os.listdir(path_WAVE);
        for spk_ori in list_spk:

            path_spk_ori="%s/%s"%(path_WAVE, spk_ori)
            spk_new = trans_spk[spk_ori[-4:]]
            path_spk_new="%s/WAVE/%s"%(path_dvc_new, spk_new)

            path_ses_ori="%s/SESSION0"%(path_spk_ori)
            path_ses_new="%s/%s"%(path_spk_new, map_spk_final[spk_new]['SESID'])

            #print("makedirs  %s"%(path_spk_new));
            os.makedirs(path_ses_new);

            list_wav = os.listdir(path_ses_ori);
            for wav_ori in list_wav: 
                ## 230100188.WAV
                path_wav_ori = "%s/%s"%(path_ses_ori, wav_ori);
                wav_new = "%s.WAV"%(trans_wav(wav_ori[0:9]))
                path_wav_new = "%s/%s"%(path_ses_new, wav_new);
                #print("mv  %s  --->  %s"%(path_wav_ori, path_wav_new));
                shutil.move(path_wav_ori, path_wav_new);
                ##os.rename(path_wav_ori, path_wav_new);

    return 0;


## 处理所有wav对应的script  
## King-ASR-358_out2/DATA/CHANNEL1/SCRIPT/100500.TXT
def create_script():
    ## ['CHANNEL0', 'CHANNEL1', 'CHANNEL2'] 
    for dvc_ori in list_dvc_ori:

        dvc_new = trans_dvc[dvc_ori];

        ## King-ASR-358_out2/DATA/DEVICE02/SCRIPT
        path_scp_ori = "%s/%s/SCRIPT"%(king_out_data, dvc_ori);
        path_scp_new = "%s/%s/SCRIPT"%(king_out_data, dvc_new);
        os.makedirs(path_scp_new);
        list_scp=os.listdir(path_scp_ori);
        for scp_ori in list_scp:
            scp_new = "%s.TXT"%(trans_scp(scp_ori[0:6]));

            fp_in=open("%s/%s"%(path_scp_ori, scp_ori))
            fp_out=open("%s/%s"%(path_scp_new, scp_new), "w")
            ##100500001	拨打张瑜的133的电话
            ##	拨打张瑜的幺三三的电话
            num_line=0;
            for line in fp_in:

                num_line += 1;

                line=line.strip();
                if line == "":
                    continue;

                vec_line = line.split("\t");

                if num_line%2 == 1:
                    fp_out.write("%s\t"%(trans_wav(vec_line[0])));
                else:
                    fp_out.write("%s\n"%(vec_line[0]));

            fp_in.close();
            fp_out.close();

        ## 删除其他无用数据 
        ## King-ASR-358_out2/DATA/CHANNEL
        dir_rm="%s/%s"%(king_out_data, dvc_ori)
        shutil.rmtree(dir_rm);


if __name__ == '__main__':
    #if len(sys.argv)<3:
    #    print("usage: %s in_file out_file "%(sys.argv[0]));
    #    sys.exit(0)


    ##   1. 载入table 表格 
    ##  map[0000][SEX] = F
    ## SCD	SEX	AGE	ACC
    ## 0001	M	35	China, Liaoning,
    map_spk={}
    load_table_1("%s/speaker.txt"%(king_table), map_spk, 1);
    ##out_table_1(map_spk);
    count_rate_1(map_spk, 'SEX')
    count_rate_1(map_spk, 'AGE')
    count_rate_1(map_spk, 'ACC')

    ## map_smp[UTTID][SPKRID] = '0001'
    ## SPKRID	SESID	UTTID	SAMPRATE	BITS	DUR	SNR	CLP	MAXAMP	MEANAMP
    ## 0300	0	003000001	16000	16	1.790	20.854	0.000	-5.65440062727062	-14
    map_smp={}
    load_table_1("%s/sampstat.txt"%(king_table), map_smp, 3);
    #out_table_1(map_smp);
    #count_rate_1(map_smp, 'SPKRID')
    #count_rate_1(map_smp, 'SESID')


    ##SES	SCD	CHN	DVC	REP	ENV	NSC	UTN
    ##0	0001	0	Samsung	China	office	quite	116
    map_ses={}
    load_table_1("%s/session.txt"%(king_table), map_ses, 2);
    #out_table_1(map_ses);
    count_rate_1(map_ses, 'DVC')
    count_rate_1(map_ses, 'NSC')




    ###  2. 根据各种信息均衡 挑选出50*3个说话人 
    ##### 每个设备(channel)内选取  50人 
    ##### 按照一定的标准  选取出NUM_SEL个spk
    vec_res_spk = select_spk_chn(map_spk, map_ses);

    ##### 获取map_spk 中 ['3550', '3330', '3770', '3380'] 个speaker 对应的所有SEX列
    ##### 统计这些spk的各项信息 比例 
    #print("\n所有说话人的比例信息");
    #count_rate_3( get_row_1(map_spk, vec_res_spk, 'SEX') );
    #count_rate_3( get_row_1(map_spk, vec_res_spk, 'AGE') );
    #count_rate_3( get_row_1(map_spk, vec_res_spk, 'ACC') );

    ##################################  3. 格式固定的table中   修改具体信息项
    #format_table();


    ### 重新命名所有wav和相关目录 
    #if flag_wav == 1:
    #    rename_data();

    ### 创建script目录 和 重新命名所有script  
    #create_script();


    #print("\n\n最终数据库的统计信息:");
    #### 对于最终生成的库   统计 DEVICE  SESSION AGE SEX ACC 等比例 
    #### SPKID	SEX	AGE	ACC
    #vec_tmp=('SEX','AGE','ACC');
    #statistic_table("%s/SPEAKER.txt"%(king_out_table), 1, vec_tmp);

    #vec_tmp=('SESID','DVCID');
    #statistic_table("%s/SESSION.txt"%(king_out_table), 2, vec_tmp);



    sys.exit(0);









