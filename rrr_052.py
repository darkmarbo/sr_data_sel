#-*- coding: utf-8 -*-

import os
import sys
import string
import shutil

'''
    King-ASR-052 数据库 
    400个SPEAKER   每个SPEAKER 包含2个session  总计300多句
    根据 DVC NSC SEX AGE ACC 均衡 选取总计 300人 

    所有spk 第一个session0 对应的都是office安静  所以 只需要记录另一个session即可！！！

'''

## 是否生成wav语音  耗时 
flag_wav_1=1    ## 第1次copy
flag_wav_2=1    ## 第2次 rename

king="King-ASR-052"
king_table="%s/TABLE"%(king)
king_data="%s/DATA"%(king)

king_out="%s_out"%(king)
king_out_table="%s/TABLE"%(king_out)
king_out_data="%s/DATA"%(king_out)

list_dvc_ori=('CHANNEL0'); 

NUM_SEL=300 ### 每个channel 总数  

#### DEVICE04-07  SESSION03-04
trans_dvc={"Huawei D1Q":"DEVICE08", "Huawei D2":"DEVICE09", "Huawei P1":"DEVICE10",                       "DEVICE08":"Huawei D1Q", "DEVICE09":"Huawei D2", "DEVICE10":"Huawei P1" }; 

trans_ses={"office":"SESSION04", "campus":"SESSION05", "car":"SESSION06", "family":"SESSION07","restaurant":"SESSION08", "street":"SESSION09","subway":"SESSION10",    "SESSION04":"office", "SESSION05":"campus", "SESSION06":"car", "SESSION07":"family", "SESSION08":"restaurant", "SESSION09":"street", "SESSION10":"subway" };


### 记录处理过程中  原始speaker 与 新SPEAKER的对应关系 
### 记录了 ori2new 和  new2ori 两种情况  
###  1234  --->   SPEAKER0001
trans_spk={}

## 记录最终的 spk 的所有信息: 
## SPKID	DVCID       SESID	    NSC	    UTN	 SEX AGE ACC TOTDUR	MINDUR	MAXDUR	AVEDUR
## SPEAKER0001	    DEVICE01    SESSION02	noisy	220
## SPEAKER0001	    DEVICE01    SESSION04	noisy	220
map_spk_final={};




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
##    map[0000][0][DVC] = "SHURE WH30"
##    map[0000][1][DVC] = "xxxx"
##
##    key1 表示第1个key 所在的列  = 2  SCD 
##    key2 表示第2个key 所在的列  = 1  SES 
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
### 返回 说话人的list 
def select_spk_chn(map_spk, map_ses):
    map_sel={}  ### 记录选取出来的SPEAKER 

    ### map_count['DVC NSC SEX AGE ACC'] = ['2310', '2820']
    map_count={} 

    ## count_rate_1(map_spk, 'SEX')
    ## count_rate_1(map_spk, 'AGE')
    ## count_rate_1(map_spk, 'ACC')

    ## count_rate_2(map_ses, 'DVC');   ## Huwei D1Q  D2  P1
    ## count_rate_2(map_ses, 'ENV');   ### campus  car street
    ## count_rate_2(map_ses, 'NSC');  ### noisy quiet  每人的2个session 分别安静和噪音 

    ### map[0000][0][DVC] = "SHURE WH30"
    for SPK in map_ses.keys():
        SEX=map_spk[SPK]['SEX']
        ## AGE=map_spk[SPK]['AGE']
        ## AGE=age2str(AGE);
        ACC=map_spk[SPK]['ACC']

        DVC_0=map_ses[SPK]['0']['DVC']
        DVC_1=map_ses[SPK]['1']['DVC']
        ENV_0=map_ses[SPK]['0']['ENV']
        ENV_1=map_ses[SPK]['1']['ENV']
        NSC_0=map_ses[SPK]['0']['NSC']
        NSC_1=map_ses[SPK]['1']['NSC']

        key = "%s\t%s\t%s\t%s\t%s"%(DVC_0, DVC_1, ENV_0, ENV_1, SEX)
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
    

    vec_res_spk=[];  
    num_sel=0
    while(num_sel < NUM_SEL):
        for key in map_count.keys():  ### 每一个组合
            vec_spk=map_count[key]; ###  当前组合中的所有spk
            for spk_tmp in vec_spk:
                ### 每一个spk  检测其是否 存在于map_sel中 
                if num_sel<NUM_SEL and (not map_sel.has_key(spk_tmp)):
                    map_sel[spk_tmp] = 1;
                    num_sel += 1;
                    vec_res_spk.append(spk_tmp);
                    break;


    return vec_res_spk;



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



## 转换 UTTID   ABBBBCDDD.wav   --->  AA_BBBB_CC_DDDD.wav
## 01_0001_01_0001  其中AA和CC 都用map_spk_final 来查找 
## SPKID	SESID	UTTID	SAMPRATE	BITS	DUR	SNR
## 0340	street	003401193	16000	16	7.200	24.014
## C=0或者1  ==0表示普通安静office  ==1表示特殊session  使用map查找 
def trans_wav(name):
    ## name=003401193
    ##chn=int(name[0]) + 1;
    spk=trans_spk[name[1:5]][-4:];
    chn=int(map_spk_final[trans_spk[name[1:5]]]['DVCID'][-2:]);

    ## 此说话人 特殊的那个session 
    ses=int(map_spk_final[trans_spk[name[1:5]]]['SESID'][-2:]);
    if name[5] == '0':
        ses = 4; ### office  

    wav=int(name[6:])

    name_new="%02d_%s_%02d_%04d"%(chn, spk, ses, wav);

    return name_new;


## 转换 0 1060 0  ---->  AA_BBBB_CC
def trans_scp(name):

    ##chn=int(name[0]) + 1;
    spk=trans_spk[name[1:5]][-4:];
    chn=int(map_spk_final[trans_spk[name[1:5]]]['DVCID'][-2:]);

    ##ses=int(name[5]);
    ses=int(map_spk_final[trans_spk[name[1:5]]]['SESID'][-2:]);
    if name[5] == '0':
        ses = 4; ### office  

    name_new="%02d_%s_%02d"%(chn, spk, ses);

    return name_new;



'''
    根据提取出  200 个spk
    把相应 wav script  table 数据拷贝出来  
'''
def format_table_1(vec_spk_chn):
    ### 拷贝相应的wav和script 到指定目录 
    CHN='0'
    for spk in vec_spk_chn:
        if flag_wav_1 == 1:
            #### 1. wave ABBBBCDDD.wav 
            ## King-ASR-052/DATA/CHANNEL0/WAVE/SPEAKER0001/SESSION1/000011150.WAV
            dir_wav="%s/DATA/CHANNEL%s/WAVE/SPEAKER%s"%(king, CHN, spk)
            #print("test:path_dir_wav=%s"%(dir_wav));
            if not os.path.isdir(dir_wav):
                print("error:path=%s not exist!"%(dir_wav));
                sys.exit(0);
            dir_wav_out="%s/DATA/CHANNEL%s/WAVE"%(king_out, CHN)
            if not os.path.isdir(dir_wav_out):
                os.makedirs(dir_wav_out);
            shutil.copytree(dir_wav, "%s/SPEAKER%s"%(dir_wav_out,spk));

        #### 2. script   ABBBBC.TXT
        ## King-ASR-052/DATA/CHANNEL0/SCRIPT/000010.TXT
        for ses_tmp in ['0','1']:
            file_name="%s%s%s"%(CHN,spk, ses_tmp)
            file_scp="%s/DATA/CHANNEL%s/SCRIPT/%s.TXT"%(king, CHN, file_name)
            if not os.path.isfile(file_scp):
                print("errror:file=%s not exist!"%(file_scp));
                sys.exit(0);
            dir_scp_out="%s/DATA/CHANNEL%s/SCRIPT"%(king_out, CHN)
            file_scp_out="%s/%s.TXT"%(dir_scp_out, file_name)
            if not os.path.isdir(dir_scp_out):
                os.makedirs(dir_scp_out);
            shutil.copy(file_scp, file_scp_out);

    #### 3. SESSION.TXT
    #### 新格式 
    ###  DVCID		SPKID		SESID		NSC		UTN	TOTDUR	MINDUR	MAXDUR	AVEDUR
    ###  DEVICE01	SPEAKER0001	SESSION01	quiet	100	xx		xx		xx		xx
    #### 原始格式 :
    ## SES	SCD	    CHN	DVC	        REP	    ENV	    NSC	    UTN
    ## 0	0001	0	Huawei  P1	China	office	quiet	150

    #### map_ses['0001']['0'][DVC]='Huawei P1'
    #### map_ses['0001']['1'][DVC]='xxxx'
    for spk in vec_spk_chn:
        ### 每个speaker 对应两个ses=0|1
        for ses_tmp in ['0','1']:
            vec_write_ses=[];
            vec_write_ses.append(map_ses[spk][ses_tmp]['DVC']);  ## DVCID
            vec_write_ses.append(map_ses[spk][ses_tmp]['SCD']);  ## SPKID
            ## ENV=[subway office ...] 来代替SESSION
            ## 所有office 全部对应 quiet 其他所有情景全部对应 noisy
            vec_write_ses.append(map_ses[spk][ses_tmp]['ENV']);  ## SESID
            vec_write_ses.append(map_ses[spk][ses_tmp]['NSC']);  ## NSC
            vec_write_ses.append(map_ses[spk][ses_tmp]['UTN']);
            write_session('SESSION', vec_write_ses);




    #### 4. SAMPSTAT.TXT
    #### 新格式 
    ###SPKID		SESID		UTTID				SAMPRATE	BITS	DUR		SNR	
    ###SPEAKER0001	SESSION01	01_0001_01_0001	44100		16		2.570	55.939
    #### 原始格式 :
    #### SPKRID	SESID	UTTID	SAMPRATE	BITS	DUR	SNR	CLP	MAXAMP	MEANAMP
    #### 0001	0	000010000	16000	16	3.040	31.224	0.000	-10.7378196135792	-11

    #### 第3列wav的id 是map的key 通过它来查找...
    for utt in map_smp.keys():
        ## 300000001  ABBBBCDDD
        utt_chn=utt[0]
        utt_spk=utt[1:5]
        utt_ses=utt[5]
        utt_wav=utt[6:]
        ##print("test:%s\t%s\t%s\t%s\t%s"%(utt, utt_chn, utt_spk, utt_ses, utt_wav));
        if utt_chn == CHN and utt_spk in vec_spk_chn:
            vec_write_ses=[];
            vec_write_ses.append(utt_spk);
            vec_write_ses.append(map_ses[utt_spk][utt_ses]['ENV']);
            vec_write_ses.append(utt);
            vec_write_ses.append(map_smp[utt]['SAMPRATE']);
            vec_write_ses.append(map_smp[utt]['BITS']);
            vec_write_ses.append(map_smp[utt]['DUR']);
            vec_write_ses.append(map_smp[utt]['SNR']);
            write_session('SAMPSTAT', vec_write_ses);



    #### 5. SPEAKER.TXT  
    #### SPKID	SEX	AGE	ACC
    #### SPEAKER0001	F	25	China, Wu, Jiangsu
    #### SCD	SEX	AGE	ACC
    #### 0001	M	35	China, Liaoning,
    for spk in vec_spk_chn:
        vec_write_ses=[];
        vec_write_ses.append(spk);
        vec_write_ses.append(map_spk[spk]['SEX']);
        vec_write_ses.append(map_spk[spk]['AGE']);
        vec_write_ses.append(map_spk[spk]['ACC']);
        write_session('SPEAKER', vec_write_ses);



"""
    ### 格式固定之后  转换内容 名字等  
    ABBBBCDDD.wav
    ABBBBC.TXT
    A表示通道0   BBBB说话人  C是session默认0     DDD语音

"""
def format_table_2():

    ## 1.  SESSION.txt:
    ## 原始:
    ## DVCID	    SPKID	SESID	NSC	UTN	TOTDUR	MINDUR	MAXDUR	AVEDUR
    ## Huawei P1	0139	office	quiet	150
    ## 结果:
    ## DVCID		SPKID		SESID		NSC		UTN	TOTDUR	MINDUR	MAXDUR	AVEDUR
    ## DEVICE04	SPEAKER0301	SESSION03	quiet	100	xx		xx		xx		xx

    #######  1. SESSION.TXT 输入  SESSION.txt 输出 
    fp_ses=open("%s/SESSION.TXT"%(king_out_table));
    fp_ses_out=open("%s/SESSION.txt"%(king_out_table), "w");
    flag=0;
    num_spk=500; ## 第一个库已经提取了300人  第二个库200人  
    line_tmp = 0;
    spk_new="";

    print("\ntrans_spk: 最终选取的说话人原始ID的转换:");
    print("dvc_ori\tspk_ori\tspk_new\t:::");
    for line in fp_ses:

        line=line.strip();
        vec_line=line.split("\t");

        if flag == 0:
           fp_ses_out.write("%s\n"%(line)); 
           flag=1;
           continue;
        
        ## 转换 
        dvc = trans_dvc[vec_line[0]]; ## Huawei P1
        ses = trans_ses[vec_line[2]]; ## subway

        spk_ori = vec_line[1];
        line_tmp += 1;
        if line_tmp%2 == 1:
            num_spk += 1;
            spk_new = "SPEAKER%04d"%(num_spk);

        ### 记录所有spk的信息  一个spk 对应两个session !!!  
        ### 其中一个为 office  只需要记录另一个即可 
        if ses != "SESSION04":

            map_spk_final[spk_new]={};
            map_spk_final[spk_new]['DVCID']=dvc;
            map_spk_final[spk_new]['SESID']=ses;

            trans_spk[spk_ori] = spk_new;
            trans_spk[spk_new] = spk_ori;
            print("%s\t%s  --->  %s"%(vec_line[0], spk_ori, spk_new));

        fp_ses_out.write("%s\t%s\t%s"%(dvc, spk_new, ses));
        for value in vec_line[3:]:
            fp_ses_out.write("\t%s"%(value));
        fp_ses_out.write("\n");
        

    fp_ses.close();
    fp_ses_out.close();

    
    ## 2.  SPEAKER.txt:
    ## 原始:
    ## SPKID	SEX	AGE	ACC
    ## 0139	M	40	China, Northern,
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



    ## 3. SAMPSTAT.txt:
    ## 原始:
    ## SPKID	SESID	UTTID	SAMPRATE	BITS	DUR	SNR
    ## 0340	street	0 0340 1 193	16000	16	7.200	24.014
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

        ### 特殊处理 
        wav_new=trans_wav(vec_line[2]);
        fp_smp_out.write("\t%s"%(wav_new));

        for value in vec_line[3:]:
            fp_smp_out.write("\t%s"%(value));
        fp_smp_out.write("\n");
        

    fp_smp.close();
    fp_smp_out.close();


    ### 4. 使用 sample文件中的 dur信息 重写SESSION文件
    ### 同一个spk 两个session 分别统计！@！！！

    ##SPKID	        SESID	    UTTID	SAMPRATE	BITS	DUR	SNR
    ##SPEAKER0570	SESSION09	09_0570_09_0193	16000	16	7.200	24.014
    ##SPEAKER0570	SESSION09	09_0570_09_0192	16000	16	5.760	24.600

    fp_smp=open("%s/SAMPSTAT.txt"%(king_out_table));
    fp_ses=open("%s/SESSION.txt"%(king_out_table));


    ### todo 记录每个spk对应的: UTN TOTDUR  MINDUR  MAXDUR 
    map_spk_smp={}; ### map[spk][ses]['TOTDUR'] = 150; 
    flag=0;
    for line in fp_smp:

        line=line.strip();
        vec_line=line.split("\t");
        if flag == 0:
           flag=1;
           continue;
        
        spk=vec_line[0];
        ses=vec_line[1];
        dur=float(vec_line[5]);

        if map_spk_smp.has_key(spk):
            if map_spk_smp[spk].has_key(ses):
                map_spk_smp[spk][ses]['UTN'] += 1;
                map_spk_smp[spk][ses]['TOTDUR'] += dur;
                if map_spk_smp[spk][ses]['MINDUR'] > dur:
                    map_spk_smp[spk][ses]['MINDUR'] = dur;
                if map_spk_smp[spk][ses]['MAXDUR'] < dur:
                    map_spk_smp[spk][ses]['MAXDUR'] = dur;
            else:
                map_spk_smp[spk][ses] = {};
                map_spk_smp[spk][ses]['UTN'] = 1;
                map_spk_smp[spk][ses]['TOTDUR'] = dur;
                map_spk_smp[spk][ses]['MINDUR'] = dur;
                map_spk_smp[spk][ses]['MAXDUR'] = dur;
        else:
            map_spk_smp[spk] = {};
            map_spk_smp[spk][ses] = {};
            map_spk_smp[spk][ses]['UTN'] = 1;
            map_spk_smp[spk][ses]['TOTDUR'] = dur;
            map_spk_smp[spk][ses]['MINDUR'] = dur;
            map_spk_smp[spk][ses]['MAXDUR'] = dur;


    ## 读 SESSION.txt 中每行 
    ## DVCID	SPKID	SESID	NSC	UTN	TOTDUR	MINDUR	MAXDUR	AVEDUR
    ## DEVICE10	SPEAKER0501	SESSION04	quiet	150
    ## DEVICE10	SPEAKER0501	SESSION08	noisy	151
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
        ses = vec_line[2];
        utn=vec_line[4];
        utn_2=map_spk_smp[spk][ses]['UTN'];
        totdur=map_spk_smp[spk][ses]['TOTDUR'];
        mindur=map_spk_smp[spk][ses]['MINDUR'];
        maxdur=map_spk_smp[spk][ses]['MAXDUR'];

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
    shutil.move("%s/SESSION_out.txt"%(king_out_table) ,"%s/SESSION.txt"%(king_out_table));




## 生成 wav 的最终格式  所有wav和目录重命名 
## 原始: King-ASR-052_out/DATA/CHANNEL0/WAVE/SPEAKER0002/SESSION1/000021150.WAV
## 新的: King-ASR-052_out/DATA/DEVICE04/WAVE/SPEAKER0301/SESSION04/02_0001_02_0188.wav
## 每个SPEAKER目录下有2个SESSION目录  0和1 
def rename_data():

    ## 不同的 speaker 进入到不同的 session 中 
    path_WAVE="%s/CHANNEL0/WAVE"%(king_out_data)
    list_spk=os.listdir(path_WAVE);
    for spk_ori in list_spk:

        spk_new = trans_spk[spk_ori[-4:]]
        dvc_new = map_spk_final[spk_new]['DVCID']

        ### map_spk_final 只记录的特殊的那个SESSION 
        ses_off = 'SESSION04'  ## 对应原始的SESSION0
        ses_new = map_spk_final[spk_new]['SESID']

        path_spk_new="%s/%s/WAVE/%s"%(king_out_data, dvc_new, spk_new)
        path_spk_ori="%s/%s"%(path_WAVE, spk_ori)


        ### 1. 普通SESSION0 
        path_ses_ori="%s/SESSION0"%(path_spk_ori)
        path_ses_new="%s/%s"%(path_spk_new, ses_off)

        os.makedirs(path_ses_new);

        list_wav = os.listdir(path_ses_ori);
        for wav_ori in list_wav: 
            ## 230100188.WAV
            path_wav_ori = "%s/%s"%(path_ses_ori, wav_ori);
            wav_new = "%s.WAV"%(trans_wav(wav_ori[0:9]))
            path_wav_new = "%s/%s"%(path_ses_new, wav_new);
            shutil.move(path_wav_ori, path_wav_new);

        ### 2. 特殊SESSION1 
        path_ses_ori="%s/SESSION1"%(path_spk_ori)
        path_ses_new="%s/%s"%(path_spk_new, ses_new)

        os.makedirs(path_ses_new);

        list_wav = os.listdir(path_ses_ori);
        for wav_ori in list_wav: 
            ## 230100188.WAV
            path_wav_ori = "%s/%s"%(path_ses_ori, wav_ori);
            wav_new = "%s.WAV"%(trans_wav(wav_ori[0:9]))
            path_wav_new = "%s/%s"%(path_ses_new, wav_new);
            shutil.move(path_wav_ori, path_wav_new);



## 处理所有 wav 对应的script  
## King-ASR-052_out/DATA/CHANNEL0/SCRIPT/000300.TXT
def rename_script():

    dvc_ori='CHANNEL0'

    ## King-ASR-052_out/DATA/CHANNEL0/SCRIPT
    path_scp_ori = "%s/%s/SCRIPT"%(king_out_data, dvc_ori);
    list_scp=os.listdir(path_scp_ori);
    for scp_ori in list_scp:

        spk_ori=scp_ori[1:5]
        spk_new = trans_spk[spk_ori]
        dvc_new = map_spk_final[spk_new]['DVCID']
        scp_new = "%s.TXT"%(trans_scp(scp_ori[0:6]));

        path_scp_new = "%s/%s/SCRIPT"%(king_out_data, dvc_new);
        if not os.path.isdir(path_scp_new):
            os.makedirs(path_scp_new);

        file_tmp_in="%s/%s"%(path_scp_ori, scp_ori);
        os.system('dos2unix %s '%(file_tmp_in));

        fp_in=open("%s/%s"%(path_scp_ori, scp_ori))
        fp_out=open("%s/%s"%(path_scp_new, scp_new), "w")

        ##100500001	拨打张瑜的133的电话
        ##	拨打张瑜的幺三三的电话
        num_line=0;
        flag=0;
        content_old = ""
        for line in fp_in:

            num_line += 1;

            line=line.strip();
            if line == "":
                flag = 1;
            else:
                flag = 0;

            vec_line = line.split("\t");

            if num_line%2 == 1:
                fp_out.write("%s\t"%( trans_wav(vec_line[0]).strip().strip() ));
                content_old = vec_line[1];
            else:
                if flag == 1:
                    fp_out.write("%s\n"%( content_old.strip().strip() ));
                else:
                    fp_out.write("%s\n"%( vec_line[0].strip().strip() ));

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
    ## 0001	M	41	China, Northern,
    map_spk={}
    load_table_1("%s/SPEAKER.TXT"%(king_table), map_spk, 1);
    ##out_table_1(map_spk);
    count_rate_1(map_spk, 'SEX')
    count_rate_1(map_spk, 'AGE')
    count_rate_1(map_spk, 'ACC')



    ## SES	SCD	CHN	DVC	REP	ENV	NSC	UTN
    ## 0	0001	0	Huawei P1	China	office	quiet	150

    ## 1	0001	0	Huawei P1	China	family	noisy	151
    ## 0	0001	0	Huawei P1	China	office	quiet	150
    ## 同一个人  ENV+NSC 不同而已 也是 session 不同 

    ### map_ses['0001']['0'][DVC]='Huawei P1'
    ### map_ses['0001']['1'][DVC]='xxxx'
    map_ses={}
    load_table_2("%s/SESSION.TXT"%(king_table), map_ses, 2, 1);
    #out_table_2(map_ses);
    count_rate_2(map_ses, 'DVC');   ## Huwei D1Q  D2  P1
    count_rate_2(map_ses, 'ENV');   ### campus  car street
    count_rate_2(map_ses, 'NSC');  ### noisy quiet  每人的2个session 分别安静和噪音 


    ### map_smp[UTTID][SPKRID] = '0001'
    ## SPKRID	SESID	UTTID	SAMPRATE	BITS	DUR	SNR	CLP	MAXAMP	MEANAMP
    ## 0001	0	000010000	16000	16	3.040	31.224	0.000	-10.7378196135792	-11
    map_smp={}
    load_table_1("%s/SAMPSTAT.TXT"%(king_table), map_smp, 3);
    #out_table_1(map_smp);
    count_rate_1(map_smp, 'SPKRID')
    count_rate_1(map_smp, 'SESID')



    ####  2. 根据各种信息均衡 挑选出 200 个spk 
    vec_res_spk = select_spk_chn(map_spk, map_ses);

    #####  200个spk的 分类的比例  
    print("\n所有说话人的比例信息");
    count_rate_3( get_row_1(map_spk, vec_res_spk, 'SEX') );
    count_rate_3( get_row_1(map_spk, vec_res_spk, 'AGE') );
    count_rate_3( get_row_1(map_spk, vec_res_spk, 'ACC') );

    ### session=0 全是 office quite 
    ### session=1 种类: campus	car	family	restaurant	street	subway  全是noisy
    count_rate_3( get_row_2(map_ses, vec_res_spk, '0', 'DVC') );
    count_rate_3( get_row_2(map_ses, vec_res_spk, '1', 'DVC') );
    count_rate_3( get_row_2(map_ses, vec_res_spk, '0', 'ENV') );
    count_rate_3( get_row_2(map_ses, vec_res_spk, '1', 'ENV') );
    count_rate_3( get_row_2(map_ses, vec_res_spk, '0', 'NSC') );
    count_rate_3( get_row_2(map_ses, vec_res_spk, '1', 'NSC') );

    ####  3. 拷贝原始的 wav script table等数据 
    format_table_1(vec_res_spk);

    ####  3. 格式固定的table中   修改具体信息项
    format_table_2();


    ##### 重新命名所有wav和相关目录 
    if flag_wav_2 == 1:
        rename_data();

    #### 创建script目录 和 重新命名所有script  
    rename_script();


    ##print("\n\n最终数据库的统计信息:");
    ##### 对于最终生成的库   统计 DEVICE  SESSION AGE SEX ACC 等比例 
    ##### SPKID	SEX	AGE	ACC
    vec_tmp=('SEX','AGE','ACC');
    statistic_table("%s/SPEAKER.txt"%(king_out_table), 1, vec_tmp);

    vec_tmp=('SESID','DVCID');
    statistic_table("%s/SESSION.txt"%(king_out_table), 2, vec_tmp);



    sys.exit(0);









