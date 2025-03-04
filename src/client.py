import socket
import select
import msvcrt

IP = "127.0.0.1"
PORT = 8820

my_socket = socket.socket()
my_socket.connect((IP,PORT))
data_input = ""
is_connected = True

print("to send press enter, to exit write exit")
print(f"user: >", end=" ", flush=True)
while is_connected:
    rlist, wlist, xlist = select.select([my_socket], [my_socket], [])
    for connect in rlist:
        if connect is my_socket:
            data = connect.recv(1024).decode()
            if data != "":
                print("")
                print(f"server sent: {data}")
                print(f"user: >", end=" ", flush=True)

    for message in wlist:
        if message is my_socket:
            char = None
            while msvcrt.kbhit():
                char = msvcrt.getwch()

            if char != None:
                print(char, end="", flush=True)
                data_input += char
                if char ==  "\b":
                    print(" ", end="\b", flush=True)
                if char in "\n\r":
                    data_input = data_input[:-1]
                    message.send(str(data_input).encode())
                    if  data_input == "exit":
                        is_connected = False
                        break
                    data_input = ""
                    print("")
                    print(f"user: >", end=" ", flush=True)

my_socket.close()
