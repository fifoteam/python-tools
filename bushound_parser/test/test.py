#coding=utf-8
#! usr/bin/python

import sys
print ("name is ",sys.argv[0]);
for i in range(1, len(sys.argv)):
	print("arg is", i, sys.argv[i]);
