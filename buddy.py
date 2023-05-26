import socket
import select
import threading

# Create a TCP/IP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to a specific address and port

HOST = '161.35.34.149'
PORT = 4444

server_address = (HOST, PORT)
server_socket.bind(server_address)

# Listen for incoming connections
server_socket.listen()

print(f"Listening for incoming connections on port {server_address[1]}...")

# List of connected clients
connected_clients = []

def list_clients():
    print("\nList of connected clients:")
    for i, client_socket in enumerate(connected_clients):
        client_address = client_socket.getpeername()
        print(f"{i}: {client_address[0]}:{client_address[1]}")

def send_message():
    if connected_clients:
        try:
            client_numbers = input("\nEnter client number(s) to send message to (comma-separated): ")
            client_numbers = [int(num) for num in client_numbers.split(",")]
            message = input("Enter the message to send: ")

            for client_number in client_numbers:
                client_socket = connected_clients[client_number]
                client_socket.send(message.encode())
        except (ValueError, IndexError):
            # Ignore any input errors and continue listening for connections
            pass

def terminalx():
    while True:
        terminal = str(input("server -->")).lower()
        if terminal == "list":
            list_clients()
        if terminal == "send":
            send_message()

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
            print(f"New connection from {client_address[0]}:{client_address[1]}")


            # Add the client to the list of connected clients
            connected_clients.append(client_socket)

        # If a message is received from a client
        else:
            message = socket_ready.recv(1024).decode()
            client_address = socket_ready.getpeername()
            print(f"Received message from {client_address[0]}:{client_address[1]} - {message}")
