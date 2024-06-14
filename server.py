import socket
import threading
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Server Configuration
host = '172.30.4.145'
port = 55555

# Start Server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []
nicknames = []
lock = threading.Lock()

def broadcast(message):
    with lock:
        for client in clients:
            try:
                client.send(message)
            except socket.error as e:
                logging.error(f"Error sending message to client: {e}")

def handle(client):
    while True:
        try:
            message = client.recv(1024)
            if not message:
                raise socket.error("Client disconnected")
            broadcast(message)
        except socket.error as e:
            logging.error(f"Error receiving message: {e}")
            with lock:
                index = clients.index(client)
                clients.remove(client)
                client.close()
                nickname = nicknames.pop(index)
                broadcast(f'{nickname} left!'.encode('utf-8'))
            break

def receive():
    while True:
        try:
            client, address = server.accept()
            logging.info(f'Connected with {address}')

            client.send('NICK'.encode('utf-8'))
            nickname = client.recv(1024).decode('utf-8')
            with lock:
                nicknames.append(nickname)
                clients.append(client)

            logging.info(f'Nickname is {nickname}')
            broadcast(f'{nickname} joined!'.encode('utf-8'))
            client.send('Connected to server!'.encode('utf-8'))

            thread = threading.Thread(target=handle, args=(client,))
            thread.start()
        except socket.error as e:
            logging.error(f"Error accepting connections: {e}")

def main():
    logging.info('Server is listening...')
    try:
        receive()
    except KeyboardInterrupt:
        logging.info("Server is shutting down.")
        server.close()

if __name__ == "__main__":
    main()
