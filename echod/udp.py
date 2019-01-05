import .base
import socket

class UDPServer(base.BaseServer):
    max_buffer_size = 1024

    def __init__(self, server_address, version, HandlerClass):
        super().__init__(server_address,
                         version,
                         socket.SOCK_DGRAM,
                         HandlerClass)

    def accept_connection(self):
        data, _ = self.socket.recvfrom(self.max_buffer_size)
        return (self.socket, data)
