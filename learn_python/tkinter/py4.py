# -*- coding: utf-8 -*-
  
__author__ = 'xsc'
  
from tkinter import *
  
#����Tkinter���߰�
def hello():
    print('hello world!')
  
win = Tk()
#����һ������
  
win.title('Hello World')
#���崰�����
  
win.geometry('800x200')
#���崰��Ĵ�С����400X200����
  
btn = Button(win, text='Click me', command=hello)
#ע������ط�����Ҫд��hello(),�����hello()�Ļ���
#����mainloop�е���hello������
# �����ǵ���button��ťʱ�����¼�
  
btn.pack(expand=YES, fill=BOTH)
#����ťpack��������������(ֻ��pack�����ʵ��������ʾ)
  
mainloop()  #������ѭ������������