import sys
import socket

HOST = '127.0.0.1'  # Standard loop-back interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

while True:
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		s.bind((HOST, PORT))
		
		print('Start listen')
		s.listen()
		conn, addr = s.accept()

		with conn:
			print('Connected by', addr)
			while True:
				input_data = conn.recv(1024)
				if not input_data:
					break

				output_data = "Odebrałem: " + input_data + " - serwis" 
					
				conn.sendall(output_data.encode())