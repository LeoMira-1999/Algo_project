#!/usr/bin/env python
# -*- coding: utf-8 -*-


from Tkinter import Entry, Label, StringVar, Tk , Button, END, Radiobutton, Checkbutton, IntVar
from tkFileDialog import askopenfilename, asksaveasfile

def openfile():
    """
    Arguments: None
    Description: Open a file containing a nucleotide sequence
    Returns: None
    """
    filename = askopenfilename(parent=root)
    file = open(filename)
    lines = file.readlines()

root = Tk()
root.title("FANCY ALGO LEO")
root.geometry("200x200")

test = IntVar()
rad_1 = Radiobutton(root, text='BWT', value=0, variable = test)
rad_2 = Radiobutton(root, text='Hufman', value=0, variable = test)
rad_3 = Radiobutton(root, text='BWT + Huffman', value=0, variable = test)
rad_4 = Checkbutton(root, text='Verbose')

rad_1.grid(row=0, column = 0)
rad_2.grid(row=1, column = 0)
rad_3.grid(row=2, column = 0)
rad_4.grid(row=0, column = 2)


root.mainloop()
