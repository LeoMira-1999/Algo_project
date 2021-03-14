#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#import BWT frame
from tk_BWT import main_BWT

#import Huffman frame
from tk_huffman import main_huffman

#import BWT with Huffman frame
from tk_BWT_huffman import main_BWT_huffman

#import tkinter and rename it as tk
import tkinter as tk

#import messagebox to create error messages when appropriate
from tkinter import messagebox

#Allows selection of algorithm
def window_selector():
    """
    Allows user to select which algorithm he wishes to work with
    """
    #based on the Radiobutton he clicks on, the main frame will close to let the
    #other frame open
    if value.get() == 1:
        root.destroy()
        main_BWT()
    elif value.get() == 2:
        root.destroy()
        main_huffman()
    elif value.get() == 3:
        root.destroy()
        main_BWT_huffman()
    else:

        #if no Radiobutton is selected
        messagebox.showerror(title="NO METHOD SELECTED", message="Please select a method to continue")

#When this file is called the following commands are launched to generate the main
#frame
if __name__ == "__main__" :

    #initialise main frame
    root = tk.Tk()

    #Give it a title
    root.title("Algorithme selector")

    #Appropriate size
    root.geometry("200x200")

    #initialise a tkinter variable that will only take integers
    value = tk.IntVar()

    #create a lable for the method selectot
    tk.Label(root,
            text="""Choose a method:""",
            justify = tk.LEFT,
            padx = 20).pack()

    #create all three Radiobuttons and each of them will carry the variable value
    #which will vary based on its own parameter value
    tk.Radiobutton(root,
                   text="BWT",
                   padx = 20,
                   variable=value,
                   value=1).pack(anchor=tk.W)

    tk.Radiobutton(root,
                   text="Huffman",
                   padx = 20,
                   variable=value,
                   value=2).pack(anchor=tk.W)

    tk.Radiobutton(root,
                   text="BWT + Huffman",
                   padx = 20,
                   variable=value,
                   value=3).pack(anchor=tk.W)

    #Create a next button to validate the selection
    tk.Button(root,
               text="Next",
               padx = 20,
               command=window_selector,
               ).pack(anchor=tk.W)

    #Essential for a responsive GUI
    root.mainloop()
