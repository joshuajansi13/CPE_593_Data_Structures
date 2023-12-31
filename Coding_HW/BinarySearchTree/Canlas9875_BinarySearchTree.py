

class Node:
    def __init__(self, val) -> None:
        self.val = val
        self.left = None
        self.right = None

class BinarySearchTree:

    def __init__(self) -> None:
        self.root = None
        
    def buildBinarySearchTree(self):
        '''
        This should take a user's input and build a binary search tree.
        Assume that the input will be a set of numbers, separated by whitespace.
        This will call the insert function for the length of list passed in by the user.
        '''
        userInput = input("Please enter a list of numbers, separated by spaces: ")
        valList = [int(x) for x in userInput.split()]
        print(f"User input = {valList}")

        for item in valList:
            self.insert(item)

    def insert(self, val):
        '''
        Inserts new nodes into the tree.
        '''
        p = self.root

        if p is None:
            self.root = Node(val)
            return
        
        while p is not None:
            if p.val < val:
                if p.right is None:
                    p.right = Node(val)
                    return
                p = p.right
            else:
                if p.left is None:
                    p.left = Node(val)
                    return
                p = p.left

    def printOrder(self):
        result = []
        self.inorderTraversal(self.root, result)
        print(f"In-order traversal: {result}")

    def inorderTraversal(self, root, list):
        '''
        Should in-order traverse the tree and print out the tree that was built.
        '''
        if root:
            self.inorderTraversal(root.left, list)
            list.append(root.val)
            self.inorderTraversal(root.right, list)

    def insert_at(self, i, val):
        '''
        Should take user's input for two values, index i, and value val, and insert val to be the ith item of the tree.
        '''
        sorted_list = []
        self.inorderTraversal(self.root, sorted_list)

        # sorted_list.insert(i, val)
        if i < 0 or i >= len(sorted_list):
            print("Index provided is out of range!")
            return
        elif i == 0:
            if val > sorted_list[i]:
                print(f"{i} is not the correct index for {val}")
                return
        elif i == len(sorted_list)-1:
            if val < sorted_list[len(sorted_list)-1]:
                print(f"{i} is not the correct index for {val}")
                return
        else:
            if val > sorted_list[i] or val < sorted_list[i - 1]:
                print(f"{i} is not the correct index for {val}")
                return
        
        sorted_list.clear()
        self.insert(val)
        self.inorderTraversal(self.root, sorted_list)
        print(f"New tree built: {sorted_list}")

    def findNode(self, root, x):
        if root is None:
            return None
        if root.val == x:
            return root
        if root.val > x:
            return self.findNode(root.left, x)
        return self.findNode(root.right, x)
    
    def findMin(self, node):
        while node.left is not None:
            node = node.left
        return node

    def delete(self, x):
        '''
        Should check whether value x exists in the tree, and:
        - If exists, delete x, and print the resulting tree using in-order traversal.
        - If value does not exist, output message accordingly, and print the tree using in-order traversal.
        '''

        inorder_list = []
        if self.findNode(self.root, x) is None:
            self.inorderTraversal(self.root, inorder_list)
            print(f"{x} does not exist in the tree. {inorder_list}")
        else:
            self.recursiveDelete(self.root, x)
            self.inorderTraversal(self.root, inorder_list)
            print(f"Updated tree: {inorder_list}")

    def recursiveDelete(self, root, x):
        if root is None:
            return root
        if root.val > x:
            root.left = self.recursiveDelete(root.left, x)
        elif root.val < x:
            root.right = self.recursiveDelete(root.right, x)
        else:
            if root.left is None:
                return root.right
            elif root.right is None:
                return root.left
            root.val = self.findMin(root.right).val
            root.right - self.recursiveDelete(root.right, root.val)
        return root

    def firstCommonAncestor(self, root, x, y):
        if root is None:
            print("The binary search tree is empty.")
            return None
        
        node1 = self.findNode(self.root, x)
        node2 = self.findNode(self.root, y)

        if node1 is None or node2 is None:
            print("One of the input values don't exist in the tree.")
            return None
        
        else:
            # Checks to see if both inputs are in the left subtree
            if node1.val < root.val and node2.val < root.val:
                return self.firstCommonAncestor(root.left, node1, node2)
            # Checks to see if both inputs are in the left subtree
            elif node1.val > root.val and node2.val > root.val:
                return self.firstCommonAncestor(root.right, node1, node2)
            # Current node is the first common ancestor
            else:
                return root


# Create an instance of BinarySearchTree
bst = BinarySearchTree()

# Test buildBinarySearchTree (The user will be prompted for their input here)
print("\nTesting buildBinarySearchTree...")
bst.buildBinarySearchTree()

# Test printOrder (which calls inorderTraversal)
print("\nTesting inorderTraversal...")
bst.printOrder() 

# Test insert_at
print("\nTesting insert_at...")
bst.insert_at(2, 18)

# Test delete
print("\nTesting delete...")
bst.delete(24)
bst.delete(30)

# Test firstCommonAncestor
print("\nTesting firstCommonAncestor...")
first_common_ancestor = bst.firstCommonAncestor(bst.root, 18, 12)
if first_common_ancestor:
    print(f"The first common ancestor value: {first_common_ancestor.val}")
