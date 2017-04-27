#coding=utf-8
import re
from tkinter import Tk


##	-------------------------------------------------------------------------------------
##	精确查找一个单词。\b means word boundary, basically. Can be space, punctuation, etc
##	-------------------------------------------------------------------------------------
def find_word(text, search):
	result = re.findall('\\b'+search+'\\b', text, flags=re.IGNORECASE)
	#result = re.findall(r'\b' + search + r'\b', text, flags=re.IGNORECASE)
	if len(result)>0:
		return 1
	else:
		return 0

##	-------------------------------------------------------------------------------------
##	去掉注释
##	-------------------------------------------------------------------------------------
def trim_comment(line_content):
	index_value	= 0;
	line_value	= line_content;
	try:
	    index_value = line_content.index("//")
	except ValueError:
	    index_value = -1
	if(index_value!=-1): line_value	= line_content[0:index_value];
	return	line_value;

##	-------------------------------------------------------------------------------------
##	去除结尾回车符
##	-------------------------------------------------------------------------------------
def trim_eol(line_content):
	index_value	= 0;
	line_value	= line_content;
	try:
	    index_value = line_content.index("/n")
	except ValueError:
	    index_value = -1
	if(index_value!=-1): line_value	= line_content[0:index_value];

	try:
	    index_value = line_content.index("/r/n")
	except ValueError:
	    index_value = -1
	if(index_value!=-1): line_value	= line_content[0:index_value];

	try:
	    index_value = line_content.index("/r")
	except ValueError:
	    index_value = -1
	if(index_value!=-1): line_value	= line_content[0:index_value];

	return	line_value;

##	-------------------------------------------------------------------------------------
##	复制剪贴板的字符
##	-------------------------------------------------------------------------------------
def copy_clip():
	r = Tk()
	c = r.clipboard_get()
	return c

##	-------------------------------------------------------------------------------------
##	判断字符串是否是赋值语句
##	-------------------------------------------------------------------------------------
def judge_driver(line_content):
	line_value	= "";

	##	-------------------------------------------------------------------------------------
	##	检查是否包含赋值符号
	##	-------------------------------------------------------------------------------------
	try:
	    index_value = line_content.index("=")
	except ValueError:
	    index_value = -1
	if(index_value!=-1):
		line_value	= line_content[0:index_value];
	else:
		line_value	= "";
		return	line_value

	##	-------------------------------------------------------------------------------------
	##	如果是case赋值，那么会有冒号
	##	-------------------------------------------------------------------------------------
	try:
	    index_value = line_content.index(":")
	except ValueError:
	    index_value = -1
	if(index_value!=-1):
		line_value	= line_content[index_value:len(line_value)];
		line_value	= line_value.replace("\t"," ");
		line_value	= line_value.strip();

	if(line_value.split(' ')[0]=="assign"):
		judge	= 1;
	elif(line_value.split(' ')[0][0:len(word_sel)]==word_sel):
		driver_list.append(all_list[i]);

	judge	= 0;
	if(line_content.split(' ')[0]=="parameter"):
		judge	= 1;
	elif(line_content.split(' ')[0]=="localparam"):
		judge	= 1;
	elif(line_content.split(' ')[0]=="function"):
		judge	= 1;
	elif(line_content.split(' ')[0]=="task"):
		judge	= 1;
	elif(line_content.split(' ')[0]=="input"):
		judge	= 1;
	elif(line_content.split(' ')[0]=="output"):
		judge	= 1;
	elif(line_content.split(' ')[0]=="inout"):
		judge	= 1;
	elif(line_content.split(' ')[0]=="wire"):
		judge	= 1;
	elif(line_content.split(' ')[0]=="reg"):
		judge	= 1;

	return	judge


##	-------------------------------------------------------------------------------------
##	判断字符串是否一个语句的结尾
##	-------------------------------------------------------------------------------------
end
if
/Indent Strings = "module" "generate" "begin" "case" "fork" "specify" "table" "config" "function" "`ifdef" "`ifndef" "`elsif" "`else" "task"
/Unindent Strings = "endmodule" "endgenerate" "end" "endcase" "join" "endspecify" "endtable" "endconfig" "endfunction" "`elsif" "`endif" "`else" "endtask"
/Open Fold Strings = "module" "task" "function" "generate" "primitive" "begin" "case" "fork" "specify" "table" "config" "`ifdef" "(" "{" "`ifdef" "`ifndef"
/Close Fold Strings = "endmodule" "endtask" "endfunction" "endgenerate" "endprimitive" "end" "endcase" "join" "endspecify" "endtable" "endconfig" "`endif" ")" "}" "`endif"
