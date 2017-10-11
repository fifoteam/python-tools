#coding=utf-8

import os
import sys
import ctypes
import struct
import math
##import sub_func
#from sub_func import *

def raw_info() :
	##	===============================================================================================
	##	ref ***commond line parameter***
	##	===============================================================================================
	##	-------------------------------------------------------------------------------------
	##	debug			调试开关，默认关闭
	##	pix_format		像素格式，默认8bit
	##	pix_th			像素阈值，默认0，高于阈值的数值会被统计
	##	all_features	所有功能，默认关闭，打开之后会增加时间
	##	-------------------------------------------------------------------------------------
	debug 			= 0;
	src_path		= 0;
	pix_format		= 8;
	pix_th			= 0;
	all_features	= 0;

	##	-------------------------------------------------------------------------------------
	##	循环查找参数
	##	-------------------------------------------------------------------------------------
	for i in range(0,len(sys.argv)):
		if(sys.argv[i]=="-d"):
			debug		= 1;
		if(sys.argv[i]=="-f"):
			src_path	= sys.argv[i+1];
		if(sys.argv[i]=="-p"):
			pix_format	= int(sys.argv[i+1]);
		if(sys.argv[i]=="-t"):
			pix_th		= int(sys.argv[i+1]);
		if(sys.argv[i]=="-a"):
			all_features = 1;

	##	-------------------------------------------------------------------------------------
	##	从命令行中获得像素格式
	##	-------------------------------------------------------------------------------------
	if(pix_format<=8):
		pix_format	= 8;
	elif(pix_format>8 & pix_format<=16):
		pix_format	= 16;
	else:
		pix_format	= 32;

	##	===============================================================================================
	##	ref ***file operation***
	##	===============================================================================================
	##	-------------------------------------------------------------------------------------
	##	判断输入的是否是一个文件
	##	--如果不是文件，打印错误，退出
	##	--如果是一个文件，打开文件
	##	-------------------------------------------------------------------------------------
	if(os.path.isfile(src_path)==False):	return -1
	if(debug==1):	print("src_path is really exist");
	infile	= open(src_path,"rb")

	##	===============================================================================================
	##	ref ***图像深度***
	##	===============================================================================================
	##	-------------------------------------------------------------------------------------
	##	每个像素占用多少个byte
	##	-------------------------------------------------------------------------------------
	pix_byte	= pix_format/8;

	##	===============================================================================================
	##	ref ***读文件 统计信息***
	##	===============================================================================================
	##	-------------------------------------------------------------------------------------
	##	基本的计算需要的参数
	##	-------------------------------------------------------------------------------------
	pixel			= 0;	##当前像素点的数值
	pixel_list		= [];	##像素点，列表，把整个图像都读到内存中
	pixel_max		= 0;	##像素最大值
	pixel_min		= 0;	##像素最小值
	pixel_sum		= 0;	##像素累加值
	pixel_aver		= 0;	##像素平均值
	pixel_num		= 0;	##像素个数

	##	-------------------------------------------------------------------------------------
	##	计算图像大小，进而得出像素个数
	##	-------------------------------------------------------------------------------------
	file_size		= os.path.getsize(src_path);
	pixel_num		= int(file_size/pix_byte);

	##	===============================================================================================
	##	ref ***minimal function***
	##	包括1.找出最大值 2.找出最小值 3.找出平均值
	##	===============================================================================================
	##	-------------------------------------------------------------------------------------
	##	循环读图像
	##	-------------------------------------------------------------------------------------
	for i in range(0, pixel_num):
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

#		##	-------------------------------------------------------------------------------------
#		##	像素最大值
#		##	-------------------------------------------------------------------------------------
#		if(i==0):
#			pixel_max		= pixel_list[i];
#		else:
#			if(pixel_max<pixel_list[i]):
#				pixel_max	= pixel_list[i];
#
#		##	-------------------------------------------------------------------------------------
#		##	像素最小值
#		##	-------------------------------------------------------------------------------------
#		if(i==0):
#			pixel_min		= pixel_list[i];
#		else:
#			if(pixel_min>pixel_list[i]):
#				pixel_min	= pixel_list[i];

		##	-------------------------------------------------------------------------------------
		##	像素累加值
		##	-------------------------------------------------------------------------------------
		pixel_sum	= pixel_sum + pixel_list[i];

	##	-------------------------------------------------------------------------------------
	##	像素平均值
	##	-------------------------------------------------------------------------------------
	pixel_aver	= pixel_sum/pixel_num;

	##	-------------------------------------------------------------------------------------
	##	像素最大值
	##	-------------------------------------------------------------------------------------
	pixel_max	= max(pixel_list);

	##	-------------------------------------------------------------------------------------
	##	像素最小值
	##	-------------------------------------------------------------------------------------
	pixel_min	= min(pixel_list);

	##	===============================================================================================
	##	ref ***all features function***
	##	包括1.计算方差 2.计算均方差 3.计算像素最小值的个数 4.计算像素最大值的个数
	##	===============================================================================================
	##	-------------------------------------------------------------------------------------
	##	高级功能需要的参数
	##	-------------------------------------------------------------------------------------
	pixel_max_num		= 0;	##像素最大值的个数
	pixel_min_num		= 0;	##像素最小值的个数
	pixel_variance		= 0;	##方差
	pixel_std_dev		= 0;	##标准差
	pixel_th_above_num	= 0;	##超过阈值的像素个数


	if(all_features==1):
		##	-------------------------------------------------------------------------------------
		##	找出最大值 最小值的个数
		##	-------------------------------------------------------------------------------------
		pixel_max_num	= pixel_list.count(pixel_max);
		pixel_min_num	= pixel_list.count(pixel_min);

		##	-------------------------------------------------------------------------------------
		##	计算方差和平均差
		##	-------------------------------------------------------------------------------------
		for i in range(0, pixel_num):
			pixel_variance	= (pixel_variance + math.pow(pixel_list[i]-pixel_aver,2));
		pixel_variance	= pixel_variance/pixel_num;
		pixel_std_dev	= math.sqrt(pixel_variance);

		##	-------------------------------------------------------------------------------------
		##	找出所有超过 th 的像素点的个数
		##	由于这一步操作会更改原先的list，因此建议这一步放到最后面
		##	sort是升序函数
		##	-------------------------------------------------------------------------------------
		pixel_list.append(pix_th);
		pixel_list.sort();
		pixel_list.reverse();
		pixel_th_above_num	= pixel_list.index(pix_th);

	##	===============================================================================================
	##	ref ***输出信息***
	##	===============================================================================================
	info_list	= [];
	info_list.append("pixel_num is "+str(pixel_num)+"");
	info_list.append("pixel_min is "+str(pixel_min)+"");
	info_list.append("pixel_max is "+str(pixel_max)+"");
	info_list.append("pixel_aver is "+str(pixel_aver)+"");

	if(all_features==1):
		info_list.append("pixel_max_num is "+str(pixel_max_num)+"");
		info_list.append("pixel_min_num is "+str(pixel_min_num)+"");
		info_list.append("pixel_variance is "+str(pixel_variance)+"");
		info_list.append("pixel_std_dev is "+str(pixel_std_dev)+"");
		info_list.append("pixel_th_above_num is "+str(pixel_th_above_num)+"");

	for eachline in info_list:
		print(eachline);
	infile.close();

	##	===============================================================================================
	##	ref ***输出文件***
	##	===============================================================================================
	##	-------------------------------------------------------------------------------------
	##	从源文件的路径得到目的文件路径
	##	--解析后的文件名字是"select_line.txt"
	##	-------------------------------------------------------------------------------------
	temp = os.path.split(src_path);
	only_path = temp[0];
	only_name = temp[1];
	if(only_name.rindex(".")!=-1):
		only_name	= only_name[0:only_name.rindex(".")];
#	print("only_path is ",only_path);
#	print("only_name is ",only_name);
	path = only_path+'\\'+only_name+"_info.txt";

	##	-------------------------------------------------------------------------------------
	##	建立新的文件
	##	-------------------------------------------------------------------------------------
	outfile_summary = open(path,"w+");

	##	-------------------------------------------------------------------------------------
	##	建立新的文件
	##	-------------------------------------------------------------------------------------
	outfile_summary.write("src file is "+src_path+"\n");
	for eachline in info_list:
		outfile_summary.write(str(eachline));
		outfile_summary.write("\n");

	##	===============================================================================================
	##	ref ***结束***
	##	===============================================================================================
	outfile_summary.close()



raw_info()
