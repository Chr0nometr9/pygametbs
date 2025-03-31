import socket
import threading
from json import dumps

class Server:
    def __init__(self):
        self.players = {}
        self.user_threads = []
        self.__running = True
        self.server_socket = None

    def handle_client(self, client_socket: socket.socket, addr):
        with client_socket:
            print(f"Користувач {addr} під'єднаний до серверу\n> ", end='')
            
            login = client_socket.recv(1024).decode()
            self.players[login] = [400, 500]

            client_socket.settimeout(0.01)
            while self.__running:
                try:
                    try:
                        client_socket.sendall(dumps(self.players).encode())
                    except (BrokenPipeError, ConnectionResetError):
                        break
                    data = client_socket.recv(1024)
                    if data == b'close':
                        break
                    elif data == b'left':
                        self.players[login][0] -= 10
                    elif data == b'right':
                        self.players[login][0] += 10
                    elif data == b'up':
                        self.players[login][1] -= 10
                    elif data == b'down':
                        self.players[login][1] += 10
                except socket.timeout:
                    continue
                except Exception as e:
                    print(f"Помилка з {addr}: {e}\n> ", end='')
                    break
            del self.players[login]
            print(f"Користувач {addr} від'єднаний\n> ", end='')

    def console(self):
        while True:
            cmd = input("> ")
            if cmd == 'stop':
                self.__running = False
                if self.server_socket:
                    self.server_socket.close()
                for thread in self.user_threads:
                    thread.join()
                print("Сервер зупинено")
                return
            elif cmd == 'show':
                print(self.players)

    def serve(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(('26.159.171.202', 8001))
        self.server_socket.listen(5)
        print("Сервер запущено!\n> ", end='')
        while self.__running:
            try:
                client_socket, addr = self.server_socket.accept()
                thread = threading.Thread(target=self.handle_client, args=(client_socket, addr))
                self.user_threads.append(thread)
                thread.start()
            except Exception as e:
                if self.__running:
                    print(f"Помилка прийому з'єднання: {e}\n> ", end='')
        self.server_socket.close()
        print("Серверний сокет закрито")


server = Server()
server_thread = threading.Thread(target=server.serve)
console_thread = threading.Thread(target=server.console)

server_thread.start()
console_thread.start()

server_thread.join()
console_thread.join()