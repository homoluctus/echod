# Echo server and client
This is simple echo server and client written by Python3.  
Supported platform is most UNIX systems.

## Support Protocol
- IPv4
- TCP
- UDP

## Feature
- I/O Multiplexing
- Multi Clients
- Command Line

## Demo

```
$ python3 demo_server.py
Server started
Accepted from ('127.0.0.1', 40620)
Received 'hello' from ('127.0.0.1', 40620)
Accepted from ('127.0.0.1', 40622)
Received 'hello' from ('127.0.0.1', 40622)
Accepted from ('127.0.0.1', 40624)
Received 'hello' from ('127.0.0.1', 40624)
Closed connection from ('127.0.0.1', 40624)
Closed connection from ('127.0.0.1', 40622)
Closed connection from ('127.0.0.1', 40620)
```