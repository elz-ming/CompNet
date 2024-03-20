import socket
import threading

# Client.py initiated
# |-> Enter username (John)
#     |-> Enter message (xyz, where xyz is a string message)
#     |-> Enter command (@xyz, where xyz is a string command)
#         |-> @quit
#         |-> @names
#         |-> @<username> xyz (where username is a list of username in server, xyz is a string message)
#         |-> @group
#             |-> set group xyz (where ggg is a string groupname, xyz is a string of users)
#             |-> send xyz (where xyz is a string message)
#             |-> delete <group>
#             |-> leave <group>

# Function to handle client connections
def handle_client(client_socket, clients, client_username, group_socketList, username_groupName):
    # A boolean to state : 
    # i. Whether username has been keyed in (properly)
    # ii. Whether a user has disconnected
    handshake = False
    first_run = True

    # Requirment 2 - Prompt until a non-duplicate name is inserted
    while not handshake:
        if first_run:
            client_socket.sendall("[Enter your name: ]".encode('utf-8'))
            first_run = False
        else:
           client_socket.sendall("[Username has already been used. Please enter another name: ]".encode('utf-8')) 
        username = client_socket.recv(1024).decode('utf-8').strip()

        if username not in client_username.values():
            handshake = True

        client_socket.sendall(str(handshake).encode('utf-8'))
        handshake = client_socket.recv(1024).decode('utf-8').lower() == 'true'
    
    client_username[client_socket] = username

    # Add client to list
    clients.append(client_socket)

    # Requirement 1a - Welcome the user, e.g. [Welcome John!]
    client_socket.sendall(f"[Welcome {client_username[client_socket]}!]".encode('utf-8'))
    # Requirement 1b - Shows user joined, e.g. [John joined]
    for client in clients:
        if client != client_socket:
            client.sendall(f"[{client_username[client_socket]} joined]".encode('utf-8'))

    
    
    #while handshake:
    while True:
        try:
            # Receive message from client
            message = client_socket.recv(1024).decode('utf-8')
            print(message)
            username = client_username[client_socket]
            
            # If client is sending a command
            if message[0] == "@":
                command, *rest = message[1:].split(maxsplit=1)  # Extract command and the rest of the message
                user_message = " ".join(rest) if rest else ""  # Join the rest back if it exists, otherwise empty string

                # 1st Command - QUIT
                if command == "quit":
                    print(f"User {username} exited")

                    # Inform other clients that this client has quit
                    for client in clients:
                        if client != client_socket:
                            client.sendall(f"[{username} exited]".encode('utf-8'))
                    break  # Exit the loop and proceed to disconnect the client
            
                # 2nd Command - NAMES
                elif command == "names":
                    client_socket.sendall(f"[Connected users: {', '.join(list(client_username.values()))}]".encode('utf-8'))
 
                # 4th Command - GROUP Functions
                elif command == "group":
                    second_command = message.split(" ")[1]

                    # 4.1 - GROUP SET
                    if second_command == "set":
                        group_name = message.split(" ")[2]
                        group_members = message.split(" ")[3:]
                        group_members = " ".join(group_members)
                        group_members = group_members.split(", ")
                        group_members_sockets = [key for key, value in client_username.items() if value in group_members]
                        
                        # To ensure the creator is in the group too
                        if client_socket not in group_members_sockets:
                            group_members_sockets.append(client_socket)

                        # To assign groupname to a list of user
                        group_socketList[group_name] = group_members_sockets
                        
                        # To tie the member to a group
                        for member in group_members:
                            if member not in username_groupName:
                                username_groupName[member] = group_name

                        # To send success message to all members of a group
                        for client in group_socketList[group_name]:
                            client.sendall(f"[You are enrolled in the {group_name} group]".encode('utf-8'))

                    elif second_command == "send":
                        if username not in username_groupName:
                            client_socket.sendall(f"[You are not enrolled in any groups!]".encode('utf-8'))
                        else:
                            message = message.split(" ")[3:]
                            message = " ".join(message)

                            group_name = username_groupName[username]
                            for client in group_socketList[group_name]:
                                if client != client_socket:
                                    client.sendall(f"[{group_name}:] {message}".encode('utf-8'))

                    elif second_command == "delete":
                        if username not in username_groupName:
                            client_socket.sendall(f"[You are not enrolled in any groups!]".encode('utf-8'))
                        else:
                            group_name = message.split(" ")[3]
                            if group_name not in group_socketList.keys():
                                client_socket.sendall(f"[The group {group_name} does not exist!]".encode('utf-8'))
                            else:
                                group_members_sockets = group_socketList[group_name]
                                for client in group_members_sockets:
                                    client.sendall(f"[The group {group_name} has been deleted!]".encode('utf-8'))

                                group_members = [client_username[key] for key in group_members_sockets]
                                for member in group_members:
                                    del username_groupName[member]
                                
                                del group_members_sockets[group_name]


                    elif second_command == "leave":
                        if username not in username_groupName:
                            client_socket.sendall(f"[]".encode('utf-8'))
                        else:
                            group_name = message.split(" ")[3]
                            if group_name == username_groupName[username]:
                                client_socket.sendall(f"[You have successfully left the group {group_name}]".encode('utf-8'))
                                del username_groupName[username]

                                group_members_sockets[group_name].remove(client_socket)

                    else:
                        client_socket.sendall(f"Invalid command!".encode('utf-8'))
            
                # 3rd Command - PRIVATE MESSAGE
                elif command in client_username.values():
                    # Check if the target username exists among connected clients
                    target_sockets = [key for key, value in client_username.items() if value == command] 
                        # If there's a message provided and the username exists
                    if target_sockets: #check if user exists
                        target_socket = target_sockets[0]
                        if user_message:  # check if there is a message provided
                            target_socket.sendall(f"[{username}:] {user_message}".encode('utf-8'))
                        else: # User not found
                            print(f"Sending error message1 to {username}")
                            client_socket.sendall(f"[No message provided.]".encode('utf-8')) #this works
                else: #user not found
                    print(f"Sending error message2 to {username}")
                    client_socket.sendall(f"[User '{command}' not found.]".encode('utf-8'))


            elif message == ' ':
                client_socket.sendall(f"Invalid input!".encode('utf-8'))
            
            # If client is sending a message
            else:
                # Broadcast message to all clients
                for client in clients:
                    if client != client_socket:
                        client.sendall(f"[{client_username[client_socket]}:] {message}".encode('utf-8'))
        
        
        except Exception as e:
            print(f"Error: {e}")
            break

    # Remove client from list and close connection
    clients.remove(client_socket)
    client_socket.close()
    del client_username[client_socket]

# Main function
def main():
    # Server configuration
    host = 'localhost'
    port = 8888

    # Create server socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    server_socket.settimeout(1)

    print(f"[*] Listening on {host}:{port}")

    # A list of client sockets
    clients = []

    # A dictionary of client_socket:username
    client_username = {}

    # A dictionary of groupname:list(client_socket)
    group_socketList = {}

    # A dictionary of username:groupName
    username_groupName = {}

    #dict for groupnames

    listening = True
    try:
        while listening:
            try:
                # Accept client connection
                client_socket, addr = server_socket.accept()
                print(f"[*] Accepted connection from {addr[0]}:{addr[1]}")

                # Create thread to handle client
                client_thread = threading.Thread(target=handle_client, args=(client_socket, clients, client_username, group_socketList, username_groupName))
                client_thread.start()

            except socket.timeout:
                pass

    except KeyboardInterrupt:
        print("Shutting down server...")
        listening = False

    for client in clients:
        client.close()
    server_socket.close() 
    print("Server successfully shut down.")

if __name__ == "__main__":
    main()
