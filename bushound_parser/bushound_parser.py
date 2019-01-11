#coding=utf-8

import os
import sys
import ctypes
#import sub_func
from sub_func_vision import *

def bushound_parser() :

	##	-------------------------------------------------------------------------------------
	##	debug			调试开关，默认关闭
	##	src_path		文件路径
	##	parse_info		解析leader trailer control的信息
	##	save_image		保存图像
	##	cut_device		提取某些端口的数据
	##	-------------------------------------------------------------------------------------
	debug 		= 0;
	src_path	= 0;
	parse_info	= 0;
	save_image	= 0;
	cut_device	= 0;
	device_num	= 0;
	device_selected	= 0;



	for i in range(0,len(sys.argv)):
		if(sys.argv[i]=="-d"):
			debug = 1;
		if(sys.argv[i]=="-f"):
			src_path	= sys.argv[i+1];
		if(sys.argv[i]=="-p"):
			parse_info	= 1;
		if(sys.argv[i]=="-s"):
			save_image	= 1;
		if(sys.argv[i]=="-c"):
			cut_device	= 1;
		if(sys.argv[i]=="-n"):
			device_num	= sys.argv[i+1];

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

		if (cut_device==0):
			##	-------------------------------------------------------------------------------------
			##	如果一行的开头是 "------"，那么就认为下面就是数据开始
			##	-------------------------------------------------------------------------------------
			if(line_content.find("55 33 56 ")>=0):
				if(debug==1):	print("******find U3V pattern line num is ",i);
				line_start=i;
				break
			##	-------------------------------------------------------------------------------------
			##	如果最后一行都没有找到，那么就是没有pattern，就会退出
			##	-------------------------------------------------------------------------------------
			if(i==line_num-1):
				if(debug==1):	print("******not found U3V pattern");
				return -1
		else:
			##	-------------------------------------------------------------------------------------
			##	如果要分割数据，那么从第一行开始找
			##	-------------------------------------------------------------------------------------
			line_start=0;
			break

	##	-------------------------------------------------------------------------------------
	##	在一行中定位"55 33 56 "出现的位置
	##	-------------------------------------------------------------------------------------
	first_byte_pos = file_content[line_start].find('55 33 56 ');
	if(debug==1):	print("first byte position is ",first_byte_pos);

	##	===============================================================================================
	##	ref ***parse file by keyword***
	##	===============================================================================================
	##	-------------------------------------------------------------------------------------
	##	如果不是分割数据
	##	-------------------------------------------------------------------------------------
	if (cut_device==0):
		##	-------------------------------------------------------------------------------------
		##	从line start开始，找 U3VC U3VL U3VT 的关键字
		##	-------------------------------------------------------------------------------------
		list_parser = [];
		for i in range(line_start,line_num):
			line_content	= file_content[i];
			if(line_content[first_byte_pos:first_byte_pos+11]=="55 33 56 43"):
				if(debug==1):	print("find U3VC");
				list_parser.append(u3vc_proc(debug,first_byte_pos,i,file_content));
			elif(line_content[first_byte_pos:first_byte_pos+11]=="55 33 56 4c"):
				if(debug==1):	print("find U3VL");
				list_parser.append(u3vl_proc(debug,first_byte_pos,i,file_content));
			elif(line_content[first_byte_pos:first_byte_pos+11]=="55 33 56 54"):
				if(debug==1):	print("find U3VT");
				list_parser.append(u3vt_proc(debug,first_byte_pos,i,file_content));

			if(i==int(line_num*0.1)):	print(".",end="");
			if(i==int(line_num*0.2)):	print(".",end="");
			if(i==int(line_num*0.3)):	print(".",end="");
			if(i==int(line_num*0.4)):	print(".",end="");
			if(i==int(line_num*0.5)):	print(".",end="");
			if(i==int(line_num*0.6)):	print(".",end="");
			if(i==int(line_num*0.7)):	print(".",end="");
			if(i==int(line_num*0.8)):	print(".",end="");
			if(i==int(line_num*0.9)):	print(".",end="");
			if(i==int(line_num-1)):		print("!",end="");
	##	-------------------------------------------------------------------------------------
	##	如果是分割数据
	##	-------------------------------------------------------------------------------------
	else:
		list_parser = [];
		for i in range(line_start,line_num):
			line_content	= file_content[i];
			##	-------------------------------------------------------------------------------------
			##	如果port端口包含信息
			##	-------------------------------------------------------------------------------------
			if('.' in line_content[0:5]):
				##	-------------------------------------------------------------------------------------
				##	如果端口是所选端口，那么要声明选中，保留信息
				##	-------------------------------------------------------------------------------------
				if(device_num in line_content[0:5]):
					device_selected	= 1;
					list_parser.append(line_content);
					if(debug==1):	print("line_num is "+str(i)+",find device");
				##	-------------------------------------------------------------------------------------
				##	如果端口不是所选端口，那么要声明未选中
				##	-------------------------------------------------------------------------------------
				else:
					device_selected	= 0;
			##	-------------------------------------------------------------------------------------
			##	如果port端口不包含信息
			##	-------------------------------------------------------------------------------------
			else:
				##	-------------------------------------------------------------------------------------
				##	如果端口已经被选中，说明还是被选择的端口的数据，应该要保留下来
				##	-------------------------------------------------------------------------------------
				if (device_selected==1):
					list_parser.append(line_content);

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
	parser_name = only_name + "_parser.txt";
	summary_name = only_name + "_summary.txt";
	parser_path = only_path+'\\'+parser_name;
	summary_path = only_path+'\\'+summary_name;

	cut_name	= only_name + "_" + device_num + "cut" +".txt";
	cut_path	= only_path+'\\'+cut_name;

	if (cut_device==0):
		##	-------------------------------------------------------------------------------------
		##	重新编辑file_content 把要写入的内容添加到其中
		##	--list_parser是一个二维列表，每一个元素都是一个列表，其中0代表行号，1代表解析内容
		##	--要把list_parser列表中的内容添加到对应行中，file_content的最后一个字符是回车符要去掉
		##	-------------------------------------------------------------------------------------
		for i in range(0,len(list_parser)):
			file_content[list_parser[i][0]]	= file_content[list_parser[i][0]].rstrip("\n")+"\t#"+list_parser[i][1]+"\n";

		file_content_summay = list_parser;
		for i in range(0,len(list_parser)):
			file_content_summay[i]	= "line num is "+str(list_parser[i][0]+1)+"\t"+list_parser[i][1]+"\n";

		##	-------------------------------------------------------------------------------------
		##	建立新的文件
		##	-------------------------------------------------------------------------------------
		outfile_parser = open(parser_path,"w+");
		outfile_summary = open(summary_path,"w+");

		##	-------------------------------------------------------------------------------------
		##	建立新的文件
		##	-------------------------------------------------------------------------------------
		outfile_parser.writelines(file_content);
		outfile_summary.writelines(file_content_summay);

		##	===============================================================================================
		##	ref ***end***
		##	===============================================================================================
		outfile_parser.close()
		outfile_summary.close()
		infile.close()

	else:
		##	-------------------------------------------------------------------------------------
		##	建立新的文件
		##	-------------------------------------------------------------------------------------
		outfile_cut = open(cut_path,"w+");
		outfile_cut.writelines(list_parser);
		outfile_cut.close()



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

bushound_parser()


