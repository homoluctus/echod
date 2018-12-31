import argparse
import threading
import logging
import hashlib
import ipaddress

def handle_args():
    parser = argparse.ArgumentParser(description='Simple Socket IO with TCP')
    parser.add_argument('-b', '--bind_address', metavar='address', default='127.0.0.1', dest='address', help='bind address (default 127.0.0.1)')
    parser.add_argument('-p', '--port', metavar='port', default=9999, type=int, help='bind port (default 9999)')

    return parser.parse_args()

def terminate_threads(timeout=None):
    threads = threading.enumerate()
    threads.remove(threading.main_thread())

    if threads:
        for th in threads:
            th.join(timeout)

def hash_password(password, salt=None):
    if not isinstance(password, bytes):
        password = password.encode()

    if salt and not isinstance(salt, bytes):
        salt = salt.encode()

    seed = password + salt
    return hashlib.sha256(seed).hexdigest()

def set_logger(name=None, filename="server.log", level="info"):
    """
    Logger outputs logs to both file and stream
    """

    numeric_level = getattr(logging, level.upper())
    if not isinstance(numeric_level, int):
        raise ValueError('Invalid log level: %s' % level)

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # For file
    handler1 = logging.FileHandler(filename)
    handler1.setLevel(numeric_level)
    log_format = logging.Formatter('%(asctime)s | [%(levelname)s] %(message)s')
    handler1.setFormatter(log_format)

    # For stream
    handler2 = logging.StreamHandler()
    handler2.setLevel(logging.DEBUG)
    handler2.setFormatter(logging.Formatter('[*] %(message)s'))

    logger.addHandler(handler1)
    logger.addHandler(handler2)

    return logger

def validate_address(host, port, version):
    """
    Validate host address, port and ip address version
    """

    try:
        ip_address = ipaddress.ip_address(host)
    except:
        raise
        
    if not isinstance(version, int):
        raise TypeError('Invalid object type')
        
    if ip_address.version != version:
        raise ValueError('Missmatch ip address version')

    if port not in range(0, 65536):
        raise ValueError('Invalid port number')

    return True