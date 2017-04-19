# -*- coding: utf-8 -*-
#��/usr/bin/python

from tkinter import *

def updateDisplay(buttonString):
    content = display.get()
    if content == "0":
        content = ""
    display.set(content + buttonString)

def calculate():
    result = eval(display.get())
    display.set(display.get() + '=\n' + str(result))

def clear():
    display.set('0')

def backspace():
    display.set(str(display.get()[:-1]))


mainUI = Tk()
mainUI.title('Caculator')
mainUI.geometry('230x200+300+400')


#������ʾ����,Ĭ����ʾ0

display = StringVar()
display.set('0')

# ��Ӽ�������ʾ����ʹ��Label�������ñ���ɫ����С
textLabel = Label(mainUI)

# ������Ҫע��width��ȵĵ�λ���������Label����ʾ�ı���
# ��ô��Щѡ����ı��ĵ�λΪ���尴ť�ĳߴ硣
# ����������֮��ʾͼ����ô��ť�ĳߴ罫�����أ�����������Ļ��λ����
textLabel.config(bg='grey',width=28,height=3,anchor=SE)
textLabel['textvariable']=display

# ������ʾ������Grid�����е�λ��
textLabel.grid(row=0,column=0,columnspan=4)

# ��Ӱ�ť�����õ��ʵ�������
# ��հ�ť������textΪ��ť�ϵ����֣�fgΪ��ť��������ɫ��bgΪ���ֱ����İ�ť��ɫ����widthΪ��ť���
# command����Ϊ��ť�¼��󶨺������󶨵�clear()��������ť����ʱ����
clearButton = Button(mainUI,text = 'C', fg = 'orange',width = 3,command = clear)
# ������հ�ť��λ�ã��к�Ϊ1���к�Ϊ0�����ڶ��е�һ��
clearButton.grid(row = 1,column =0)

# ������ťλ�ã���������հ�ť���Ʋ���ע�ͣ������в鿴Grid�е�λ�ã��еİ�ť����lambda����������������ԭ������Ҫ������Ĳ���
Button(mainUI,text = 'DEL',width=3,command=backspace).grid(row=1,column=1)
Button(mainUI,text = "/",width = 3,command = lambda:updateDisplay('/')).grid(row=1,column=2)
Button(mainUI,text = '*',width = 3,command = lambda:updateDisplay('*')).grid(row=1,column=3)
Button(mainUI,text = '7',width = 3,command = lambda:updateDisplay('7')).grid(row=2,column=0)
Button(mainUI,text = '8',width = 3,command = lambda:updateDisplay('8')).grid(row=2,column=1)
Button(mainUI,text = '9',width = 3,command = lambda:updateDisplay('9')).grid(row=2,column=2)
Button(mainUI, text = '-', width = 3, command = lambda:updateDisplay('-')).grid(row = 2 ,column = 3)
Button(mainUI, text = '4', width = 3, command = lambda:updateDisplay('4')).grid(row = 3, column = 0)
Button(mainUI, text = '5', width = 3, command = lambda:updateDisplay('5')).grid(row = 3, column = 1)
Button(mainUI, text = '6', width = 3, command = lambda:updateDisplay('6')).grid(row = 3, column = 2)
Button(mainUI, text = '+', width = 3, command = lambda:updateDisplay('+')).grid(row = 3, column = 3)
Button(mainUI, text = '1', width = 3, command = lambda:updateDisplay('1')).grid(row = 4, column = 0)
Button(mainUI, text = '2', width = 3, command = lambda:updateDisplay('2')).grid(row = 4, column = 1)
Button(mainUI, text = '3', width = 3, command = lambda:updateDisplay('3')).grid(row = 4, column = 2)


Button(mainUI, text = '=', width = 3, bg = 'orange', height = 3, command = lambda:calculate()).grid(row = 4, column = 3, rowspan = 2)

Button(mainUI, text = '0', width = 10, command = lambda:updateDisplay('0')).grid(row = 5, column = 0, columnspan = 2)
Button(mainUI, text = '.', width = 3, command = lambda:updateDisplay('.')).grid(row = 5, column = 2)


mainUI.mainloop()