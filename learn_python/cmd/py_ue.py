#coding=utf-8
import os

def MyFirstFunction() :
	cmd = "cmd.exe /k uedit32 D:/Tools/UltraEdit/HDL_script/FindInside.js/15"
#	cmd = "cmd.exe /k ping www.baidu.com"
	os.system(cmd)

MyFirstFunction()