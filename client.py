import sys
import socket
from utils import handle_args

args = handle_args()

with socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM, proto=0) as sock:
    sock.connect((args.address, args.port))

    print("[*] Please input message")

    try:
        while True:
            msg = input('>>> ')

            if msg == 'exit':
                print("[*] Connection shutdown")
                break

            try:
                sock.sendall(msg.encode())
            except Exception as err:
                sys.exit(err)

            data = sock.recv(1024)
            if not data:
                break

            print("[+] Received", repr(data.decode()))

    except KeyboardInterrupt:
        sys.exit("\n[*] Forced shutdown")

    except Exception as err:
        sys.exit(err)
        
    finally:
        print("[*] Terminated")