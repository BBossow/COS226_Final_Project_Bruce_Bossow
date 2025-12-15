
class Tree:
    def __init__(self, maxdegree):
        self.root = None # reference to the root node
        self.maxdegree = maxdegree # the number of keys that will cause a split

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

 
    def add(self, item, leftLink = None):
        # bucket add
        # find the correct spot for DataItem in the bucket
        # insert DataItem in correct spot
        if self.is_leaf: #leaf bucket
            targetIndex = 0
            for itemData in self.keys:
                if item.key < itemData.key:
                    break
                targetIndex += 1
            self.keys.insert(targetIndex, item)
            return len(self.keys)
        else: # internal bucket, called when split
            target = 0
            for key in self.keys:
                if item.key < key.key:
                    break
                target += 1
            self.keys.insert(target, item)
            self.links.insert(target, leftLink)
            return (len(self.keys))

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

class BTree(Tree):
    # goes through the tree to find the correct leaf bucket for the add
    def add(self, key, value):
        data = DataItem(key, value)
        if (self.root == None): # if there is no root (first add)
            self.root = BucketNode(self.maxdegree)
            self.root.is_leaf = True
            self.root.keys.append(data)
            return
        else: 
            curBucket = self.root
            while (curBucket.is_leaf == False): #curBucket is internal
                targetLink = 0
                for bucket_key in curBucket.keys:
                    if data.key < bucket_key.key:
                        break
                    targetLink += 1
                curBucket = curBucket.links[targetLink]
            size = curBucket.add(data)
            if (size >= self.maxdegree):
                self.leaf_split(curBucket)


    def remove(self, key):
        # find the correct bucket based on the key
        curBucket = self.root
        memory = None #bucket where we find the key early
        memory_index = 0 # which index in the memory bucket


        while (curBucket.is_leaf == False): # searching for the correct bucket
                targetLink = 0
                for bucket_key in curBucket.keys:
                    if bucket_key.key == key:
                        memory = curBucket
                        memory_index = targetLink
                    if key < bucket_key.key:
                        break
                    targetLink += 1
                if targetLink >= len(curBucket.links):
                    targetLink -= 1
                curBucket = curBucket.links[targetLink]

        # curBucket is the correct leaf where "key" *might* exist
        remove = curBucket.remove(key)

        if memory != None:
            #fix the memory node
            next_key = self.find_next_key(curBucket)
            if next_key != None:
                memory.keys[memory_index].key = next_key

        if remove != -1:
            # it found something
            #check if bucket is too small
            if len(curBucket.keys) < ((self.maxdegree - 1) // 2):
                self.fix_leaf_bucket(curBucket) # fix the leaf bucket
            return f"Found {key} and removed {remove.value}"
        else:
            # didn't find the remove key, let the outside world know
            return f"Did not find {key}"
    
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

        #when maxdegree is reached in a leaf node, a leaf split occurs, creates a new node
    def leaf_split(self, node):
        newLeft = BucketNode(self.maxdegree)
        middleIndex = self.maxdegree//2
        newLeft.keys = node.keys[:middleIndex]
        node.keys = node.keys[middleIndex:]
        if node.prev != None: #if a right leaf node splits, fixes connections
            node.prev.next = newLeft
            newLeft.prev = node.prev
        newLeft.next = node
        node.prev = newLeft
        if (node.parent == None):
            self.root = BucketNode(self.maxdegree)
            self.root.is_leaf = False
            node.parent = self.root
            newLeft.parent = self.root
            self.root.keys = [node.keys[0]]
            self.root.links = [newLeft, node]
            return
        newLeft.parent = node.parent # fix parent
        split = node.parent.add(node.keys[0], newLeft)
        if (split >= self.maxdegree):
            self.internal_split(node.parent)

        # when maxdegree is reached in a internal node, a internal split occurs, creates a new node
    def internal_split(self, node):
        leftNode = BucketNode(self.maxdegree)
        leftNode.is_leaf = False
        middle = self.maxdegree//2
        leftNode.keys = node.keys[:middle]
        store = node.keys[middle]
        node.keys = node.keys[middle + 1:]
        leftNode.links = node.links[:middle + 1]
        node.links = node.links[middle + 1:]
        for i in leftNode.links:
            i.parent = leftNode
        if node.parent == None:
            self.root = BucketNode(self.maxdegree) 
            self.root.is_leaf = False
            self.root.keys = [store]
            self.root.links = [leftNode, node]
            leftNode.parent = self.root
            node.parent = self.root
            return
        if leftNode.parent == None:
            leftNode.parent = node.parent
        split = node.parent.add(store, leftNode)
        if (split >= self.maxdegree):
            self.internal_split(node.parent)

    # is the merge leaf function for when the node size is too small and a steal cannot happen
    def merge_leaf(self, leftNode, rightNode):
        # take everything in the rightNode, and stuff it into the left node

        leftNode.keys.extend(rightNode.keys)
        target = 0
        for link in leftNode.parent.links:
            if link == leftNode:
                break
            target += 1
        # now target is the index where leftNode is.
        leftNode.parent.keys.pop(target)
        leftNode.parent.links.pop(target + 1)
        leftNode.next = rightNode.next # fix the next prev connections
        if leftNode.next:
            leftNode.next.prev = leftNode
            #check if bucket is too small
        if (len(leftNode.parent.keys)) < ((self.maxdegree-1)//2):
                self.fix_internal_bucket(leftNode.parent) # fix the internal bucket

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
        if node.parent == None:
            return
        
        if direction == "left": # stealing from the left
            target = 0
            for link in node.parent.links:
                if link == node:
                    break
                target += 1
            # now target = link to node

            left_node = node.parent.links[target-1] # left sibling that we steal from

            
            node.parent.keys[target-1] = left_node.keys[-1]
            node.keys.insert(0, left_node.keys.pop(-1))

        else: 

            target = 0
            for link in node.parent.links:
                if link == node:
                    break
                target += 1
            # now target = link to node

            right_node = node.parent.links[target+1] # right sibling that we steal from

            node.keys.append(right_node.keys.pop(0))
            node.parent.keys[target] = right_node.keys[0]
    
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