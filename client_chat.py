import socket
import threading

SERVER_IP = "127.0.0.1"  # Change this to the server's IP if running on LAN
SERVER_PORT = 5000

def receive_messages(sock):
    while True:
        try:
            msg = sock.recv(1024).decode().strip()
            if not msg:
                break
            print(msg)
        except:
            break

def start_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((SERVER_IP, SERVER_PORT))

    username = input("Enter a unique username: ")
    client.send(username.encode())

    server_response = client.recv(1024).decode()
    if "ERROR" in server_response:
        print(server_response)
        client.close()
        return

    print("Connected! Type messages or 'exit' to leave.")

    threading.Thread(target=receive_messages, args=(client,), daemon=True).start()

    while True:
        msg = input()
        if msg.lower() == "exit":
            break
        client.send(msg.encode())

    client.close()

if __name__ == "__main__":
    start_client()
