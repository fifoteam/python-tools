# -*- coding: utf-8 -*-
#！/usr/bin/python

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


#设置显示内容,默认显示0

display = StringVar()
display.set('0')

# 添加计算器显示区域，使用Label，并设置背景色及大小
textLabel = Label(mainUI)

# 这里需要注意width宽度的单位，如果你在Label中显示文本，
# 那么这些选项将以文本的单位为定义按钮的尺寸。
# 如果你替而代之显示图象，那么按钮的尺寸将是像素（或其它的屏幕单位）。
textLabel.config(bg='grey',width=28,height=3,anchor=SE)
textLabel['textvariable']=display

# 设置显示区域在Grid布局中的位置
textLabel.grid(row=0,column=0,columnspan=4)

# 添加按钮并放置到适当的区域
# 清空按钮，其中text为按钮上的文字，fg为按钮的字体颜色（bg为文字背景的按钮颜色），width为按钮宽度
# command参数为按钮事件绑定函数，绑定到clear()函数，按钮按下时触发
clearButton = Button(mainUI,text = 'C', fg = 'orange',width = 3,command = clear)
# 设置清空按钮的位置，行号为1，列号为0，即第二行第一列
clearButton.grid(row = 1,column =0)

# 其他按钮位置，由于与清空按钮类似不再注释，请自行查看Grid中的位置，有的按钮采用lambda来生成匿名函数，原因是需要处理传入的参数
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