

class Node(object):
    def __init__(self, elme):
        self.elme = elme
        self.next = None
    

class SingleLinkedList(object):
    def __init__(self):
        self.head = None
    
    def is_empty(self):
        if self.head is None:
            return True
        return False

    def append(self, elme):
        node = Node(elme)
        if self.is_empty():
            self.head = node
            return
        
        cursor = self.head
        while cursor.next is not None:
            cursor = cursor.next
        cursor.next = node
        return

    def terval(self):
        res = []
        if self.is_empty():
            return res
        
        cursor = self.head
        while cursor is not None:
            res.append(cursor.elme)
            cursor = cursor.next
        return res

    def length(self):
        num = 0
        if self.is_empty():
            return 0
        cursor = self.head
        while cursor is not None:
            num+=1
            cursor = cursor.next
        return num

    def reverse(self):
        res = []
        if self.is_empty():
            return res
        
        phead = self.head
        last = None

        while phead:
            tmp = phead.next
            phead.next = last

            last = phead
            phead = tmp
        
        cursor = last
        while cursor is not None:
            res.append(cursor.elme)
            cursor = cursor.next
        return res




singleLinkedList = SingleLinkedList()
for i in range(1,11):
    singleLinkedList.append(i)
print(singleLinkedList.terval())
print(singleLinkedList.length())
print(singleLinkedList.reverse())







        