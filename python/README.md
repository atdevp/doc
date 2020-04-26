# Python实践
<!-- TOC -->

- [Python实践](#python实践)
    - [Python转码](#python转码)
    - [Python并发执行之多线程](#python并发执行之多线程)
        - [函数方式实现多线程](#函数方式实现多线程)
        - [类方式实现多线程](#类方式实现多线程)
        - [聊下Python的全局解释锁GIL](#聊下python的全局解释锁gil)
        - [多线程并发线程锁](#多线程并发线程锁)
            - [无锁](#无锁)
            - [有锁](#有锁)
    - [socket 编程简单构造](#socket-编程简单构造)
    - [排序](#排序)
        - [冒泡](#冒泡)
        - [选择](#选择)
        - [归并](#归并)
        - [快排](#快排)
    - [数据结构-链表](#数据结构-链表)
    - [TODO](#todo)

<!-- /TOC -->

## Python转码
* str --> byte
```
old="abc"
new=old.encode('UTF-8')
```

* byte --> str
```
old=u"abc"
new=old.decode('UTF-8')
```

## Python并发执行之多线程
> 正常情况下，我们启动一个应用程序就会启动一个进程。进程启动之后，至少有一个线程启动了，线程是干活的，进程只会要内存资源。虽然线程不要内存资源，但是他会要CPU资源。所以需要cpu协助。这种模式就像一个工厂。工厂是进程，工人是线程。干活的人多了，工作效率也就高了。工人太多了也会引来新的问题，厂长就管不过来了，所以就需要在厂长的能力下招一定数量的工人。正是线程的多少应该看cpu的的性能。

> Python实现多线程的方式有两种，一种是函数形式，一种是类形式。这个类继承threading.Thread父类。

### 函数方式实现多线程
```
import time
import threading

def f(num):
    for i in range(num):
        time.sleep(1)
        print(i)

threads = []
for i in range(3):
    t = threading.Thread(target=f, args=(5,))
    threads.append(t)
for t in threads:
    t.start()

for t in threads:
    if t.isAlive():
        t.join()
```

### 类方式实现多线程
```
import time
import threading


class Mythread(threading.Thread):
    def __init__(self, num):
        threading.Thread.__init__(self)
        self.num = num
    
    def run(self):
        for i in range(self.num):
            print(i)
            time.sleep(1)

if __name__ == "__main__":
    threads = []
    for i in range(3):
        mt = Mythread(5)
        threads.append(mt)
    for t in threads:
        t.start()
    for t in threads:
        if t.isAlive():
            t.join()
    
```

### 聊下Python的全局解释锁GIL
> GIL是python的全局解释锁简称。干啥用的呢？说白了，就是控制线程调用cpu内核用的。多线程<理论上>可以实现同时调用多个cpu同时工作。比如java、golang就可以做到。但是python因为GIL的存在，同1时间只能有一个线程在cpu内核中处理。虽然我们可以看到同时执行的现象，其实都是假象。因为cpu内核通过上下文切换快速将多个线程来回执行。所以才产生了这种现象。

### 多线程并发线程锁
#### 无锁
```
import threading

num = 0

def work():
    global num
    num+=1
    print(num)

threads = []
for i in range(10):
    t = threading.Thread(target=work)
    threads.append(t)
for t in threads:
    t.start()
for t in threads:
    if t.isAlive():
        t.join()

错误输出：
1
 23

4
5
6
 7
8
9
 10
```
#### 有锁
> 什么是线程锁呢？当遇到多个线程同时并发操作一个资源的时候，哪个线程先抢到这把锁，哪个线程就先执行，直到这个线程操作释放了这把锁，其他线程才能操作，这个叫线程安全。也就是线程锁了。
> 定义锁： lock = threading.Rlock()
> 加锁： lock.acquire()
> 释放锁： lock.release()
```
import threading

num = 0
lock = threading.RLock()

def work():
    lock.acquire()
    global num
    num+=1
    lock.release()
    print(num)

threads = []
for i in range(10):
    t = threading.Thread(target=work)
    threads.append(t)
for t in threads:
    t.start()
for t in threads:
    if t.isAlive():
        t.join()

```

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
def mergesort(l):
    if len(l) <= 1:
    ¦   return l

    mid = len(l) / 2
    left = mergesort(l[:mid])
    right = mergesort(l[mid:])
    return merge(left, right)


def merge(left, right):
    m = 0
    n = 0
    result = []
    while m < len(left) and n < len(right):
    ¦   if left[m] < right[n]:
    ¦   ¦   result.append(left[m])
    ¦   ¦   m += 1
    ¦   else:
    ¦   ¦   result.append(right[n])
    ¦   ¦   n += 1

    result += left[m:]
    result += right[n:]
    return result


l = [12, 234, 345345, 456456, 29]
print(mergesort(l))
```
### 快排
```
def quickSort(alist, left, right):
    if left >= right:
        return

    pivot = alist[left]

    low = left
    high = right

    while low < high:
        while low < high and alist[high] >= pivot:
            high -= 1
        alist[low] = alist[high]

        while low < high and alist[low] <= pivot:
            low += 1
        alist[high] = alist[low]

    alist[low] = pivot
    quickSort(alist, left, low - 1)
    quickSort(alist, high + 1, right)


alist = [54, 26, 93, 17, 77, 31, 44, 55, 20, 26, 31]
quickSort(alist, 0, len(alist) - 1)
print(alist)
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

## TODO
