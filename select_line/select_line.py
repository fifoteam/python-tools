#coding=utf-8

import os
import sys
import ctypes
##import sub_func
#from sub_func import *

def select_line() :

	##	-------------------------------------------------------------------------------------
	##	调试开关
	##	-------------------------------------------------------------------------------------
	debug		= 0;
	src_path	= 0;
	save_option	= 0;
	save_list	= [];
	del_option	= 0;
	del_list	= [];

	for i in range(0,len(sys.argv)):
		if(sys.argv[i]=="-d"):
			debug		= 1;
		if(sys.argv[i]=="-f"):
			src_path	= sys.argv[i+1];
		if(sys.argv[i]=="-s"):
			save_option	= 1;
			for j in range(1,len(sys.argv)-i):
				if(sys.argv[i+j][0]=="-"):
					break;
				else:
					save_list.append(sys.argv[i+j]);
		if(sys.argv[i]=="-e"):
			del_option	= 1;
			for j in range(1,len(sys.argv)-i):
				if(sys.argv[i+j][0]=="-"):
					break;
				else:
					del_list.append(sys.argv[i+j]);

	##	===============================================================================================
	##	ref ***源文件操作***
	##	===============================================================================================
	##	-------------------------------------------------------------------------------------
	##	获取输入文件
	##	-------------------------------------------------------------------------------------
	if(debug==1):	print("src_path is",src_path);

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
	##	ref ***找到pattern***
	##	===============================================================================================
	if(debug==1):
		print("save_list is");
		for eachline in save_list:
			print(eachline);
		print("del_list is");
		for eachline in del_list:
			print(eachline);

	##	===============================================================================================
	##	ref ***读文件 找关键字***
	##	===============================================================================================
	##	-------------------------------------------------------------------------------------
	##	如果 pattern1找到了，那么再找 pattern2 如果能找到，说明没有问题
	##	-------------------------------------------------------------------------------------
	list_parser = [];
	for i in range(0,line_num):
		line_content	= file_content[i];
		if(save_option==1):
			for j in range(0,len(save_list)):
				pattern	= save_list[j];
				if(line_content.find(pattern)>=0):
					if(debug==1):	print("******find save pattern line num is ",i);
					list_parser.append(line_content);
					break;
		else:
			list_parser.append(line_content);

	list_length	= len(list_parser);
	for i in range(0,list_length):
		line_content	= list_parser[list_length-i-1];
		if(del_option==1):
			for j in range(0,len(del_list)):
				pattern	= del_list[j];
				if(line_content.find(pattern)>=0):
					if(debug==1):	print("******find del pattern line num is ",i);
					del list_parser[list_length-i-1];
					break;

	##	===============================================================================================
	##	ref ***输出文件***
	##	===============================================================================================
	##	-------------------------------------------------------------------------------------
	##	从源文件的路径得到目的文件路径
	##	--解析后的文件名字是"select_line.txt"
	##	-------------------------------------------------------------------------------------
	temp = os.path.split(src_path);
	only_path = temp[0];
	temp = os.path.basename(src_path);
	temp = temp.split('.');
	only_name = temp[0];
	path = only_path+'\\'+only_name+"_select_line.txt";


	##	-------------------------------------------------------------------------------------
	##	建立新的文件
	##	-------------------------------------------------------------------------------------
	outfile_summary = open(path,"w+");

	##	-------------------------------------------------------------------------------------
	##	建立新的文件
	##	-------------------------------------------------------------------------------------
	for eachline in list_parser:
		outfile_summary.write(str(eachline));

	##	===============================================================================================
	##	ref ***结束***
	##	===============================================================================================
	outfile_summary.close()
	infile.close()

select_line()


