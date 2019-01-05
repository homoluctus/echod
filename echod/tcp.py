import .base
import socket

class TCPServer(base.BaseServer):
    connection_queue_size = 5

    def __init__(self, server_address, version, HandlerClass):
        super().__init__(server_address,
                         version,
                         socket.SOCK_STREAM,
                         HandlerClass)

    def listen(self):
        self.socket.listen(self.connection_queue_size)

    def accept_connection(self):
        return self.socket.accept()

    def close_connection(self, connection):
        connection.close()
