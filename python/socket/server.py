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


        



