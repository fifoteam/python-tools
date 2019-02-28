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
	##	debug			调试开关，默认关闭
	##	out_path		输出文件的路径
	##	pix_format		像素格式，默认8bit
	##	resolution_list	输入图像的分辨率
	##	width			输入图像的宽度
	##	height			输入图像的高度
	##	roi_width		roi宽度
	##	roi_height		roi高度
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
	##	循环查找参数
	##	-------------------------------------------------------------------------------------
	for i in range(0,len(sys.argv)):
		if(sys.argv[i]=="-d"):
			param_avail		= 1;
			debug			= 1;
		if(sys.argv[i]=="-o"):
			param_avail		= 1;
			src_path		= sys.argv[i+1];
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
					pattern_list.append(int(sys.argv[i+j]));

	if (param_avail==0):
		print("-d debug switch,if exist -d,debug will be on");
		print("-o [file path] output file path");
		print("-p [8 to 16] defines byte numbers");
		print("-i [width height] defines resolution,default is 64x64");
		print("-m [pattern mode] supports \"random\" \"pix_inc\" \"pix_inc_by_line\" \"line_inc\" \"frame_fix N\" ");
		print("\t\"randomm\"\t\t\t- random numbers");
		print("\t\"pix_inc\"\t\t\t- first pix is 0,increase in frame");
		print("\t\"slide_fix\"\t\t- first pix is 0,increase in line");
		print("\t\"line_inc\"\t\t\t- first line is 0,increase by line");
		print("\t\"frame_fix N\"\t- full frame is N,N is 0 to 255");
		return


	##	-------------------------------------------------------------------------------------
	##	从命令行中获得像素格式
	##	-------------------------------------------------------------------------------------
	if(pix_format<=8):
		pix_format	= 8;
	elif(pix_format>8 & pix_format<=16):
		pix_format	= 16;
	else:
		pix_format	= 32;

	##	-------------------------------------------------------------------------------------
	##	从列表中信息
	##	------	-------------------------------------------------------------------------------
	width			= resolution_list[0];
	height			= resolution_list[1];
	pattern_mode	= pattern_list[0];

	##	===============================================================================================
	##	ref ***file operation***
	##	===============================================================================================
	##	===============================================================================================
	##	ref ***图像深度***
	##	===============================================================================================
	##	-------------------------------------------------------------------------------------
	##	每个像素占用多少个byte
	##	-------------------------------------------------------------------------------------
	pix_byte	= pix_format/8;

	##	===============================================================================================
	##	ref ***data pattern***
	##	===============================================================================================

	##	-------------------------------------------------------------------------------------
	##	外层循环-高度
	##	-------------------------------------------------------------------------------------
	pixel		= 0;
	pixel_list	= [];
	for i in range(0, height):

		if (pattern_mode=="slide_fix"):
			pixel		= i;
		elif (pattern_mode=="line_inc"):
			pixel		= i;
		elif (pattern_mode=="frame_fix"):
			pixel		= pattern_list[1];

		##	-------------------------------------------------------------------------------------
		##	内层循环-宽度
		##	-------------------------------------------------------------------------------------
		for j in range(0, width):
			##	-------------------------------------------------------------------------------------
			##	第一步，获取一个像素的数据
			##	1byte unsigned char
			##	2byte unsigned short
			##	4byte unsigned int
			##	-------------------------------------------------------------------------------------
			if(pix_byte==1):
				(pixel,)	 = struct.unpack("B",infile.read(1));
			elif(pix_byte==2):
				(pixel,)	 = struct.unpack("H",infile.read(2));
			elif(pix_byte==4):
				(pixel,)	 = struct.unpack("I",infile.read(4));
			pixel_list.append(pixel);

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
	##	ref ***输出文件***
	##	===============================================================================================
	##	-------------------------------------------------------------------------------------
	##	从源文件的路径得到目的文件路径
	##	--解析后的文件名字是"select_line.txt"
	##	-------------------------------------------------------------------------------------
	temp = os.path.split(out_path);
	only_path = temp[0];
	only_name = temp[1];
	if(only_name.rindex(".")!=-1):
		only_name	= only_name[0:only_name.rindex(".")];
#	print("only_path is ",only_path);
#	print("only_name is ",only_name);
	path = only_path+'\\'+only_name+'_'+str(width)+'-'+str(height)+'-'+str(pattern_mode)+".raw";

	##	-------------------------------------------------------------------------------------
	##	建立新的文件
	##	-------------------------------------------------------------------------------------
	outfile	= open(path,"wb+");

	##	-------------------------------------------------------------------------------------
	##	写入新的文件
	##	-------------------------------------------------------------------------------------
	for eachpix in pixel_list:
		if(pix_byte==1):
			write_data	 = struct.pack("B",eachpix);
		elif(pix_byte==2):
			write_data	 = struct.pack("H",eachpix);
		elif(pix_byte==4):
			write_data	 = struct.pack("I",eachpix);
		outfile.write(write_data);

	##	===============================================================================================
	##	ref ***结束***
	##	===============================================================================================
	outfile.close()



raw_pattern()
