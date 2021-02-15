#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os #REMOVE WHEN YOU LL WORK ON GUI

def combinations_recurs(sequence, combinations, verbose = None):
    """
    Arguments: Nucleotide sequence, list of all the possible combinations

    Returns: A list with all the final possible combinations
    """
    #do the first 2 combinations
    if len(combinations) < 2:
        len_seq = len(sequence) - 1

        #the actual combination
        combinations.append(sequence)

        # The opposite combination
        combinations.append(sequence[len_seq] + sequence[:len_seq])

    #while the length of the combination inside the list hasn't reached the size
    #of the sequence length
    while len(sequence) != len(combinations):

        #split from the $ sign
        process = sequence.split("$")

        #prefix will be before the $
        prefix = process[0]

        #suffix will be after the $
        suffix = process[1]

        #if the suffix has nothing
        if len(suffix) == 0:

            #work on the prefix only
            sequence = prefix[-1]+"$"+prefix[0:len(prefix)-1]

            #store the result
            combinations.append(sequence)

            #recursion
            combinations_recurs(sequence, combinations)

        #if suffix and prefix length are greater than 0
        elif len(suffix) >= 1 and len(prefix) >= 1:

            #work with prefix and suffix
            sequence = suffix[-1]+prefix[:]+"$"+suffix[:len(suffix)-1]

            #append results to combination
            combinations.append(sequence)

            #recursion
            combinations_recurs(sequence, combinations)

        #return a list of all the combinations
        return combinations

def BWT(file, verbose = None):
    """
    Arguments: Takes a nucleotide file
    Description: Do a Burrows Weeler Compression/Transformation
    Returns: A string with the compressed sequence
    """

    #Open the file containing sequence
    document = open(file, "r")

    #read lines
    raw_sequence = document.readlines()

    #add $ at the end of the line
    raw_sequence.append("$")

    #transform list to string
    sequence = ''.join(raw_sequence)

    #initialise empty list
    combinations = []

    #send the sequence with $ and empty combination list to get all the combinations
    combinations_recurs(sequence, combinations)

    #sort the combinations by alphabetical order
    sort_combinations = sorted(combinations)

    #initialise empty string
    result = ""

    #iter through sorted sort_combinations
    for elem in sort_combinations:

        #add up only the last elements of each list
        result += elem[-1]

    #return the compressed BWT string
    return result

def BWT_decypher(compressed_BWT, combinations = None, verbose = None):
    """
    Arguments: The compressed BWT nucleotide sequence, doesn't need a second
                argument because it will do it automatically during the recursion

    Returns: The original sequence as a string
    """

    #if combination hasn't been given as argument
    if combinations is None:

        #initialise combination list empty
        combinations = []

    #if the length of combinations list isn't as long as the BWT sequence
    if len(combinations) < len(compressed_BWT):

        #for each elements in the BWT string sequence
        for elem in compressed_BWT:

            #append the letter and initialise it with list
            combinations.append([elem])

        #recursion with sorted combinations list
        BWT_decypher(compressed_BWT,sorted(combinations))

    #if the lengths match
    else:

        #cycle in both combinations list and compressed_BWT string
        for attempts, element in zip(combinations, compressed_BWT):

            #insert at each pace, the next caracter with the next list(attempts)
            attempts.insert(0, element)

        #if the length of the last attempt in combinations hasn't reached the
        #length of compressed_BWT string
        if len(combinations[-1]) != len(compressed_BWT):

            #recursion with sorted combinations
            BWT_decypher(compressed_BWT,sorted(combinations))

    #the final combination is combinations sorted
    final_comb = sorted(combinations)

    #iter through final combinations
    for attempts in final_comb:

        #if the $ sign is in the last position
        if attempts.index("$") == len(compressed_BWT)-1:

            #transform the selected attempt into a string and remove the $ at
            # end
            return(''.join(attempts[:len(compressed_BWT)-1]))


"""os.chdir("/Users/mirandolaleonardo/github/Algo_project")#REMOVE WHEN YOU LL WORK ON GUI
print(BWT("test.txt"))
print(BWT_decypher(BWT("test.txt")))"""
