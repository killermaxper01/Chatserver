import socket
import threading

HOST = "0.0.0.0"  # Allows LAN connection, change to "127.0.0.1" for local-only
PORT = 5000

clients = {}

def handle_client(client, address):
    try:
        client.send("Enter your username: ".encode())
        username = client.recv(1024).decode().strip()

        if not username or username in clients:
            client.send("ERROR: Username already taken!\n".encode())
            client.close()
            return
        
        clients[username] = client
        print(f"[INFO] {username} joined from {address}")
        
        broadcast(f"[SERVER] {username} has joined the chat!", "Server")

        while True:
            msg = client.recv(1024).decode().strip()
            if not msg or msg.lower() == "exit":
                break
            broadcast(msg, username)
    
    except:
        pass
    finally:
        if username in clients:
            del clients[username]
        broadcast(f"[SERVER] {username} has left the chat!", "Server")
        client.close()

def broadcast(message, sender):
    for user, conn in clients.items():
        try:
            conn.send(f"{sender}: {message}\n".encode())
        except:
            conn.close()
            del clients[user]

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)
    print(f"[SERVER] Running on {HOST}:{PORT}")

    while True:
        client, address = server.accept()
        threading.Thread(target=handle_client, args=(client, address)).start()

if __name__ == "__main__":
    start_server()
