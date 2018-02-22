
import sys

#fp=open(sys.argv[1])
#for line in fp:
#    line = line.strip();
#    print line;


fp_in=open("King-ASR-052/DATA/CHANNEL0/SCRIPT/002001.TXT")
fp_out=open("ttt.out", "w")

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
        fp_out.write("%s\t"%( (vec_line[0]).strip() ));
        content_old = vec_line[1];
    else:
        if flag == 1:
            fp_out.write("%s\n"%( content_old.strip() ));
        else:
            fp_out.write("%s\n"%( vec_line[0].strip() ));

fp_in.close();
fp_out.close();



