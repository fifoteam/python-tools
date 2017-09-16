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
	##	�汾��Ϣ���ں�����ӡ
	##	-------------------------------------------------------------------------------------
	version_message	= "https://github.com/fifoteam/python-tools/rtl_module_map v1.0 2017.9.14";
	##	-------------------------------------------------------------------------------------
	##	debug			���Կ��أ�Ĭ�Ϲر�
	##	src_path		�ļ�·��
	##	word_sel		ѡ��ĵ���
	##	-------------------------------------------------------------------------------------
	debug			= 0;
	src_path		= 0;

	##	-------------------------------------------------------------------------------------
	##	ѭ�����Ҳ���
	##	-------------------------------------------------------------------------------------
	for i in range(0,len(sys.argv)):
		if(sys.argv[i]=="-d"):
			debug		= 1;
		if(sys.argv[i]=="-f"):
			src_path	= sys.argv[i+1];

	##	-------------------------------------------------------------------------------------
	##	��ȡ�����ļ�
	##	-------------------------------------------------------------------------------------
	if(debug==1):	print("src_path is",src_path);

	##	-------------------------------------------------------------------------------------
	##	�ж�������Ƿ���һ���ļ�
	##	--��������ļ�����ӡ�����˳�
	##	--�����һ���ļ������ļ�
	##	-------------------------------------------------------------------------------------
	if(os.path.isfile(src_path)==False):	return -1
	if(debug==1):	print("src_path is really exist");
	infile	= open(src_path,"r")

	##	-------------------------------------------------------------------------------------
	##	�жϺ�׺���Ƿ��� .v
	##	-------------------------------------------------------------------------------------
	if(os.path.splitext(src_path)[1]=='.v'):
		if(debug==1):	print("src_extend is verilog");
	else:	return -1

	##	-------------------------------------------------------------------------------------
	##	��¼�ļ�����������ȡmodule�ĵ�һ�γ��ֵĵط�
	##	-------------------------------------------------------------------------------------
	file_content 		= infile.readlines();
	line_num 			= len(file_content);
	module_start_num	= search_module(debug,line_num,"module",file_content);
	module_end_num		= line_num;
	para_start_num		= module_start_num;
	para_end_num		= line_num;

	##	===============================================================================================
	##	ref ***search parameter define***
	##	===============================================================================================
	##	-------------------------------------------------------------------------------------
	##	��ñ�ѡ�������
	##	-------------------------------------------------------------------------------------
	line_content	= 0;
	line_temp		= 0;
	index_value		= 0;
	para_find		= 0;
	para_name		= [];
	para_value		= [];
	signal_direc	= [];
	signal_type		= [];


	##	-------------------------------------------------------------------------------------
	##	�ҵ�һ��"("���˿�������ʼ��һ��
	##	-------------------------------------------------------------------------------------
	for i in range(module_start_num,line_num):
		line_content	= file_content[i];
		##	-------------------------------------------------------------------------------------
		##	ȥ��ע�� �س� �ַ������ߵĿո� tabת��Ϊ�ո�
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
	##	��entitystart �� ��һ�� ( ֮���Ƿ��� #
	##	-------------------------------------------------------------------------------------
	for i in range(module_start_num,para_start_num+1):
		line_content	= file_content[i];
		##	-------------------------------------------------------------------------------------
		##	ȥ��ע�� �س� �ַ������ߵĿո� tabת��Ϊ�ո�
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
	##	ref ***ȷ�� module ��ͷ��β***
	##	===============================================================================================
	##	-------------------------------------------------------------------------------------
	##	������parameter�ĺ궨��
	##	-------------------------------------------------------------------------------------
	if(para_find==0):
		if(debug==1):	print("para not find");
		##	-------------------------------------------------------------------------------------
		##	find module_end_num
		##	-------------------------------------------------------------------------------------
		for i in range(module_start_num,line_num+1):
			line_content	= file_content[i];
			##	-------------------------------------------------------------------------------------
			##	ȥ��ע�� �س� �ַ������ߵĿո� tabת��Ϊ�ո�
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
	##	����parameter�ĺ궨��
	##	-------------------------------------------------------------------------------------
	else:
		if(debug==1):	print("para find");
		##	-------------------------------------------------------------------------------------
		##	find para_end_num
		##	-------------------------------------------------------------------------------------
		for i in range(para_start_num,line_num):
			line_content	= file_content[i];
			##	-------------------------------------------------------------------------------------
			##	ȥ��ע�� �س� �ַ������ߵĿո� tabת��Ϊ�ո�
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
			##	ȥ��ע�� �س� �ַ������ߵĿո� tabת��Ϊ�ո�
			##	-------------------------------------------------------------------------------------
			line_content	= trim_eol(line_content);
			line_content	= trim_comment(line_content);
			##	-------------------------------------------------------------------------------------
			##	para ��ʼ�ͽ�����ͬһ��
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
			##	ȥ��ע�� �س� �ַ������ߵĿո� tabת��Ϊ�ո�
			##	-------------------------------------------------------------------------------------
			line_content	= trim_eol(line_content);
			line_content	= trim_comment(line_content);
			##	-------------------------------------------------------------------------------------
			##	para ��ʼ�ͽ�����ͬһ��,entity ��ʼ�ͽ���Ҳ����һ��
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
	##	ref ***����parameter��Ϣ***
	##	===============================================================================================
	j=0;
	if(para_find==1):
		for i in range(para_start_num,para_end_num):
			line_content	= file_content[i];
			##	-------------------------------------------------------------------------------------
			##	ȥ��ע�� �س� �ַ������ߵĿո� tabת��Ϊ�ո�
			##	-------------------------------------------------------------------------------------
			line_content	= trim_eol(line_content);
			line_content	= trim_comment(line_content);

			if(find_index(line_content,"(")!=-1):	line_content = line_content[line_content.index("(")+1:len(line_content)];
			if(find_index(line_content,")")!=-1):	line_content = line_content[0:line_content.index(")")];
			if(line_content==""):
				continue;

			##	-------------------------------------------------------------------------------------
			##	��ͬһ���п��ܴ��ڶ���źŵ��������ö�������
			##	-------------------------------------------------------------------------------------
			line_comma_split	= line_content.split(",");
			for i in range(0,len(line_comma_split)):
				line_content	= line_comma_split[i];
				line_content	= line_content.strip();
				line_content	= line_content.replace("\t"," ");
				line_space_split	= line_content.split(' ');
				##	-------------------------------------------------------------------------------------
				##	˵����ͷ�ĵ�һ���ַ��� parameter
				##	-------------------------------------------------------------------------------------
				if(line_space_split[0].lower()=="parameter"):
					##	-------------------------------------------------------------------------------------
					##	line_space_split[1] ��ʱ�洢 line_content
					##	-------------------------------------------------------------------------------------
					line_space_split[1]	= line_content;
					##	-------------------------------------------------------------------------------------
					##	����ͷ�ĵ�һ���ո�ʼ��λ
					##	-------------------------------------------------------------------------------------
					line_content	= line_content[line_content.index(" "):len(line_content)];
					##	-------------------------------------------------------------------------------------
					##	ȥ����β�� =
					##	-------------------------------------------------------------------------------------
					if(find_index(line_content,"=")!=-1):	line_content	= line_content[0:line_content.index("=")];
					line_content	= line_content.strip();
					para_name[j]	= line_content;

					##	-------------------------------------------------------------------------------------
					##	line_space_split[1]�лָ� line_content
					##	-------------------------------------------------------------------------------------
					line_content	= line_space_split[1];
					##	-------------------------------------------------------------------------------------
					##	parameter �������а��� =
					##	-------------------------------------------------------------------------------------
					if(find_index(line_content,"=")!=-1):
						line_content	= line_content[line_content.index("=")+1:len(line_content)];
						line_content	= line_content.strip();
						para_value[j]	= line_content;
					##	-------------------------------------------------------------------------------------
					##	parameter �������в����� =
					##	-------------------------------------------------------------------------------------
					else:
						para_value[j]	= 0;

					j=j+1;

	##+test+
	if(para_find==1 and debug==1):
		for i in range(0,len(para_name)):
			print("para_name"+i+" is "+para_name[i]+"");
			print("para_value"+i+" is "+para_value[i]+"");
	##-test-

	##	===============================================================================================
	##	ref ���� port ��Ϣ
	##	===============================================================================================
	j=0;
	for i in range(module_start_num,module_end_num+1):
		line_content	= file_content[i];
		##	-------------------------------------------------------------------------------------
		##	ȥ��ע�� �س� �ַ������ߵĿո� tabת��Ϊ�ո�
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
		##	��ͬһ���п��ܴ��ڶ���źŵ��������ö�������
		##	-------------------------------------------------------------------------------------
		line_comma_split	= line_content.split(",");
		for k in range(0,len(line_comma_split)):
			if(debug==1):	print("j is "+str(j)+"");
			if(debug==1):	print("line_content is "+line_content+"");
			line_content	= line_comma_split[k];
			##	-------------------------------------------------------------------------------------
			##	Ĭ�ϣ�û�ж��巽�� �ź���single bit
			##	-------------------------------------------------------------------------------------
			signal_direc[j]	= "na";
			signal_type[j]	= "s";

			##	-------------------------------------------------------------------------------------
			##	ֻ��declare=0��ʱ���ж��Ƿ���module name����һ��
			##	-------------------------------------------------------------------------------------
			if(port_declare==0):
				line_temp	= line_content.strip();
				line_temp	= line_temp.replace("\t"," ");
				line_space_split	= line_temp.split(' ');
				##	-------------------------------------------------------------------------------------
				##	module name ����һ��,��������һ��
				##	-------------------------------------------------------------------------------------
				if(line_space_split[0].lower()=="module"):
					continue;

			##	-------------------------------------------------------------------------------------
			##	port_declare=2 ˵���ڶ˿���û��ָ��port�ķ���
			##	-------------------------------------------------------------------------------------
			if(port_declare==2):
				##	-------------------------------------------------------------------------------------
				##	ȥ��ע�� �س� �ַ������ߵĿո� tabת��Ϊ�ո�
				##	-------------------------------------------------------------------------------------
				line_content		= line_content.strip();
				line_content		= line_content.replace("\t"," ");
				line_space_split	= line_content.split(' ');
				if(line_space_split[0]!=""):
					signal_name[j]	= line_space_split[0];
					j=j+1;

			else:
				##	-------------------------------------------------------------------------------------
				##	ȥ��ע�� �س� �ַ������ߵĿո� tabת��Ϊ�ո�
				##	-------------------------------------------------------------------------------------
				line_content		= line_content.strip();
				line_content		= line_content.replace("\t"," ");
				line_space_split	= line_content.split(' ');

				if(line_space_split[0].lower()=="input"):
					port_declare=1;
					line_content	= line_content[5,len(line_content)-1];
					signal_direc[j]	= line_space_split[0];
				elif(line_space_split[0].lower()=="output"):
					port_declare=1;
					line_content	= line_content[6,len(line_content)-1];
					signal_direc[j]	= line_space_split[0];
				elif(line_space_split[0].lower()=="inout"):
					port_declare=1;
					line_content	= line_content[5,len(line_content)-1];
					signal_direc[j]	= line_space_split[0];
				else:
					if(port_declare==1):
						signal_direc[j]	= signal_direc[j-1];

				line_content		= line_content.strip();
				line_content		= line_content.replace("\t"," ");
				line_space_split	= line_content.split(' ');

				if(line_space_split[0].lower()=="wire"):
					line_content	= line_content[4,len(line_content)-1];
				elif(line_space_split[0].lower()=="reg"):
					line_content	= line_content[3,len(line_content)-1];

				##	-------------------------------------------------------------------------------------
				##	��ȡvector��Ϣ
				##	-------------------------------------------------------------------------------------
				if(find_index(line_content,"]")!=-1):
					signal_type[j]	= "v";
					line_temp	= line_content[line_content.index("[")+1,line_content.index("]")];
					line_space_split	= line_temp.split(":");
					line_space_split[0]	= line_space_split[0].strip();
					line_space_split[1]	= line_space_split[1].strip();
					if(line_space_split[0]>line_space_split[1]):
						signal_dimen_high[j]	= line_space_split[0];
						signal_dimen_low[j]		= line_space_split[1];
					else:
						signal_dimen_high[j]	= line_space_split[1];
						signal_dimen_low[j]		= line_space_split[0];
					line_content	= line_content[line_content.index("]")+1,len(line_content)-1];

				##	-------------------------------------------------------------------------------------
				##	��ȡ�ź���
				##	-------------------------------------------------------------------------------------
				line_content	= line_content.strip();
				if(line_content!=""):
					signal_name[j]	= line_content;
					##	-------------------------------------------------------------------------------------
					##	��port���Ѿ����˷��������
					##	-------------------------------------------------------------------------------------
					if(port_declare==1):
						port_declare=1;
					##	-------------------------------------------------------------------------------------
					##	��port��û�з��������������ҵ����ź���
					##	-------------------------------------------------------------------------------------
					else:
						port_declare=2;
					j=j+1;

	if(debug==1):
		print("TotalLine is "+line_num+"");
		print("entityEndNum is "+module_end_num+"");
		##++test
		for i in range(0,len(signal_name)):
			print("signal_name "+i+" is "+signal_name[i]+"");
		##--test

	##	===============================================================================================
	##	ref �����port��û������ inout ��Ϣ�����������Ѱ��
	##	===============================================================================================
	if(port_declare==2):
		if(debug==1):	print("go into port declare = 2");
		##	-------------------------------------------------------------------------------------
		##	��ÿһ��signal������
		##	-------------------------------------------------------------------------------------
		for j in range(0,len(signal_name)):
			if(debug==1):	print("signal be serached "+j+" "+signal_name[j]+"");

			for i in range(module_end_num+1,line_num):
				line_content	= file_content[i];
				if(debug==1):	print("current line num is "+i+"");
				##	-------------------------------------------------------------------------------------
				##	ȥ��ע�� �س� �ַ������ߵĿո� tabת��Ϊ�ո�
				##	-------------------------------------------------------------------------------------
				line_content	= trim_eol(line_content);
				line_content	= trim_comment(line_content);
				line_content	= line_content.strip();
				##	-------------------------------------------------------------------------------------
				##	�ǿյ��ַ���
				##	-------------------------------------------------------------------------------------
				if(line_content!=""):
					line_comma_split	= line_content.split(",");
					##	-------------------------------------------------------------------------------------
					##	��ͬһ���п��ܴ��ڶ���źŵ��������ö�������
					##	-------------------------------------------------------------------------------------
					for k in range(0,len(line_comma_split)):
						line_content	= line_comma_split[k];
						if(find_index(line_content,";")!=-1):
							line_content	= line_content[0,line_content.index(";")];

							line_content		= line_content.replace("\t"," ");
							line_space_split	= line_content.strip();
							##	-------------------------------------------------------------------------------------
							##	�ȼ�������һ����û��signal���ź���
							##	-------------------------------------------------------------------------------------
							line_index			= 0;
							for l in range(0,len(line_space_split)):
								if(debug==1):	print("line_space_split "+l+" is "+line_space_split[l]+"");
								##	-------------------------------------------------------------------------------------
								##	����һ������signal���ź���
								##	-------------------------------------------------------------------------------------
								if(line_space_split[l]==signal_name[j]):
									line_index	= 1;

							if(debug==1):	print("line_index is "+line_index+"");
							##	-------------------------------------------------------------------------------------
							##	����һ������signal���ź���,����һ��Ѱ��signal����������
							##	-------------------------------------------------------------------------------------
							if(line_index==1):
								signal_direc[j]	= "na";
								signal_type[j]	= "s";

								##	-------------------------------------------------------------------------------------
								##	�ڱ����ж����˷����γ��
								##	-------------------------------------------------------------------------------------
								if(k==0):
									signal_direc[j]	= line_space_split[0];
									##	-------------------------------------------------------------------------------------
									##	��ȡvector��Ϣ
									##	-------------------------------------------------------------------------------------
									if(find_index(line_content,"]")!=-1):
										signal_type[j]	= "v";
										line_temp	= line_content[line_content.index("[")+1,line_content.index("]")]
										line_colon_split	= line_temp.split(":");
										line_colon_split[0]	= line_colon_split.strip();
										line_colon_split[1]	= line_colon_split.strip();
										if(line_colon_split[0]>line_colon_split[1]):
											signal_dimen_high[j]	= line_colon_split[0];
											signal_dimen_low[j]		= line_colon_split[1];
										else:
											signal_dimen_high[j]	= line_colon_split[1];
											signal_dimen_low[j]		= line_colon_split[0];
										line_content	= line_content[line_content.index("]")+1,len(line_content)];
								##	-------------------------------------------------------------------------------------
								##	û���ڱ����ж��巽���γ��
								##	-------------------------------------------------------------------------------------
								else:
									signal_direc[j]	= signal_direc[j-1];
									signal_type[j]	= signal_type[j-1];
									signal_dimen_high[j]	= signal_dimen_high[j-1];
									signal_dimen_low[j]		= signal_dimen_low[j-1];
								if(debug==1):	print("signal "+j+" have been found");
								##	-------------------------------------------------------------------------------------
								##	���ź��Ѿ����꣬����Ѱ����һ���ź�
								##	-------------------------------------------------------------------------------------
								break;

				##	-------------------------------------------------------------------------------------
				##	�������һ�����ҵ����źŵ���������ô��Ҫ�˳�ѭ��
				##	-------------------------------------------------------------------------------------
				if(line_index==1):	break;

	if(debug==1):
		for i in range(0,len(signal_name)):
			print("signal_name "+i+" is "+signal_name[i]+"");
			print("signal_direc "+i+" is "+signal_direc[i]+"");
			print("signal_type "+i+" is "+signal_type[i]+"");

	##	===============================================================================================
	##	ref �ַ�����չ��һ���Ŀ��
	##	===============================================================================================
	##	-------------------------------------------------------------------------------------
	##	-- ref ͳ��param sig �����һ���ַ���
	##	-------------------------------------------------------------------------------------
	sig_max_length	= 0;
	sig_max_tab		= 0;
	for i in range(0,len(para_name)):
		if(sig_max_length < len(para_name[i])):
			sig_max_length	= len(para_name[i]);

	for i in range(0,len(signal_name)):
		if(sig_max_length < len(signal_name[i])):
			sig_max_length	= len(signal_name[i]);
	if(debug==1):	print("sig_max_length is "+sig_max_length+"");

	##	-------------------------------------------------------------------------------------
	##	-- ref �����󳤶Ȳ���0��������һ������
	##	-------------------------------------------------------------------------------------
	sig_tab_num	= 0;
	if(sig_max_length!=0):
		sig_max_tab	= int(sig_max_length/4)+1;
		if(debug==1):	print("sig_max_tab is "+sig_max_tab+"");
		for i in range(0,len(para_name)):
			##	-------------------------------------------------------------------------------------
			##	�������Ҫ��ȫ��tab�����������ź�����ǰ���� . (����˼��㳤�ȵ�ʱ��Ҫ+1
			##	-------------------------------------------------------------------------------------
			sig_tab_num	= sig_max_tab-int((len(para_name[i])+1)/4);
			if(debug==1):	print("sig_tab_num is "+sig_tab_num+"");
			for j in range(0,sig_tab_num):
				para_name[i]	= para_name[i] + "\t";

		for i in range(0,len(signal_name)):
			##	-------------------------------------------------------------------------------------
			##	�������Ҫ��ȫ��tab�����������ź�����ǰ���� . (����˼��㳤�ȵ�ʱ��Ҫ+1
			##	-------------------------------------------------------------------------------------
			sig_tab_num	= sig_max_tab-int((len(signalName[i])+1)/4);
			if(debug==1): print("sig_tab_num is "+sig_tab_num+"");
			for j in range(0,sig_tab_num):
				signal_name[i]	= signal_name[i] + "\t";

	if (debug==1):
		print("after signal length supply");
		for i in range(0,len(signal_name)):
			print("signal_name "+i+" is "+signal_name[i]+"");

	##	===============================================================================================
	##	ref write file
	##	===============================================================================================
	##	-------------------------------------------------------------------------------------
	##	--ref verilog module map
	##	-------------------------------------------------------------------------------------
	if(para_find==1):
		##	-------------------------------------------------------------------------------------
		##	����parameter��map
		##	-------------------------------------------------------------------------------------
		print(""+module_name+" # (\r\n");
		for i in range(0,len(para_name)):
			print("."+para_name[i]+"	("+para_name[i]+"	),\r\n");
		print("."+para_name[i]+"	("+para_name[i]+"	)\r\n");
		print(")\r\n");
		print(""+module_name+"_inst (\r\n");
		for i in range(0,len(signal_name)):
			print("."+signal_name[i]+"\t("+signal_name[i]+"	),\r\n");
		print("."+signal_name[i]+"\t("+signal_name[i]+"	)\r\n");
		print(");\r\n\r\n");
	else:
		##	-------------------------------------------------------------------------------------
		##	û��parameter��map
		##	-------------------------------------------------------------------------------------
		print(""+module_name+" "+module_name+"_inst (\r\n");
		for i in range(0,len(signal_name)):
			print("."+signal_name[i]+"\t("+signal_name[i]+"	),\r\n");
		print("."+signal_name[i]+"\t("+signal_name[i]+"	)\r\n");
		print(");\r\n\r\n");

	##	-------------------------------------------------------------------------------------
	##	дparameter
	##	-------------------------------------------------------------------------------------
	if(para_find==1):
		for i in range(0,len(para_name)):
			print("parameter	"+para_name[i]+"	= "+para_name[i]+"	;\r\n");
		print("\r\n\r\n\r\n");

	if(para_find==1):
		for i in range(0,len(para_name)):
			print("parameter	"+para_name[i]+"	= "+para_value[i]+"	;\r\n");
		print("\r\n\r\n\r\n");

	##	-------------------------------------------------------------------------------------
	##	дsignal
	##	-------------------------------------------------------------------------------------
	for i in len(signal_name):
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
			print("wire\t"+line_content+""+signal_name[i]+"	;\r\n");
		else:
			if(line_temp=="na"):
				print("reg\t\t"+line_content+""+signal_name[i]+"	= 'b0	;\r\n");
			else:
				print("reg\t\t"+line_content+""+signal_name[i]+"	= "+line_temp+"'b0	;\r\n");

	##	-------------------------------------------------------------------------------------
	##	дsignal
	##	-------------------------------------------------------------------------------------
	print("\r\n\r\n\r\n");
	for i in range(0,len(signal_name)):
		if(signal_type[i]=="s"):
			line_content	= "";
		else:
			line_content	= "["+signal_dimen_high[i]+":"+signal_dimen_low[i]+"]\t";
		print("wire\t"+line_content+""+signal_name[i]+"	;\r\n");

	##	-------------------------------------------------------------------------------------
	##	--ref vhdl module map
	##	-------------------------------------------------------------------------------------
	print("\r\n\r\n\r\n");
	##	-------------------------------------------------------------------------------------
	##	component
	##	-------------------------------------------------------------------------------------
	print("component "+module_name+"\r\n");
	if(para_find == 1):
		print("	generic (\r\n");
		for i in range(len(para_name)):
			print("	"+para_name[i]+" : integer := "+para_value[i]+";\r\n");
		print("	"+para_name[i]+" : integer := "+para_value[i]+"\r\n");
		print("	);\r\n");

	print("	port (\r\n");
	for i in range(0,len(signal_name)):
		if(signal_type[i]=="s"):
			line_content	= "std_logic";
			line_index		= "";
		else:
			line_content	= "std_logic_vector";
			line_index		= "("+signal_dimen_high[i]+" downto "+signal_dimen_low[i]+")";
		if(signal_direc[i].lower()=="input"):
			signal_direc[i]="in";
		elif(signal_direc[i].lower()=="output"):
			signal_direc[i]="out";
		print("	"+signal_name[i]+"\t: "+signal_direc[i]+"\t"+line_content+""+line_index+";\r\n");

	if(signal_type[i]=="s"):
		line_content	= "std_logic";
		line_index		= "";
	else:
		line_content	= "std_logic_vector";
		line_index		= "("+signal_dimen_high[i]+" downto "+signal_dimen_low[i]+")";

	if(signal_direc[i].lower()=="input"):
		signal_direc[i]="in";
	elif(signal_direc[i].lower()=="output"):
		signal_direc[i]="out";
	print("	"+signal_name[i]+"\t: "+signal_direc[i]+"\t"+line_content+""+line_index+"\r\n");
	print("	);\r\n");
	print("end component;\r\n\r\n");

	##	-------------------------------------------------------------------------------------
	##	map
	##	-------------------------------------------------------------------------------------
	print("inst_"+module_name+" : "+module_name+"\r\n");
	if(para_find == 1):
		print("generic map (\r\n");
		for i in range(0,len(para_name)):
			print(""+para_name[i]+"	=> "+para_value[i]+",\r\n");
		print(""+para_name[i]+"	=> "+para_value[i]+"\r\n");
		print(")\r\n");

	print("port map (\r\n");
	for i in range(0,len(signal_name)):
		print(""+signal_name[i]+"\t=> "+signal_name[i]+",\r\n");
	print(""+signal_name[i]+"\t=> "+signal_name[i]+"\r\n");
	print(");\r\n\r\n");

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
		print("signal "+signal_name[i]+"\t: "+line_content+""+line_index+" "+line_temp+";\r\n");

	UltraEdit.activeDocument.bottom();
	UltraEdit.save();

rtl_module_map()