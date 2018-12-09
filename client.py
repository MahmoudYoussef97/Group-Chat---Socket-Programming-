""" Client Side of the chat room in P2P """
import socket       # import Socket for P2P communication
import threading    #import threading for using Multithread

"""AF_INET is the address family of the socket. This is used when we have an Internet Domain with 
any two hosts, SOCK_STREAM means that data or characters are read in a continuous flow. TCP """
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()             # Return a string containing the hostname of the machine
port = 2424
client_socket.connect((host, port))     # Connect the client to the server socket

""" Receiving function """
def receive(client):
    serverDown = False
    while True and (not serverDown):            # If the server is available then go
        message = client.recv(2048).decode()    # Receiving ...
        if not message:                         # If there's any failure while receiving
            print('Server is Down. You are now Disconnected. Press enter to exit...')
            exit(0)
        print(message)

""" Sending function """
def send(client):
    while True:
        message = input()
        print("[Me]: " + message)       # Showing the message on the prompt
        client.send(message.encode())   # Send the message to the server as to be send to other clients


if __name__ == '__main__':
    threading.Thread(target=receive, args=(client_socket,)).start()     # Making a thread for sending
    threading.Thread(target=send, args=(client_socket,)).start()        # Making a thread for receiving

