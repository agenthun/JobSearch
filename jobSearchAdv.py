# encoding: utf-8
import sys
sys.path.append('../')

import re
import json
import codecs
import urllib2

import jieba
import jieba.analyse
from optparse import OptionParser

USAGE="usage: python jobSearchAdv.py [file name.json]"

parser=OptionParser(USAGE)
opt, args=parser.parse_args()

if len(args)<1:
	print USAGE
	sys.exit(1)

file_name=args[0]
data=[]

#read info.json to get the big data
def readJSON(fname):
	with open(fname) as f:
		for line in f:
			data.append(json.loads(line))
	data.sort(reverse=True)

#to find the keywords
def findKeywords(data):
	jieba.analyse.set_stop_words("./dict/stop_words.txt")
	# jieba.analyse.set_idf_path("./dict/mydict.txt.big")
	jieba.load_userdict("./dict/mydict.txt.big")
	# jieba.analyse.set_idf_path("myidf.txt.big")

	# file_object=codecs.open('./dict/mydict.txt.big', 'w+', encoding='utf-8')
	for i in range(len(data)):
		try:
			detailURL=urllib2.urlopen(data[i]['detailLink']).read().decode('gbk')
			detail=re.findall(u"标  题: (.*?)--", detailURL, re.S)
			tags=jieba.analyse.extract_tags(detail[0], topK=10, withWeight=True)
			# tags=jieba.analyse.textrank(detail[0], topK=10, withWeight=True)
			for tag, weight in tags:
				# data[i]['keywords']+="%s: %s, " %(tag, weight)
				data[i]['keywords']+="%s, " %(tag)
				# stemp="%s %s\r\n" %(tag, weight*100)
				# file_object.write(stemp)
		except:
			data[i]['keywords']="?"
			continue
	# file_object.close()
		# finally:
		# 	print data[i]['keywords']

readJSON(file_name)
findKeywords(data)
subdata="\r\n"
for item in data:
	subdata+="insert into jobinfo (catalog, publishTime, name, detailLink, keywords) values"
	subdata+="('%s','%s','%s','%s','%s');\r\n" %(item['catalog'], item['publishTime'], item['name'], item['detailLink'], item['keywords'])

file_object=codecs.open('detail.sql', 'w', encoding='utf-8')
file_object.write(subdata)
file_object.close()

print "success"

def addKeywords():
	file_object=codecs.open('mydict.txt.big', 'w', encoding='utf-8')
	for i in range(len(data)):
		data[i]=data[i]+" 50.00000000000\r\n"
		file_object.write(data[i])
	file_object.close()
