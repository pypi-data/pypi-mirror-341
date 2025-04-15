import random
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def append(self, data):
        newNode = Node(data)
        currentNode = self.head
        if not self.head:
            self.head = newNode
        else:
            lastNode = currentNode
            while lastNode.next:
                lastNode = lastNode.next
            lastNode.next = newNode

    def push(self, data, index=None):
        newNode = Node(data)

        if self.head is None:
            self.head = newNode
            return

        if index is not None:
            if index == 0:
                newNode.next = self.head
                self.head = newNode
                return

            currentNode = self.head
            count = 0
            while currentNode and count < index - 1:
                currentNode = currentNode.next
                count += 1

            if currentNode is None:
                return

            newNode.next = currentNode.next
            currentNode.next = newNode
            return

        lastNode = self.head
        while lastNode.next:
            lastNode = lastNode.next
        lastNode.next = newNode

    def pop(self, index=None):
        if self.head is None:
            return None

        currentNode = self.head

        if len(self) == 1:
            self.head = None
            return currentNode.data

        if index is not None:
            count = 0
            previousNode = None

            while currentNode and count != index:
                previousNode = currentNode
                currentNode = currentNode.next
                count += 1

            if currentNode is None:
                return None

            if previousNode is None:
                self.head = currentNode.next
            else:
                previousNode.next = currentNode.next

            return currentNode.data

        previousNode = None
        lastNode = currentNode
        while lastNode.next:
            previousNode = lastNode
            lastNode = lastNode.next

        if previousNode:
            previousNode.next = None

        return lastNode.data
    def insertBefore(self, target, data):
        newNode = Node(data)
        currentNode = self.head
        if currentNode and currentNode.data == target:
           newNode.next = self.head
           self.head = newNode
           return

        previousNode = None
        while currentNode:
           if currentNode.data == target:
               previousNode.next = newNode
               newNode.next = currentNode
               return
           previousNode = currentNode
           currentNode = currentNode.next
    
    def insertAfter(self, target, data):
        newNode = Node(data)
        currentNode = self.head
        while currentNode:
           if currentNode.data == target:
               newNode.next = currentNode.next
               currentNode.next = newNode
               return
           currentNode = currentNode.next
    
    def removeByValue(self, value):
        currentNode = self.head
        if currentNode and currentNode.data == value:
           self.head = currentNode.next
           return

        previousNode = None
        while currentNode:
           if currentNode.data == value:
               previousNode.next = currentNode.next
               return
           previousNode = currentNode
           currentNode = currentNode.next       
    
    def clone(self):
        clonedList = LinkedList()
        currentNode = self.head
        while currentNode:
            clonedList.append(currentNode.data)
            currentNode = currentNode.next
            
        return clonedList
       
    def reverse(self):
        prev = None
        current = self.head
        while current:
            nextNode = current.next
            current.next = prev
            prev = current
            current = nextNode
            self.head = prev
            
    def findIndexOf(self,data):
        currentNode = self.head
        count = 0
        while currentNode:
            if currentNode.data == data:
                return count
            currentNode = currentNode.next
            count += 1
        return -1
    def indexOfAll(self,data):
        if self.head is None:
            return []
        else:
            index = []
            currentNode = self.head
            count  = 0
            while currentNode:
                if currentNode.data == data:
                    index.append(count)
                currentNode = currentNode.next
                count += 1
        return index      
                
    def contains(self,data):
        currentNode = self.head
        while currentNode:
            if currentNode.data == data:
                return True
            currentNode = currentNode.next
        return False       
    def __len__(self):
        count = 0
        currentNode = self.head
        while currentNode:
            count += 1
            currentNode = currentNode.next
        return count
    def isEmpty(self):
        return True if len(self) == 0 else False
    
    def toList(self):
        if not self.head:
            return 
        result = [] 
        currentNode = self.head
        while currentNode:
            result.append(currentNode.data)
            currentNode = currentNode.next
        return result
    def fromList(self,arr):
        for i in arr:
            self.push(i)   
    def merge(self, otherList):
        if not isinstance(otherList, LinkedList):
            raise TypeError("Argument must be a LinkedList")

        currentNode = otherList.head
        while currentNode:
           self.append(currentNode.data)
           currentNode = currentNode.next
    def removeDuplicates(self):
        seen = set()
        currentNode = self.head
        previousNode = None
        while currentNode:
            if currentNode.data in seen:
                previousNode.next = currentNode.next
            else:
                seen.add(currentNode.data)
                previousNode = currentNode
            currentNode = currentNode.next
                
        
    def detail(self):
        result = []
        count = 0
        currentNode = self.head
        while currentNode:
            result.append(str({
                "data": currentNode.data,
                "address": id(currentNode.next),
                "index": count
            }))
            currentNode = currentNode.next
            count += 1

        nodeData = [",".join(result)]
        nodeLength = len(self)
        nodeInfo = {
            "length": str(nodeLength),
            "nodeData": nodeData
        }

        return str(nodeInfo)
    
    def sliceLinkedList(self,start,end):
        if start < 0 and end > len(self):
            raise IndexError("Index out of range")
        currentNode  = self.head
        index = 0
        slicedList = LinkedList()
        while currentNode and index < end:
            if index >= start:
                slicedList.append(currentNode.data)
            currentNode = currentNode.next 
            index += 1
        return slicedList   
    
    def replace(self,old,new):
        if self.head is None:
            return
        else:
            currentNode = self.head
            while currentNode:
                if currentNode.data == old:
                    currentNode.data = new
                currentNode = currentNode.next  
    
    def map (self , function):
        if self.head is None:
            return
        else:
            currentNode  = self.head
            while currentNode:
                currentNode.data = function(currentNode.data)
                currentNode = currentNode.next
                
    def filteredList(self,function):
        if self.head is None:
            return
        else:
            currentNode = self.head
            filteredList = LinkedList()
            while currentNode:
                if function(currentNode.data):
                    filteredList.append(currentNode.data)
                currentNode = currentNode.next
        return filteredList
    
    def reduceList(self, function, initializer=None):
        if self.head is None:
           return initializer
    
        currentNode = self.head
        accumulator = initializer if initializer is not None else currentNode.data
        if initializer is None:
           currentNode = currentNode.next

        while currentNode:
           accumulator = function(accumulator, currentNode.data)
           currentNode = currentNode.next

        return accumulator


    def min(self):
        if self.head is None:
            return None
        else:
            arr = self.toList()  
            return min(arr) 
        
    def max(self):
        if self.head is None:
            return None
        else:
            arr = self.toList()
            return max(arr)
                           
    def __getitem__(self,index):
        
        if index < 0 or index >= len(self):
            raise IndexError("Index out of range")
        
        currentNode = self.head
        count = 0
        while currentNode:
            if count == index:
                return currentNode.data
            currentNode = currentNode.next
            count += 1   
                 
    def __setitem__(self,index,value):
        if index < 0 or index > len(self):
            raise IndexError("Index out range")
        currentNode = self.head
        count = 0
        while currentNode:
            if count == index:
                currentNode.data = value
                return 
            currentNode = currentNode.next
            count += 1    
          
    def __str__(self):
        result = []
        currentNode = self.head
        while currentNode:
            result.append(f"[{currentNode.data}]")
            currentNode = currentNode.next
        return "->".join(result) + "-> None"
    
    def __iter__(self):
        current = self.head
        while current:
            yield current.data
            current = current.next
    def sortedList(self, mode="asc"):
        data = self.toList()
        if not data:
            return LinkedList()

        if mode == "asc":
            data.sort()
        elif mode == "desc":
            data.sort(reverse=True)
        elif mode == "reverse":
            data.reverse()
        elif mode == "random":
            random.shuffle(data)
        else:
            raise ValueError("Invalid mode. Use 'asc', 'desc', 'reverse', or 'random'.")

        sorted_linked_list = LinkedList()
        for item in data:
            sorted_linked_list.append(item)

        return sorted_linked_list
    
    def clear(self):
        self.head = None
        
    def docs(self):
        url = "https://adhithya200503.github.io/LinkedList/"
        githubLink = "https://github.com/Adhithya200503/LinkedList/blob/main/linkedList.py"
        print(f"click the url to view the docs {url}\n") 
        print(f"github link {githubLink}")
        

ll = LinkedList()
ll.docs()
