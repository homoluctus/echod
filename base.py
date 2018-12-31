import sys
import socket
import ipaddress
from enum import Enum

from utils import validate_address

class Version(Enum):
    AF_INET = 4
    AF_INET6 = 6

    def __str__(self):
        return '{}: IPv{}'.format(self.name, self.value)

class BaseServer:
    def __init__(self,
                 server_address,
                 version,
                 socket_type,
                 HandlerClass,
                 active=True):
        """
        :param server_address: tuple of host address and port
        :param version: IP version (4 or 6)
        :param protocol: Layer 4 protocol (TCP or UDP)
        :param HandlerClass: Class to handle, send and receive data
        :param active: Boolean to activate server
        """

        self.server_address = server_address
        self._version = version

        try:
            validate_address(self.server_address[0], self.server_address[1], version)
        except:
            raise

        self.__shutdown_flag = False
        self.__preparation_for_acceptance = False
        self.HandlerClass = HandlerClass

        self.address_family = getattr(socket, Version(version).name)
        self.socket_type = socket_type
        self.socket = socket.socket(self.address_family,
                                    self.socket_type)

        if active:
            try:
                self.bind()
                self.listen()
                self.__preparation_for_acceptance = True
            except:
                self.stop()
                raise

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.stop()

    @property
    def version(self):
        return str(Version(self._version))

    def start(self):
        self.start_connection()

    def bind(self):
        self.socket.bind(self.server_address)

    def listen(self):
        """
        Overriden by TCPServer subclass
        """
        pass
    
    def stop(self):
        self.__shutdown_flag = True
        self.stop_server()

    def stop_server(self):
        """
        Overriden threading class
        """

        self.socket.close()

    def start_connection(self):
        if self.__preparation_for_acceptance:
            while not self.__shutdown_flag:
                self._handle_connection()

    def _handle_connection(self):
        try:
            connection, client_address = self.accept_connection()
        except:
            raise

        try:
            self.start_process(connection, client_address)
        except:
            self.handle_process_error(client_address)
        finally:
            self.close_connection(connection)
            self.__shutdown_flag = True

    def accept_connection(self):
        """
        Return a pair (connection, client address)
        where connection is a socket object (and data if UDP)
        """
        pass

    def start_process(self, connection, client_address):
        """
        Overriden by threading class
        """

        self.handle_process(connection, client_address)

    def handle_process(self, connection, client_address):
        """
        Handle to send and receive data
        """

        self.HandlerClass(connection, client_address)

    def close_connection(self, connection):
        """
        Overriden subclass and threading class
        """
        pass

    def handle_process_error(self, client_address):
        sys.stderr.write('Exception occurred on the connection from {}'.format(client_address))

        from traceback import print_exc
        print_exc(file=sys.stderr)