#!/bin/sh


### 得到样例格式的数据库 
### 但是命名规范未统一
### 
rm -rf King-ASR-358_out2/TABLE/*
python2.7 read_table.py  > King-ASR-358.log 

### 统一命名规则 



