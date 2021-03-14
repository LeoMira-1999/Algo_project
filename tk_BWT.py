#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# from BWT import the encryption and decryption
from BWT import BWT, BWT_decypher

#import filedialog from tkinter to open and save files
from tkinter import filedialog

#import messagebox from tkinter allows pop-ups
from tkinter import messagebox

#import tkinter and renamed it as tk
import tkinter as tk

#import stat from os to find size of file
from os import stat

def main_BWT():
    """
    Description: Function that when called creates the interface for BWT
    """

    # Allows the usage of i counter, combination_decrypt by other fonctions inside main_BWT
    global i, combination_decrypt

    def clear():
        """
        Description: Allows the user and some functions to automatically clear every textbox
        """

        #Calls the combination_decrypt and i variables and allows them to be modified globally
        global combination_decrypt, i

        #reset both variables
        combination_decrypt = None
        i = 1

        #Allow the corresponding textboxes to be modified
        text_bwt.config(state=tk.NORMAL)
        Textbox.config(state=tk.NORMAL)
        text_seq.config(state=tk.NORMAL)

        #Delete all content of corresponding textboxes
        Textbox.delete("1.0", tk.END)
        text_seq.delete("1.0", tk.END)
        text_bwt.delete("1.0", tk.END)

        #enable button file opener
        file_opener.config(state=tk.NORMAL)

        #Allow the corresponding textboxes to be modified
        text_bwt.config(state=tk.DISABLED)
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

        #shows GUI of location and name to save the file
        file = filedialog.asksaveasfilename()

        #if the user selected either encryption or decryption, saves appropriate file
        if value.get() == 1:
            with open(file+".txt", "w") as f:
                f.write(result)
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

                #warn user
                messagebox.showerror(title="WRONG FILE FORMAT", message="Please select a .txt file format")

                #retry
                return openfile()

        #open the file to have a look
        with open(file) as document:

            #if there is a $ in the file
            if "$" in document.read():

                # and he selected encryption then divert him to decryption automatically
                if value.get() == 1:

                    #change to decryption
                    value.set(2)

                    #warn user
                    messagebox.showwarning(title="SWITCHING TO DECRYTPION", message="SWITCHING TO DECRYTPION")
                else:
                    pass

            #if there is no $ in the file
            elif "$" not in document.read():

                #and he selected decryption
                if value.get() == 2:

                    #change to encryption
                    value.set(1)

                    #warn user
                    messagebox.showwarning(title="SWITCHING TO ENCRYTPION", message="SWITCHING TO ENCRYTPION")
                else:
                    pass

        #enable appropriate buttons
        next_button.config(state=tk.NORMAL)
        result_button.config(state=tk.NORMAL)
        clear_fields.config(state=tk.NORMAL)

        #if he selected encryption
        if value.get() == 1:

            #enable sequence textbox
            text_seq.config(state=tk.NORMAL)

            #globalise the variable that will be attributed to BWT encryption results
            global result, sorted_combinations, combinations

            #initiate BWT
            result, sorted_combinations, combinations = BWT(file)

            #open the file
            with open(file, "r") as file:

                #retreive the sequence
                sequence = ''.join(file.readlines())

                #insert sequence in sequence textbox
                text_seq.insert(tk.END, sequence)

            #disable sequence texbox
            text_seq.config(state=tk.DISABLED)

        #if he selected decryption
        else:

            #open the file
            with open(file, "r") as file:

                #globalise the variables that will be attributed to the BWT decypher
                global result_decrypt, sequence_encrypted

                #enable editing of BWT textbox
                text_bwt.config(state=tk.NORMAL)

                #retreive encrypted sequence
                sequence_encrypted = ''.join(file.readlines())

                #insert encrypted sequence
                text_bwt.insert(tk.END, sequence_encrypted)

                #initialise decryption
                result_decrypt= BWT_decypher(sequence_encrypted)

                #disable textbox BWT
                text_bwt.config(state=tk.DISABLED)

    def next():
        """
        Description: Allows the user to click next
        """

        #if he selected encryption
        if value.get() == 1:

            #globalise the i variable so that it can be modified and stored
            global i

            #enable the appropriate textboxes
            Textbox.config(state=tk.NORMAL)
            text_bwt.config(state=tk.NORMAL)

            #shows the user the different $ combinations in the sequence
            if i <= len(combinations):
                Textbox.insert(tk.END, combinations[i-1]+"\n")

            #once it has finished with all the $ combinations
            else:

                #introduce a separator
                Textbox.insert(tk.END, "\n"+"#"*len(combinations)+"\n\n")

                #show the BWT matrix that will be used to get the encrypted sequence
                for j in range (0, len(sorted_combinations),1):

                    Textbox.insert(tk.END, sorted_combinations[j]+"\n")

                #show the resutl
                text_bwt.insert(tk.END, result)

                #disable appropriate buttons and text fields
                text_bwt.config(state=tk.DISABLED)
                next_button.config(state=tk.DISABLED)
                result_button.config(state=tk.DISABLED)
                Textbox.config(state=tk.DISABLED)

                #enable appropriate buttons
                savefile.config(state=tk.NORMAL)
                clear_fields.config(state=tk.NORMAL)

            #increment counter
            i += 1

        #if he selected decryption
        else:

            #globalise combination_decrypt
            global combination_decrypt

            #enable texbox and delete everything inside
            Textbox.config(state=tk.NORMAL)
            Textbox.delete('1.0', tk.END)

            if combination_decrypt is None:

                #if it is the first run, then add every caracter in a separate list
                # which will be added to a list
                combination_decrypt = [[element] for element in sequence_encrypted]

            else:

                #cycle in the encrypted sequence and the decrypted combinations
                for caracter, attempts in zip(sequence_encrypted, combination_decrypt):

                    #for each attempt insert the attempts to the textbox
                    attempts.insert(0, caracter)

            #sort the decrypted combinations
            combination_decrypt = sorted(combination_decrypt)

            #show the final combinations
            for element in combination_decrypt:

                Textbox.insert(tk.END, "".join(element)+"\n")

            #if the length of the last combination is the same length as the encrypted sequence
            if len(combination_decrypt[-1]) == len(sequence_encrypted):

                #enable the sequence texbox
                text_seq.config(state=tk.NORMAL)

                #insert the sequence
                text_seq.insert(tk.END, result_decrypt)

                #disable appropriate buttons
                text_seq.config(state=tk.DISABLED)
                next_button.config(state=tk.DISABLED)
                result_button.config(state=tk.DISABLED)

                #enable appropriate buttons
                savefile.config(state=tk.NORMAL)
                clear_fields.config(state=tk.NORMAL)

            #disable texbox
            Textbox.config(state=tk.DISABLED)

    def result_button():
        """
        Description: Allows the user to click on the result button
        """

        #if he selected encryption
        if value.get() == 1:

            #enable BWT textbox
            text_bwt.config(state=tk.NORMAL)

            #insert the encrypted sequence
            text_bwt.insert(tk.END, result)

            #disable appropriate buttons
            text_bwt.config(state=tk.DISABLED)
            Textbox.config(state=tk.DISABLED)
            text_seq.config(state=tk.DISABLED)

        #if he selected decryption
        else:

            #enable sequence texbox
            text_seq.config(state=tk.NORMAL)

            #insert decrypted sequence
            text_seq.insert(tk.END, result_decrypt)

            #desable appropriate buttons
            text_seq.config(state=tk.DISABLED)
            Textbox.config(state=tk.DISABLED)
            text_seq.config(state=tk.DISABLED)

        #disable appropriate buttons
        next_button.config(state=tk.DISABLED)
        result_button.config(state=tk.DISABLED)

        #enable appropriate buttons
        savefile.config(state=tk.NORMAL)
        clear_fields.config(state=tk.NORMAL)

    #initialise frame
    root = tk.Tk()

    #give it a size
    root.geometry("600x500")

    #give it a color
    root.configure(bg="#F0F5F5")

    #initialise tkinter StringVar for sequence and BWT
    display_BWT = tk.StringVar()
    display_seq = tk.StringVar()

    #initialise value selector IntVar
    value = tk.IntVar()

    #set empty variable and counter
    combination_decrypt = None
    i = 1

    #create label to choose method and pack it
    tk.Label(root,
            text="""Choose a method:""",
            justify = tk.LEFT,
            padx = 20).pack()

    #create Radiobuttons for the user to select between encryption and decryption
    #with attributed values
    tk.Radiobutton(root,
                   text="Encrypt",
                   padx = 20,
                   variable=value,
                   value=1,
                   command = clear).pack(anchor=tk.W)

    tk.Radiobutton(root,
                   text="Decrypt",
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

    #create BWT label and pack it
    bwt_label = tk.Label(root, text="BWT:").pack()

    #create BWT X axis Scrollbar
    xscrollbar_bwt = tk.Scrollbar(root, orient=tk.HORIZONTAL)
    xscrollbar_bwt.pack(side=tk.BOTTOM, fill=tk.X)

    #create BWT textbox
    text_bwt = tk.Text(root, height = 1, width = 50 ,wrap=tk.NONE, xscrollcommand=xscrollbar_bwt.set)
    text_bwt.pack()

    #attach scrollbar to BWT texbox
    xscrollbar_bwt.config(command=text_bwt.xview)

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
    Textbox.config(state=tk.DISABLED)
    text_seq.config(state=tk.DISABLED)
    text_bwt.config(state=tk.DISABLED)
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
    main_BWT()
