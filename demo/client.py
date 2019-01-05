import sys
import socket
from time import sleep
from threading import Thread

try:
    from echod.client import SocketClient
    from echod.utils import handle_args
except (ModuleNotFoundError, ImportError):
    from traceback import print_exc
    print_exc()
    sys.exit("\n[!] Please add echod path to PYTHONPATH")
except:
    raise

def callback(sock, kwargs={}):
    try:
        if sock.sendall(b'hello') is not None:
            sock.shutdown(socket.SHUT_WR)
    except:
        sys.exit(sys.exc_info()[1])
    else:
        if 'interval' in kwargs.keys():
            sleep(kwargs['interval'])

def client(callback, addr, proto, version, **kwargs):
    with SocketClient(callback,
                      server_address=addr,
                      protocol=proto,
                      version=version) as client:

        client.run(kwargs)


if __name__ == '__main__':
    args = handle_args()
    server_address = (args.address, args.port)

    c1 = Thread(target=client, args=(callback, server_address, args.protocol, args.version), kwargs={'interval': 3})
    c2 = Thread(target=client, args=(callback, server_address, args.protocol, args.version), kwargs={'interval': 1})
    c3 = Thread(target=client, args=(callback, server_address, args.protocol, args.version))
    c1.start()
    c2.start()
    c3.start()