import socket
import threading
import json

class NetworkChatServer:
    def __init__(self, host='localhost', port=12345):
        self.host = host
        self.port = port
        self.clients = {}
        self.server_socket = None
        self.running = False
        self.lock = threading.Lock()

    def start_server(self):
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(10)
            self.running = True
            print(f"Server started on {self.host}:{self.port}")
            print("Waiting for client connections...")

            while self.running:
                client_socket, client_address = self.server_socket.accept()
                threading.Thread(target=self.handle_client, args=(client_socket, client_address), daemon=True).start()
        except OSError as e:
            if e.errno == 10048: # Address already in use
                 print(f"ERROR: Port {self.port} is already in use.")
            else:
                 print(f"Server error: {e}")
        except Exception as e:
            print(f"An unexpected server error occurred: {e}")
        finally:
            self.shutdown()

    def handle_client(self, client_socket, client_address):
        username = None
        try:
            data = client_socket.recv(1024).decode('utf-8')
            username = json.loads(data)['username']
            
            with self.lock:
                self.clients[client_socket] = username
            
            print(f"{username} has connected from {client_address}.")
            
            join_message = json.dumps({'sender': 'Server', 'original_text': f"{username} has joined the chat."})
            self.broadcast_message(join_message.encode('utf-8'), client_socket)

            while self.running:
                data = client_socket.recv(4096)
                if not data:
                    break
                self.broadcast_message(data, client_socket)
        except (ConnectionResetError, json.JSONDecodeError):
             pass # Client disconnected abruptly or sent invalid data
        except Exception as e:
            print(f"Error with client {username or 'unknown'}: {e}")
        finally:
            with self.lock:
                if client_socket in self.clients:
                    username = self.clients.pop(client_socket)
                    print(f"{username} has disconnected.")
                    leave_message = json.dumps({'sender': 'Server', 'original_text': f"{username} has left the chat."})
                    self.broadcast_message(leave_message.encode('utf-8'), None)
            client_socket.close()

    def broadcast_message(self, message, sender_socket):
        with self.lock:
            # Iterate over a copy of the keys to allow safe modification
            for client_socket in list(self.clients.keys()):
                if client_socket != sender_socket:
                    try:
                        client_socket.send(message)
                    except:
                        # On failure, assume client disconnected and remove them
                        client_socket.close()
                        if client_socket in self.clients:
                            self.clients.pop(client_socket)

    def shutdown(self):
        self.running = False
        with self.lock:
            for client_socket in self.clients:
                client_socket.close()
        if self.server_socket:
            self.server_socket.close()
        print("Server has been shut down.")

if __name__ == "__main__":
    server = NetworkChatServer()
    try:
        server.start_server()
    except KeyboardInterrupt:
        print("\nServer shutdown initiated by user.")
        server.shutdown()