# Python实践
<!-- TOC -->

- [Python实践](#python%e5%ae%9e%e8%b7%b5)
  - [socket 编程简单构造](#socket-%e7%bc%96%e7%a8%8b%e7%ae%80%e5%8d%95%e6%9e%84%e9%80%a0)

<!-- /TOC -->

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