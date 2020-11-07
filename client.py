import socket
import threading
from datetime import datetime

stop_threads = False
class Client:

	def __init__(self):
		self.create_connection()

	# menginisiasi koneksi client
	def create_connection(self):
		self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		
		# membuat koneksi dengan server yang sedang berjalan
		while 1:
			try:
				host = "127.0.0.1"
				port = 1234
				self.s.connect((host,port))
				
				break
			except:
				print("Couldn't connect to server")

		# menentukan username
		self.username = input('Enter username --> ')
		self.s.send(self.username.encode())

		# pesan inisiasi
		print("Hello! Welcome to the chatroom.")
		print("1. Simply type the message to send broadcast to all active clients")
		print("2. Type '@username<space>yourmessage' without quotes to send message to desired client")
		print("3. Type 'WHOISIN' without quotes to see list of active clients")
		print("4. Type 'LOGOUT to log off from the server\n")
		
		# thread untuk menghandle pesan masuk
		message_handler = threading.Thread(target=self.handle_messages,args=())
		message_handler.start()

		# thread untuk menghandle pesan keluar
		input_handler = threading.Thread(target=self.input_handler,args=())
		input_handler.start()

	# fungsi untuk menghandle pesan masuk
	def handle_messages(self):
		while 1:
			global stop_threads
			if stop_threads:
				break
			print(self.s.recv(1204).decode())

	# fungsi untuk menghandle pesan keluar
	def input_handler(self):
		while 1:
			global stop_threads
			if stop_threads:
				break
			input_user = input()
			if input_user == "LOGOUT":
				self.s.send((f"{datetime.now().strftime('%H:%M:%S')} {self.username}: {input_user}").encode())
				stop_threads = True
				self.s.close()
			else:
				self.s.send((f"{datetime.now().strftime('%H:%M:%S')} {self.username}: {input_user}").encode())

client = Client()

### Sumber benchmark code: https://github.com/TomPrograms/Python-Internet-Chat-Room