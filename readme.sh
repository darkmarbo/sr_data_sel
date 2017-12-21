


=====================================================================
read_table.py:

    log: file = King-ASR-358/TABLE/SPEAKER.TXT
    SCD     SEX     AGE     ACC
    0000    F       45      China, Jilin
    0010    M       33      China, Shandong

    map[0000] = {};
        map[0000][SEX] = F
        map[0000][AGE] = 45
        map[0000][ACC] = China_Jilin

=====================================================================
358:

方言区：China, Shandong  不符合规则
TABLE 中的txt文件 处理成utf8格式 

log: file = King-ASR-358/TABLE/CONTENT.TXT
SCD     SES     UID     TRS
0000    0       000000001       打开短程极速赛车二
0000    0       000000002       来一首背水姑娘

log: file = King-ASR-358/TABLE/SAMPSTAT.TXT
SPKRID  SESID   UTTID   SAMPRATE        BITS    DUR     SNR     CLP     MAXAMP  MEANAMP
0000    0       000000001       16000   16      3.475   22.165  0.000   -11.070824149477      0
0000    0       000000002       16000   16      2.579   20.348  0.000   -12.6275606809552     0

log: file = King-ASR-358/TABLE/SESSION.TXT
SES     SCD     CHN     DVC             REP     ENV     NSC     UTN     CAR
0       0000    0       SHURE WH30      China   car     noisy   220     Honda Accord
0       0010    0       SHURE WH30      China   car     noisy   220     Toyota Corolla

log: file = King-ASR-358/TABLE/SPEAKER.TXT
SCD     SEX     AGE     ACC
0000    F       45      China, Jilin
0010    M       33      China, Shandong




----------------------------------------------------
选取200人  每种设备下选取 50人 
然后需要保证其他参数的均衡 

    SESSION:
        设备均衡:CHN+DVC
        环境均衡:CAR
            awk -F"\t" '{print $7"_"$9}' King-ASR-358/TABLE/SESSION.TXT |sort|uniq 
        
    SPEAKER
        性别均衡  : 2种 SEX 
            F M
        年龄均衡 : 6种  AGE
            0-10years
            10-18years
            18 – 30 years
            31 – 45 years
            45 – 60 years
            60- years

        方言区均衡:7种 ACC
            Northern
            Wu
            Hakka
            Cantonese
            Min
            Xiang
            Gan

定义数组:a
    a0=说话人ID
    a1=设备类型 4
    a2=环境类型 2 
    a3=性别 2
    a4=年龄 6
    a5=方言 7


=====================================================================

data_sample:
    数据库样例  最终需要生成的统一格式！ 

每个数据库 单独一个主shell  处理整个数据库格式

=====================================================================



修改wav名字为统一格式: aa_bbbb_cc_dddd.wav 
硬件 说话人 环境  id



