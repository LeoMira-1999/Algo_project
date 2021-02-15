#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import tkinter as tk
import sys
from tkinter import filedialog
from BWT import BWT, BWT_decypher, combinations_recurs

"""class TextRedirector(object):
    def __init__(self, widget, tag="stdout"):
        self.widget = widget
        self.tag = tag

    def write(self, str):
        self.widget.configure(state="normal")
        self.widget.insert("end", str, (self.tag,))
        self.widget.configure(state="disabled")"""

def openfile():
    """
    Arguments: None
    Description: Open a file containing a nucleotide sequence
    Returns: None
    """
    filename = filedialog.askopenfilename(parent=newWindow)
    BWT_ = BWT(filename)

    BWT_decypher_= BWT_decypher(BWT_)

    T.insert(tk.END, BWT_+"\n")
    T.insert(tk.END, BWT_decypher_)


def window_selector():

    if v.get() == 1:
        BWT_window()
    elif v.get() == 2:
        Huffman_window()
    elif v.get() == 3:
        BWT_Huffman_window()

def BWT_window():
    global newWindow, T
    # Toplevel object which will
    # be treated as a new window
    newWindow = tk.Tk()
    root.destroy()

    # sets the title of the
    # Toplevel widget
    newWindow.title("BWT")

    # sets the geometry of toplevel
    newWindow.geometry("400x400")

    # A Label widget to show in toplevel
    tk.Label(newWindow,
          text ="BWT Window Work in progress").pack(side=tk.TOP)

    file_opener = tk.Button(newWindow, text = "Open file and RUN", command = openfile)

    file_opener.pack(side=tk.BOTTOM)

    S = tk.Scrollbar(newWindow)
    T = tk.Text(newWindow, height=4, width=50, bd= 10, pady = 10, padx = 10, wrap="word")
    S.pack(side=tk.RIGHT)
    """T.tag_configure("stderr", foreground="#b22222")"""
    T.pack(side=tk.LEFT)
    S.config(command=T.yview)
    T.config(yscrollcommand=S.set)

    """sys.stdout = TextRedirector(T, "stdout")
    sys.stderr = TextRedirector(T, "stderr")"""

    newWindow.mainloop()


def Huffman_window():

    # Toplevel object which will
    # be treated as a new window
    newWindow = tk.Tk()
    root.destroy()

    # sets the title of the
    # Toplevel widget
    newWindow.title("Huffman")

    # sets the geometry of toplevel
    newWindow.geometry("400x400")

    # A Label widget to show in toplevel
    tk.Label(newWindow,
          text ="Huffman Window Work in progress").pack(side=tk.TOP)

    S = tk.Scrollbar(newWindow)
    T = tk.Text(newWindow, height=4, width=50)
    S.pack(side=tk.RIGHT, fill=tk.Y)
    T.pack(side=tk.LEFT, fill=tk.Y)
    S.config(command=T.yview)
    T.config(yscrollcommand=S.set)
    quote = """HAMLET: To be, or not to be--that is the question:
    Whether 'tis nobler in the mind to suffer
    The slings and arrows of outrageous fortune
    Or to take arms against a sea of troubles
    And by opposing end them. To die, to sleep--
    No more--and by a sleep to say we end
    The heartache, and the thousand natural shocks
    That flesh is heir to. 'Tis a consummation
    Devoutly to be wished."""
    T.insert(tk.END, quote)


def BWT_Huffman_window():

    # Toplevel object which will
    # be treated as a new window
    newWindow = tk.Tk()
    root.destroy()

    # sets the title of the
    # Toplevel widget
    newWindow.title("Huffman and BWT")

    # sets the geometry of toplevel
    newWindow.geometry("400x400")

    # A Label widget to show in toplevel
    tk.Label(newWindow,
          text ="Huffman and BWT Window Work in progress").pack(side=tk.TOP)

    S = tk.Scrollbar(newWindow)
    T = tk.Text(newWindow, height=4, width=50)
    S.pack(side=tk.RIGHT, fill=tk.Y)
    T.pack(side=tk.LEFT, fill=tk.Y)
    S.config(command=T.yview)
    T.config(yscrollcommand=S.set)
    quote = """HAMLET: To be, or not to be--that is the question:
    Whether 'tis nobler in the mind to suffer
    The slings and arrows of outrageous fortune
    Or to take arms against a sea of troubles
    And by opposing end them. To die, to sleep--
    No more--and by a sleep to say we end
    The heartache, and the thousand natural shocks
    That flesh is heir to. 'Tis a consummation
    Devoutly to be wished."""
    T.insert(tk.END, quote)


root = tk.Tk()
root.title("FANCY ALGO LEO")
root.geometry("200x200")

v = tk.IntVar()

tk.Label(root,
        text="""Choose a method:""",
        justify = tk.LEFT,
        padx = 20).pack()

tk.Radiobutton(root,
               text="BWT",
               padx = 20,
               variable=v,
               value=1).pack(anchor=tk.W)

tk.Radiobutton(root,
               text="Huffman",
               padx = 20,
               variable=v,
               value=2).pack(anchor=tk.W)

tk.Radiobutton(root,
               text="BWT + Huffman",
               padx = 20,
               variable=v,
               value=3).pack(anchor=tk.W)

tk.Button(root,
           text="Next",
           padx = 20,
           command=window_selector,
           ).pack(anchor=tk.W)

root.mainloop()
