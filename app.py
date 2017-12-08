#!/usr/bin/python
# -*- coding: UTF-8 -*-

from tkinter import *           # 导入 Tkinter 库
master = Tk()                     # 创建窗口对象的背景色
                                # 创建两个列表
# li     = ['C','python','php','html','SQL','java']
# movie  = ['CSS','jQuery','Bootstrap']
# listb  = Listbox(root)          #  创建两个列表组件
# listb2 = Listbox(root)
# for item in li:                 # 第一个小部件插入数据
#     listb.insert(0,item)

# for item in movie:              # 第二个小部件插入数据
#     listb2.insert(0,item)

# listb.pack()                    # 将小部件放置到主窗口中
# listb2.pack()

text_url = Text(master, height=1)
text_url.pack()
text_name = Text(master, height=1)
text_name.pack()

def callback():
    print("click!")

b = Button(master, text="OK", command=callback)
b.pack()


text_log = Text()
text_log.pack()

master.mainloop()                 # 进入消息循环
