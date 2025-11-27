import socket

HOST = '0.0.0.0'    
PORT = 5001           

file_path = input("Enter the file path to send: ")

with open(file_path, "rb") as f:
    file_data = f.read()

server = socket.socket()
server.bind((HOST, PORT))
server.listen(1)

print("Waiting for connection...")
conn, addr = server.accept()
print(f"Connected to {addr}")

file_name = file_path.split("/")[-1]
conn.send(file_name.encode())
conn.recv(1024)  # Acknowledgement

conn.send(str(len(file_data)).encode())
conn.recv(1024)

conn.sendall(file_data)
print("File sent successfully!")

conn.close()
server.close()
