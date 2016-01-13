# -*- coding: utf-8 -*-
import codecs
import sys
sys.path.append('../')
from optparse import OptionParser

USAGE = "usage:    python edit_dict.py [file name]"
#get the name of file
parser = OptionParser(USAGE)
opt, args = parser.parse_args()
if len(args) < 1:
    print USAGE
    sys.exit(1)
file_name = args[0]
#open the file
data=[]
f=codecs.open(file_name, 'r', encoding='gbk')
for line in f:
	data.append(line.strip('\n'))
f.close()
#edit the parameter
file_object=codecs.open('mydict.txt.big', 'w', encoding='utf-8')
for i in range(len(data)):
	data[i]=data[i]+" 40.00000000000\r\n"
	file_object.write(data[i])
file_object.close()

print "success"
