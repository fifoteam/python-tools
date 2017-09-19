#coding=utf-8

import os
import sys
import ctypes
from sub_func import *

def rtl_module_map() :
	##	===============================================================================================
	##	ref ***commond line parameter***
	##	===============================================================================================
	##	-------------------------------------------------------------------------------------
	##	版本信息，在后面会打印
	##	-------------------------------------------------------------------------------------
	version_message	= "https://github.com/fifoteam/python-tools/rtl_module_map v1.0 2017.9.14";
	##	-------------------------------------------------------------------------------------
	##	debug			调试开关，默认关闭
	##	vhdl			是否例化vhdl调用的模块，默认关闭
	##	src_path		文件路径
	##	-------------------------------------------------------------------------------------
	debug			= 0;
	vhdl			= 0;
	src_path		= 0;

	##	-------------------------------------------------------------------------------------
	##	循环查找参数
	##	-------------------------------------------------------------------------------------
	for i in range(0,len(sys.argv)):
		if(sys.argv[i]=="-d"):
			debug		= 1;
		if(sys.argv[i]=="-h"):
			vhdl		= 1;
		if(sys.argv[i]=="-f"):
			src_path	= sys.argv[i+1];

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
	infile	= open(src_path,"r")

	##	-------------------------------------------------------------------------------------
	##	判断后缀名是否是 .v
	##	-------------------------------------------------------------------------------------
	if(os.path.splitext(src_path)[1]=='.v'):
		if(debug==1):	print("src_extend is verilog");
	else:	return -1

	##	-------------------------------------------------------------------------------------
	##	记录文件总行数，获取module的第一次出现的地方
	##	-------------------------------------------------------------------------------------
	file_content 		= infile.readlines();
	line_num 			= len(file_content);
	[module_start_num,module_name]	= search_module(debug,line_num,"module",file_content);
	module_end_num		= line_num;
	para_start_num		= module_start_num;
	para_end_num		= line_num;

	##	===============================================================================================
	##	ref ***search parameter define***
	##	===============================================================================================
	##	-------------------------------------------------------------------------------------
	##	获得被选择的数据
	##	-------------------------------------------------------------------------------------
	line_content	= 0;
	line_temp		= 0;
	index_value		= 0;
	para_find		= 0;
	para_name		= [];
	para_value		= [];
	signal_name		= [];
	signal_direc	= [];
	signal_type		= [];
	signal_dimen_high	= [];
	signal_dimen_low	= [];
	line_index			= 0;

	##	-------------------------------------------------------------------------------------
	##	找第一个"("，端口声明开始的一行
	##	-------------------------------------------------------------------------------------
	for i in range(module_start_num,line_num+1):
		line_content	= file_content[i];
		##	-------------------------------------------------------------------------------------
		##	去掉注释 回车 字符串两边的空格 tab转换为空格
		##	-------------------------------------------------------------------------------------
		line_content	= trim_eol(line_content);
		line_content	= trim_comment(line_content);

		if(find_index(line_content,"(")!=-1):
			para_start_num = i;
			break;
		if(i==line_num):
			if(debug==1):	print("No ( Keyword!");
			return;

	if(debug==1):	print("para_start_num is "+str(para_start_num)+"");
	##	-------------------------------------------------------------------------------------
	##	在entitystart 与 第一个 ( 之间是否有 #
	##	-------------------------------------------------------------------------------------
	for i in range(module_start_num,para_start_num+1):
		line_content	= file_content[i];
		##	-------------------------------------------------------------------------------------
		##	去掉注释 回车 字符串两边的空格 tab转换为空格
		##	-------------------------------------------------------------------------------------
		line_content	= trim_eol(line_content);
		line_content	= trim_comment(line_content);

		if(find_index(line_content,"#")!=-1):
			para_find = 1;
			if(debug==1):	print("Have Parameter");
			break;
		if(i==para_start_num):
			module_start_num	= para_start_num;
			if(debug==1):	print("No Parameter");
			if(debug==1):	print("para_start_num is "+str(para_start_num)+"");

	##	===============================================================================================
	##	ref ***确定 module 的头和尾***
	##	===============================================================================================
	##	-------------------------------------------------------------------------------------
	##	不存在parameter的宏定义
	##	-------------------------------------------------------------------------------------
	if(para_find==0):
		if(debug==1):	print("para not find");
		##	-------------------------------------------------------------------------------------
		##	find module_end_num
		##	-------------------------------------------------------------------------------------
		for i in range(module_start_num,line_num+1):
			line_content	= file_content[i];
			##	-------------------------------------------------------------------------------------
			##	去掉注释 回车 字符串两边的空格 tab转换为空格
			##	-------------------------------------------------------------------------------------
			line_content	= trim_eol(line_content);
			line_content	= trim_comment(line_content);

			if(find_index(line_content,")")!=-1):
				module_end_num = i;
				if(debug==1):	print("module_end_num is "+str(module_end_num)+"");
				break;
			if(i==line_num):
				if(debug==1):	print("No ) Keyword!");
				return;
	##	-------------------------------------------------------------------------------------
	##	存在parameter的宏定义
	##	-------------------------------------------------------------------------------------
	else:
		if(debug==1):	print("para find");
		##	-------------------------------------------------------------------------------------
		##	find para_end_num
		##	-------------------------------------------------------------------------------------
		for i in range(para_start_num,line_num):
			line_content	= file_content[i];
			##	-------------------------------------------------------------------------------------
			##	去掉注释 回车 字符串两边的空格 tab转换为空格
			##	-------------------------------------------------------------------------------------
			line_content	= trim_eol(line_content);
			line_content	= trim_comment(line_content);

			if(find_index(line_content,")")!=-1):
				para_end_num = i;
				break;
			if(i==line_num):
				if(debug==1):	print("No ) Keyword!");
				return;

		##	-------------------------------------------------------------------------------------
		##	find module_start_num
		##	-------------------------------------------------------------------------------------
		for i in range(para_end_num,line_num):
			line_content	= file_content[i];
			##	-------------------------------------------------------------------------------------
			##	去掉注释 回车 字符串两边的空格 tab转换为空格
			##	-------------------------------------------------------------------------------------
			line_content	= trim_eol(line_content);
			line_content	= trim_comment(line_content);
			##	-------------------------------------------------------------------------------------
			##	para 开始和结束在同一行
			##	-------------------------------------------------------------------------------------
			if(i==para_start_num):
				line_content = line_content[line_content.index(")")+1:len(line_content)];
			if(find_index(line_content,"(")!=-1):
				module_start_num = i;
				break;
			if(i==line_num):
				if(debug==1):	print("No ( Keyword!");
				return;

		##	-------------------------------------------------------------------------------------
		##	find module_end_num
		##	-------------------------------------------------------------------------------------
		for i in range(module_start_num,line_num):
			line_content	= file_content[i];
			##	-------------------------------------------------------------------------------------
			##	去掉注释 回车 字符串两边的空格 tab转换为空格
			##	-------------------------------------------------------------------------------------
			line_content	= trim_eol(line_content);
			line_content	= trim_comment(line_content);
			##	-------------------------------------------------------------------------------------
			##	para 开始和结束在同一行,entity 开始和结束也在这一行
			##	-------------------------------------------------------------------------------------
			if(i==para_start_num):
				line_content = line_content[line_content.index(")")+1:len(line_content)];
			if(find_index(line_content,")")!=-1):
				module_end_num = i;
				break;
			if(i==line_num):
				if(debug==1):	print("No ) Keyword!");
				return;

	##	===============================================================================================
	##	ref ***处理parameter信息***
	##	===============================================================================================
	if(para_find==1):
		for i in range(para_start_num,para_end_num):
			line_content	= file_content[i];
			##	-------------------------------------------------------------------------------------
			##	去掉注释 回车 字符串两边的空格 tab转换为空格
			##	-------------------------------------------------------------------------------------
			line_content	= trim_eol(line_content);
			line_content	= trim_comment(line_content);

			if(find_index(line_content,"(")!=-1):	line_content = line_content[line_content.index("(")+1:len(line_content)];
			if(find_index(line_content,")")!=-1):	line_content = line_content[0:line_content.index(")")];
			if(line_content==""):
				continue;

			##	-------------------------------------------------------------------------------------
			##	在同一行中可能存在多个信号的声明，用逗号区分
			##	-------------------------------------------------------------------------------------
			line_comma_split	= line_content.split(",");
			for i in range(0,len(line_comma_split)):
				line_content	= line_comma_split[i];
				line_content	= line_content.strip();
				line_content	= line_content.replace("\t"," ");
				line_space_split	= line_content.split(' ');
				##	-------------------------------------------------------------------------------------
				##	说明行头的第一个字符是 parameter
				##	-------------------------------------------------------------------------------------
				if(line_space_split[0].lower()=="parameter"):
					##	-------------------------------------------------------------------------------------
					##	line_temp 暂时存储 line_content
					##	-------------------------------------------------------------------------------------
					line_temp		= line_content;
					##	-------------------------------------------------------------------------------------
					##	从行头的第一个空格开始截位
					##	-------------------------------------------------------------------------------------
					line_content	= line_content[line_content.index(" "):len(line_content)];
					##	-------------------------------------------------------------------------------------
					##	去掉行尾的 =
					##	-------------------------------------------------------------------------------------
					if(find_index(line_content,"=")!=-1):	line_content	= line_content[0:line_content.index("=")];
					line_content	= line_content.strip();
					para_name.append(line_content);

					##	-------------------------------------------------------------------------------------
					##	line_temp 中恢复 line_content
					##	-------------------------------------------------------------------------------------
					line_content	= line_temp;
					##	-------------------------------------------------------------------------------------
					##	parameter 的声明中包含 =
					##	-------------------------------------------------------------------------------------
					if(find_index(line_content,"=")!=-1):
						line_content	= line_content[line_content.index("=")+1:len(line_content)];
						line_content	= line_content.strip();
						para_value.append(line_content);
					##	-------------------------------------------------------------------------------------
					##	parameter 的声明中不包含 =
					##	-------------------------------------------------------------------------------------
					else:
						para_value.append(0);

	##+test+
	if(para_find==1 and debug==1):
		for i in range(0,len(para_name)):
			print("para_name"+i+" is "+para_name[i]+"");
			print("para_value"+i+" is "+para_value[i]+"");
	##-test-

	##	===============================================================================================
	##	ref 处理 port 信息
	##	===============================================================================================
	port_declare=0;
	for i in range(module_start_num,module_end_num+1):
		line_content	= file_content[i];
		##	-------------------------------------------------------------------------------------
		##	去掉注释 回车 字符串两边的空格 tab转换为空格
		##	-------------------------------------------------------------------------------------
		line_content	= trim_eol(line_content);
		line_content	= trim_comment(line_content);
		if(debug==1):	print("CurrentLine num is "+str(i)+"");

		##	-------------------------------------------------------------------------------------
		##
		##	-------------------------------------------------------------------------------------
		if(find_index(line_content,"(")!=-1):
			line_content	= line_content[line_content.index("(")+1:len(line_content)];
		##	-------------------------------------------------------------------------------------
		##
		##	-------------------------------------------------------------------------------------
		if(find_index(line_content,")")!=-1):
			line_content	= line_content[0:line_content.index(")")];
		##	-------------------------------------------------------------------------------------
		##
		##	-------------------------------------------------------------------------------------
		if(find_index(line_content,"=")!=-1):
			line_content	= line_content[0:line_content.index("=")];

		line_content	= line_content.strip();
		if(line_content==""):
			if(debug==1):	print("line_content do not have signal info");
			continue;

		##	-------------------------------------------------------------------------------------
		##	在同一行中可能存在多个信号的声明，用逗号区分
		##	-------------------------------------------------------------------------------------
		line_comma_split	= line_content.split(",");
		for k in range(0,len(line_comma_split)):
			if(debug==1):	print("line_comma_split is "+line_comma_split[k]+"");
			line_content	= line_comma_split[k];
			##	-------------------------------------------------------------------------------------
			##	如果逗号分隔符之后是空字符串，不做处理
			##	-------------------------------------------------------------------------------------
			if(line_content.strip()==""):
				continue;
			##	-------------------------------------------------------------------------------------
			##	只在declare=0的时候判断是否处于module name的这一行
			##	declare=0，说明刚开始搜索。=2说明已经搜索到信号名，但是没有在module中指明方向。=1说明在module中指明了方向。
			##	-------------------------------------------------------------------------------------
			if(port_declare==0):
				if(debug==1):	print("go into port declare==0");
				line_temp	= line_content.strip();
				line_temp	= line_temp.replace("\t"," ");
				line_space_split	= line_temp.split(' ');
				##	-------------------------------------------------------------------------------------
				##	module name 的这一行,不搜索这一行
				##	-------------------------------------------------------------------------------------
				if(line_space_split[0].lower()=="module"):
					continue;
			##	-------------------------------------------------------------------------------------
			##	port_declare=2 说明在端口中没有指明port的方向
			##	-------------------------------------------------------------------------------------
			if(port_declare==2):
				if(debug==1):	print("go into port declare==2");
				##	-------------------------------------------------------------------------------------
				##	去掉注释 回车 字符串两边的空格 tab转换为空格
				##	-------------------------------------------------------------------------------------
				line_content		= line_content.strip();
				line_content		= line_content.replace("\t"," ");
				line_space_split	= line_content.split(' ');
				if(line_space_split[0]!=""):
					signal_name.append(line_space_split[0]);

			else:
				if(debug==1):	print("go into port declare==1");
				##	-------------------------------------------------------------------------------------
				##	去掉注释 回车 字符串两边的空格 tab转换为空格
				##	-------------------------------------------------------------------------------------
				line_content		= line_content.strip();
				line_content		= line_content.replace("\t"," ");
				line_space_split	= line_content.split(' ');

				if(line_space_split[0].lower()=="input"):
					port_declare=1;
					line_content	= line_content[5:len(line_content)];
					signal_direc.append(line_space_split[0]);
				elif(line_space_split[0].lower()=="output"):
					port_declare=1;
					line_content	= line_content[6:len(line_content)];
					signal_direc.append(line_space_split[0]);
				elif(line_space_split[0].lower()=="inout"):
					port_declare=1;
					line_content	= line_content[5:len(line_content)];
					signal_direc.append(line_space_split[0]);
				else:
					##	-------------------------------------------------------------------------------------
					##	如果没有方向信息，但是前一个信号已经有了方向信息，那么这个信号的方向和前一个方向是一样的
					##	-------------------------------------------------------------------------------------
					if(port_declare==1):
						if(debug==1):	print("go into comma line,this line does not have direction,but last line has direction");
						signal_direc.append(signal_direc[len(signal_direc)-1]);
					##	-------------------------------------------------------------------------------------
					##	如果没有方向信息，且前一个信号也没有方向信息，那么就没有方向
					##	-------------------------------------------------------------------------------------
					else:
						if(debug==1):	print("go into comma line,this line does not have direction,but last line has direction");
						port_declare	= 2;

				##	-------------------------------------------------------------------------------------
				##	只有在本行有方向信息时，才有可能wire reg 宽度等信息
				##	-------------------------------------------------------------------------------------
				if(port_declare==1):
					##	-------------------------------------------------------------------------------------
					##	方向后面还有可能有 wire reg 属性信息。要把这些属性信息去掉
					##	-------------------------------------------------------------------------------------
					line_content		= line_content.strip();
					line_content		= line_content.replace("\t"," ");
					line_space_split	= line_content.split(' ');

					if(line_space_split[0].lower()=="wire"):
						line_content	= line_content[4:len(line_content)];
					elif(line_space_split[0].lower()=="reg"):
						line_content	= line_content[3:len(line_content)];

					##	-------------------------------------------------------------------------------------
					##	提取vector信息
					##	-------------------------------------------------------------------------------------
					if(find_index(line_content,"]")!=-1):
						signal_type.append("v");
						line_temp			= line_content[line_content.index("[")+1:line_content.index("]")];
						line_space_split	= line_temp.split(":");
						line_space_split[0]	= line_space_split[0].strip();
						line_space_split[1]	= line_space_split[1].strip();
						if(line_space_split[0]>line_space_split[1]):
							signal_dimen_high.append(line_space_split[0]);
							signal_dimen_low.append(line_space_split[1]);
						else:
							signal_dimen_high.append(line_space_split[1]);
							signal_dimen_low.append(line_space_split[0]);
						line_content	= line_content[line_content.index("]")+1:len(line_content)];
					else:
						signal_type.append("s");
						signal_dimen_high.append(0);
						signal_dimen_low.append(0);
				##	-------------------------------------------------------------------------------------
				##	提取信号名
				##	-------------------------------------------------------------------------------------
				line_content	= line_content.strip();
				if(line_content!=""):
					signal_name.append(line_content);


	if(debug==1):
		print("TotalLine is "+str(line_num)+"");
		print("entityEndNum is "+str(module_end_num)+"");
		##++test
		for i in range(0,len(signal_name)):
			print("signal_name "+str(i)+" is "+signal_name[i]+"");
		for i in range(0,len(signal_type)):
			print("signal_type "+str(i)+" is "+signal_type[i]+"");
		for i in range(0,len(signal_direc)):
			print("signal_direc "+str(i)+" is "+signal_direc[i]+"");
		##--test

	##	===============================================================================================
	##	ref 如果在port中没有声明 inout 信息，则继续向下寻找
	##	===============================================================================================
	if(port_declare==2):
		if(debug==1):	print("go into port declare = 2");
		##	-------------------------------------------------------------------------------------
		##	找每一个signal的声明
		##	-------------------------------------------------------------------------------------
		for j in range(0,len(signal_name)):
			if(debug==1):	print("signal be serached "+str(j)+" "+signal_name[j]+"");
			##	-------------------------------------------------------------------------------------
			##	某个信号在每一行中寻找
			##	-------------------------------------------------------------------------------------
			for i in range(module_end_num+1,line_num+1):
				line_content	= file_content[i];
				if(debug==1):	print("current line num is "+str(i)+"");
				##	-------------------------------------------------------------------------------------
				##	去掉注释 回车 字符串两边的空格 tab转换为空格
				##	-------------------------------------------------------------------------------------
				line_content	= trim_eol(line_content);
				line_content	= trim_comment(line_content);
				line_content	= line_content.strip();
				##	-------------------------------------------------------------------------------------
				##	非空的字符串
				##	-------------------------------------------------------------------------------------
				if(line_content!=""):
					line_comma_split	= line_content.split(",");
					##	-------------------------------------------------------------------------------------
					##	在同一行中可能存在多个信号的声明，用逗号区分
					##	-------------------------------------------------------------------------------------
					for k in range(0,len(line_comma_split)):
						line_content	= line_comma_split[k];
						if(find_index(line_content,";")!=-1):
							line_content		= line_content[0:line_content.index(";")];
						line_content		= line_content.replace("\t"," ");
						line_content		= line_content.strip();
						line_space_split	= line_content.split(" ");
						##	-------------------------------------------------------------------------------------
						##	先假设在这一行中没有signal的信号名
						##	-------------------------------------------------------------------------------------
						line_index			= 0;
						for l in range(0,len(line_space_split)):
							if(debug==1):	print("line_space_split "+str(l)+" is "+line_space_split[l]+"");
							##	-------------------------------------------------------------------------------------
							##	在这一行中有signal的信号名
							##	-------------------------------------------------------------------------------------
							if(line_space_split[l]==signal_name[j]):
								line_index	= 1;
								break;

						if(debug==1):	print("line_index is "+str(line_index)+"");
						##	-------------------------------------------------------------------------------------
						##	在这一行中有signal的信号名,在这一行寻找signal的其他属性
						##	-------------------------------------------------------------------------------------
						if(line_index==1):
							##	-------------------------------------------------------------------------------------
							##	在本行中定义了方向和纬度
							##	k==0表示一行的第一个声明
							##	-------------------------------------------------------------------------------------
							if(k==0):
								if(debug==1):	print("the direction is "+line_space_split[0]+"");
								signal_direc.append(line_space_split[0]);
								##	-------------------------------------------------------------------------------------
								##	提取vector信息
								##	-------------------------------------------------------------------------------------
								if(find_index(line_content,"]")!=-1):
									signal_type.append("v");
									line_temp	= line_content[line_content.index("[")+1:line_content.index("]")]
									line_colon_split	= line_temp.split(":");
									line_colon_split[0]	= line_colon_split[0].strip();
									line_colon_split[1]	= line_colon_split[1].strip();
									if(line_colon_split[0]>line_colon_split[1]):
										signal_dimen_high.append(line_colon_split[0]);
										signal_dimen_low.append(line_colon_split[1]);
									else:
										signal_dimen_high.append(line_colon_split[1]);
										signal_dimen_low.append(line_colon_split[0]);
									line_content	= line_content[line_content.index("]")+1:len(line_content)];
								else:
									signal_type.append("s");
									signal_dimen_high.append(0);
									signal_dimen_low.append(0);
							##	-------------------------------------------------------------------------------------
							##	没有在本行中定义方向和纬度
							##	-------------------------------------------------------------------------------------
							else:
								signal_direc.append(signal_direc[-1]);
								signal_type.append(signal_type[-1]);
								signal_dimen_high.append(signal_dimen_high[-1]);
								signal_dimen_low.append(signal_dimen_low[-1]);
							if(debug==1):	print("signal "+str(j)+" have been found");
							if(debug==1):	print(""+signal_name[j]+"");
							if(debug==1):	print("signal_direc is "+signal_direc[-1]+"");
							if(debug==1):	print("signal_type is "+signal_type[-1]+"");
							if(debug==1):	print("signal_dimen_high is "+str(signal_dimen_high[-1])+"");
							if(debug==1):	print("signal_dimen_low is "+str(signal_dimen_low[-1])+"");
							##	-------------------------------------------------------------------------------------
							##	该信号已经找完，可以寻找下一个信号
							##	-------------------------------------------------------------------------------------
							break;
				##	-------------------------------------------------------------------------------------
				##	空字符串
				##	-------------------------------------------------------------------------------------
				else:
					if(debug==1):	print("empty line");
					line_index	= 0;

				##	-------------------------------------------------------------------------------------
				##	如果在这一行中找到了信号的声明，那么就要退出循环
				##	-------------------------------------------------------------------------------------
				if(line_index==1):	break;

	if(debug==1):
		for i in range(0,len(signal_name)):
			print("signal_name "+str(i)+" is "+signal_name[i]+"");
			print("signal_direc "+str(i)+" is "+signal_direc[i]+"");
			print("signal_type "+str(i)+" is "+signal_type[i]+"");

	##	===============================================================================================
	##	ref 字符串扩展到一样的宽度
	##	===============================================================================================
	##	-------------------------------------------------------------------------------------
	##	-- ref 统计param sig 中最长的一个字符串
	##	-------------------------------------------------------------------------------------
	sig_max_length	= 0;
	sig_max_tab		= 0;
	for i in range(0,len(para_name)):
		if(sig_max_length < len(para_name[i])):
			sig_max_length	= len(para_name[i]);

	for i in range(0,len(signal_name)):
		if(sig_max_length < len(signal_name[i])):
			sig_max_length	= len(signal_name[i]);
	if(debug==1):	print("sig_max_length is "+str(sig_max_length)+"");

	##	-------------------------------------------------------------------------------------
	##	-- ref 如果最大长度不是0，进行下一步操作
	##	-------------------------------------------------------------------------------------
	sig_tab_num	= 0;
	if(sig_max_length!=0):
		sig_max_tab	= int(sig_max_length/4)+1;
		if(debug==1):	print("sig_max_tab is "+str(sig_max_tab)+"");
		for i in range(0,len(para_name)):
			##	-------------------------------------------------------------------------------------
			##	计算出需要补全的tab个数，由于信号名字前面有 . (，因此计算长度的时候要+1
			##	-------------------------------------------------------------------------------------
			sig_tab_num	= sig_max_tab-int((len(para_name[i])+1)/4);
			if(debug==1):	print("sig_tab_num is "+str(sig_tab_num)+"");
			for j in range(0,sig_tab_num):
				para_name[i]	= para_name[i] + "\t";

		for i in range(0,len(signal_name)):
			##	-------------------------------------------------------------------------------------
			##	计算出需要补全的tab个数，由于信号名字前面有 . (，因此计算长度的时候要+1
			##	-------------------------------------------------------------------------------------
			sig_tab_num	= sig_max_tab-int((len(signal_name[i])+1)/4);
			if(debug==1): print("sig_tab_num is "+str(sig_tab_num)+"");
			for j in range(0,sig_tab_num):
				signal_name[i]	= signal_name[i] + "\t";

	if(debug==1):
		print("after signal length supply");
		for i in range(0,len(signal_name)):
			print("signal_name "+str(i)+" is "+signal_name[i]+"");

	##	===============================================================================================
	##	ref write file
	##	===============================================================================================
	##	-------------------------------------------------------------------------------------
	##	--ref verilog module map
	##	-------------------------------------------------------------------------------------
	if(para_find==1):
		##	-------------------------------------------------------------------------------------
		##	包含parameter的map
		##	-------------------------------------------------------------------------------------
		print(""+module_name+" # (");
		for i in range(0,len(para_name)-1):
			print("."+para_name[i]+"	("+para_name[i]+"	),");
		if(len(para_name)>0):
			print("."+para_name[i]+"	("+para_name[i]+"	)");
		print(")");
		print(""+module_name+"_inst (");
		for i in range(0,len(signal_name)-1):
			print("."+signal_name[i]+"\t("+signal_name[i]+"	),");
		if(len(signal_name)>0):
			i	= i+1;
			print("."+signal_name[i]+"\t("+signal_name[i]+"	)");
		print(");\r\n");
	else:
		##	-------------------------------------------------------------------------------------
		##	没有parameter的map
		##	-------------------------------------------------------------------------------------
		print(""+module_name+" "+module_name+"_inst (");
		for i in range(0,len(signal_name)-1):
			print("."+signal_name[i]+"\t("+signal_name[i]+"	),");
		if(len(signal_name)>0):
			i	= i+1;
			print("."+signal_name[i]+"\t("+signal_name[i]+"	)");
		print(");\r\n");

	##	-------------------------------------------------------------------------------------
	##	写parameter
	##	-------------------------------------------------------------------------------------
	if(para_find==1):
		for i in range(0,len(para_name)):
			print("parameter	"+para_name[i]+"	= "+para_name[i]+"	;");
		print("\r\n\r\n");

	if(para_find==1):
		for i in range(0,len(para_name)):
			print("parameter	"+para_name[i]+"	= "+para_value[i]+"	;");
		print("\r\n\r\n");

	##	-------------------------------------------------------------------------------------
	##	写signal
	##	-------------------------------------------------------------------------------------
	for i in range(0,len(signal_name)):
		if(signal_type[i]=="s"):
			line_content	= "";
			line_temp		= "1";
		else:
			line_content	= "["+signal_dimen_high[i]+":"+signal_dimen_low[i]+"]\t";
			try:
				line_temp		= int(signal_dimen_high[i])-int(signal_dimen_low[i])+1;
			except ValueError:
				line_temp		= "na";

		if(signal_direc[i]=="output" or signal_direc[i]=="inout"):
			print("wire\t"+line_content+""+signal_name[i]+"	;");
		else:
			if(line_temp=="na"):
				print("reg\t\t"+line_content+""+signal_name[i]+"	= 'b0	;");
			else:
				print("reg\t\t"+line_content+""+signal_name[i]+"	= "+str(line_temp)+"'b0	;");

	##	-------------------------------------------------------------------------------------
	##	写signal
	##	-------------------------------------------------------------------------------------
	print("\r\n\r\n");
	for i in range(0,len(signal_name)):
		if(signal_type[i]=="s"):
			line_content	= "";
		else:
			line_content	= "["+signal_dimen_high[i]+":"+signal_dimen_low[i]+"]\t";
		print("wire\t"+line_content+""+signal_name[i]+"	;");

	##	-------------------------------------------------------------------------------------
	##	--ref vhdl module map
	##	-------------------------------------------------------------------------------------
	if(vhdl==1):
		print("\r\n\r\n");
		##	-------------------------------------------------------------------------------------
		##	component
		##	-------------------------------------------------------------------------------------
		print("component "+module_name+"");
		if(para_find == 1):
			print("	generic (");
			for i in range(0,len(para_name)-1):
				print("	"+para_name[i]+" : integer := "+str(para_value[i])+";");
			if(len(para_name)>0):
				i	= i+1;
				print("	"+para_name[i]+" : integer := "+str(para_value[i])+"");
			print("	);");

		print("	port (");
		for i in range(0,len(signal_name)-1):
			if(signal_type[i]=="s"):
				line_content	= "std_logic";
				line_index		= "";
			else:
				line_content	= "std_logic_vector";
				line_index		= "("+str(signal_dimen_high[i])+" downto "+str(signal_dimen_low[i])+")";
			if(signal_direc[i].lower()=="input"):
				signal_direc[i]="in";
			elif(signal_direc[i].lower()=="output"):
				signal_direc[i]="out";
			print("	"+signal_name[i]+"\t: "+signal_direc[i]+"\t"+line_content+""+str(line_index)+";");

		if(len(signal_name)>0):
			i	= i+1;
			if(signal_type[i]=="s"):
				line_content	= "std_logic";
				line_index		= "";
			else:
				line_content	= "std_logic_vector";
				line_index		= "("+str(signal_dimen_high[i])+" downto "+str(signal_dimen_low[i])+")";

			if(signal_direc[i].lower()=="input"):
				signal_direc[i]="in";
			elif(signal_direc[i].lower()=="output"):
				signal_direc[i]="out";
			print("	"+signal_name[i]+"\t: "+signal_direc[i]+"\t"+line_content+""+str(line_index)+"");

		print("	);");
		print("end component;\r\n");

		##	-------------------------------------------------------------------------------------
		##	map
		##	-------------------------------------------------------------------------------------
		print("inst_"+module_name+" : "+module_name+"");
		if(para_find == 1):
			print("generic map (");
			for i in range(0,len(para_name)-1):
				print(""+para_name[i]+"	=> "+str(para_value[i])+",");
			if(len(para_name)>0):
				i	= i+1;
				print(""+para_name[i]+"	=> "+str(para_value[i])+"");
			print(")");

		print("port map (");
		for i in range(0,len(signal_name)-1):
			print(""+signal_name[i]+"\t=> "+signal_name[i]+",");
		if(len(signal_name)>0):
			i	= i+1;
			print(""+signal_name[i]+"\t=> "+signal_name[i]+"");
		print(");\r\n");

		##	-------------------------------------------------------------------------------------
		##	singal
		##	-------------------------------------------------------------------------------------
		for i in range(0,len(signal_name)):
			if(signal_type[i]=="s"):
				line_content	= "std_logic";
				line_index		= "";
				line_temp		= ":= '0'";
			else:
				line_content	= "std_logic_vector";
				line_index		= "("+signal_dimen_high[i]+" downto "+signal_dimen_low[i]+")";
				line_temp		= ":= (others => '0')";
			print("signal "+signal_name[i]+"\t: "+line_content+""+line_index+" "+line_temp+";");

rtl_module_map()