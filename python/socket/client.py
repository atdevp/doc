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