import os
import hashlib

from utils import hash_password

class Auth:
    __users = {
        1: {'username': 'test1',
            'password': '8a87f0f11bca428c86f918632a636e38d40018cf0f5e71ab95c5d86fd927906d'},
        2: {'username': 'test2',
            'password': 'a6aaa967c8b53e6e22603472c946484c9b26440fe71db27d9c88b43bac2947be'},
    }

    def __init__(self, username):
        self.__username = username
        self.__session_token = None
        self.__is_authenticated = False

    @property
    def username(self):
        return self.__username

    @property
    def is_authenticated(self):
        return self.__is_authenticated

    @property
    def session_token(self):
        return self.__session_token

    def authenticate(self, password):
        if self.__is_authenticated:
            return True

        for i in Auth.__users:
            if Auth.__users[i]['username'] == self.username \
                and Auth.__users[i]['password'] == password:

                self.__is_authenticated = True
                return True

        return False

    def generate_session_token(self, salt=None):
        if not self.__is_authenticated:
            return False

        if not salt:
            salt = os.urandom(5)
        elif not isinstance(salt, bytes):
            salt = salt.encode()
            
        seed = self.username.encode() + salt
        self.__session_token = hashlib.sha256(seed).hexdigest()

        return True