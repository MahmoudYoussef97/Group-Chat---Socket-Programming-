""" Server Side of the chat room in P2P """
import socket   # import Socket for P2P communication
import threading    #import threading for using Multithread


"""AF_INET is the address family of the socket. This is used when we have an Internet Domain with 
any two hosts, SOCK_STREAM means that data or characters are read in a continuous flow."""
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()         # Return a string containing the hostname of the machine
port = 2424
server_socket.bind((host, port))    # Bind the server with ip address and the port
server_socket.listen(10)            # Listen for 10 active connections.
clients = []                        # Client List

""" Making a thread for each client as all clients work in parallel  """
def client_thread(conn, address):
    welcome = "[Server]: Welcome to our group chat\nPlease Enter Your Name:"    # Welcome Message
    conn.send(welcome.encode())             # Send the message to all clients
    name = conn.recv(2048).decode()         # Receive the name of each client
    enter = name + " has joined the room"   # Client Entered the room
    broadcast(enter, conn)                  # Send to other clients that the user has entered the room

    while True:
        try:
            message = conn.recv(2048).decode()              # Receiving a message from a client
            if message:                                     # If there's a valid message then send it to other clients
                print(str(address) + ": " + message)
                broadcast_message = "[" + name + "]" + ": " + message
                broadcast(broadcast_message, conn)
            else:                                           # If not, then there's a failure so close the connection
                print(str(address)+": disconnected")
                broadcast_message = "[" + name + "]" +" has disconnected "
                broadcast(broadcast_message, conn)
                conn.close()
                delete(conn)
        except:
            continue

""" Sending Messages to all users except the sender """
def broadcast(messages, connection):
    for client in clients:
        if client != connection:
            try:
                client.send(messages.encode())
            except:     # If any failure happened from the client receiving close the connection
                connection.close()

""" Deleting the client from the client list and close the connection """
def delete(conn):
    if conn in clients:
        clients.remove(conn)

while True:

    conn, address = server_socket.accept()  # Accept the connection from client
    clients.append(conn)                    # List of all available clients
    print(str(address) + " :Connected Successfully")
    threading.Thread(target=client_thread, args=(conn, address,)).start()   # Making a thread for every client

server_socket.close()       # Closing the server socket
