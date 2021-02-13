#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os #REMOVE WHEN YOU LL WORK ON GUI

def combinations_recurs(sequence, combinations):

    if len(combinations) < 2:
        len_seq = len(sequence) - 1
        combinations.append(sequence)
        combinations.append(sequence[len_seq] + sequence[:len_seq])

    while len(sequence) != len(combinations):
        process = sequence.split("$")

        prefix = process[0]
        suffix = process[1]

        if len(suffix) == 0:
            sequence = prefix[-1]+"$"+prefix[0:len(prefix)-1]

            combinations.append(sequence)
            combinations_recurs(sequence, combinations)

        elif len(suffix) >= 1 and len(prefix) >= 1:

            sequence = suffix[-1]+prefix[:]+"$"+suffix[:len(suffix)-1]

            combinations.append(sequence)
            combinations_recurs(sequence, combinations)

        return combinations

def BWT(file):
    """
    Arguments: Takes a nucleotide file
    Description: Do a Burrows Weeler Compression/Transformation
    Returns: A string with the compressed sequence
    """

    document = open(file, "r") #Open the file containing sequence

    raw_sequence = document.readlines()
    raw_sequence.append("$")
    sequence = ''.join(raw_sequence)
    combinations = []
    combinations_recurs(sequence, combinations)

    sort_combinations = sorted(combinations)

    result = ""
    for elem in sort_combinations:
        result += elem[-1]
    return result

def BWT_decypher(compressed_BWT, combinations = None):

    if combinations is None:
        combinations = []

    if len(combinations) < len(compressed_BWT):
        for elem in compressed_BWT:

            combinations.append([elem])

        BWT_decypher(compressed_BWT,sorted(combinations))

    else:

        for attempts, element in zip(combinations, compressed_BWT):
            attempts.insert(0, element)

        if len(combinations[-1]) != len(compressed_BWT):

            BWT_decypher(compressed_BWT,sorted(combinations))


    final_comb = sorted(combinations)

    for attempts in final_comb:
        if attempts.index("$") == len(compressed_BWT)-1:

            return(''.join(attempts[:len(compressed_BWT)-1]))












os.chdir("/Users/mirandolaleonardo/github/Algo_project")#REMOVE WHEN YOU LL WORK ON GUI
print(BWT("test.txt"))
print(BWT_decypher(BWT("test.txt")))
