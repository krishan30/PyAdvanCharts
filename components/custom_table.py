import customtkinter
from tkinter import *
from tkinter import ttk
import pandas as pd


def  get_table(root):

    #csv_data = pd.read_csv('https://raw.githubusercontent.com/uiuc-cse/data-fa14/gh-pages/data/iris.csv')
    csv_data = pd.read_csv('./csv_samples/sankey_sample.csv')
    k = csv_data.shape
    #print(k)
    values = csv_data.values
    columns = csv_data.columns
    frame = customtkinter.CTkFrame(root)
    #frame.pack()
    tree = ttk.Treeview(frame, columns = (sorted(col for col in range(1,k[1]+1))),height = 2, show = "tree headings")
    #print(tree['columns'])
    tree.pack(side = 'left',fill='both',expand=1)

    scroll1 = Scrollbar(frame, orient="vertical", command=tree.yview)
    scroll1.pack(side = 'right', fill = 'y')

    tree.configure(yscrollcommand=scroll1.set)

    scroll2 = Scrollbar(root, orient="horizontal", command=tree.xview)
    #scroll2.pack(side = 'bottom', fill = 'x')

    tree.configure(xscrollcommand=scroll2.set)

    for i in range(1,k[1]+1):
        #print(i)
        tree.heading(i, text=columns[i-1])#(k for k in range(k[1]))
        tree.column(i, width = 80)


    for i,val in enumerate(values):

        i1 = i%2
        if (i1==0):

            tree.insert('', 'end',text=i+1, values = tuple(val[sorted(j for j in range(k[1]))]),tag = 'gray')
        else:
            tree.insert('', 'end',text=i+1, values =tuple (val[sorted(j for j in range(k[1]))]))
        tree.tag_configure('gray', background='#cccccc')

    return frame
