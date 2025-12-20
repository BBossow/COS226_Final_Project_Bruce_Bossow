
class Tree:
    def __init__(self, maxdegree, field):
        self.root = None # reference to the root node
        self.maxdegree = maxdegree # the number of keys that will cause a split
        self.field = field

class DataItem:
    def __init__(self, key, value):
        self.key = key  # key is used to organize
        self.value = value  # value is the data associated with the key

    def __str__(self):
        return str(self.key)

    def __repr__(self):
        return str(self.key)

class Bucket:

    def __init__(self, maxdegree):
        self.keys = [] # A list of Keys that are used to organize the data
        self.links = [] # A list of links potential child nodes
        self.parent = None # A link to the parent node
        self.is_leaf = True # A boolean indicating if the node is a leaf node (and thus holds the data in the keys)
        self.next = None # A link to the next leaf node in the chain
        self.prev = None
        self.maxdegree = maxdegree

    def __str__(self):
        return str(self.keys)

    def __repr__(self):
        return str(self.keys)



class BucketNode(Bucket):

    def remove(self, remove_key):
        # bucket remove
        # find the DataItem in .keys that matches "key"
        # pop it fromm the list if it exists. return the popped dataitem
        # if it doesn't, return -1

        if self.is_leaf: #leaf bucket
            targetIndex = 0
            for itemData in self.keys:
                if remove_key == itemData.key:
                    break
                targetIndex += 1
            if targetIndex >= len(self.keys):
                targetIndex -= 1
            if self.keys[targetIndex].key == remove_key:
                del_node = self.keys.pop(targetIndex)
                return del_node
            else:
                return -1
class LeafNode:
    
    def __init__(self, maxdegree):
        self.keys = []          # list of IndexItem
        self.is_leaf = True
        self.next = None        # pointer to next leaf
        self.prev = None        # pointer to previous leaf
        self.maxdegree = maxdegree

    def remove(self, key):
        i = 0
        while i < len(self.keys):
            if self.keys[i].key == key:
                return self.keys.pop(i)  
            i += 1
        return -1

class InternalNode:
    
    def __init__(self, maxdegree):
        self.is_leaf = False
        self.keys = []          # separator keys
        self.links = []         # child pointers
        self.maxdegree = maxdegree
        self.parent = None

class BTree(Tree):
    # goes through the tree to find the correct leaf bucket for the add
    def get_value(self, item):
        if self.field == "release_date":
            return item.release_date
        elif self.field == "revenue":
            return item.revenue
        elif self.field == "rating":
            return item.rating
        elif self.field == "min_duration":
            return item.min_duration
        
    def range_search(self, low=None, high=None):
        
        if self.root is None:
            return []

        results = []

        #Traverses to the first leaf node that could contain 'low'
        node = self.root
        while not node.is_leaf:
            node = node.links[0]

        #Traverse leaf nodes sequentially
        while node:
            for item in node.keys:  # item is a DataItem
                key = item.key

                if (low is None or key >= low) and (high is None or key <= high):
                    results.append(item.value)

            node = node.next

        return results
    
    def bulk_load(self, records):

        if len(records) == 0:
            return

        leaves = []
        i = 0

        # creating the leaf nodes and bulking loading them
        while i < len(records):
            leaf = LeafNode(self.maxdegree)

            while len(leaf.keys) < self.maxdegree - 1 and i < len(records):
                key = self.get_value(records[i])  # INDEX FIELD
                item = DataItem(key, records[i])
                leaf.keys.append(item)

                i += 1

            leaves.append(leaf)
        
        # This is for linking the leaf nodes
        for i in range(len(leaves) - 1):
            leaves[i].next = leaves[i + 1]
            leaves[i + 1].prev = leaves[i]

        # creating the internal nodes
        self.root = self.build_internal(leaves)

    def build_internal(self, nodes):
        # builds internal nodes
        if len(nodes) == 1:
            return nodes[0]

        parents = []
        i = 0

        while i < len(nodes):
            parent = InternalNode(self.maxdegree)
            children = nodes[i:i + self.maxdegree]
            parent.links = children

            # set parent reference for child nodes
            for child in children:
                child.parent = parent

            # append keys for parent (skip empty children)
            for child in children[1:]:
                if len(child.keys) == 0:
                    continue  # skip empty child keys

                # if leaf node, take DataItem.key
                if 'next' in child.__dict__:
                    first_key = child.keys[0].key
                else:  # internal node, keys are already raw numbers
                    first_key = child.keys[0]
                parent.keys.append(first_key)

            parents.append(parent)
            i += self.maxdegree

        # recursively build higher levels
        return self.build_internal(parents)


    def remove(self, key):
        curBucket = self.root
        memory = None  # for updating parent keys if needed
        memory_index = 0

        # Traverse internal nodes to find the correct leaf
        while not curBucket.is_leaf:
            targetLink = 0
            for bucket_key in curBucket.keys:
                # if bucket_key is a DataItem, get its .key; otherwise use directly
                if isinstance(bucket_key, DataItem):
                    compare_key = bucket_key.key
                else:
                    compare_key = bucket_key

                if key < compare_key:
                    break
                targetLink += 1

            # Clamp targetLink to valid range
            if targetLink >= len(curBucket.links):
                targetLink = len(curBucket.links) - 1

            # Track memory for updating parent keys if needed
            if targetLink < len(curBucket.keys):
                bk = curBucket.keys[targetLink]
                bk_value = bk.key if isinstance(bk, DataItem) else bk
                if key == bk_value:
                    memory = curBucket
                    memory_index = targetLink

            curBucket = curBucket.links[targetLink]

        # Now curBucket is the correct leaf
        removed = None
        i = 0
        while i < len(curBucket.keys):
            if curBucket.keys[i].key == key:
                removed = curBucket.keys.pop(i)
                break
            i += 1

        if removed is None:
            return f"Did not find {key}"

        # Update parent key if needed
        if memory is not None:
            next_key = self.find_next_key(curBucket)
            if next_key is not None:
                memory.keys[memory_index] = next_key

        # Fix leaf if it is too small
        if len(curBucket.keys) < ((self.maxdegree - 1) // 2):
            self.fix_leaf_bucket(curBucket)

        return f"Found {key} and removed {removed.value}"
    
    def fix_leaf_bucket(self, node):
        # the leaf node is too small

        if node == self.root: # root can't be too small
            return
        
        # grab the sibling info and where we are at
        left_node, right_node, link_index = self.get_siblings(node)

        # check if we can...

        # steal from left
        if self.isValidSteal(left_node) == True:
            self.steal_leaf(node, "left")

        # steal from right
        elif self.isValidSteal(right_node) == True:
            self.steal_leaf(node, "right")

        # merge to the left
        elif left_node != None: 
            self.merge_leaf(left_node, node)

        # merge to the right
        else: 
            self.merge_leaf(node, right_node)

    def get_siblings(self, node):
        # find the valid left and right sibling

        left_node = None
        right_node = None

        # find out where we are
        if node.parent == None:
            return
        target = 0
        for i in node.parent.links:
            if i == node:
                break
            target += 1
        
        if target > 0: # if it's possible to have a left sibling
            left_node = node.parent.links[target-1]
        if target < len(node.parent.links)-1:
            # if it's possible to have a right sibling
            right_node = node.parent.links[target+1]
        # return all the information

        return left_node, right_node, target

        
    def fix_keys(self, node): # will only run on internal buckets
        for link_index in range(1, len(node.links)): 
            # we're working with numbers
            # start at 1, continue to end of link list
            node.keys[link_index-1] = node.links[link_index]
        

    def find_next_key(self, node): 
        # only runs on leaf buckets
        # find the next key, after key for the parent node, happens when remove occurs
        if len(node.keys) >= 1: #bucket is large enough, the next key is here
            return node.keys[0].key # return next
        elif node.next != None:
            return node.next.keys[0].key
        else:
            return None

    # is the merge leaf function for when the node size is too small and a steal cannot happen
    def merge_leaf(self, leftNode, rightNode):
        leftNode.keys.extend(rightNode.keys)

        parent = leftNode.parent
        # find index of leftNode in parent.links
        target = 0
        for link in parent.links:
            if link == leftNode:
                break
            target += 1

        # remove parent key safely
        if target > 0 and target - 1 < len(parent.keys):
            parent.keys.pop(target - 1)

        # remove rightNode from parent.links safely
        if target + 1 < len(parent.links):
            parent.links.pop(target + 1)

        # fix leaf chain
        leftNode.next = rightNode.next
        if leftNode.next:
            leftNode.next.prev = leftNode

        # check parent minimum size
        if len(parent.keys) < ((self.maxdegree - 1) // 2):
            self.fix_internal_bucket(parent)

    # checks to see if a steal is possible
    def isValidSteal(self, node):
        if node == None:
            return False
        if len(node.keys) <= (self.maxdegree-1)//2:
            return False
        return True

    def fix_internal_bucket(self, node):
        # node is an internal bucket and is too small

        if node == self.root: # root can't be too small
            return
        
        left_sibling, right_sibling, my_link = self.get_siblings(node)

        # check if...

        # you can steal left
        if self.isValidSteal(left_sibling) == True:
            self.steal_internal(node, "left")

        # you can steal right
        elif self.isValidSteal(right_sibling) == True:
            self.steal_internal(node, "right")

        # you can merge left
        elif left_sibling != None:
            self.internal_merge(left_sibling, node)

        # you can merge right
        else:
            self.internal_merge(node, right_sibling)
    
    # is the function to steal from another leaf node, when the node is too small
    def steal_leaf(self, node, direction):
        if node.parent is None:
            return

        # find target index of node in parent.links
        target = 0
        for link in node.parent.links:
            if link == node:
                break
            target += 1

        if direction == "left":  # stealing from the left
            left_node = node.parent.links[target - 1]
            if len(left_node.keys) == 0:
                return  # nothing to steal

            # only update parent key if target > 0
            if target > 0 and len(node.parent.keys) >= target:
                node.parent.keys[target - 1] = left_node.keys[-1]

            node.keys.insert(0, left_node.keys.pop(-1))

        else:  # stealing from the right
            right_node = node.parent.links[target + 1]
            if len(right_node.keys) == 0:
                return  # nothing to steal

            if len(node.parent.keys) > target:
                node.parent.keys[target] = right_node.keys[0]

            node.keys.append(right_node.keys.pop(0))
    
    # is the function to steal from another internal node, when the node is too small
    def steal_internal(self, node, direction):
        if direction == "left": # stealing from the left
            target = 0
            for link in node.parent.links:
                if link == node:
                    break
                target += 1
            # now target = link to node

            left_node = node.parent.links[target-1] # left sibling that we steal from

            node.keys.insert(0, node.parent.keys.pop(target-1))
            node.links.insert(0, left_node.links.pop(-1))
            node.parent.keys.insert(target-1, left_node.keys.pop(-1))

        else: # stealing from the right
            target = 0
            for link in node.parent.links:
                if link == node:
                    break
                target += 1
            # now target = link to node

            right_node = node.parent.links[target+1] # right sibling that we steal from

            node.keys.append(node.parent.keys.pop(target))
            node.links.append(right_node.links.pop(0))
            node.parent.keys.insert(target+1, right_node.keys.pop(0))

    def internal_merge(self, leftNode, rightNode):
        # take parent key between left and right, pop it, and append to left_node.keys
        parent = leftNode.parent
        target = 0
        for link in parent.links:
            if link == rightNode:
                break
            target += 1
        leftNode.keys.append(parent.keys.pop(target-1))
        
        parent.links.pop(target)
        for link in rightNode.links:
            link.parent = leftNode

        leftNode.keys.extend(rightNode.keys)
        leftNode.links.extend(rightNode.links)

        # if parent.keys length is now 0, and it's the root, set root to left_node
        if len(parent.keys) == 0:
            self.root = leftNode

        # check if parent too small (but not zero), if it is, another internal_fix
        if (len(parent.keys)) < ((self.maxdegree-1)//2) and (len(parent.keys)) > 0:
                self.fix_internal_bucket(parent)