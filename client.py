import sys
import socket
from utils import handle_args, Version, validate_address

class SocketClient:
    def __init__(self,
                 callback,
                 server_address,
                 protocol,
                 version,
                 active=False):

        self.callback = callback
        self.server_address = server_address
        self.socket_type = self._get_socket_type(protocol)
        self.address_family = getattr(socket, Version(version).name)

        try:
            validate_address(self.server_address[0],
                             self.server_address[1],
                             version)
        except:
            raise

        self.socket = socket.socket(family=self.address_family,
                                    type=self.socket_type)

        if protocol == 'tcp':
            try:
                self._connect_tcp_server()
            except:
                self.stop()
                raise

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
        except:
            raise

    def run(self):
        try:
            self.callback(self.socket)
        except:
            raise

def callback(sock):
    print("[*] Please input message")

    while True:
        msg = input('>>> ')

        if msg == 'exit':
            sock.shutdown(socket.SHUT_WR)
            break

        try:
            sock.sendall(msg.encode())
        except Exception as err:
            sys.exit(err)

        data = sock.recv(1024)
        if not data:
            break

        print("[+] Received", repr(data.decode()))

if __name__ == '__main__':
    args = handle_args()

    try:
        with SocketClient(callback,
                          server_address=(args.address, args.port),
                          protocol=args.protocol,
                          version=args.version) as client:
            client.run()
    except KeyboardInterrupt:
            print("\n[!] Forced shutdown")
    except:
        from traceback import print_exc
        print_exc()