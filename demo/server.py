import sys

try:
    from echod.utils import handle_args
    from echod.handle import BaseHandler
    from echod.tcp import TCPServer
except (ModuleNotFoundError, ImportError):
    from traceback import print_exc
    print_exc()
    sys.exit("\n[!] Please add echod path to PYTHONPATH")


class MyHandler(BaseHandler):
    max_buffer_size = 1024

    def process(self):
        raw_data = self.connection.recv(self.max_buffer_size)
        if not raw_data:
            raise ValueError

        decoded_data = raw_data.decode()
        print('Received {} from {}'.format(
                    repr(decoded_data), self.client_address))


if __name__ == '__main__':
    args = handle_args()

    address = ((args.address, args.port))

    try:
        with TCPServer(address, 4, MyHandler) as server:
            print("Server started")
            server.start()
    except KeyboardInterrupt:
        sys.stderr.write('[!] EXIT\n')
