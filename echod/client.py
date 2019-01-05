import sys
import socket

from .utils import Version, validate_address


class SocketClient:
    def __init__(self,
                 callback,
                 server_address,
                 protocol,
                 version,
                 active=False):

        self._callback = callback
        self.server_address = server_address
        self.socket_type = self._get_socket_type(protocol)
        self.address_family = getattr(socket, Version(version).name)

        try:
            validate_address(self.server_address[0],
                             self.server_address[1],
                             version)
        except (ValueError, TypeError):
            raise

        self.socket = socket.socket(family=self.address_family,
                                    type=self.socket_type)

        if active:
            self.run()

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.stop()

    def stop(self):
        self.socket.close()

    def _get_socket_type(self, protocol):
        if protocol == 'tcp':
            socket_type = socket.SOCK_STREAM
        else:
            socket_type = socket.SOCK_DGRAM

        return socket_type

    def _connect_tcp_server(self):
        try:
            self.socket.connect(self.server_address)
        except ConnectionRefusedError:
            raise

    def run(self, kwargs={}):
        if self.socket_type == socket.SOCK_STREAM:
            try:
                self._connect_tcp_server()
            except:
                self.stop()
                raise

        try:
            self._callback(self.socket, kwargs)
        except:
            raise
