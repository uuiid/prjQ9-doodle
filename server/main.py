import logging
import os
import pathlib

import pyftpdlib.authorizers as ftpauth
import pyftpdlib.handlers as ftphand
import pyftpdlib.servers as ftpsevers

import DoodleServer.DoodleSql as DoleSql


def maim():
    authorizer = ftpauth.DummyAuthorizer()
    addUser(authorizer)

    authorizer.add_anonymous("C:\\Users\\teXiao\\doodle")

    handler = ftphand.FTPHandler
    handler.authorizer = authorizer

    handler.banner = "pyftpdlib based ftpd ready."

    address = ("192.168.10.213", 21)
    sevrve = ftpsevers.FTPServer(address, handler)

    sevrve.max_cons = 256
    sevrve.max_cons_per_ip = 32

    sevrve.serve_forever()


def addUser(authorizer):
    prj = {"dubuxiaoyao": "W:\\", "changanhuanjie": "X:\\", "dubuxiaoyao3": "V:\\", "kuangshenmozun": "T:\\"}
    # server_user = script.MySqlComm.selsctCommMysql("myuser", "", "", """SELECT `user`,password FROM `user`""")
    with DoleSql.commMysql().engine.connect() as connect:
        server_user = connect.execute("""SELECT `user`,password FROM myuser.`user`""").fetchall()
    for user, pow in server_user:
        for key, value in prj.items():
            authorizer.add_user(f"{key}{pow}", pow, value, perm="elradfmwMT")
    for key, value in prj.items():
        authorizer.add_user(f"{key}", "12345", value, perm="elradfmwMT")


if __name__ == '__main__':
    logpath = pathlib.Path("F:/doodle/var/log")
    if not logpath.exists():
        logpath.mkdir(parents=True)
    # config_log = pathlib.Path.cwd()
    # config_log = config_log.joinpath('doodleServerLog.ini')
    # logging.config.fileConfig(config_log)
    logging.basicConfig(filename='F:/doodle/var/log/pyftpd.log', level=logging.INFO)
    logging.FileHandler("F:/doodle/var/log/pyftpd.log", encoding='utf-8')
    maim()
