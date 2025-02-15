import socket
import threading

HOST = "0.0.0.0"  # Listen on all interfaces
PORT = 5000

clients = {}
lock = threading.Lock()

def handle_client(client, addr):
    try:
        username = client.recv(1024).decode()
        with lock:
            if username in clients:
                client.send("Username already taken!".encode())
                client.close()
                return
            clients[username] = client
            print(f"{username} joined from {addr}")

        # Notify all users
        broadcast(f"{username} has joined the chat!", "Server")

        while True:
            msg = client.recv(1024).decode()
            if not msg or msg.lower() == "exit":
                break
            broadcast(msg, username)
        
    except:
        pass
    finally:
        with lock:
            del clients[username]
        print(f"{username} left the chat")
        broadcast(f"{username} has left the chat", "Server")
        client.close()

def broadcast(msg, sender):
    with lock:
        for user, conn in clients.items():
            try:
                conn.send(f"{sender}: {msg}".encode())
            except:
                conn.close()
                del clients[user]

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f"Server started on {HOST}:{PORT}")

    while True:
        client, addr = server.accept()
        threading.Thread(target=handle_client, args=(client, addr)).start()

if __name__ == "__main__":
    start_server()
