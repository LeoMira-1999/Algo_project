#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from heapq import heapify, heappop, heappush

def freq_counter(seq):

    dico = {}

    for nucl in seq:
        if nucl not in dico:
            dico[nucl] = 1
        else:
            dico[nucl] += 1
    return dict(sorted(dico.items(), key=lambda item: item[1]))

def huffman_tree(occurrences):

    # Tree construction with nucl as leafs
    tree = [(occ, nucl) for (nucl, occ) in occurrences.items()]
    print(tree)
    heapify(tree)

    # Creating the tree with node values 0 or 1
    while len(tree) > 1:

        # node with smallest weight
        occ1, node1 = heappop(tree)
        print(type(occ1), node1)
        # node of second smallest weight
        occ2, node2 = heappop(tree)

        # Push (add) onto the tree occ1 + occ2 and give 0 or 1 to the nodes
        heappush(tree, (occ1 + occ2, {0: node1, 1: node2}))

    return heappop(tree)[1]


def binary_code(dico):

    for binary, node 

print(huffman_tree(freq_counter("ATCGCGAGCGAGAATCGCTAGCTTATCTAGCAGGCGATCGGGATTCGAGGCTAGCGTAGCGGCTGAGCTAGCGAT")))
