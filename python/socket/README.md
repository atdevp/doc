
# Socket


### 1、socket涉及的一些函数
```
socket()
bind()
listen()
accept()
connect()
connect_ex()
send()
recv()
close()

```

### server端
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


### client端
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