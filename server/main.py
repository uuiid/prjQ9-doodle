import os

import pyftpdlib.authorizers as ftpauth
import pyftpdlib.handlers as ftphand
import pyftpdlib.servers as ftpsevers


def maim():
    authorizer = ftpauth.DummyAuthorizer()
    # dubuxiaoyao
    authorizer.add_user("dubuxiaoyao", "12345", "W:\\", perm="elradfmwMT")
    # changanhuanjie
    authorizer.add_user("changanhuanjie", "12345", "X:\\", perm="elradfmwMT")

    authorizer.add_anonymous("X:\\")

    handler = ftphand.FTPHandler
    handler.authorizer = authorizer

    handler.banner = "pyftpdlib based ftpd ready."

    address = ("192.168.10.213", 21)
    sevrve = ftpsevers.FTPServer(address, handler)

    sevrve.max_cons = 256
    sevrve.max_cons_per_ip = 32

    sevrve.serve_forever()


def addUser(authorizer):
    pass


if __name__ == '__main__':
    maim()
