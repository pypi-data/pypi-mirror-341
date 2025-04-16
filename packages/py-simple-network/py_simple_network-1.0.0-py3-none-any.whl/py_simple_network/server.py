import socket
from threading import Thread

class Server:
    def __init__(self, ip:str, port:int, backlog:int, bufsize:int):
        self.ip = ip
        self.port = port
        self.backlog = backlog
        self.bufsize = bufsize
        self.clients = []
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __broadcast(self, data:bytes, sender:socket.socket):
        for client in self.clients:
            if client != sender:
                try:
                    client.send(data)
                except BrokenPipeError:
                    raise ConnectionError(f'Error: Failed to send data to {client.getpeername()}.')

    def __handle_clients(self, client:socket.socket, address:tuple):
        self.clients.append(client)
        try:
            while True:
                data = client.recv(self.bufsize)
                if not data:
                    break
                self.__broadcast(data, client)
        except ConnectionResetError:
            raise ConnectionError(f'Error: Client {address} disconnected unexpectedly.')
        except Exception as e:
            raise RuntimeError(f'Error processing client {address} data: {e}')
        finally:
            self.clients.remove(client)
            client.close()

    def run(self):
        try:
            self.socket.bind((self.ip, self.port))
            self.socket.listen(self.backlog)
        except Exception as e:
            raise RuntimeError(f'Error starting the server: {e}')

        while True:
            try:
                client, address = self.socket.accept()
                Thread(target=self.__handle_clients, args=(client, address)).start()
            except Exception as e:
                raise ConnectionError(f'Error accepting connection: {e}')