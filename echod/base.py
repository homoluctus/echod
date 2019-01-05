import sys
import socket
import selectors
from traceback import print_exc

from utils import validate_address, Version


class BaseServer:
    def __init__(self,
                 server_address,
                 version,
                 socket_type,
                 HandlerClass,
                 active=False):
        """
        :param server_address: tuple of host address and port
        :param version: IP version (4 or 6)
        :param protocol: Layer 4 protocol (TCP or UDP)
        :param HandlerClass: Class to handle, send and receive data
        :param active: Boolean to start server
        """

        self.server_address = server_address
        self._version = version

        try:
            validate_address(self.server_address[0],
                             self.server_address[1],
                             version)
        except (ValueError, TypeError):
            raise

        self.__shutdown_flag = False
        self.__continue_flag = True
        self.HandlerClass = HandlerClass

        self.address_family = getattr(socket, Version(version).name)
        self.socket_type = socket_type
        self.socket = socket.socket(self.address_family,
                                    self.socket_type)

        if active:
            try:
                self.start()
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
        try:
            self.bind()
            self.listen()
            self.start_connection()
        except:
            raise

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

    def start_connection(self, timeout=None):
        self.selector = selectors.DefaultSelector()
        self.selector.register(self.socket, selectors.EVENT_READ)

        while not self.__shutdown_flag:
            ready = self.selector.select(timeout)

            if not ready:
                break

            for key, _ in ready:
                self.__continue_flag = True

                if key.fileobj == self.socket:
                    try:
                        self._handle_acceptance()
                    except:
                        print_exc()

                else:
                    self._handle_connection(key.fileobj)

                    if not self.__continue_flag:
                        self.stop_connection(key.fileobj)

        self.selector.close()

    def _handle_acceptance(self):
        connection = self.accept_connection()
        self.selector.register(connection[0], selectors.EVENT_READ)
        print("Accepted from", connection[0].getpeername())

        if connection[0].type == socket.SOCK_DGRAM:
            self._handle_connection(connection)

            if not self.__continue_flag:
                self.stop_connection(connection[0])

    def _handle_connection(self, connection):
        try:
            self.start_process(connection)
        except ValueError:
            self.__continue_flag = False
        except:
            self.handle_process_error(connection)

    def accept_connection(self):
        """
        Return a pair (connection, client address)
        where connection is a socket object (and data if UDP)
        """
        pass

    def start_process(self, connection):
        """
        Overriden by threading class
        """

        self.handle_process(connection)

    def handle_process(self, connection):
        """
        Handle to send and receive data
        """
        client_address = connection.getpeername()
        self.HandlerClass(connection, client_address)

    def stop_connection(self, connection):
        print("Closed connection from", connection.getpeername())
        self.selector.unregister(connection)
        self.close_connection(connection)

    def close_connection(self, connection):
        """
        Overriden subclass and threading class
        """
        pass

    def handle_process_error(self, connection):
        sys.stderr.write('Exception occurred on the connection from {}'.format(
                    connection.getpeername()))

        print_exc()
