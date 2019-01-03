import sys

from utils import handle_args
from handle import BaseHandler
from tcp import TCPServer

class MyHandler(BaseHandler):
    max_buffer_size = 1024

    def process(self):
        while True:
            raw_data = self.connection.recv(self.max_buffer_size)
            if not raw_data:
                break

            decoded_data = raw_data.decode()
            print(decoded_data)

            try:
                self.connection.sendall(b'ACK')
            except:
                from traceback import print_exc
                print_exc()
                break

if __name__ == '__main__':
    args = handle_args()

    address = ((args.address, args.port))

    try:
        with TCPServer(address, 4, MyHandler) as server:
            server.start()
    except KeyboardInterrupt:
        sys.stderr.write('[!] EXIT\n')
    except:
        from traceback import print_exc
        print_exc()