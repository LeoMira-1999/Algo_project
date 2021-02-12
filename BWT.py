#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

def combinations_recurs(sequence, combinations):
    print(len(combinations))
    if len(combinations) < 2:
        len_seq = len(sequence) - 1
        combinations.append(sequence)
        combinations.append(sequence[len_seq] + sequence[:len_seq])
        print(combinations)
    while len(sequence) != len(combinations):
        process = sequence.split("$")

        prefix = process[0]
        suffix = process[1]

        if len(suffix) == 0:
            sequence = prefix[-1]+"$"+prefix[0:len(prefix)-1]
            print(sequence)
            combinations.append(sequence)
            combinations_recurs(sequence, combinations)

        elif len(suffix) >= 1 and len(prefix) >= 1:

            sequence = suffix[-1]+prefix[:]+"$"+suffix[:len(suffix)-1]
            print(sequence)
            combinations.append(sequence)
            combinations_recurs(sequence, combinations)




        return combinations

def BWT(file):
    """
    Arguments: Takes a nucleotide file
    Description: Do a Burrows Weeler Compression/Transformation
    Returns: A file with the compressed sequence
    """

    document = open(file, "r") #Open the file containing sequence

    raw_sequence = document.readlines()
    raw_sequence.append("$")
    sequence = ''.join(raw_sequence)
    combinations = []
    return combinations_recurs(sequence, combinations)



print(os.chdir("/Users/mirandolaleonardo/github/Algo_project"))
print(BWT("test.txt"))
