import cv2
import socket
import pickle

# Receiver IP and Port
receiver_ip = "192.168.1.42"
receiver_port = 9000

# Create socket
receiver_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
receiver_socket.bind((receiver_ip, receiver_port))
receiver_socket.listen(1)

# Accept connection
conn, addr = receiver_socket.accept()

while True:
    # Receive encoded frame
    encoded_frame = b""
    while True:
        chunk = conn.recv(4096)
        if not chunk:
            break
        encoded_frame += chunk
    # Decode frame
    frame = pickle.loads(encoded_frame)
    # Display frame
    cv2.imshow('Received Frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
