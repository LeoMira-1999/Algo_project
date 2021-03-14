#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""import os"""

def frequence_counter(seq):
    """
    Arguments: Takes in a string sequence

    Description: Counts the repetition of each letter

    Returns: sorted dictionary with key = Letter, value = numbers of reps

    """

    # initialise empty Dictionary
    dico = {}

    # cycle in the sequence
    for elem in seq:

        # if the letter hasn't seen before then initialise it with 1
        if elem not in dico:

            dico[elem] = 1

        # otherwise increment by 1
        else:

            dico[elem] += 1

    # return a sorted dictionary
    return dict(sorted(dico.items(), key=lambda item: item[1]))


def huffman_binary_tree(freq_counter):
    """
    Arguments: takes a dictionnary of frequence of each letters

    Description: Transform the dict frequence into a sorted

    Returns: A sorted dictionary key  = letter, value = binary number
    """

    #initialise tree list as a list containing for each weight, the letter and
    # an empty string both inside another list
    tree = [[weight, [nucl, ""]] for nucl, weight in freq_counter.items()]

    #until the tree hasn't reach a size of 1
    while len(tree) >= 2:

        #take the lowest weight
        low_node = min(tree)

        #remove it from the tree
        tree.pop(tree.index(min(tree)))

        #repeat the process another time to remove the second lowest value here
        high_node = min(tree)

        #remove it from the tree
        tree.pop(tree.index(min(tree)))

        #add 0 (lowest) or 1 (second lowest) to the appropriate letters in front
        # of the string
        for pair in low_node[1:]:#[nucl,""]
            pair[1] = '0' + pair[1]
        for pair in high_node[1:]:
            pair[1] = '1' + pair[1]

        # add to the tree a list containing the cumulated weights and with
        # each letter + binary code
        tree.append([low_node[0] + high_node[0]] + low_node[1:] + high_node[1:])

    #sort the tree by their binary number
    tree_list = sorted(tree[0][1:])

    #create two empty lists
    first_list = []
    second_list = []

    #cycle in the tree list
    for value in tree_list:

        #append each value to the lists
        first_list.append(value[0])
        second_list.append(value[1])

    #create dictionary based on the two lists, key = first list, value = second list
    res_code = dict(zip(first_list, second_list))

    # sort the dictionary
    return dict(sorted(res_code.items(), key=lambda item: item[1]))

def zero_reps_start_finder(binary_seq):
    """
    Arguments: takes the binary sequence

    Description: Finds if there are any zeros at the beginning of the binary sequence

    Returns: a string with the zeros found or empty if none
    """

    # initialise empty string
    reps = ""

    #if the start of the sequence starts with a 0
    if binary_seq[0] == "0":

        #split the sequence by all its ones
        binary_seq = binary_seq.split("1")

        #reassign the zeros found to reps
        reps = binary_seq[0]

    #return the string with what it has found or not
    return reps

def huffman_encoding(code, seq):
    """
    Arguments: takes the binary tree and sequence

    Description: Transforms the sequence into a binary sequence using the binary
                tree and transforms the binary sequence into a caracter of 16 bits

    Returns: A list of binary caracter, a list of the associated unsigned zeros
            to each binary caracter and the binary sequence
    """

    #Initialise empty string to store the binary sequence
    encoded_res = ""

    #cycle in the sequence
    for nucl in seq:

        #add to the binary sequence the corresponding binary combination for the nucleotide
        encoded_res += code[nucl]

    #initialise 2 lists (store caracter and store left over unsigned zeros)
    # and a string
    bits_caracter = []
    bits_leftover = []
    bits_length = ""

    # if the length of the binary sequence has a remainder after a division by 16
    if len(encoded_res) % 16 != 0:

        #store the difference
        difference = len(encoded_res) % 16

        #sliding a window of length 16 over the binary sequence
        for i in range (0, len(encoded_res) - difference, 16):

            #retreive a string of the zeros that might have at the beginning
            zero_start_counter = zero_reps_start_finder(encoded_res[i:i+16])

            #append to the caracter list the appropriate caracter associated to the binary window
            bits_caracter.append(chr(int(encoded_res[i:i+16], 2)))

            #append to the left over zeros list the corresponding zeros that were
            # present (or not, in this case empty string) with the binary window
            bits_leftover.append(zero_start_counter) #lost because of unsagnied caracter

        #finally add an extra to the caracter list which will be associated with
        # the leftover of the sequence division by 16
        bits_caracter.append("extra")
        bits_leftover.append(encoded_res[-difference:])

    #if no leftovers after the division by 16
    else:

        #cycle in the binary sequence
        for binary in encoded_res:

            #append each caracter
            bits_length += binary

            #when bits_length reaches a length of 16
            if len(bits_length) == 16:

                #retreive a string of the zeros that might have at the beginning
                zero_start_counter = zero_reps_start_finder(bits_length)

                #append to the caracter list the appropriate caracter associated to the binary window
                bits_caracter.append(chr(int(bits_length, 2)))

                #append to the left over zeros list the corresponding zeros that were
                # present (or not, in this case empty string) with the binary window
                bits_leftover.append(zero_start_counter) #lost because of unsagnied caracter

                #reset bits_length
                bits_length = ""

    #return the results as listed previously above
    return bits_caracter, bits_leftover, encoded_res

def decode_bits(bits_caracter, bits_leftover):
    """
    Arguments: takes the bits caracter list and bits_leftover list from huffman_encoding

    Description: Transform the caracters in binary sequence

    Returns: a binary sequence
    """

    #store binary sequence string
    binary_code = ""

    #cycle in both input lists
    for caractere, binary in zip(bits_caracter, bits_leftover):

        #if the caracter found isn't "extra"
        if caractere != "extra":
            
            #append the binary sequence (zeros) with the binary form of the caracter
            binary_code += binary + format(ord(caractere), 'b')

        #if "extra" is found
        else:

            #append the binary sequence of extra
            binary_code += binary

    #return the binary sequence
    return binary_code

def huffman_decoding(binary_seq, binary_tree):
    """
    Arguments: takes the binary sequence and the binary tree

    Description: retreive the original sequence

    Returns: The original sequence
    """
    # empty dictionary used to reverse the binary tree dictionary
    binary_tree_reverse = {}

    #for each caracter and binary code in the binary tree dictionary
    for nucl, binary in binary_tree.items():

        #swap binary and caracter when adding it to the reverse dictionary
        binary_tree_reverse[binary] = nucl

    #store the original sequence
    result = ""

    #temporary storage
    temp = ""

    #cycle in the binary sequence
    for nucl in binary_seq:

        #append each binary to the temporary string
        temp += nucl

        #if the temporary string is found in the binary reversed tree
        if temp in binary_tree_reverse:

            #add to the result the corresponding caracter from the tree
            result += binary_tree_reverse[temp]

            #reset temporary
            temp = ""

    #return the original sequence
    return result

###############################

"""os.chdir("/Users/mirandolaleonardo/Desktop")

with open("Test.txt") as file:
    sequence = ''.join(file.readlines())
    print(sequence)

    freq_counter = frequence_counter(sequence)
    print(freq_counter)

    code = huffman_binary_tree(freq_counter)
    print(code)

    binary_caracter, binary_leftover, simple_bin_code = huffman_encoding(code, sequence)
    print(binary_caracter, binary_leftover, simple_bin_code)

    bits = decode_bits(binary_caracter, binary_leftover)

    decoded_seq = huffman_decoding(bits, code)"""
