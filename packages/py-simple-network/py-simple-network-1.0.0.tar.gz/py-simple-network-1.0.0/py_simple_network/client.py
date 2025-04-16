import socket
from abc import abstractmethod
from threading import Thread

class Client:
    def __init__(self, ip:str, port:int, bufsize:int):
        self.ip = ip
        self.port = port
        self.bufsize = bufsize
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            self.socket.connect((self.ip, self.port))
        except ConnectionRefusedError:
            raise ConnectionError(f'Error: Could not connect to server {self.ip}:{self.port}')
        except Exception as e:
            raise RuntimeError(f'Error connecting to server: {e}')

    @abstractmethod
    def process(self, data:str):
        print(data)

    def send_data(self, data:str):
        try:
            self.socket.send(data.encode())
        except BrokenPipeError:
            raise ConnectionError('Error: Lost connection while sending data.')
        except Exception as e:
            raise RuntimeError(f'Error sending data: {e}')

    def __receive_data(self):
        try:
            while True:
                data = self.socket.recv(self.bufsize)
                if not data:
                    break
                self.process(data.decode())
        except ConnectionResetError:
            raise ConnectionError('Error: Connection to the server was closed unexpectedly.')
        except Exception as e:
            raise RuntimeError(f'Error receiving data: {e}')

    def run(self):
        Thread(target=self.__receive_data).start()