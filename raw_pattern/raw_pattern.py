#coding=utf-8

import os
import sys
import ctypes
import struct
import math
import random

##import sub_func
#from sub_func import *

def raw_pattern() :
	##	===============================================================================================
	##	ref ***commond line parameter***
	##	===============================================================================================
	##	-------------------------------------------------------------------------------------
	##	debug			���Կ��أ�Ĭ�Ϲر�
	##	out_path		����ļ���·��
	##	pix_format		���ظ�ʽ��Ĭ��8bit
	##	resolution_list	����ͼ��ķֱ���
	##	width			����ͼ��Ŀ��
	##	height			����ͼ��ĸ߶�
	##	roi_width		roi���
	##	roi_height		roi�߶�
	##	-------------------------------------------------------------------------------------
	param_avail		= 0;
	debug 			= 0;
	out_path		= "";
	pix_format		= 8;
	bayer_format	= "mono";
	resolution_list	= [];
	pattern_list	= [];

	width			= 0;
	height			= 0;
	pattern_mode	= "";

	##	-------------------------------------------------------------------------------------
	##	ѭ�����Ҳ���
	##	-------------------------------------------------------------------------------------
	for i in range(0,len(sys.argv)):
		if(sys.argv[i]=="-d"):
			param_avail		= 1;
			debug			= 1;
		if(sys.argv[i]=="-o"):
			param_avail		= 1;
			out_path		= sys.argv[i+1];
		if(sys.argv[i]=="-p"):
			param_avail		= 1;
			pix_format		= int(sys.argv[i+1]);
		if(sys.argv[i]=="-b"):
			param_avail		= 1;
			bayer_format	= int(sys.argv[i+1]);
		if(sys.argv[i]=="-i"):
			param_avail		= 1;
			for j in range(1,len(sys.argv)-i):
				if(sys.argv[i+j][0]=="-"):
					break;
				else:
					resolution_list.append(int(sys.argv[i+j]));
		if(sys.argv[i]=="-m"):
			param_avail		= 1;
			for j in range(1,len(sys.argv)-i):
				if(sys.argv[i+j][0]=="-"):
					break;
				else:
					pattern_list.append(sys.argv[i+j]);

	if (param_avail==0):
		print("-d debug switch,if exist -d,debug will be on");
		print("-o [file path] output file path");
		print("-b [\"mono\" or \"rg\" \"gr\" \"bg\" \"gb\"] bayer format,default is mono,and only support mono");
		print("-p [8 to 16] pixel bit width");
		print("-i [width height] defines resolution,default is 64x64");
		print("-m [pattern mode]");
		print("\t\"randomm\"\t\t\t- random numbers");
		print("\t\"pix_inc\"\t\t\t- first pix is 0,increase in frame");
		print("\t\"slide_fix\"\t\t- first pix is 0,increase in line");
		print("\t\"line_inc\"\t\t\t- first line is 0,increase by line");
		print("\t\"frame_fix integer\"\t- full frame is N,N is integer");
		print("\t\"color \"red\" or \"green\" or \"blue\" or \"yellow\" or \"cyan\" or \"magenta\" \"\t- pure color");
		return


	##	-------------------------------------------------------------------------------------
	##	���������л�����ظ�ʽ
	##	-------------------------------------------------------------------------------------
	if(pix_format<=8):
		pix_format	= 8;
	elif(pix_format>8 & pix_format<=16):
		pix_format	= 16;
	else:
		pix_format	= 32;

	##	-------------------------------------------------------------------------------------
	##	���б�����Ϣ
	##	------	-------------------------------------------------------------------------------
	width			= resolution_list[0];
	height			= resolution_list[1];
	pattern_mode	= pattern_list[0];

	##	===============================================================================================
	##	ref ***file operation***
	##	===============================================================================================
	##	===============================================================================================
	##	ref ***ͼ�����***
	##	===============================================================================================
	##	-------------------------------------------------------------------------------------
	##	ÿ������ռ�ö��ٸ�byte
	##	-------------------------------------------------------------------------------------
	pix_byte	= pix_format/8;

	##	===============================================================================================
	##	ref ***data pattern***
	##	===============================================================================================

	##	-------------------------------------------------------------------------------------
	##	���ѭ��-�߶�
	##	-------------------------------------------------------------------------------------
	pixel		= 0;
	pixel_list	= [];
	for i in range(0, height):

		if (pattern_mode=="slide_fix"):
			pixel		= i;
		elif (pattern_mode=="line_inc"):
			pixel		= i;
		elif (pattern_mode=="frame_fix"):
			pixel		= int(pattern_list[1]);

		##	-------------------------------------------------------------------------------------
		##	�ڲ�ѭ��-���
		##	-------------------------------------------------------------------------------------
		for j in range(0, width):
			if (pattern_mode=="random"):
				if(pix_byte==1):
					pixel_list.append(random.randint(0,255));
				elif(pix_byte==2):
					pixel_list.append(random.randint(0,65535));
				elif(pix_byte==4):
					pixel_list.append(random.randint(0,4294967295));

			elif (pattern_mode=="pix_inc"):
				pixel_list.append(pixel);
				pixel		= pixel + 1;

			elif (pattern_mode=="slide_fix"):
				pixel_list.append(pixel);
				pixel		= pixel + 1;

			elif (pattern_mode=="line_inc"):
				pixel_list.append(pixel);

			elif (pattern_mode=="frame_fix"):
				pixel_list.append(pixel);

	##	===============================================================================================
	##	ref ***����ļ�***
	##	===============================================================================================
	##	-------------------------------------------------------------------------------------
	##	��Դ�ļ���·���õ�Ŀ���ļ�·��
	##	--��������ļ�������"select_line.txt"
	##	-------------------------------------------------------------------------------------
	temp = os.path.split(out_path);
	only_path = temp[0];
	only_name = temp[1];
#	if(only_name.rindex(".")!=-1):
#		only_name	= only_name[0:only_name.rindex(".")];
#	print("only_path is ",only_path);
#	print("only_name is ",only_name);
	path = only_path+'\\'+str(width)+'x'+str(height)+'-'+str(pattern_mode)+".raw";
#	print("path is "+path+"");



	##	-------------------------------------------------------------------------------------
	##	�ж��Ƿ�������
	##	-------------------------------------------------------------------------------------
	i=0;
	while (os.path.isfile(path)):
		path = only_path+'\\'+str(width)+'x'+str(height)+'-'+str(pattern_mode)+'_'+str(i)+".raw";
		i=i+1;


	##	-------------------------------------------------------------------------------------
	##	�����µ��ļ�
	##	-------------------------------------------------------------------------------------
	outfile	= open(path,"wb+");

	##	-------------------------------------------------------------------------------------
	##	д���µ��ļ�
	##	-------------------------------------------------------------------------------------
	for eachpix in pixel_list:
		if(pix_byte==1):
			eachpix	= eachpix%256;
			write_data	 = struct.pack("B",eachpix);
		elif(pix_byte==2):
			eachpix	= eachpix%65536;
			write_data	 = struct.pack("H",eachpix);
		elif(pix_byte==4):
			eachpix	= eachpix%4294967295;
			write_data	 = struct.pack("I",eachpix);
		outfile.write(write_data);

	##	===============================================================================================
	##	ref ***����***
	##	===============================================================================================
	outfile.close()



raw_pattern()
