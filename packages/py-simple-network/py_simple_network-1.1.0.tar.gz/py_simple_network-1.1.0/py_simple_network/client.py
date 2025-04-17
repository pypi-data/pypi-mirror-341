import socket
from abc import abstractmethod
from threading import Thread
import json

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
        pass

    def send_data(self, data:str):
        try:
            self.socket.send((data + '\n').encode())
        except BrokenPipeError:
            raise ConnectionError('Error: Lost connection while sending data.')
        except Exception as e:
            raise RuntimeError(f'Error sending data: {e}')

    def __receive_data(self):
        try:
            buffer = ''
            while True:
                data = self.socket.recv(self.bufsize).decode()
                if not data:
                    break

                buffer += data
                while '\n' in buffer:
                    line, buffer = buffer.split('\n', 1)
                    data = json.loads(line)

                self.process(json.dumps(data))
        except ConnectionResetError:
            raise ConnectionError('Error: Connection to the server was closed unexpectedly.')
        except Exception as e:
            raise RuntimeError(f'Error receiving data: {e}')

    def run(self):
        Thread(target=self.__receive_data).start()