#Program to compaer performance of skip lists vs balanced trees(AVL) vs unbalanced trees(bst)

import sys
import time
import random

#------------------------AVL-------------------------- 
#avl tree node
class TreeNode(object):
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 1

class AVLTree(object):
#insert node method
    def insert_node(self, root, key):
#empty tree
        if not root:
            return TreeNode(key)
        elif key < root.key:
            root.left = self.insert_node(root.left, key)
        else:
            root.right = self.insert_node(root.right, key)
#update heigth of nodes after inserting
        root.height = 1 + max(self.getHeight(root.left),
                              self.getHeight(root.right))

# Update the balance factor and balance the tree
        bfactor = self.getBalance(root)       
        if bfactor > 1:
#left imbalance
            if key < root.left.key:
                return self.rightRotate(root)
            else: 
#left-right imbalance 
                root.left = self.leftRotate(root.left)
                return self.rightRotate(root)

        if bfactor < -1:
#right imbalance
            if key > root.right.key:
                return self.leftRotate(root)
            else:
#right-left imbalance
                root.right = self.rightRotate(root.right)
                return self.leftRotate(root)

        return root

#delete node method 
    def delete_node(self, root, key):
#tree is empty
        if not root:
            return root
        elif key < root.key:
            root.left = self.delete_node(root.left, key)
        elif key > root.key:
            root.right = self.delete_node(root.right, key)
        else:
            if root.left is None:
                temp = root.right
                root = None
                return temp
            elif root.right is None:
                temp = root.left
                root = None
                return temp
            temp = self.getMinValueNode(root.right)
            root.key = temp.key
            root.right = self.delete_node(root.right,
                                          temp.key)
        if root is None:
            return root

#update node height after deleting
        root.height = 1 + max(self.getHeight(root.left),
                              self.getHeight(root.right))
#update balance fator of nodes
        bfactor = self.getBalance(root)

#check for imbalance and rotate to balance
        if bfactor > 1:
            if self.getBalance(root.left) >= 0:
                return self.rightRotate(root)
            else:
                root.left = self.leftRotate(root.left)
                return self.rightRotate(root)
        if bfactor < -1:
            if self.getBalance(root.right) <= 0:
                return self.leftRotate(root)
            else:
                root.right = self.rightRotate(root.right)
                return self.leftRotate(root)
        return root

#left rotate method
    def leftRotate(self, z):
        y = z.right
        T2 = y.left
        y.left = z
        z.right = T2
        z.height = 1 + max(self.getHeight(z.left),
                           self.getHeight(z.right))
        y.height = 1 + max(self.getHeight(y.left),
                           self.getHeight(y.right))
        return y

#right rotate method
    def rightRotate(self, z):
        y = z.left
        T3 = y.right
        y.right = z
        z.left = T3
        z.height = 1 + max(self.getHeight(z.left),
                           self.getHeight(z.right))
        y.height = 1 + max(self.getHeight(y.left),
                           self.getHeight(y.right))
        return y

#method to return height
    def getHeight(self, root):
        if not root:
            return 0
        return root.height

#method to return balance of a node 
    def getBalance(self, root):
        if not root:
            return 0
        return self.getHeight(root.left) - self.getHeight(root.right)
#method to return smallest value node
    def getMinValueNode(self, root):
        if root is None or root.left is None:
            return root
        return self.getMinValueNode(root.left)
#method to print avl tree using inorder
    def inOrder(self, root):
        if not root:
            return
        self.inOrder(root.left)
        print("{0} ".format(root.key), end="")
        self.inOrder(root.right)
#searching method for bst    
    def bsearch(self,root,key):
        if not root:
            print("\nkey not found!")
            return
        elif root.key==key:
            print("\nkey found!")
            return
        elif key < root.key:
            root.left = self.bsearch(root.left, key)
        else:
            root.right = self.bsearch(root.right, key)




#-------------------BST(unbalanced)---------------------

class BSTree(object):
#insert node method
    def insert_node(self,root,key):

        if not root:
            return TreeNode(key)
        elif key< root.key:
            root.left = self.insert_node(root.left,key)
        else:
            root.right = self.insert_node(root.right,key)

#delete node method 
    def delete_node(self, root, key):
#tree is empty
        if not root:
            return root
        elif key < root.key:
            root.left = self.delete_node(root.left, key)
        elif key > root.key:
            root.right = self.delete_node(root.right, key)
        else:
            if root.left is None:
                temp = root.right
                root = None
                return temp
            elif root.right is None:
                temp = root.left
                root = None
                return temp
            temp = self.getMinValueNode(root.right)
            root.key = temp.key
            root.right = self.delete_node(root.right,
                                          temp.key)
        if root is None:
            return root
#method to return smallest value node
    def getMinValueNode(self, root):
        if root is None or root.left is None:
            return root
        return self.getMinValueNode(root.left)
#method to print avl tree using inorder
    def inOrder(self, root):
        if not root:
            return
        self.inOrder(root.left)
        print("{0} ".format(root.key), end="")
        self.inOrder(root.right)

#searching method for bst    
    def bsearch(self,root,key):
        if not root:
            print("\nkey not found!")
            return
        elif root.key==key:
            print("\nkey found!")
            return
        elif key < root.key:
            root.left = self.bsearch(root.left, key)
        else:
            root.right = self.bsearch(root.right, key)

        

#-------------------Skiplist----------------------------

#skip list node
class Node(object):
    def __init__(self, key, level):
        self.key = key
        self.forward = [None]*(level+1)  #un-initialized list of pointer levels
        
 
class SkipList(object):
#initialize node with level 0    
    def __init__(self, max_lvl, P):
        self.MAXLVL = max_lvl
 
        self.P = P
 
        self.header = self.createNode(self.MAXLVL, -1)
 
        self.level = 0

    def createNode(self, lvl, key):
        n = Node(key, lvl)
        return n

#generates a randomized level less than max for a node     
    def randomLevel(self):
        lvl = 0
        while random.random()<self.P and \
              lvl<self.MAXLVL:lvl += 1
        return lvl

#method to insert node into skip list 
    def insertElement(self, key):
 # create update array and initialize it
        update = [None]*(self.MAXLVL+1)
        current = self.header
#find correct position starting from highest level
        for i in range(self.level, -1, -1):
            while current.forward[i] and \
                  current.forward[i].key < key:
                current = current.forward[i]
            update[i] = current
#reach lvl 0 insert node
        current = current.forward[0]
 
        
#if current is NULL that means we have reached node to be inserted between update[0] and current node
       
        if current == None or current.key != key:
# Generate a random level for node
            rlevel = self.randomLevel()

            if rlevel > self.level:
                for i in range(self.level+1, rlevel+1):
                    update[i] = self.header
                self.level = rlevel
 
            n = self.createNode(rlevel, key)
 
# insert node by rearranging references
            for i in range(rlevel+1):
                n.forward[i] = update[i].forward[i]
                update[i].forward[i] = n
 
            print("Successfully inserted key {}".format(key))

#method to delete node from list 
    def deleteNode(self, search_key):
#update list to store path information 
        update = [None]*(self.MAXLVL+1)
        current = self.header

        for i in range(self.level, -1, -1):
            while(current.forward[i] and \
                  current.forward[i].key < search_key):
                current = current.forward[i]
            update[i] = current
 
        current = current.forward[0]
 
# If current node is target node
        if current != None and current.key == search_key:
 
            
#start from lowest level and rearrange references
            
            for i in range(self.level+1):
 
                if update[i].forward[i] != current:
                    break
                update[i].forward[i] = current.forward[i]
 
# Remove levels having no elements
            while(self.level>0 and\
                  self.header.forward[self.level] == None):
                self.level -= 1
            print("Successfully deleted {}".format(search_key))

#skip list search method, we start from the highest level down 
    def skipSearch(self, key):
        current = self.header
 
        for i in range(self.level, -1, -1):
            while(current.forward[i] and\
                  current.forward[i].key < key):
                current = current.forward[i]
 
# reached level 0 and advance reference to right, which is possibly our desired node
        current = current.forward[0]
        if current and current.key == key:
            print("Key Found! ")
 
#print list elements level wise 
    def printList(self):
        head = self.header
        print("\n")
        for lvl in range(self.level+1):
            print("Level {}: ".format(lvl), end=" ")
            node = head.forward[lvl]
            while(node != None):
                print(node.key, end=" ")
                node = node.forward[lvl]
            print("")










#MAIN
#avl
avltree = AVLTree()
root = None
#dataset taken
nums = [33, 13, 52, 9, 21, 61, 8, 11]
for num in nums:
    root = avltree.insert_node(root, num)
avltree.inOrder(root)
key = 13
root = avltree.delete_node(root, key)
print("\nAfter Deletion: ")
avltree.inOrder(root)
key = 52
print("\nsearching 52:")
st = time.time()
avltree.bsearch(root,key)
time.sleep(3)
et = time.time()
avl_exe = et - st
print('AVL tree search time:', avl_exe, ',seconds')

#skip
lst = SkipList(3, 0.5)
print("\n-------Skip List-------")
for num in nums:
    lst.insertElement(num)
lst.printList()
 
lst.deleteNode(13) 
lst.printList()


print("\nsearching 52:")
start = time.time()
lst.skipSearch(52)
time.sleep(3)
end = time.time()
skip_exe = end - start
print('Skiplist search time:', skip_exe, ',seconds')

#bst
bst = BSTree()
root=None
for num in nums:
    root = bst.insert_node(root, num)
bst.inOrder(root)
key = 13
root = bst.delete_node(root, key)
print("\nAfter Deletion: ")
bst.inOrder(root)
key = 52
print("\nsearching 52:")
begin = time.time()
bst.bsearch(root,key)
time.sleep(3)
finish = time.time()
bst_exe = finish - begin
print('BST search time:', bst_exe, ',seconds')

print("\n\n Analysis:\n bst(unbalanced) efficiency  O(n) for binary tree and BST test: ",bst_exe,"\nand O(Logn) for AVL test:",avl_exe," \nand O(Logn) for SkipLists(avg case)",skip_exe)