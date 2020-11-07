import socket
import threading
from datetime import datetime

class Server:
    def __init__(self):
        self.start_server()

    # menginisiasi server
    def start_server(self):

        # melakukan bind ip dan port untuk server
        host = "127.0.0.1"
        port = 1234
        self.s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.s.bind((host,port))
        
        # list untuk menyimpan username dan address client
        self.clients = []
        self.usernames = []

    
        print('Running on host: '+str(host))
        print('Running on port: '+str(port))

        # thread untuk menghandle pesan dari client
        threading.Thread(target=self.handle_client).start()

    # fungsi untuk melakukan broadcast ke semua client
    def broadcast(self,msg):
        for c in self.clients:
            self.s.sendto(msg.encode(),c)

    # fungsi untuk menghandle pesan dari client
    def handle_client(self):
        while True:
            msg, client = self.s.recvfrom(1024)

            # jika belum pernah connect, maka akan dimasukan ke list address client dan username dan dilakukan broadcast
            if client not in self.clients:
                if msg not in self.usernames:
                    self.usernames.append(msg.decode())
                    self.clients.append(client)
                    print(f'{datetime.now().strftime("%H:%M:%S")} *** {msg.decode()} has joined the chatroom. ***')
                    self.broadcast(f'{datetime.now().strftime("%H:%M:%S")} New person joined the room. Username: {msg.decode()}')

            else:
                decoded_message = msg.decode()
                msg_lst = decoded_message.split()

                if decoded_message != '':
                    print(str(decoded_message))
                    
                    # menghandle fitur private message
                    if "@" in decoded_message:
                        try:
                            username_tujuan = msg_lst[2][1::]
                            idx_username = self.usernames.index(username_tujuan)
                            client_tujuan = self.clients[idx_username]
                            msg_lst_temp = msg_lst
                            msg_lst_temp.remove(msg_lst[2])
                            private_message = f"(private) {' '.join(msg_lst_temp)}"
                            self.s.sendto(private_message.encode(), client_tujuan)
                        except:
                            err_msg = f"{datetime.now().strftime('%H:%M:%S')} Username tidak ada pada chatroom"
                            self.s.sendto(err_msg.encode(), client)

                    # menghandle fitur logout
                    elif "LOGOUT" in decoded_message:
                        idx_client_logout = self.clients.index(client)
                        username_logout = self.usernames[idx_client_logout]
                        self.clients.remove(client)
                        self.usernames.remove(username_logout)
                        for c in self.clients:
                            msg_logout = f"{datetime.now().strftime('%H:%M:%S')} *** {username_logout} has left the chatroom. ***"
                            self.s.sendto(msg_logout.encode(), c)

                    # menghandle fitur lihat active user
                    elif "WHOISIN" in decoded_message:
                        lst_username = []
                        lst_username.append(f"{datetime.now().strftime('%H:%M:%S')} User yang aktif pada chatroom:")
                        num = 1
                        for user in self.usernames:
                            lst_username.append(str(num) + ". " + user)
                            num+=1
                            
                        seluruh_username = ("\n").join(lst_username)
                        self.s.sendto(seluruh_username.encode(), client)
                    else:
                        for c in self.clients:
                            if c != client:
                                self.s.sendto(msg, c)
                        
# inisiasi
server = Server()

### Sumber benchmark code: https://github.com/TomPrograms/Python-Internet-Chat-Room