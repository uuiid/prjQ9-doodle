import os

import pyftpdlib.authorizers as ftpauth
import pyftpdlib.handlers as ftphand
import pyftpdlib.servers as ftpsevers


def maim():
    authorizer = ftpauth.DummyAuthorizer()
    authorizer.add_user("user", "12345", "X:\\", perm="elradfmwMT")
    authorizer.add_anonymous("X:\\")

    handler = ftphand.FTPHandler
    handler.authorizer = authorizer

    handler.banner = "pyftpdlib based ftpd ready."

    address = ("127.0.0.1", 2121)
    sevrve = ftpsevers.FTPServer(address, handler)

    sevrve.max_cons = 256
    sevrve.max_cons_per_ip = 32

    sevrve.serve_forever()


if __name__ == '__main__':
    maim()
