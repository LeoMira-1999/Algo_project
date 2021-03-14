#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#from huffman import all necessary function for compression and Decompression
from huffman import frequence_counter, huffman_binary_tree, huffman_encoding, decode_bits, huffman_decoding

# from BWT import the encryption and decryption
from BWT import BWT, BWT_decypher

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

def main_BWT_huffman():
    """
    Description: Function that when called creates the interface for BWT + huffman
    """

    # Allows the usage of i/j counter and combination_decrypt by other fonctions inside main_BWT_huffman
    global i, j, combination_decrypt

    def clear():
        """
        Description: Allows the user and some functions to automatically clear every textbox
        """

        #Calls the combination_decrypt j and i variables and allows them to be modified globally
        global i, j, combination_decrypt

        #reset all variables
        combination_decrypt = None
        i = 0
        j = None

        #Enable appropriate buttons
        text_huffman.config(state=tk.NORMAL)
        text_bwt.config(state=tk.NORMAL)
        Textbox.config(state=tk.NORMAL)
        text_seq.config(state=tk.NORMAL)

        #Delete textboxes
        Textbox.delete("1.0", tk.END)
        text_seq.delete("1.0", tk.END)
        text_huffman.delete("1.0", tk.END)
        text_bwt.delete("1.0", tk.END)

        #enable file opener button
        file_opener.config(state=tk.NORMAL)

        #disable all textboxes
        text_huffman.config(state=tk.DISABLED)
        text_bwt.config(state=tk.DISABLED)
        Textbox.config(state=tk.DISABLED)
        text_seq.config(state=tk.DISABLED)

        #disable appropriate buttons
        next_button.config(state=tk.DISABLED)
        result_button.config(state=tk.DISABLED)
        savefile.config(state=tk.DISABLED)

        #update frame
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

        #if the user selected either encryption + compression or Decompression + decryption, saves appropriate file
        if value.get() == 1:
            with open(file+".txt", "w") as f:
                f.write(str(binary_caracter)+"\n"+str_leftover+"\n"+str_tree)
        else:
            with open(file+".txt", "w") as f:
                f.write(result_decrypt)

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
        with open(file) as document:

            #if there is a [ in the file
            if "[" in document.read():

                # and he selected encryption + Compression then divert him to Decompression + decryption automatically
                if value.get() == 1:

                    #change to Decompression + decryption
                    value.set(2)

                    #warn user
                    messagebox.showwarning(title="SWITCHING TO DECOMPRESSION + DECRYTPION", message="SWITCHING TO DECOMPRESSION + DECRYTPION")
                else:
                    pass
            #if there isn't a [ in the file
            elif "[" not in document.read():

                # and he selected Decompression + decryption then divert him to encryption + Compression automatically
                if value.get() == 2:

                    #change to encryption + Compression
                    value.set(1)

                    #warn user
                    messagebox.showwarning(title="SWITCHING TO COMPRESSION + ENCRYTPION", message="SWITCHING TO COMPRESSION + ENCRYTPION")
                else:
                    pass

        #enable appropriate buttons
        next_button.config(state=tk.NORMAL)
        result_button.config(state=tk.NORMAL)
        clear_fields.config(state=tk.NORMAL)

        #if he selected encryption + Compression
        if value.get() == 1:

            #globalise the variable that will be attributed to encryption + Compression result
            global freq_counter, code, binary_caracter, binary_leftover, sequence, simple_bin_code, result, sorted_combinations, combinations

            #enable sequence textbox
            text_seq.config(state=tk.NORMAL)

            #initiate BWT
            result, sorted_combinations, combinations = BWT(file)

            #open the file
            with open(file, "r") as file:

                #retreive the sequence
                sequence = ''.join(file.readlines())

                #insert sequence in sequence textbox
                text_seq.insert(tk.END, sequence)

                #count and store frequency of letters in encrypted sequence
                freq_counter = frequence_counter(result)

                #create binary tree with frequency counter
                code = huffman_binary_tree(freq_counter)

                #create caracter list, leftover and the binary code
                binary_caracter, binary_leftover, simple_bin_code = huffman_encoding(code, result)

            #disable sequence texbox
            text_seq.config(state=tk.DISABLED)

        #if he selected Decompression + decryption
        else:

            #globalise the variables that will be attributed to the Decompression + decryption
            global bin_code, seq_code, bits, decoded_seq, result_decrypt

            #initialise empty list to store read lines
            result = []

            #open the file
            with open(file, "r") as file:

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

                #get the original encrypted sequence
                decoded_seq = huffman_decoding(bits, seq_code)

                #initialise decryption
                result_decrypt= BWT_decypher(decoded_seq)


    def next():
        """
        Description: Allows the user to click next
        """

        #globalise i/j counter and combination_decrypt
        global i, j, combination_decrypt

        #enable editing of textbox
        Textbox.config(state=tk.NORMAL)

        #if compression + decryption is selected
        if value.get() == 1:

            #enable editing of BWT textbox
            text_bwt.config(state=tk.NORMAL)

            #if i counter has not been disabled
            if i is not None:

                #shows the user the different $ combinations in the sequence
                if i <= len(combinations):
                    Textbox.insert(tk.END, combinations[i]+"\n")

            #if i is disabled (None)
            else:

                #finalise BWT
                if j == 0:

                    #insert separation
                    Textbox.insert(tk.END, "\n"+"#"*len(combinations)+"\n\n")

                    #insert combinations in texbox
                    for comb in range (0, len(sorted_combinations),1):

                        Textbox.insert(tk.END, sorted_combinations[comb]+"\n")

                    #display encrypted result in BWT textbox
                    text_bwt.insert(tk.END, result)

                    #disable BWT textbox
                    text_bwt.config(state=tk.DISABLED)

                #When the user clicks again on next it will move to huffman compression
                if j == 1:

                    #insert separation
                    Textbox.insert(tk.END, "\n\n"+"#"*len(combinations)+"\n\n")
                    Textbox.insert(tk.END, "\n"+"Caracter counter:"+"\n")

                    #loop in the frequency counter
                    for nucl, count in freq_counter.items():

                        #insert in textbox the invasion well displayed
                        Textbox.insert(tk.END, nucl+" --> "+str(count)+"\n")

                #second click on next after entering huffman compression
                elif j == 2:

                    #insert separation
                    Textbox.insert(tk.END, "\n"+"#"*20+"\n")
                    Textbox.insert(tk.END, "\n"+"Huffman Binary Tree Caracter Values:"+"\n")

                    #loop in the binary tree to show the caracters and there associated code
                    for nucl, number in code.items():
                        Textbox.insert(tk.END, nucl+" --> "+str(number)+"\n")

                    #also insert the sequence and the binary of the sequence under it
                    Textbox.insert(tk.END, "\n"+result+"\n"+simple_bin_code+"\n")

                #third click on next
                elif j == 3:

                    #separation
                    Textbox.insert(tk.END, "\n"+"#"*20+"\n")
                    Textbox.insert(tk.END, "\n"+"Binary Caracter assignation (extra is non convertible tail of sequence):"+"\n")

                    #enabling editing of huffman textbox
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

            #code used to switch from i counter to j counter (BWT to huffman)
            if i is not None:
                if i <= len(combinations)-2:
                    i += 1
                else:
                    i = None
                    j = 0
            else:
                j += 1

        #if he selected Decompression + encryption
        else:

            #When the user will click the first time on next
            if i == 0:

                #insert the separator
                Textbox.insert(tk.END, "\n"+"Binary code of sequence:"+"\n\n")

                #initialise emty string
                res = ""

                #if exception rises means that there is a caracter the computer
                #print and won't be able to be shown on the GUI, however it will
                #still be present in the final result when saving
                try:

                    #loop in binary caracters and leftovers
                    for caracter, binary in zip(bin_caracter, bin_leftover):

                        #if extra not found
                        if caracter != "extra":

                            binary_result = str(format(ord(caracter), 'b'))
                            #show caracter and its associated binary sequence
                            Textbox.insert(tk.END, caracter+" --> "+binary_result+binary+"\n")

                            #append results
                            res += binary_result+binary

                        #otherwise
                        else:

                            #show extra and the binary code
                            Textbox.insert(tk.END, caracter+" --> "+binary+"\n")

                            #append results
                            res += binary

                #if a caracter can't be printed
                except Exception:

                    #warn user
                    Textbox.insert(tk.END, "\nCannot print all caracters due to incompatibility, but don't worry they are here")

                #display result
                Textbox.insert(tk.END, "\nResult: "+res+"\n")

            #if the user clicks a second time on next
            elif i == 1:

                #enable BWT textbox editing
                text_bwt.config(state=tk.NORMAL)

                #print separator
                Textbox.insert(tk.END, "\n"+"#"*20+"\n")
                Textbox.insert(tk.END, "\n"+"Original Sequence:"+"\n\n")

                #insert decoded sequence in textbox and BWT
                Textbox.insert(tk.END,decoded_seq)
                text_bwt.insert(tk.END,decoded_seq)

                #disable BWT texbox
                text_bwt.config(state=tk.DISABLED)

            #if the user clicks a second time on next
            elif i == 2:

                #delete content in textbox
                Textbox.delete('1.0', tk.END)

                #setup the combination decrypt variable
                if combination_decrypt is None:
                    combination_decrypt = [[element] for element in decoded_seq]

                #once done
                else:

                    #insert elements in combination decrypt
                    for caracter, attempts in zip(decoded_seq, combination_decrypt):

                        attempts.insert(0, caracter)

                #sort the values
                combination_decrypt = sorted(combination_decrypt)

                #insert each value in the textbox
                for element in combination_decrypt:
                    Textbox.insert(tk.END, "".join(element)+"\n")

                #if all values were inserted
                if len(combination_decrypt[-1]) == len(decoded_seq):

                    #enable sequence textbox
                    text_seq.config(state=tk.NORMAL)

                    #insert sequence
                    text_seq.insert(tk.END, result_decrypt)

                    #disable sequence textbox, next and result buttons
                    text_seq.config(state=tk.DISABLED)
                    next_button.config(state=tk.DISABLED)
                    result_button.config(state=tk.DISABLED)

                    #enable save and clear buttons
                    savefile.config(state=tk.NORMAL)
                    clear_fields.config(state=tk.NORMAL)

            #doesn't allow i to be greater than 2
            if i < 2:
                i += 1
            else:
                i = 2

        #disable textbox
        Textbox.config(state=tk.DISABLED)

    def result_button():
        """
        Description: Allows the user to click on the result button
        """

        #if compression + decryption is selected
        if value.get() == 1:

            #enable BWT textbox
            text_bwt.config(state=tk.NORMAL)

            #insert results in BWT textbox
            text_bwt.insert(tk.END, result)

            #disable BWT texbox
            text_bwt.config(state=tk.DISABLED)

            #enable huffman textbox
            text_huffman.config(state=tk.NORMAL)

            #if exception rises means that there is a caracter the computer
            #print and won't be able to be shown on the GUI, however it will
            #still be present in the final result when saving
            try:

                #loop in binary caracters and leftovers
                for caracter, binary in zip(binary_caracter, binary_leftover):

                    #show caracter and its associated binary sequence
                    text_huffman.insert(tk.END, caracter+binary)

            #if there is a caracter that can't be printed
            except Exception:

                #warn user
                text_huffman.insert(tk.END, "\nCannot print all caracters due to incompatibility, but don't worry they are stored")

            #separator
            text_huffman.insert(tk.END, "\n")

            #insert letters and associated binary code
            for nucl, number in code.items():
                text_huffman.insert(tk.END, nucl+" = "+number+", ")

            # disable previously enabled buttons
            text_huffman.config(state=tk.DISABLED)
            next_button.config(state=tk.DISABLED)
            result_button.config(state=tk.DISABLED)

            #enable save and clear buttons
            savefile.config(state=tk.NORMAL)
            clear_fields.config(state=tk.NORMAL)

        #if he selected Decompression + encryption
        else:

            # enable appropriate buttons
            text_bwt.config(state=tk.NORMAL)
            text_seq.config(state=tk.NORMAL)
            savefile.config(state=tk.NORMAL)
            clear_fields.config(state=tk.NORMAL)

            #insert in BWT and sequence Textbox
            text_bwt.insert(tk.END,decoded_seq)
            text_seq.insert(tk.END, result_decrypt)

            #disable appropriate buttons
            text_bwt.config(state=tk.DISABLED)
            text_seq.config(state=tk.DISABLED)
            next_button.config(state=tk.DISABLED)
            result_button.config(state=tk.DISABLED)


    #initialise frame
    root = tk.Tk()

    #give it a size
    root.geometry("600x500")

    #color it
    root.configure(bg="#F0F5F5")

    #initialise variables that will be used by other functions
    combination_decrypt = None
    i = 0
    j = None
    value = tk.IntVar()

    #create a label
    tk.Label(root,
            text="""Choose a method:""",
            justify = tk.LEFT,
            padx = 20).pack()

    #create two Radiobuttons for process selection
    tk.Radiobutton(root,
                   text="Encrypt + Compress",
                   padx = 20,
                   variable=value,
                   value=1,
                   command = clear).pack(anchor=tk.W)

    tk.Radiobutton(root,
                   text="Decrompress + Decrypt",
                   padx = 20,
                   variable=value,
                   value=2,
                   command = clear).pack(anchor=tk.W)

    #sequence label
    sequence_label = tk.Label(root, text="SEQUENCE:").pack()

    #Scrollbar for X axis on sequence textbox
    xscrollbar_seq = tk.Scrollbar(root, orient=tk.HORIZONTAL)
    xscrollbar_seq.pack(side=tk.BOTTOM, fill=tk.X)

    #create sequence texbox
    text_seq = tk.Text(root, height = 1, width = 50 ,wrap=tk.NONE, xscrollcommand=xscrollbar_seq.set)
    text_seq.pack()

    #setup X axis scrollbar on sequence textbox
    xscrollbar_seq.config(command=text_seq.xview)

    #create label
    bwt_label = tk.Label(root, text="BWT:").pack()

    #create BWT scrollbar X axis
    xscrollbar_bwt = tk.Scrollbar(root, orient=tk.HORIZONTAL)
    xscrollbar_bwt.pack(side=tk.BOTTOM, fill=tk.X)

    #create BWT textbox
    text_bwt = tk.Text(root, height = 1, width = 50 ,wrap=tk.NONE, xscrollcommand=xscrollbar_bwt.set)
    text_bwt.pack()

    #associate scrollbar to BWT textbox
    xscrollbar_bwt.config(command=text_bwt.xview)

    #create huffman label
    huffman_label = tk.Label(root, text="Huffman:").pack()

    #create huffman scrollbar X axis
    xscrollbar_huffman = tk.Scrollbar(root, orient=tk.HORIZONTAL)
    xscrollbar_huffman.pack(side=tk.BOTTOM, fill=tk.X)

    #create huffman textbox
    text_huffman = tk.Text(root, height = 2, width = 50 ,wrap=tk.NONE, xscrollcommand=xscrollbar_huffman.set)
    text_huffman.pack()

    #associate scrollbar to huffman textbox
    xscrollbar_huffman.config(command=text_huffman.xview)

    #create scrollbar Y axis
    yscrollbar = tk.Scrollbar(root)

    #create textbox
    Textbox = tk.Text(root, height=20, width=50)

    #create scrollbar X axis
    xscrollbar = tk.Scrollbar(root, orient=tk.HORIZONTAL)
    xscrollbar.pack(side=tk.BOTTOM, fill=tk.X)
    xscrollbar.config(command=Textbox.xview)

    yscrollbar.pack(side=tk.LEFT, fill=tk.X)
    Textbox.pack(side=tk.LEFT, fill=tk.X)

    #associate scrollbar X and Y axis to textbox
    yscrollbar.config(command=Textbox.yview)
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
    Textbox.config(state=tk.DISABLED)
    text_seq.config(state=tk.DISABLED)
    text_huffman.config(state=tk.DISABLED)
    next_button.config(state=tk.DISABLED)
    result_button.config(state=tk.DISABLED)
    file_opener.config(state=tk.DISABLED)
    savefile.config(state=tk.DISABLED)
    clear_fields.config(state=tk.DISABLED)

    #loops the main frame (refresh)
    root.mainloop()

#if the file is called
if __name__ == "__main__" :

    #launch the frame
    main_BWT_huffman()
