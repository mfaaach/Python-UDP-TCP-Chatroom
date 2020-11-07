import socket
import threading
from datetime import datetime

# dijalankan ketika ingin log out
stop_threads = False
class Client:
    def __init__(self):
        self.create_connection()

    def create_connection(self):
        # membuat koneksi udp
        self.s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        
        # melakukan bind ip dan port untuk client
        while 1:
            try:
                host = "127.0.0.1"
                port = int(input("Enter port --> "))
                self.s.bind((host,port))
                self.client_address = ('127.0.0.1', port)
                self.server_address = ('127.0.0.1', 1234)
                
                break
            except:
                print("Couldn't connect to server")

        # menentukan username
        self.username = input('Enter username --> ')
        self.s.sendto(self.username.encode(), self.server_address)

        # pesan masuk
        print("Hello! Welcome to the chatroom.")
        print("1. Simply type the message to send broadcast to all active clients")
        print("2. Type '@username<space>yourmessage' without quotes to send message to desired client")
        print("3. Type 'WHOISIN' without quotes to see list of active clients")
        print("4. Type 'LOGOUT to log off from the server\n")
        
        # membuat thread untuk menghandle pesan masuk
        message_handler = threading.Thread(target=self.handle_messages,args=())
        message_handler.start()

        # membuat thread untuk menghandle pesan keluar 
        input_handler = threading.Thread(target=self.input_handler,args=())
        input_handler.start()

    # fungsi untuk menghandle pesan masuk
    def handle_messages(self):
        while 1:
            global stop_threads
            if stop_threads:
                break
            data = self.s.recvfrom(1024)
            message = data[0].decode()
            print(message)

    # fungsi untuk menghandle pesan keluar
    def input_handler(self):
        while 1:
            global stop_threads
            if stop_threads:
                break
            input_user = input()
            # menghandle fitur logout
            if input_user == "LOGOUT":
                self.s.sendto((f"{datetime.now().strftime('%H:%M:%S')} {self.username}: {input_user}").encode(), self.server_address)
                stop_threads = True
                self.s.close()
            else:
                # mengirim pesan ke server yang akan ditujukan ke client lain
                self.s.sendto((f"{datetime.now().strftime('%H:%M:%S')} {self.username}: {input_user}").encode(), self.server_address)

# inisiasi
client = Client()

### Sumber benchmark code : https://github.com/TomPrograms/Python-Internet-Chat-Room