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