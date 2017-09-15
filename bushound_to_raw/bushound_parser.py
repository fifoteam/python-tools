#coding=utf-8

import os
import sys
import ctypes
#import sub_func
from sub_func import *

def bushound_parser() :

	##	-------------------------------------------------------------------------------------
	##	debug			���Կ��أ�Ĭ�Ϲر�
	##	src_path		�ļ�·��
	##	parse_info		����leader trailer control����Ϣ
	##	save_raw		����ͼ��
	##	sel_port		bushound���ж���˿ڣ���Ҫѡ��һЩ��ͼ
	##	sel_port_list	ѡ��ĳЩ�˿�
	##	cut_port		ȥ��ĳЩ�˿ڵ�����
	##	-------------------------------------------------------------------------------------
	debug 		= 0;
	src_path	= 0;
	parse_info	= 0;
	save_raw	= 0;
	sel_port	= 0;
	sel_port_list	= [];
	cut_port	= 0;

	for i in range(0,len(sys.argv)):
		if(sys.argv[i]=="-d"):
			debug = 1;
		if(sys.argv[i]=="-f"):
			src_path	= sys.argv[i+1];
		if(sys.argv[i]=="-i"):
			parse_info	= 1;
		if(sys.argv[i]=="-r"):
			save_raw	= 1;
		if(sys.argv[i]=="-c"):
			cut_port	= 1;
		if(sys.argv[i]=="-s"):
			sel_port	= 1;
			for j in range(1,len(sys.argv)-i):
				if(sys.argv[i+j][0]=="-"):
					break;
				else:
					sel_port_list.append(sys.argv[i+j]);

	##	===============================================================================================
	##	ref ***source file operation***
	##	===============================================================================================
	##	-------------------------------------------------------------------------------------
	##	�ж�������Ƿ���һ���ļ�
	##	--��������ļ�����ӡ�����˳�
	##	--�����һ���ļ������ļ�
	##	-------------------------------------------------------------------------------------
	if(os.path.isfile(src_path)==False):	return -1
	if(debug==1):	print("src_path is really exist");
	infile	= open(src_path,"r")

	##	-------------------------------------------------------------------------------------
	##	��¼�ļ�������
	##	-------------------------------------------------------------------------------------
	file_content = infile.readlines();
	line_num = len(file_content);
	if(debug==1):	print("all line num is ",line_num);

	##	===============================================================================================
	##	ref ***read source file,search keyword***
	##	===============================================================================================
	##	-------------------------------------------------------------------------------------
	##	��ͷ��ʼ�� �� "55 33 56 " ��Ϊһ���ļ���ʼ��
	##	-------------------------------------------------------------------------------------
	for i in range(0,line_num):
		line_content	= file_content[i];
		##	-------------------------------------------------------------------------------------
		##	���һ�еĿ�ͷ�� "------"����ô����Ϊ����������ݿ�ʼ
		##	-------------------------------------------------------------------------------------
		if(line_content.find("55 33 56 ")>=0):
			if(debug==1):	print("******find U3V pattern line num is ",i);
			line_start=i;
			break
		##	-------------------------------------------------------------------------------------
		##	������һ�ж�û���ҵ�����ô����û��pattern���ͻ��˳�
		##	-------------------------------------------------------------------------------------
		if(i==line_num-1):
			if(debug==1):	print("******not found U3V pattern");
			return -1

	##	-------------------------------------------------------------------------------------
	##	��һ���ж�λ"55 33 56 "���ֵ�λ��
	##	-------------------------------------------------------------------------------------
	first_byte_pos = file_content[line_start].find('55 33 56 ');
	if(debug==1):	print("first byte position is ",first_byte_pos);

	##	===============================================================================================
	##	ref ***save_raw***
	##	===============================================================================================

	for i in range(line_start,line_num):
		line_content	= file_content[i];

		##	-------------------------------------------------------------------------------------
		##	�ϲ��ո�
		##	tab ת��Ϊ�ո�
		##	ȥ��������β�Ŀո��
		##	��ȡ�ź�����
		##	-------------------------------------------------------------------------------------
		line_content	= line_content.replace("\t"," ");
		line_content	= line_content.strip();
		signal_name		= line_content.split();

		##	-------------------------------------------------------------------------------------
		##	��������
		##	1.�˿���3
		##	2.��������Ϣ����������
		##	3.����������
		##	-------------------------------------------------------------------------------------
		if(signal_name[2]=="IN" && signal_name[1].isdigit==True):
			try:
			    index_value = signal_name[0].index(".3")
			except ValueError:
			    index_value = -1
			if(index_value!=-1):	find_port=1;


		if(find_port==1):
			##	-------------------------------------------------------------------------------------
			##	���� port ��Ϣ
			##	-------------------------------------------------------------------------------------
			if(signal_name[0] not in find_port_list):
				find_port_list.append(signal_name[0]);








	##	===============================================================================================
	##	ref ***parse info***
	##	===============================================================================================
	##	===============================================================================================
	##	--ref ***parse file by keyword***
	##	===============================================================================================
	##	-------------------------------------------------------------------------------------
	##	��line start��ʼ���� U3VC U3VL U3VT �Ĺؼ���
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

	##	===============================================================================================
	##	--ref ***output result***
	##	===============================================================================================
	##	-------------------------------------------------------------------------------------
	##	��Դ�ļ���·���õ�Ŀ���ļ�·��
	##	--��������ļ�������Դ�ļ�����+"_parser.txt"
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

	##	-------------------------------------------------------------------------------------
	##	���±༭file_content ��Ҫд���������ӵ�����
	##	--list_parser��һ����ά�б�ÿһ��Ԫ�ض���һ���б�����0�����кţ�1�����������
	##	--Ҫ��list_parser�б��е�������ӵ���Ӧ���У�file_content�����һ���ַ��ǻس���Ҫȥ��
	##	-------------------------------------------------------------------------------------
	for i in range(0,len(list_parser)):
		file_content[list_parser[i][0]]	= file_content[list_parser[i][0]].rstrip("\n")+"\t#"+list_parser[i][1]+"\n";

	file_content_summay = list_parser;
	for i in range(0,len(list_parser)):
		file_content_summay[i]	= "line num is "+str(list_parser[i][0]+1)+"\t"+list_parser[i][1]+"\n";

	##	-------------------------------------------------------------------------------------
	##	�����µ��ļ�
	##	-------------------------------------------------------------------------------------
	outfile_parser = open(parser_path,"w+");
	outfile_summary = open(summary_path,"w+");

	##	-------------------------------------------------------------------------------------
	##	�����µ��ļ�
	##	-------------------------------------------------------------------------------------
	outfile_parser.writelines(file_content);
	outfile_summary.writelines(file_content_summay);

	##	===============================================================================================
	##	--ref ***end***
	##	===============================================================================================
	outfile_parser.close()
	outfile_summary.close()
	infile.close()


bushound_parser()


