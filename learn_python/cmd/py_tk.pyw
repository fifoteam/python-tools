#coding=utf-8
import os

from tkinter import *   #引入Tkinter工具包
def hello():
#	print('hello world!')
	cmd = "cmd.exe /k uedit32 D:/Tools/UltraEdit/HDL_script/FindInside.js/15"
#	cmd = "cmd.exe /k ping www.baidu.com"
#	os.system(cmd)
	os.popen(cmd)
	return

#	cmd = 'cmd.exe /k net user'#/k表示执行完命令后不关闭shell窗口
#	os.system(cmd)

win = Tk()  #定义一个窗体
win.title('Hello World')    #定义窗体标题
win.geometry('400x200')     #定义窗体的大小，是400X200像素
win.wm_attributes('-topmost',1)		#窗口置顶
btn = Button(win, text='Click me', command=hello)
#注意这个地方，不要写成hello(),如果是hello()的话，
#会在mainloop中调用hello函数，
# 而不是单击button按钮时出发事件
btn.pack(expand=YES, fill=BOTH) #将按钮pack，充满整个窗体(只有pack的组件实例才能显示)

mainloop() #进入主循环，程序运行

