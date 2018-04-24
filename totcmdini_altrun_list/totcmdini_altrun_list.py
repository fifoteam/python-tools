#coding=utf-8

import os
import sys
import ctypes
#import sub_func
from sub_func import *

def totcmdini_altrun_list() :

	##	-------------------------------------------------------------------------------------
	##	debug			调试开关，默认关闭
	##	src_path		文件路径
	##	-------------------------------------------------------------------------------------
	debug 		= 0;
	src_path	= 0;

	for i in range(0,len(sys.argv)):
		if(sys.argv[i]=="-d"):
			debug = 1;
		if(sys.argv[i]=="-f"):
			src_path	= sys.argv[i+1];

	##	===============================================================================================
	##	ref ***source file operation***
	##	===============================================================================================
	##	-------------------------------------------------------------------------------------
	##	判断输入的是否是一个文件
	##	--如果不是文件，打印错误，退出
	##	--如果是一个文件，打开文件
	##	-------------------------------------------------------------------------------------
	if(os.path.isfile(src_path)==False):	return -1
	if(debug==1):	print("src_path is really exist");
	infile	= open(src_path,"r",encoding='gb18030')

	##	-------------------------------------------------------------------------------------
	##	记录文件总行数
	##	-------------------------------------------------------------------------------------
	file_content = infile.readlines();
	line_num = len(file_content);
	if(debug==1):	print("all line num is ",line_num);

	##	===============================================================================================
	##	ref ***read source file,search keyword***
	##	===============================================================================================
	##	-------------------------------------------------------------------------------------
	##	从头开始读 找 "55 33 56 " 作为一个文件开始符
	##	-------------------------------------------------------------------------------------
	for i in range(0,line_num):
		line_content	= file_content[i];
		##	-------------------------------------------------------------------------------------
		##	如果一行的开头是 "[DirMenu]"，那么就认为下面就是数据开始
		##	-------------------------------------------------------------------------------------
		if(line_content.find("[DirMenu]")>=0):
			if(debug==1):	print("******find [DirMenu] line num is ",i);
			line_start=i;
			break
		##	-------------------------------------------------------------------------------------
		##	如果最后一行都没有找到，那么就是没有pattern，就会退出
		##	-------------------------------------------------------------------------------------
		if(i==line_num-1):
			if(debug==1):	print("******not found [DirMenu]");
			return -1

	##	===============================================================================================
	##	ref ***parse file by keyword***
	##	===============================================================================================

	##	-------------------------------------------------------------------------------------
	##	从line start开始，找 cmd 的关键字
	##	-------------------------------------------------------------------------------------
	list_parser = [];
	line_space_split = [];
	for i in range(line_start+1,line_num):
#		if(debug==1):	print("******in proc");
		line_content	= file_content[i];
		if(line_content[0:3]=="cmd"):
#			if(debug==1):	print("find cmd");
			line_content	= line_content[line_content.index("=")+1:len(line_content)];
			line_content	= line_content.strip();
			line_content	= line_content.replace("\t"," ");
			line_space_split	= line_content.split(' ');

			if(len(line_space_split)>=2 and line_space_split[0].lower()=="cd"):
#				if(debug==1):	print("******in proc");
				list_parser.append(line_space_split[1]);
		elif(line_content[0]=="["):
			break;

	##+test+
	if(debug==1):
		for i in range(0,len(list_parser)):
			print("list_parser"+str(i)+" is "+str(list_parser[i])+"");
	##-test-

	list_parser_back	= [];
	for i in range(0,len(list_parser)):
		list_parser_back.append("F0    |    |"+list_parser[i]+"    |"+list_parser[i]+"    |"+list_parser[i]+"\n")




	##	===============================================================================================
	##	ref ***output result***
	##	===============================================================================================
	##	-------------------------------------------------------------------------------------
	##	从源文件的路径得到目的文件路径
	##	--解析后的文件名字是源文件名字+"_parser.txt"
	##	-------------------------------------------------------------------------------------
	temp = os.path.split(src_path);
	only_path = temp[0];
	temp = os.path.basename(src_path);
	temp = temp.split('.');
	only_name = temp[0];
	parser_name = only_name + "_altrunlist.txt";
	parser_path = only_path+'\\'+parser_name;

	##	-------------------------------------------------------------------------------------
	##	建立新的文件
	##	-------------------------------------------------------------------------------------
	parser_file = open(parser_path,"w+");
	parser_file.writelines(list_parser_back);
	parser_file.close()



#	path = "f:/test/UE_TMP.v"
#	infile = open(path,"r")
#	outfile = open("f:/test/UE_TMP1.v","w")
#	outfile.write("hello")
#
#
#	temp = os.path.split(src_path);
#	print('temp[1] is :',temp[1]);
#	print(os.path.basename(src_path));
#	u = os.path.basename(src_path);
#	v = u.split('.');
#	#	print(u.split(.));
#	print(v[0]);
#	#	print(os.path.split(path));
#
#	outfile.close()
#	infile.close()
##
###!/usr/bin/python
### -*- coding: UTF-8 -*-
##
##for letter in 'Python':     # 第一个实例
##   print '当前字母 :', letter
##
##fruits = ['banana', 'apple',  'mango']
##for fruit in fruits:        # 第二个实例
##   print '当前字母 :', fruit
##
##print "Good bye!"

totcmdini_altrun_list()


