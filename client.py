import socket
import pickle
import time

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
host = '172.16.89.144'  # Replace 'server_ip' with the IP address of the server
port = 12345         # Same port as used by the server
client_socket.connect((host, port))

# Receive data from the server
received_data = client_socket.recv(4096)

# Deserialize the received data (assuming it's pickled)
received_data_decoded = pickle.loads(received_data)

print("Received data:", received_data_decoded)

# Close the connection
client_socket.close()

