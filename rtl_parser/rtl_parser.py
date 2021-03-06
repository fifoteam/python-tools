#coding=utf-8

##-------------------------------------------------------------------------------------------------
##  -- Corporation  :
##  -- Email        : haitaox2013@gmail.com
##  -- Module       : rtl_parser
##-------------------------------------------------------------------------------------------------
##  -- Description  :
##
##-------------------------------------------------------------------------------------------------
##  -- Changelog    :
##  -- Author       | Version	| Date                  | Content
##  -- Michael      | V1.4		| 2019/2/18 17:52:52	| driver section,will output the previous line
##  													| reference section,will output the next line
##  -- Michael      | V1.5		| 2019/3/6 13:12:49		| dirver and reference indent
##-------------------------------------------------------------------------------------------------

import os
import sys
import ctypes
from sub_func import *

def rtl_parser() :
	##	===============================================================================================
	##	ref ***commond line parameter***
	##	===============================================================================================
	##	-------------------------------------------------------------------------------------
	##	版本信息，在后面会打印
	##	-------------------------------------------------------------------------------------
	version_message	= "https://github.com/fifoteam/python-tools/rtl_parser v1.5 2019/3/6 13:11:22";
	code_path		= sys.path[0]+'\\rtl_parser.py';
	##	-------------------------------------------------------------------------------------
	##	debug			调试开关，默认关闭
	##	src_path		文件路径
	##	word_sel		选择的单词
	##	-------------------------------------------------------------------------------------
	debug			= 0;
	reverse_message	= 0;
	src_path		= 0;
	word_sel		= 0;

	##	-------------------------------------------------------------------------------------
	##	循环查找参数
	##	-------------------------------------------------------------------------------------
	for i in range(0,len(sys.argv)):
		if(sys.argv[i]=="-d"):
			debug		= 1;
		if(sys.argv[i]=="-f"):
			src_path	= sys.argv[i+1];
		if(sys.argv[i]=="-s"):
			word_sel	= sys.argv[i+1];
		if(sys.argv[i]=="-r"):
			reverse_message	= 1;

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

	##	===============================================================================================
	##	ref ***read source file,search keyword***
	##	===============================================================================================
	##	-------------------------------------------------------------------------------------
	##	获得被选择的数据
	##	-------------------------------------------------------------------------------------
	line_content	= 0;
	all_list		= [];
	declare_list	= [];
	driver_list		= [];
	reference_list	= [];
	map_list		= [];
	index_value		= 0;

	##	-------------------------------------------------------------------------------------
	##	从头开始读，把所有相关的内容 全部剪辑出来
	##	-------------------------------------------------------------------------------------
	for i in range(0,line_num):
		line_content	= file_content[i];
		##	-------------------------------------------------------------------------------------
		##	去掉注释 回车 字符串两边的空格 tab转换为空格
		##	-------------------------------------------------------------------------------------
		line_content	= trim_eol(line_content);
		line_content	= trim_comment(line_content);
		##	-------------------------------------------------------------------------------------
		##	1.把tab转换为空格
		##	2.去掉头尾空格
		##	-------------------------------------------------------------------------------------
		line_content	= line_content.replace("\t"," ");
		line_content	= line_content.strip();
		##	-------------------------------------------------------------------------------------
		##	如果有，则先放到 all_list 中
		##	-------------------------------------------------------------------------------------
		if(find_word(line_content,word_sel)):
			all_list.append([line_content,i+1]);

	##	-------------------------------------------------------------------------------------
	##	分析所有行的内容，归类
	##	-------------------------------------------------------------------------------------
	for i in range(0,len(all_list)):
		line_content	= all_list[i][0];
		##	-------------------------------------------------------------------------------------
		##	如果赋值语句中被赋值的信号是所选单词，则添加到赋值列表
		##	-------------------------------------------------------------------------------------
		if(find_declare(line_content)==word_sel):
			declare_list.append(all_list[i]);
		elif(find_driver(line_content)==word_sel):
			driver_list.append(all_list[i]);
		else:
			line_content	= find_map(line_content);
			if(find_word(line_content,word_sel)):
				map_list.append(all_list[i]);
			else:
				reference_list.append(all_list[i]);

	##	===============================================================================================
	##	ref ***output message***
	##	===============================================================================================
	##	-------------------------------------------------------------------------------------
	##	头
	##	-------------------------------------------------------------------------------------
##	print(version_message);
	print(code_path);
	src_file_message	= "src file is : "+src_path+"";
	word_sel_message	= "selected word is \""+word_sel+"\"";
	find_num_message	= "find num : "+str(len(all_list))+"";
	print(""+src_file_message+"***"+word_sel_message+"***"+find_num_message+"");
	##	-------------------------------------------------------------------------------------
	##	引用部分
	##	-------------------------------------------------------------------------------------
	print("***declaration***");
	for i in range(0,len(declare_list)):
		if(reverse_message==0):
			print(""+src_path+"("+str(declare_list[i][1])+"):"+declare_list[i][0]+"");
		else:
			print(""+declare_list[i][0]+":"+src_path+"("+str(declare_list[i][1])+")");

	##	-------------------------------------------------------------------------------------
	##	驱动部分
	##	-------------------------------------------------------------------------------------
	print("***driver***");
	for i in range(0,len(driver_list)):
		if(reverse_message==0):
			##	-------------------------------------------------------------------------------------
			##	如果被赋值的行不是第一行，那么也要输出被赋值语句的前一行，因为前一行一般都是条件语句
			##	如果赋值语句是 assign 直接赋值，那么就没有必要将上一行的语句输出
			##	-------------------------------------------------------------------------------------
			if (driver_list[i][1]>=2 and driver_list[i][0].split()[0]!="assign"):
				line_content	= file_content[driver_list[i][1]-2];
				##	-------------------------------------------------------------------------------------
				##	去掉注释 回车 字符串两边的空格 tab转换为空格
				##	-------------------------------------------------------------------------------------
				line_content	= trim_eol(line_content);
				line_content	= trim_comment(line_content);
				##	-------------------------------------------------------------------------------------
				##	1.把tab转换为空格
				##	2.去掉头尾空格
				##	-------------------------------------------------------------------------------------
				line_content	= line_content.replace("\t"," ");
				line_content	= line_content.strip();
				print(""+src_path+"("+str(driver_list[i][1]-1)+"):"+line_content+"");
				print(""+src_path+"("+str(driver_list[i][1])+"):\t\t"+driver_list[i][0]+"");
			##	-------------------------------------------------------------------------------------
			##	当是直接赋值的时候，不用 tab
			##	-------------------------------------------------------------------------------------
			else:
				print(""+src_path+"("+str(driver_list[i][1])+"):"+driver_list[i][0]+"");
		else:
			print(""+driver_list[i][0]+":"+src_path+"("+str(driver_list[i][1])+")");

	##	-------------------------------------------------------------------------------------
	##	引用部分
	##	-------------------------------------------------------------------------------------
	print("***reference***");
	for i in range(0,len(reference_list)):
		if(reverse_message==0):
			print(""+src_path+"("+str(reference_list[i][1])+"):"+reference_list[i][0]+"");
			##	-------------------------------------------------------------------------------------
			##	如果被引用的行不是第最后一行，那么也要输出被赋值语句的前一行，因为前一行一般都是条件语句
			##	如果引用语句是 assign 直接赋值，那么就没有必要将下一行的语句输出
			##	-------------------------------------------------------------------------------------
			if (reference_list[i][1]<=line_num-2 and reference_list[i][0].split()[0]!="assign"):
				line_content	= file_content[reference_list[i][1]];
				##	-------------------------------------------------------------------------------------
				##	去掉注释 回车 字符串两边的空格 tab转换为空格
				##	-------------------------------------------------------------------------------------
				line_content	= trim_eol(line_content);
				line_content	= trim_comment(line_content);
				##	-------------------------------------------------------------------------------------
				##	1.把tab转换为空格
				##	2.去掉头尾空格
				##	-------------------------------------------------------------------------------------
				line_content	= line_content.replace("\t"," ");
				line_content	= line_content.strip();
				print(""+src_path+"("+str(reference_list[i][1]+1)+"):\t\t"+line_content+"");
		else:
			print(""+reference_list[i][0]+":"+src_path+"("+str(reference_list[i][1])+")");

	##	-------------------------------------------------------------------------------------
	##	映射部分
	##	-------------------------------------------------------------------------------------
	print("***map***");
	for i in range(0,len(map_list)):
		if(reverse_message==0):
			print(""+src_path+"("+str(map_list[i][1])+"):"+map_list[i][0]+"");
		else:
			print(""+map_list[i][0]+":"+src_path+"("+str(map_list[i][1])+")");

	infile.close()

rtl_parser()