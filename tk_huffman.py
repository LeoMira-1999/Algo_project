#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#from huffman import all necessary function for compression and Decompression
from huffman import frequence_counter, huffman_binary_tree, huffman_encoding, decode_bits, huffman_decoding

#import filedialog from tkinter to open and save files
from tkinter import filedialog

#import messagebox from tkinter allows pop-ups
from tkinter import messagebox

#import literal eval to transform string into list when reading a file
from ast import literal_eval

#import tkinter and renamed it as tk
import tkinter as tk

#import stat from os to find size of file
from os import stat

def main_huffman():
    """
    Description: Function that when called creates the interface for huffman
    """
    # Allows the usage of i counter for the functions
    global i

    def clear():
        """
        Description: Allows the user and some functions to automatically clear every textbox
        """

        #Calls the i variable and allows it to be modified globally
        global i

        #reset counter
        i = 0

        #Allow the corresponding textboxes to be modified
        text_huffman.config(state=tk.NORMAL)
        Textbox.config(state=tk.NORMAL)
        text_seq.config(state=tk.NORMAL)

        #Delete all content of corresponding textboxes
        Textbox.delete("1.0", tk.END)
        text_seq.delete("1.0", tk.END)
        text_huffman.delete("1.0", tk.END)

        #enable button file opener
        file_opener.config(state=tk.NORMAL)

        #Allow the corresponding textboxes to be modified
        text_huffman.config(state=tk.DISABLED)
        Textbox.config(state=tk.DISABLED)
        text_seq.config(state=tk.DISABLED)

        #Disable buttons that aren't useful when beginning
        next_button.config(state=tk.DISABLED)
        result_button.config(state=tk.DISABLED)
        savefile.config(state=tk.DISABLED)

        #update the main window
        root.update()

    def save():
        """
        Description: Allows the user to save it's work after pressing the result button
                    or after finishing the next button presses
        """

        #alert user about the automatic .txt file format when saving
        messagebox.showwarning(title="IMPORTANT NOTICE", message="Automatic .txt file format")

        #initialise empty strings
        str_leftover = ""
        str_tree = ""

        ###Store in a particular Format###
        for leftover in binary_leftover:

            if leftover != binary_leftover[-1]:
                str_leftover += leftover+","
            else:
                str_leftover += leftover

        for letter, binary in code.items():
            str_tree +=  letter+","+binary+" "

        str_tree = str_tree[:-1]

        #shows GUI of location and name to save the file
        file = filedialog.asksaveasfilename()

        #if the user selected either compression or Decompression, saves appropriate file
        if value.get() == 1:
            with open(file+".txt", "w", encoding="utf-8") as f:
                f.write(str(binary_caracter)+"\n"+str_leftover+"\n"+str_tree)
        else:
            with open(file+".txt", "w") as f:
                f.write(decoded_seq)

    def openfile():
        """
        Description: allows the user to select the file he wants to work with
        Returns: Error management issues to let the user know what he has done
        """

        #GUI to let user select file
        file = filedialog.askopenfilename()

        #If no file were selected
        if not file:

            #stop and tells him that he needs to select a file
            return messagebox.showerror(title="NO FILE SELECTED", message="Please select a file to continue")

        else:

            #if the file he selected has nothing inside
            if stat(file).st_size == 0:

                #warns user
                messagebox.showerror(title="EMPTY FILE", message="Please select a non empty file to continue")

                #retry
                return openfile()

            #if the file is not a .txt extension
            elif not file.endswith(".txt"):

                #warns user
                messagebox.showerror(title="WRONG FILE FORMAT", message="Please select a .txt file format")

                #retry
                return openfile()

        #open the file to have a look
        with open(file, encoding="utf-8", errors="backslashreplace") as document:

            #if there is a "," in the file
            if "," in document.read():

                # and he selected Compression then divert him to Decompression automatically
                if value.get() == 1:

                    #change to Decompression
                    value.set(2)

                    #warn user
                    messagebox.showwarning(title="SWITCHING TO DECOMPRESSION", message="SWITCHING TO DECOMPRESSION")
                else:
                    pass

            #if there is no "," in the file
            elif "," not in document.read():

                #and he selected decryption
                if value.get() == 2:

                    #change to compression
                    value.set(1)

                    #warn user
                    messagebox.showwarning(title="SWITCHING TO COMPRESSION", message="SWITCHING TO COMPRESSION")
                else:
                    pass

        #enable appropriate buttons
        next_button.config(state=tk.NORMAL)
        result_button.config(state=tk.NORMAL)
        clear_fields.config(state=tk.NORMAL)

        #if he selected compression
        if value.get() == 1:

            #globalise the variable that will be attributed to huffman compression result
            global freq_counter, code, binary_caracter, binary_leftover, sequence, list_res, simple_bin_code

            #enable sequence textbox
            text_seq.config(state=tk.NORMAL)

            #open the file
            with open(file, "r", encoding="utf-8") as file:

                #retreive the sequence
                sequence = ''.join(file.readlines())

                #insert sequence in sequence textbox
                text_seq.insert(tk.END, sequence)

                #count and store frequency of letters in sequence
                freq_counter = frequence_counter(sequence)

                #create binary tree with frequency counter
                code = huffman_binary_tree(freq_counter)

                #create caracter list, leftover and the binary code
                binary_caracter, binary_leftover, simple_bin_code = huffman_encoding(code, sequence)

            #disable sequence texbox
            text_seq.config(state=tk.DISABLED)

        #if he selected Decompression
        else:

            #globalise the variables that will be attributed to the huffman Decompression
            global bin_code, seq_code, bits, decoded_seq

            #initialise empty list to store read lines
            result = []

            #open the file
            with open(file, "r", encoding="utf-8") as file:

                #read each lines
                for line in file.readlines():

                    #append each line to result
                    result.append(line)

                #first line of result will be binary caracters
                bin_caracter = literal_eval(result[0])

                #second line of result will be binary leftovers
                bin_leftover = result[1].split(",")

                #third line of result will be binary tree
                tree_chunks = result[2].split(" ")

                #store in a dictionary the tree
                seq_code = {}

                #loop through list to store in seq_code dictionary
                for chunks in tree_chunks:

                    #split by each comas
                    pair = chunks.split(",")

                    #dictionnary assignation
                    seq_code[pair[0]]=pair[1]

                #enable huffman textbox
                text_huffman.config(state=tk.NORMAL)

                #if exception rises means that there is a caracter the computer
                #print and won't be able to be shown on the GUI, however it will
                #still be present in the final result when saving
                try:

                    #loop in binary caracters and leftovers
                    for caracter, binary in zip(bin_caracter, bin_leftover):

                        #add each one to the huffman textbox
                        text_huffman.insert(tk.END, caracter+binary)

                #if the exception rises
                except Exception:

                    #warn user
                    Textbox.insert(tk.END, "\nCannot print all caracters due to incompatibility, but don't worry they are here")

                #insert blank line
                text_huffman.insert(tk.END, "\n")

                #loop in binary tree
                for nucl, number in seq_code.items():

                    #show each caracter and its associated binary number
                    text_huffman.insert(tk.END, nucl+" = "+number+", ")

                #disable huffman textbox
                text_huffman.config(state=tk.DISABLED)

                #run the decoding to get the binary sequence
                bits = decode_bits(bin_caracter, bin_leftover)

                #get the original sequence
                decoded_seq = huffman_decoding(bits, seq_code)


    def next():
        """
        Description: Allows the user to click next
        """

        #globalise the i variable so that it can be modified and stored
        global i

        #enable textbox to be modified
        Textbox.config(state=tk.NORMAL)

        #if compression is selected
        if value.get() == 1:

            #when the user first clicks on the next button
            if i == 0:

                # show the caracter counter
                Textbox.insert(tk.END, "\n"+"Caracter counter:"+"\n")

                #loop in the frequency counter
                for nucl, count in freq_counter.items():

                    #insert in textbox the invasion well displayed
                    Textbox.insert(tk.END, nucl+" --> "+str(count)+"\n")

            #when the user clicks next a second time
            elif i == 1:

                #insert a visual separation
                Textbox.insert(tk.END, "\n"+"#"*20+"\n")
                Textbox.insert(tk.END, "\n"+"Huffman Binary Tree Caracter Values:"+"\n")

                #loop in the binary tree to show the caracters and there associated code
                for nucl, number in code.items():

                    Textbox.insert(tk.END, nucl+" --> "+str(number)+"\n")

                #also insert the sequence and the binary of the sequence under it
                Textbox.insert(tk.END, "\n"+sequence+"\n"+simple_bin_code+"\n")

            #when the user clicks next a third time
            elif i == 2:

                #insert a visual separation
                Textbox.insert(tk.END, "\n"+"#"*20+"\n")
                Textbox.insert(tk.END, "\n"+"Binary Caracter assignation (extra is non convertible tail of sequence):"+"\n")

                #enable huffman textbox to be modified
                text_huffman.config(state=tk.NORMAL)

                #if exception rises means that there is a caracter the computer
                #print and won't be able to be shown on the GUI, however it will
                #still be present in the final result when saving
                try:

                    #loop in binary caracters and leftovers
                    for caracter, binary in zip(binary_caracter, binary_leftover):

                        #if extra not found
                        if caracter != "extra":

                            #show caracter and its associated binary sequence
                            Textbox.insert(tk.END, caracter+" --> "+str(format(ord(caracter), 'b'))+binary+"\n")

                        #if extra is found
                        else:

                            #show extra and its associated binary sequence
                            Textbox.insert(tk.END, caracter+" --> "+binary+"\n")

                        #insert the results to the huffman textbox
                        text_huffman.insert(tk.END, caracter+binary)

                #if the exception rises
                except Exception:

                    #warn the user
                    Textbox.insert(tk.END, "\nCannot print all caracters due to incompatibility, but don't worry they are here")

                #insert blank line in huffman textbox
                text_huffman.insert(tk.END, "\n")

                #loop in binary tree
                for nucl, number in code.items():

                    #show the user the caracter and its attributed binary
                    text_huffman.insert(tk.END, nucl+" = "+number+", ")

                #disable appropriate buttons
                text_huffman.config(state=tk.DISABLED)
                next_button.config(state=tk.DISABLED)
                result_button.config(state=tk.DISABLED)

                #enable save and clear buttons
                savefile.config(state=tk.NORMAL)
                clear_fields.config(state=tk.NORMAL)

        #if he selected Decompression
        else:

            #when the user first clicks on the next button
            if i == 0:

                #insert in the textbox a title
                Textbox.insert(tk.END, "\n"+"Binary code of sequence:"+"\n\n")

                #initialise empty string
                res = ""

                #if exception rises means that there is a caracter the computer
                #print and won't be able to be shown on the GUI, however it will
                #still be present in the final result when saving
                try:

                    #loop in binary caracters and leftovers
                    for caracter, binary in zip(bin_caracter, bin_leftover):

                        #if extra not found
                        if caracter != "extra":

                            #binary format of the caracter
                            binary_result = str(format(ord(caracter), 'b'))

                            #show caracter and its associated binary sequence
                            Textbox.insert(tk.END, caracter+" --> "+binary_result+binary+"\n")

                            #append result to res
                            res += binary_result+binary

                        #if extra is found
                        else:

                            #show extra and the binary
                            Textbox.insert(tk.END, caracter+" --> "+binary+"\n")

                            #append the binary
                            res += binary
                #if exception rises
                except Exception:

                    # warn user
                    Textbox.insert(tk.END, "\nCannot print all caracters due to incompatibility, but don't worry they are here")

                #insert results in the texbox
                Textbox.insert(tk.END, "\nResult: "+res+"\n")

            #when the user clicks a second time on the next button
            elif i == 1:

                #enable sequence textbox
                text_seq.config(state=tk.NORMAL)

                #insert separation
                Textbox.insert(tk.END, "\n"+"#"*20+"\n")
                Textbox.insert(tk.END, "\n"+"Original Sequence:"+"\n\n")

                #insert in textbox and sequence textbox the Decrompressed sequence
                Textbox.insert(tk.END,decoded_seq)
                text_seq.insert(tk.END,decoded_seq)

                #disable appropriate buttons
                text_seq.config(state=tk.DISABLED)
                next_button.config(state=tk.DISABLED)
                result_button.config(state=tk.DISABLED)

                #enable appropriate buttons
                savefile.config(state=tk.NORMAL)
                clear_fields.config(state=tk.NORMAL)

        #increment counter
        i += 1

        #disabel textbox
        Textbox.config(state=tk.DISABLED)

    def result_button():
        """
        Description: Allows the user to click on the result button
        """

        #if he selected compression
        if value.get() == 1:

            #enable huffman texbox
            text_huffman.config(state=tk.NORMAL)

            #if exception rises means that there is a caracter the computer
            #print and won't be able to be shown on the GUI, however it will
            #still be present in the final result when saving
            try:

                #loop in binary caracters and leftovers
                for caracter, binary in zip(binary_caracter, binary_leftover):

                    #show caracter and its associated binary sequence in the huffman textbox
                    text_huffman.insert(tk.END, caracter+binary)

            #if the exception rises
            except Exception:

                #warn user
                text_huffman.insert(tk.END, "\nCannot print all caracters due to incompatibility, but don't worry they are stored")

            #insert new line
            text_huffman.insert(tk.END, "\n")

            #loop in binary tree
            for nucl, number in code.items():

                #show the user the caracter and its attributed binary
                text_huffman.insert(tk.END, nucl+" = "+number+", ")

            #disable appropriate buttons
            text_huffman.config(state=tk.DISABLED)
            next_button.config(state=tk.DISABLED)
            result_button.config(state=tk.DISABLED)

            #enable file saving and clear buttons
            savefile.config(state=tk.NORMAL)
            clear_fields.config(state=tk.NORMAL)

        #if he selected Decompression
        else:

            #enable sequence texbox
            text_seq.config(state=tk.NORMAL)

            #insert decoded sequence
            text_seq.insert(tk.END,decoded_seq)

            #disable appropriate buttons
            text_seq.config(state=tk.DISABLED)
            next_button.config(state=tk.DISABLED)
            result_button.config(state=tk.DISABLED)

            #enable file saving and clear buttons
            savefile.config(state=tk.NORMAL)
            clear_fields.config(state=tk.NORMAL)

    #initialise frame
    root = tk.Tk()

    #give it a size
    root.geometry("600x500")

    #give it a color
    root.configure(bg="#F0F5F5")

    #set counter
    i = 0

    #initialise tkinter IntVar
    value = tk.IntVar()

    #create label to choose method and pack it
    tk.Label(root,
            text="""Choose a method:""",
            justify = tk.LEFT,
            padx = 20).pack()

    #create Radiobuttons for the user to select between compression and Decrompression
    #with attributed values
    tk.Radiobutton(root,
                   text="Compression",
                   padx = 20,
                   variable=value,
                   value=1,
                   command = clear).pack(anchor=tk.W)

    tk.Radiobutton(root,
                   text="Decompression",
                   padx = 20,
                   variable=value,
                   value=2,
                   command = clear).pack(anchor=tk.W)

    #create sequence label and pack it
    sequence_label = tk.Label(root, text="SEQUENCE:").pack()

    #create sequence X axis Scrollbar
    xscrollbar_seq = tk.Scrollbar(root, orient=tk.HORIZONTAL)
    xscrollbar_seq.pack(side=tk.BOTTOM, fill=tk.X)

    #create sequence textbox
    text_seq = tk.Text(root, height = 1, width = 50 ,wrap=tk.NONE, xscrollcommand=xscrollbar_seq.set)
    text_seq.pack()

    #attach Scrollbar to sequence texbox
    xscrollbar_seq.config(command=text_seq.xview)

    #create huffman label and pack it
    huffman_label = tk.Label(root, text="Huffman:").pack()

    #create huffman X axis Scrollbar
    xscrollbar_huffman = tk.Scrollbar(root, orient=tk.HORIZONTAL)
    xscrollbar_huffman.pack(side=tk.BOTTOM, fill=tk.X)

    #create huffman textbox
    text_huffman = tk.Text(root, height = 2, width = 50 ,wrap=tk.NONE, xscrollcommand=xscrollbar_huffman.set)
    text_huffman.pack()

    #attach scrollbar to BWT texbox
    xscrollbar_huffman.config(command=text_huffman.xview)

    #create textbox
    Textbox = tk.Text(root, height=20, width=50)
    Textbox.pack(side=tk.LEFT, fill=tk.X)

    #create X axis textbox scrollbar
    xscrollbar = tk.Scrollbar(root, orient=tk.HORIZONTAL)
    xscrollbar.pack(side=tk.BOTTOM, fill=tk.X)
    xscrollbar.config(command=Textbox.xview)

    #create Y axis textbox scrollbar
    yscrollbar = tk.Scrollbar(root)
    yscrollbar.pack(side=tk.LEFT, fill=tk.X)
    yscrollbar.config(command=Textbox.yview)

    #attach both scrollbars to textbox
    Textbox.config(wrap=tk.NONE,
                xscrollcommand=xscrollbar.set,
                yscrollcommand=yscrollbar.set)

    #create a file opener button
    file_opener = tk.Button(root, text = "Open file", command = openfile)
    file_opener.pack(side=tk.TOP)

    #create a Next button
    next_button = tk.Button(root, text= "Next", command=next)
    next_button.pack(side=tk.TOP)

    #create a result button
    result_button = tk.Button(root, text= "Result", command= result_button)
    result_button.pack(side=tk.TOP)

    #create a save button
    savefile = tk.Button(root, text= "Save", command= save)
    savefile.pack(side=tk.TOP)

    #create a clear button
    clear_fields = tk.Button(root, text= "Clear", command= clear)
    clear_fields.pack(side=tk.TOP)

    #disable all buttons
    clear_fields.pack(side=tk.TOP)
    Textbox.config(state=tk.DISABLED)
    text_seq.config(state=tk.DISABLED)
    text_huffman.config(state=tk.DISABLED)
    next_button.config(state=tk.DISABLED)
    result_button.config(state=tk.DISABLED)
    file_opener.config(state=tk.DISABLED)
    savefile.config(state=tk.DISABLED)
    clear_fields.config(state=tk.DISABLED)

    #loops the main frame
    root.mainloop()

#if the file is called
if __name__ == "__main__" :

    #launch the frame
    main_huffman()
