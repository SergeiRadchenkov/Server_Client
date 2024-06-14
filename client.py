import socket
import threading
import logging

import socket
import threading
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Choosing Nickname
nickname = input("Choose your nickname: ")

# Connecting To Server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    client.connect(('178.124.159.252', 5555))
except socket.error as e:
    logging.error(f"Connection error: {e}")
    exit()

def receive():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message == 'NICK':
                client.send(nickname.encode('utf-8'))
            else:
                logging.info(message)
        except socket.error as e:
            logging.error(f"Receiving error: {e}")
            client.close()
            break
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            client.close()
            break

def write():
    while True:
        try:
            message = '{}: {}'.format(nickname, input(''))
            client.send(message.encode('utf-8'))
        except socket.error as e:
            logging.error(f"Sending error: {e}")
            client.close()
            break
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            client.close()
            break

# Starting Threads For Listening And Writing
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
