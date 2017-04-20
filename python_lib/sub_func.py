#coding=utf-8
import re
from tkinter import Tk


##	-------------------------------------------------------------------------------------
##	¾«È·²éÕÒÒ»¸öµ¥´Ê¡£\b means word boundary, basically. Can be space, punctuation, etc
##	-------------------------------------------------------------------------------------
def find_word(text, search):
	result = re.findall('\\b'+search+'\\b', text, flags=re.IGNORECASE)
	#result = re.findall(r'\b' + search + r'\b', text, flags=re.IGNORECASE)
	if len(result)>0:
		return 1
	else:
		return 0

##	-------------------------------------------------------------------------------------
##	È¥µô×¢ÊÍ
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
##	È¥³ı½áÎ²»Ø³µ·û
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
##	¸´ÖÆ¼ôÌù°åµÄ×Ö·û
##	-------------------------------------------------------------------------------------
def copy_clip():
	r = Tk()
	c = r.clipboard_get()
	return c

##	-------------------------------------------------------------------------------------
##	ÅĞ¶Ï×Ö·û´®ÊÇ·ñÊÇÉùÃ÷Óï¾ä
##	-------------------------------------------------------------------------------------
def find_declare(line_content):
	word	= "";
	if(line_content.split(' ')[0]=="parameter"):
		word	= line_content.split(' ')[1];
	elif(line_content.split(' ')[0]=="localparam"):
		word	= line_content.split(' ')[1];
	elif(line_content.split(' ')[0]=="function"):
		word	= line_content.split(' ')[1];
	elif(line_content.split(' ')[0]=="task"):
		word	= line_content.split(' ')[1];
	elif(line_content.split(' ')[0]=="input"):
		word	= line_content.split(' ')[1];
	elif(line_content.split(' ')[0]=="output"):
		word	= line_content.split(' ')[1];
	elif(line_content.split(' ')[0]=="inout"):
		word	= line_content.split(' ')[1];
	elif(line_content.split(' ')[0]=="wire"):
		word	= line_content.split(' ')[1];
	elif(line_content.split(' ')[0]=="reg"):
		word	= line_content.split(' ')[1];

	return	word

##	-------------------------------------------------------------------------------------
##	ÅĞ¶Ï×Ö·û´®ÊÇ·ñÊÇ¸³ÖµÓï¾ä
##	-------------------------------------------------------------------------------------
def judge_driver(line_content):
	line_value	= "";
	try:
	    index_value = line_content.index("=")
	except ValueError:
	    index_value = -1
	if(index_value!=-1):
		line_value	= line_content[0:index_value];
	else:
		line_value	= "";

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
##	ÅĞ¶Ï×Ö·û´®ÊÇ·ñÒ»¸öÓï¾äµÄ½áÎ²
##	-------------------------------------------------------------------------------------
end
if
/Indent Strings = "module" "generate" "begin" "case" "fork" "specify" "table" "config" "function" "`ifdef" "`ifndef" "`elsif" "`else" "task"
/Unindent Strings = "endmodule" "endgenerate" "end" "endcase" "join" "endspecify" "endtable" "endconfig" "endfunction" "`elsif" "`endif" "`else" "endtask"
/Open Fold Strings = "module" "task" "function" "generate" "primitive" "begin" "case" "fork" "specify" "table" "config" "`ifdef" "(" "{" "`ifdef" "`ifndef"
/Close Fold Strings = "endmodule" "endtask" "endfunction" "endgenerate" "endprimitive" "end" "endcase" "join" "endspecify" "endtable" "endconfig" "`endif" ")" "}" "`endif"
