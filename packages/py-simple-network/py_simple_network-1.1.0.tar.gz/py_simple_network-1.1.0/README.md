# py-simple-network Library

A simple Python library for TCP-based client-server communication.

## Installation
Install the library using pip:
```bash
pip install py-simple-network
```

## Usage

### Server
```bash
from py_simple_network import Server

server = Server(ip='127.0.0.1', port=8080, backlog=5, bufsize=1024)
server.run()
```

### Client
```bash
from py_simple_network import Client

class MyClient(Client):
    def process(self, data:str):
        print(f'Received: {data}')

client = MyClient(ip='127.0.0.1', port=8080, bufsize=1024)
client.run()
client.send_data('Hello, Server!')
```