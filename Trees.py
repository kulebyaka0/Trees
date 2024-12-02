import matplotlib.pyplot as plt
import numpy as np
import random
import math
from collections import deque

#///////////////////////Binary Search Tree//////////////////////////////////////
class Node:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None
 
 
class Tree:
    def __init__(self):
        self.root = None
 
    #метод вставки значения в бинарное дерево
    def find(self, node, parent, value):
        if node is None:
            return None, parent, False
 
        if value == node.data:
            return node, parent, True
 
        if value < node.data:
            if node.left:
                return self.find(node.left, node, value)
 
        if value > node.data:
            if node.right:
                return self.find(node.right, node, value)
 
        return node, parent, False
 
 
    def append(self, obj):
        if self.root is None:
            self.root = obj
            return obj
 
        s, p, fl_find = self.find(self.root, None, obj.data)
 
        if not fl_find and s:
            if obj.data < s.data:
                s.left = obj
            else:
                s.right = obj
 
        return obj
 
    #обход дерева в глубину
    def show_tree(self, node):
        if node is None:
            return
 
        self.show_tree(node.right)
        print(node.data)
        self.show_tree(node.left)
 
#удаление элемента
    def delete_leaf(self, s, p):
        if p.left == s:
            p.left = None
        elif p.right == s:
            p.right = None
 
    def delete_one_child(self, s, p):
        if p.left == s:
            if s.left is None:
                p.left = s.right
            elif s.right is None:
                p.left = s.left
        elif p.right == s:
            if s.left is None:
                p.right = s.right
            elif s.right is None:
                p.right = s.left
    
    def find_min(self, node, parent):
        if node.left:
            return self.find_min(node.left, node)
 
        return node, parent

    def delete_node(self, data):
        s, p, fl_find = self.find(self.root, None, data) #ищем вершину, которую нужно удалить
 
        if not fl_find:
            return None
 
        if s.left is None and s.right is None:
            self.delete_leaf(s, p)
        elif s.left is None or s.right is None:
            self.delete_one_child(s, p)
        else:
            sr, pr = self.find_min(s.right, s)
            s.data = sr.data
            self.delete_one_child(sr, pr)
    
    #высота дерева
    def get_height(self, node):
        if node is None: 
            return 0
        left_height = self.get_height(node.left)
        right_height = self.get_height(node.right)
        return 1 + max(left_height, right_height)

    def tree_height(self):
        return self.get_height(self.root)        

    def bfs_traversal(self):
        if self.root is None:
            return

        queue = deque([self.root])  
        while queue:
            current_node = queue.popleft()  
            print(current_node.data, end=" ")  

            if current_node.left:
                queue.append(current_node.left)  
            if current_node.right:
                queue.append(current_node.right) 

    def preorder_traversal(self, node):
        if node:
            print(node.data, end=" ")
            self.preorder_traversal(node.left)
            self.preorder_traversal(node.right)
            
    def inorder_traversal(self, node):
        if node:
            self.inorder_traversal(node.left)
            print(node.data, end=" ")
            self.inorder_traversal(node.right)

    def postorder_traversal(self, node):
        if node:
            self.postorder_traversal(node.left)
            self.postorder_traversal(node.right)
            print(node.data, end=" ")


#///////////////////////AVL-Tree/////////////////////////////////////////////         
class Node:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 1


class AVLTree:
    def __init__(self):
        self.root = None

    def _height(self, node):
        if node is None:
            return 0
        return node.height

    def _update_height(self, node):
        node.height = 1 + max(self._height(node.left), self._height(node.right))

    def _balance_factor(self, node):
        if node is None:
            return 0
        return self._height(node.left) - self._height(node.right)

    def _rotate_right(self, node):
        left_child = node.left
        right_grandchild = left_child.right
        left_child.right = node
        node.left = right_grandchild
        self._update_height(node)
        self._update_height(left_child)
        return left_child

    def _rotate_left(self, node):
        right_child = node.right
        left_grandchild = right_child.left
        right_child.left = node
        node.right = left_grandchild
        self._update_height(node)
        self._update_height(right_child)
        return right_child

    def _rebalance(self, node):
        balance = self._balance_factor(node)
        if balance > 1:
            if self._balance_factor(node.left) < 0:
                node.left = self._rotate_left(node.left)
            return self._rotate_right(node)
        elif balance < -1:
            if self._balance_factor(node.right) > 0:
                node.right = self._rotate_right(node.right)
            return self._rotate_left(node)
        return node

    def insert(self, key):
        self.root = self._insert_recursive(self.root, key)

    def _insert_recursive(self, node, key):
        if node is None:
            return Node(key)
        if key < node.key:
            node.left = self._insert_recursive(node.left, key)
        else:
            node.right = self._insert_recursive(node.right, key)
        self._update_height(node)
        return self._rebalance(node)

    def search(self, key):
        return self._search_recursive(self.root, key)

    def _search_recursive(self, node, key):
        if node is None or node.key == key:
            return node
        if key < node.key:
            return self._search_recursive(node.left, key)
        return self._search_recursive(node.right, key)

    def delete(self, key):
        if self.root is None:
            return

        self.root = self._delete_recursive(self.root, key)

    def _delete_recursive(self, node, key):
        if node is None:
            return node

        if key < node.key:
            node.left = self._delete_recursive(node.left, key)
        elif key > node.key:
            node.right = self._delete_recursive(node.right, key)
        else:
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left
            else:
                min_node = self._minimum(node.right)
                node.key = min_node.key
                node.right = self._delete_recursive(node.right, min_node.key)

        self._update_height(node)
        return self._rebalance(node)

    def _minimum(self, node):
        while node.left:
            node = node.left
        return node

    def height(self):
        return self._height(self.root)

    def bfs_traversal(self):
        if self.root is None:
            return

        queue = deque([self.root])  
        while queue:
            current_node = queue.popleft()  
            print(current_node.key, end=" ")  

            if current_node.left:
                queue.append(current_node.left)  
            if current_node.right:
                queue.append(current_node.right) 

    def preorder_traversal(self, node):
        if node:
            print(node.key, end=" ")
            self.preorder_traversal(node.left)
            self.preorder_traversal(node.right)
            
    def inorder_traversal(self, node):
        if node:
            self.inorder_traversal(node.left)
            print(node.key, end=" ")
            self.inorder_traversal(node.right)

    def postorder_traversal(self, node):
        if node:
            self.postorder_traversal(node.left)
            self.postorder_traversal(node.right)
            print(node.key, end=" ")
#/////////////RB-Tree/////////////////////////////////////

class RBNode:
        # cnostructor
    def __init__(self, value, color='red'):
        self.value = value
        self.color = color
        self.left = None
        self.right = None
        self.parent = None

    # function to get the grandparent of node
    def grandparent(self):
        if self.parent is None:
            return None
        return self.parent.parent

    # function to get the sibling of node
    def sibling(self):
        if self.parent is None:
            return None
        if self == self.parent.left:
            return self.parent.right
        return self.parent.left

    # function to get the uncle of node
    def uncle(self):
        if self.parent is None:
            return None
        return self.parent.sibling()

# function to implement Red Black Tree


class RedBlackTree:
        # constructor to initialize the RB tree
    def __init__(self):
        self.root = None

    # function to search a value in RB Tree
    def search(self, value):
        curr_node = self.root
        while curr_node is not None:
            if value == curr_node.value:
                return curr_node
            elif value < curr_node.value:
                curr_node = curr_node.left
            else:
                curr_node = curr_node.right
        return None

    # function to insert a node in RB Tree, similar to BST insertion
    def insert(self, value):
        # Regular insertion
        new_node = RBNode(value)
        if self.root is None:
            self.root = new_node
        else:
            curr_node = self.root
            while True:
                if value < curr_node.value:
                    if curr_node.left is None:
                        curr_node.left = new_node
                        new_node.parent = curr_node
                        break
                    else:
                        curr_node = curr_node.left
                else:
                    if curr_node.right is None:
                        curr_node.right = new_node
                        new_node.parent = curr_node
                        break
                    else:
                        curr_node = curr_node.right
        self.insert_fix(new_node)

    # Function to fix RB tree properties after insertion
    def insert_fix(self, new_node):
        while new_node.parent and new_node.parent.color == 'red':
            if new_node.parent == new_node.grandparent().left:
                uncle = new_node.uncle()
                if uncle and uncle.color == 'red':
                    new_node.parent.color = 'black'
                    uncle.color = 'black'
                    new_node.grandparent().color = 'red'
                    new_node = new_node.grandparent()
                else:
                    if new_node == new_node.parent.right:
                        new_node = new_node.parent
                        self.rotate_left(new_node)
                    new_node.parent.color = 'black'
                    new_node.grandparent().color = 'red'
                    self.rotate_right(new_node.grandparent())
            else:
                uncle = new_node.uncle()
                if uncle and uncle.color == 'red':
                    new_node.parent.color = 'black'
                    uncle.color = 'black'
                    new_node.grandparent().color = 'red'
                    new_node = new_node.grandparent()
                else:
                    if new_node == new_node.parent.left:
                        new_node = new_node.parent
                        self.rotate_right(new_node)
                    new_node.parent.color = 'black'
                    new_node.grandparent().color = 'red'
                    self.rotate_left(new_node.grandparent())
        self.root.color = 'black'

    # function to delete a value from RB Tree
    def delete(self, value):
        node_to_remove = self.search(value)

        if node_to_remove is None:
            return

        if node_to_remove.left is None or node_to_remove.right is None:
            self._replace_node(
                node_to_remove, node_to_remove.left or node_to_remove.right)
        else:
            successor = self._find_min(node_to_remove.right)
            node_to_remove.value = successor.value
            self._replace_node(successor, successor.right)

        self.delete_fix(node_to_remove)

    # function to fix RB Tree properties after deletion
    def delete_fix(self, x):
        while x != self.root and x.color == 'black':
            if x == x.parent.left:
                sibling = x.sibling()
                if sibling.color == 'red':
                    sibling.color = 'black'
                    x.parent.color = 'red'
                    self.rotate_left(x.parent)
                    sibling = x.sibling()
                if (sibling.left is None or sibling.left.color == 'black') and (sibling.right is None or sibling.right.color == 'black'):
                    sibling.color = 'red'
                    x = x.parent
                else:
                    if sibling.right is None or sibling.right.color == 'black':
                        sibling.left.color = 'black'
                        sibling.color = 'red'
                        self.rotate_right(sibling)
                        sibling = x.sibling()
                    sibling.color = x.parent.color
                    x.parent.color = 'black'
                    if sibling.right:
                        sibling.right.color = 'black'
                    self.rotate_left(x.parent)
                    x = self.root
            else:
                sibling = x.sibling()
                if sibling.color == 'red':
                    sibling.color = 'black'
                    x.parent.color = 'red'
                    self.rotate_right(x.parent)
                    sibling = x.sibling()
                if (sibling.left is None or sibling.left.color == 'black') and (sibling.right is None or sibling.right.color == 'black'):
                    sibling.color = 'red'
                    x = x.parent
                else:
                    if sibling.left is None or sibling.left.color == 'black':
                        sibling.right.color = 'black'
                        sibling.color = 'red'
                        self.rotate_left(sibling)
                        sibling = x.sibling()
                    sibling.color = x.parent.color
                    x.parent.color = 'black'
                    if sibling.left:
                        sibling.left.color = 'black'
                    self.rotate_right(x.parent)
                    x = self.root
        x.color = 'black'

    # Function for left rotation of RB Tree
    def rotate_left(self, node):
        right_child = node.right
        node.right = right_child.left

        if right_child.left is not None:
            right_child.left.parent = node

        right_child.parent = node.parent

        if node.parent is None:
            self.root = right_child
        elif node == node.parent.left:
            node.parent.left = right_child
        else:
            node.parent.right = right_child

        right_child.left = node
        node.parent = right_child

    # function for right rotation of RB Tree
    def rotate_right(self, node):
        left_child = node.left
        node.left = left_child.right

        if left_child.right is not None:
            left_child.right.parent = node

        left_child.parent = node.parent

        if node.parent is None:
            self.root = left_child
        elif node == node.parent.right:
            node.parent.right = left_child
        else:
            node.parent.left = left_child

        left_child.right = node
        node.parent = left_child

    # function to replace an old node with a new node
    def _replace_node(self, old_node, new_node):
        if old_node.parent is None:
            self.root = new_node
        else:
            if old_node == old_node.parent.left:
                old_node.parent.left = new_node
            else:
                old_node.parent.right = new_node
        if new_node is not None:
            new_node.parent = old_node.parent

    def get_height(self, node):
        if node is None: 
            return 0
        left_height = self.get_height(node.left)
        right_height = self.get_height(node.right)
        return 1 + max(left_height, right_height)

    def tree_height(self):
        return self.get_height(self.root)    

    # function to find node with minimum value in a subtree
    def _find_min(self, node):
        while node.left is not None:
            node = node.left
        return node

    def bfs_traversal(self):
        if self.root is None:
            return

        queue = deque([self.root])  
        while queue:
            current_node = queue.popleft()  
            print(current_node.value, end=" ")  

            if current_node.left:
                queue.append(current_node.left)  
            if current_node.right:
                queue.append(current_node.right) 

    def preorder_traversal(self, node):
        if node:
            print(node.value, end=" ")
            self.preorder_traversal(node.left)
            self.preorder_traversal(node.right)
            
    def inorder_traversal(self, node):
        if node:
            self.inorder_traversal(node.left)
            print(node.value, end=" ")
            self.inorder_traversal(node.right)

    def postorder_traversal(self, node):
        if node:
            self.postorder_traversal(node.left)
            self.postorder_traversal(node.right)
            print(node.value, end=" ")

