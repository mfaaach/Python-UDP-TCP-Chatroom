import socket
import threading
from datetime import datetime

class Server:
	def __init__(self):
		self.start_server()

	# menginisiasi server
	def start_server(self):

		# melakukan bind ip dan port untuk server
		self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		host = "127.0.0.1"
		port = 1234
		self.s.bind((host,port))
		self.s.listen(100)

		# list untuk menyimpan koneksi client
		self.clients = []

		print('Running on host: '+str(host))
		print('Running on port: '+str(port))

		# dictionary untuk menyimpan username dan koneksi
		self.username_lookup = {}
		self.connection_lookup = {}

		while True:

			# menerima koneksi awal dari suatu client dan menambahakn pada daftar client
			c, addr = self.s.accept()
			username = c.recv(1024).decode()

			print(f'{datetime.now().strftime("%H:%M:%S")} *** {str(username)} has joined the chatroom. ***')
			self.broadcast(f'{datetime.now().strftime("%H:%M:%S")} New person joined the room. Username: {username}')

			self.username_lookup[c] = username
			self.connection_lookup[username] = c

			self.clients.append(c)
			
			# thread untuk menghandle pesan dari client
			threading.Thread(target=self.handle_client,args=(c,addr,)).start()

	# fungsi untuk melakukan broadcast ke client yang active
	def broadcast(self,msg):
		for connection in self.clients:
			connection.send(msg.encode())

	# fungsi untuk menghandle pesan dari client
	def handle_client(self,c,addr):
		while True:
			try:
				msg = c.recv(1024)
			except:
				c.shutdown(socket.SHUT_RDWR)
				self.clients.remove(c)
				
				print(str(self.username_lookup[c])+' left the room.')
				self.broadcast(str(self.username_lookup[c])+' has left the room.')

				break

			decoded_message = msg.decode()
			msg_lst = decoded_message.split()

			if decoded_message != '':
				print(str(decoded_message))
				
				# menghandle fitur private message
				if "@" in decoded_message:
					try:
						username_tujuan = msg_lst[2][1::]
						connection_tujuan = self.connection_lookup[username_tujuan]
						msg_lst_temp = msg_lst
						msg_lst_temp.remove(msg_lst[2])
						private_message = f"(private) {' '.join(msg_lst_temp)}"
						connection_tujuan.send(private_message.encode())
					except:
						err_msg = f"{datetime.now().strftime('%H:%M:%S')} Username tidak ada pada chatroom"
						c.send(err_msg.encode())

				# menghandle fitur logout
				elif "LOGOUT" in decoded_message:
					username_logout = self.username_lookup[c]
					del self.username_lookup[c]
					del self.connection_lookup[username_logout]
					self.clients.remove(c)
					for connection in self.clients:
						msg_logout = f"{datetime.now().strftime('%H:%M:%S')} *** {username_logout} has left the chatroom. ***"
						connection.send(msg_logout.encode())

				# menghandle fitur active user
				elif "WHOISIN" in decoded_message:
					lst_username = []
					lst_username.append(f"{datetime.now().strftime('%H:%M:%S')} User yang aktif pada chatroom:")
					num = 1
					for user in self.connection_lookup:
						lst_username.append(str(num) + ". " + user)
						num+=1
						
					seluruh_username = ("\n").join(lst_username)
					c.send(seluruh_username.encode())
				else:
					for connection in self.clients:
						if connection != c:
							connection.send(msg)
						

server = Server()

### Sumber benchmark code: https://github.com/TomPrograms/Python-Internet-Chat-Room