import sys
import socket
from utils import handle_args, Version

def tcp_client(callback, server_address, version=4):
    with socket.socket(family=getattr(socket, Version(version).name),
                        type=socket.SOCK_STREAM) as sock:
        
        try:
            sock.connect(server_address)
        except Exception as err:
            sys.exit(err)
        except:
            raise

        try:
            callback(sock)
        except Exception as err:
            sys.exit(err)
        except KeyboardInterrupt:
            sys.exit("[!] Forced shutdown")
        except:
            raise
        else:
            print("[*] Closing connection")

    print("[*] Closed connection\n[*] Terminated")

def callback(socket):
    print("[*] Please input message")

    while True:
        msg = input('>>> ')

        if msg == 'exit':
            print("[*] Connection shutdown")
            break

        try:
            socket.sendall(msg.encode())
        except Exception as err:
            sys.exit(err)

        data = socket.recv(1024)
        if not data:
            break

        print("[+] Received", repr(data.decode()))

if __name__ == '__main__':
    args = handle_args()

    if args.protocol == 'tcp':
        tcp_client(callback, server_address=(args.address, args.port), version=args.version)
    else:
        pass