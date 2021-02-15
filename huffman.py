#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class Node:
    """
    Nodes for binary tree usage
    """

    def __init__(self, parent_node):
        self.parent_node = parent_node
        self.left = None
        self.right = None

    def __str__(self): #permet la lecture en profondeur
        if self.is_leaf():
            return str(self.parent_node)

        return "["+str(self.left) +":"+ str(self.right) + "]" + str(self.parent_node)

    def print_tree_node(self):
        """
        Print a list like view of the BT
        """
        if self.left:
            self.left.print_tree_node()
        print(self.parent_node)

        if self.right:
            self.right.print_tree_node()

    def is_leaf(self):
        """
        return True or False if self is a leaf or not
        """
        return self.left is None and self.right is None

    def delete_node(self, target_node):

        if target_node < self.parent_node:
            self.left.delete_node(target_node)
        elif target_node > self.parent_node:
            self.right.delete_node(target_node)
        elif target_node == self.parent_node:
            self.parent_node = None

    def add_node(self, node):
        """
        Add a int node arranged by size of number
        """
        if self.parent_node:
            if node < self.parent_node:
                if self.left is None:
                    self.left = Node(node)
                else:
                    self.left.add_node(node)
            elif node > self.parent_node:
                if self.right is None:
                    self.right = Node(node)
                else:
                    self.right.add_node(node)
        else:
            self.parent_node = node

class Tree:
    """
    Tree uses Nodes from binary tree to print and show it
    """

    def __init__(self, node):
        self.node = node

    def __repr__(self):
        pass

    def transversal_deep(self): #permet de faire une vue en profondeur avec __str__ de Node
        """
        Print tree
        """
        print(self.node)


def freq_counter(seq):

    dico = {}

    for nucl in seq:
        if nucl not in dico:
            dico[nucl] = 1
        else:
            dico[nucl] += 1
    return dico
