import socket
import select

BUF_SIZE = 1024
SERVER_PORT = 8820
SERVER_IP = "0.0.0.0"

print("Setting up server...")
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((SERVER_IP,SERVER_PORT))
server_socket.listen()
print("Listening for clients...")

open_client_sockets = []
masseges_to_send = []




def print_client_sockets(client_sockets):
    for c in client_sockets:
        print("\t", c.getpeername())

while True:
    rlist, wlist, xlist = select.select([server_socket]+ open_client_sockets, open_client_sockets,[])
    for client in rlist:
        if client in open_client_sockets:
            data = ""
            data = str(client.recv(BUF_SIZE).decode())
            print(data)
            if data == "exit":
                print("connection closed")
                open_client_sockets.remove(client)
                client.close()
                print_client_sockets(open_client_sockets)
            else:
                sockets_to_send = open_client_sockets.copy()
                sockets_to_send.remove(client)
                masseges_to_send.append((sockets_to_send,data))

        else:
            print("new client\n")
            new_client, addr = server_socket.accept()
            print_client_sockets(open_client_sockets)
            open_client_sockets.append(new_client)


    for message in masseges_to_send:
        client_sockets, data = message
        for client in client_sockets:
            if client in wlist:
                client.sendall(data.encode())
        masseges_to_send.remove(message)