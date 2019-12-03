# Python实践


## socket 编程简单构造
* server.py
```
import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("0.0.0.0", 8080))
server.listen()

while True:
    sock, addr = server.accept()
    print("connected by ", addr)
    while True:
        data = sock.recv(1024)
        print(data.decode('utf8'))
        if not data:
            break
        sock.send("server already read data".encode('utf8'))
        
server.close()
```
* client.py
  
```
import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("127.0.0.1", 8080))

while True:
    inp = input('>>>')
    client.send(bytes(inp, 'utf8'))
    data = client.recv(1024)
    print(data.decode('utf8'))
    if inp == "Q":
        break

client.close()
```

## 排序
### 冒泡
```
def Sort(L):
    if len(L) <= 1:
        return L

    for m in range(len(L)):
        for n in range(m+1, len(L)):
            if L[m] > L[n]:
                L[m], L[n] = L[n], L[m]   
    return L


if __name__ == '__main__':
    L = [2,1,0,38,39,3787,2098,10,88,2876,78]
    print(Sort(L))
```

### 选择
```
def Sort(L):
    if len(L) <= 1:
        return L
    for m in range(len(L)):
        Min = m
        for n in range(m+1, len(L)):
            if L[Min] > L[n]:
                Min = n
        L[Min], L[m] = L[m], L[Min]
    return L


if __name__ == '__main__':
    L = [2,1,0,38,39,3787,2098,10,88,2876,78]
    print(Sort(L))
```

### 归并
```
def mergesort(L):
    if len(L) <= 1:
        return L
    
    mid = len(L) / 2

    left = mergesort(L[:mid])
    right = mergesort(L[mid:])

    return merge(left, right)

def merge(left, right):
    result = []
    m = 0
    n = 0

    
    while m < len(left) and n < len(right):
        if left[m] < right[m]:
            result.append(left[m])
            m=m+1
        else:
            result.append(right[n])
            n=n+1

    result += left[m:]
    result += right[n:]

    return result

L = [2,1,0,38,39,3787,2098,10,88,2876,78]
print(mergesort(L))
```

## 数据结构-链表
```


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
```
