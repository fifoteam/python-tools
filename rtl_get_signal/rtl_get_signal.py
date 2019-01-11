#coding=utf-8

import os
import sys
import ctypes


from sub_func import *
from tkinter import Tk

def rtl_get_signal() :
	##	===============================================================================================
	##	ref ***commond line parameter***
	##	===============================================================================================
	##	-------------------------------------------------------------------------------------
	##	版本信息，在后面会打印
	##	-------------------------------------------------------------------------------------
	version_message	= "https://github.com/fifoteam/python-tools/rtl_get_signal v1.0 2017.9.19";
	##	-------------------------------------------------------------------------------------
	##	debug			调试开关，默认关闭
	##	-------------------------------------------------------------------------------------
	debug			= 0;
	selection		= [];
	##	-------------------------------------------------------------------------------------
	##	循环查找参数
	##	-------------------------------------------------------------------------------------
	for i in range(0,len(sys.argv)):
		if(sys.argv[i]=="-d"):
			debug		= 1;

	##	-------------------------------------------------------------------------------------
	##	获取剪贴板数据
	##	-------------------------------------------------------------------------------------
	r = Tk()
	selection = r.clipboard_get()
	if(debug==1):	print("\r\n selection is "+selection+" \r\n");

	##	-------------------------------------------------------------------------------------
	##	以换行符为分割条件
	##	-------------------------------------------------------------------------------------
	line_eol_split	= [];
	if("\r\n" in selection):
		line_eol_split	= selection.split("\r\n");
		if(debug==1):	print("go into eol1");
	elif("\n" in selection):
		line_eol_split	= selection.split("\n");
		if(debug==1):	print("go into eol2");
	elif("\r" in selection):
		line_eol_split	= selection.split("\r");
		if(debug==1):	print("go into eol3");
	else:
		line_eol_split.append(selection);
		if(debug==1):	print("no eol");

	if(debug==1):	print("line_eol_split is "+str(line_eol_split)+"");
	for i in range(0,len(line_eol_split)):
		line_eol_split[i]	= trim_comment(line_eol_split[i]);
		line_eol_split[i]	= line_eol_split[i].strip();
		##	-------------------------------------------------------------------------------------
		##	如果是空字符，则切换到下一行
		##	-------------------------------------------------------------------------------------
		if(line_eol_split[i]==""):
			continue;
		else:
			##	-------------------------------------------------------------------------------------
			##	可能会有多行混在一起
			##	-------------------------------------------------------------------------------------
			line_comma_split	= line_eol_split[i].split(";")
			for j in range(0,len(line_comma_split)):
				##	-------------------------------------------------------------------------------------
				##	如果是空字符串，不需要提取信息
				##	-------------------------------------------------------------------------------------
				if(line_comma_split[j]==""): continue;
				line_comma_split[j]	= trim_keywords(line_comma_split[j]);
				if(";" in line_comma_split[j]):	line_comma_split[j]	= line_comma_split[j][0:line_comma_split[j].index(";")];
				if("," in line_comma_split[j]):	line_comma_split[j]	= line_comma_split[j][0:line_comma_split[j].index(",")];
				if("(" in line_comma_split[j]):	line_comma_split[j]	= line_comma_split[j][0:line_comma_split[j].index("(")];
				if("=" in line_comma_split[j]):	line_comma_split[j]	= line_comma_split[j][0:line_comma_split[j].index("=")];
				if("<" in line_comma_split[j]):	line_comma_split[j]	= line_comma_split[j][0:line_comma_split[j].index("<")];

				if("]" in line_comma_split[j]):	line_comma_split[j]	= line_comma_split[j][line_comma_split[j].index("]")+1:len(line_comma_split[j])];
				if(":" in line_comma_split[j]):	line_comma_split[j]	= line_comma_split[j][line_comma_split[j].index(":")+1:len(line_comma_split[j])];

				line_comma_split[j]	= line_comma_split[j].strip();
				print(""+str(line_comma_split[j])+"");


rtl_get_signal()