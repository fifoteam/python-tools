#coding=utf-8
import re

##	-------------------------------------------------------------------------------------
##	��ȷ����һ�����ʡ�\b means word boundary, basically. Can be space, punctuation, etc
##	-------------------------------------------------------------------------------------
def find_word(text, search):
	result = re.findall('\\b'+search+'\\b', text, flags=re.IGNORECASE)
	#result = re.findall(r'\b' + search + r'\b', text, flags=re.IGNORECASE)
	if len(result)>0:
		return 1
	else:
		return 0

