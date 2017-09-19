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
	##	�汾��Ϣ���ں�����ӡ
	##	-------------------------------------------------------------------------------------
	version_message	= "https://github.com/fifoteam/python-tools/rtl_get_signal v1.0 2017.9.19";
	##	-------------------------------------------------------------------------------------
	##	debug			���Կ��أ�Ĭ�Ϲر�
	##	-------------------------------------------------------------------------------------
	debug			= 0;

	##	-------------------------------------------------------------------------------------
	##	ѭ�����Ҳ���
	##	-------------------------------------------------------------------------------------
	for i in range(0,len(sys.argv)):
		if(sys.argv[i]=="-d"):
			debug		= 1;

	##	-------------------------------------------------------------------------------------
	##	��ȡ����������
	##	-------------------------------------------------------------------------------------
	r = Tk()
	selection = r.clipboard_get()
	if(debug==1):	print(selection);

	##	-------------------------------------------------------------------------------------
	##	�Ի��з�Ϊ�ָ�����
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
		##	����ǿ��ַ������л�����һ��
		##	-------------------------------------------------------------------------------------
		if(line_eol_split[i]==""):
			continue;
		else:
			##	-------------------------------------------------------------------------------------
			##	���ܻ��ж��л���һ��
			##	-------------------------------------------------------------------------------------
			line_comma_split	= line_eol_split[i].split(";")
			for j in range(0,len(line_comma_split)):
				##	-------------------------------------------------------------------------------------
				##	����ǿ��ַ���������Ҫ��ȡ��Ϣ
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