import socket
import threading
import time
import sys

shutdown_event = threading.Event()

# Function to receive messages from server
def receive_messages(client_socket, username):
    while not shutdown_event.is_set():
        try:
            # ===== Receive message from server ============================================================
            message = client_socket.recv(1024).decode('utf-8')
            
            if not message:
                print("\nServer has disconnected.")
                shutdown_event.set()
                break
            
            else:
                print(f"\n{message}")
                
                sys.stdout.write(f"{username}: ")
                sys.stdout.flush() #clear the keyboard
                
        except Exception as e:
            print(f"Error: {e}")
            shutdown_event.set()
            break
    
# Main function
def main():
    # Client configuration
    host = 'localhost'
    port = 8888

    # Create client socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    # A boolean to state : 
    # i. Whether username has been keyed in (properly)
    # ii. Whether a user has disconnected
    handshake = False

    while not handshake:
        # Receive username prompt from server
        username = input(client_socket.recv(1024).decode('utf-8'))

        # Send username to server
        client_socket.sendall(username.encode('utf-8'))

        # To verify whether username has been accepted
        handshake = client_socket.recv(1024).decode('utf-8').lower() == 'true'
        client_socket.sendall(str(handshake).encode('utf-8'))

    # Start thread to receive messages from server
    receive_thread = threading.Thread(target=receive_messages, args=(client_socket, username))
    receive_thread.start()

    while not shutdown_event.is_set():
        try:
            # ===== Prepare message to send ============================================================
            message = input()
            if message == '':
                message = ' '
                client_socket.sendall(message.encode('utf-8'))
            else:
                client_socket.sendall(message.encode('utf-8'))

        except Exception as e:
            print(f"Error: {e}")
            shutdown_event.set()
            break


    # Wait for the receiving thread to finish
    receive_thread.join()

    # Cleanup: Close the socket after the receive thread has finished
    client_socket.close()
    print("Connection closed.")

if __name__ == "__main__":
    main()
