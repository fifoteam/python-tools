#coding=utf-8

import os
import sys
import ctypes
from sub_func import *

def rtl_parser() :

	##	-------------------------------------------------------------------------------------
	##	调试开关
	##	-------------------------------------------------------------------------------------
	debug = 0;
#	debug = 1;
#	print("debug is ",debug);

	##	===============================================================================================
	##	ref ***source file operation***
	##	===============================================================================================
	##	-------------------------------------------------------------------------------------
	##	判断传入参数的个数
	##	-------------------------------------------------------------------------------------
	if(len(sys.argv)==1):	print("please input filepath & word");
	if(len(sys.argv)==2):	print("please input word");

	##	-------------------------------------------------------------------------------------
	##	获取输入文件
	##	-------------------------------------------------------------------------------------
	src_path = sys.argv[1];
	if(debug==1):	print("src_path is",src_path);

	##	-------------------------------------------------------------------------------------
	##	判断输入的是否是一个文件
	##	--如果不是文件，打印错误，退出
	##	--如果是一个文件，打开文件
	##	-------------------------------------------------------------------------------------
	if(os.path.isfile(src_path)==False):	return -1
	if(debug==1):	print("src_path is really exist");
	infile	= open(src_path,"r")

	##	-------------------------------------------------------------------------------------
	##	记录文件总行数
	##	-------------------------------------------------------------------------------------
	file_content = infile.readlines();
	line_num = len(file_content);
#	if(debug==1):	print("all line num is ",line_num);

	##	===============================================================================================
	##	ref ***read source file,search keyword***
	##	===============================================================================================
	##	-------------------------------------------------------------------------------------
	##	获得被选择的数据
	##	-------------------------------------------------------------------------------------
	word_sel 		= sys.argv[2];
	line_content	= 0;
	all_list		= [];
	declare_list	= [];
	driver_list		= [];
	reference_list	= [];
	index_value		= 0;

	##	-------------------------------------------------------------------------------------
	##	从头开始读，把所有相关的内容 全部剪辑出来
	##	-------------------------------------------------------------------------------------
	for i in range(0,line_num):
		line_content	= file_content[i];
		##	-------------------------------------------------------------------------------------
		##	去掉注释 回车 字符串两边的空格 tab转换为空格
		##	-------------------------------------------------------------------------------------
		try:
		    index_value = line_content.index("\n")
		except ValueError:
		    index_value = -1
		if(index_value!=-1): line_content	= line_content[0:index_value];

		try:
		    index_value = line_content.index("//")
		except ValueError:
		    index_value = -1
		if(index_value!=-1): line_content	= line_content[0:index_value];

		line_content	= line_content.replace("\t"," ");
		line_content	= line_content.strip();
		##	-------------------------------------------------------------------------------------
		##	如果有，则先放到 reference_list里面
		##	-------------------------------------------------------------------------------------
#		if(line_content.find(word_sel)>=0):
		if(find_word(line_content,word_sel)):
			all_list.append([line_content,i+1]);
#			print("line_content is",line_content);
#			print("i is",i);

	##	-------------------------------------------------------------------------------------
	##
	##	-------------------------------------------------------------------------------------
	for i in range(0,len(all_list)):
		line_content	= all_list[i][0];
		##	-------------------------------------------------------------------------------------
		##	把赋值符号之前的内容截取出来
		##	-------------------------------------------------------------------------------------
		try:
		    index_value = line_content.index("=")
		except ValueError:
		    index_value = -1
		if(index_value!=-1): line_content	= line_content[0:index_value];

#		##	-------------------------------------------------------------------------------------
#		##	如果是模块映射，则需要把括号中的内容截取出来
#		##	-------------------------------------------------------------------------------------
#		try:
#		    index_value = line_content.index(".")
#		except ValueError:
#		    index_value = -1
#		if(index_value!=-1):
#			try:
#			    index_value = line_content.index("(")
#			except ValueError:
#			    index_value = -1
#			if(index_value!=-1):	line_content	= line_content[index_value+1:len(line_content)];
		##	-------------------------------------------------------------------------------------
		##	如果 = 前面有所选词，那么说明可能是声明或者赋值
		##	-------------------------------------------------------------------------------------
##		if(line_content.find(word_sel)>=0):
		if(find_word(line_content,word_sel)):
			##	-------------------------------------------------------------------------------------
			##	判断是不是赋值语句
			##	-------------------------------------------------------------------------------------
			if(line_content.split(' ')[0]=="assign"):
				driver_list.append(all_list[i]);
			elif(line_content.split(' ')[0][0:len(word_sel)]==word_sel):
				driver_list.append(all_list[i]);

			else:

				##	-------------------------------------------------------------------------------------
				##	把[]之前的内容截取出来
				##	-------------------------------------------------------------------------------------
				try:
				    index_value = line_content.index("[")
				except ValueError:
				    index_value = -1
				if(index_value!=-1): line_content	= line_content[0:index_value];

				##	-------------------------------------------------------------------------------------
				##	判断是不是声明语句
				##	-------------------------------------------------------------------------------------
				if(line_content.split(' ')[0]=="parameter"):
					declare_list.append(all_list[i]);
				elif(line_content.split(' ')[0]=="localparam"):
					declare_list.append(all_list[i]);
				elif(line_content.split(' ')[0]=="function"):
					declare_list.append(all_list[i]);
				elif(line_content.split(' ')[0]=="task"):
					declare_list.append(all_list[i]);
				elif(line_content.split(' ')[0]=="input"):
					declare_list.append(all_list[i]);
				elif(line_content.split(' ')[0]=="output"):
					declare_list.append(all_list[i]);
				elif(line_content.split(' ')[0]=="inout"):
					declare_list.append(all_list[i]);
				elif(line_content.split(' ')[0]=="wire"):
					declare_list.append(all_list[i]);
				elif(line_content.split(' ')[0]=="reg"):
					declare_list.append(all_list[i]);
				else:
					reference_list.append(all_list[i]);
		else:
			reference_list.append(all_list[i]);
	##	-------------------------------------------------------------------------------------
	##	输出
	##	-------------------------------------------------------------------------------------
	##	-------------------------------------------------------------------------------------
	##	头
	##	-------------------------------------------------------------------------------------
	print("https://github.com/fifoteam/python-tools/tree/master/rtl_parser v1.2 2016.10.31");
	print("src file is : ",src_path);
	print("selected word is \""+word_sel+"\"");
	print("find num :",len(all_list));
	##	-------------------------------------------------------------------------------------
	##	引用部分
	##	-------------------------------------------------------------------------------------
	print("***declaration***");
	for i in range(0,len(declare_list)):
		print(""+src_path+"("+str(declare_list[i][1])+"):"+declare_list[i][0]+"");

	##	-------------------------------------------------------------------------------------
	##	驱动部分
	##	-------------------------------------------------------------------------------------
	print("***driver***");
	for i in range(0,len(driver_list)):
		print(""+src_path+"("+str(driver_list[i][1])+"):"+driver_list[i][0]+"");

	##	-------------------------------------------------------------------------------------
	##	引用部分
	##	-------------------------------------------------------------------------------------
	print("***reference***");
	for i in range(0,len(reference_list)):
		print(""+src_path+"("+str(reference_list[i][1])+"):"+reference_list[i][0]+"");

	infile.close()



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

rtl_parser()


