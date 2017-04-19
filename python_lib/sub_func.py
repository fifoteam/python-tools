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
