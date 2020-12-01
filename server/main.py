import contextlib
import logging
import logging.config
import os
import pathlib

import pyftpdlib.authorizers as ftpauth
import pyftpdlib.handlers as ftphand
import pyftpdlib.servers as ftpsevers

import sqlalchemy.orm


class connSql:
    def __init__(self):
        com_lur = "mysql+mysqlconnector" \
                  "://{_departmen}:{_password}@" \
                  "192.168.10.213:3306/{_mybd}".format(_departmen="Effects", _password="Effects", _mybd="doodle_main")
        self.engine = sqlalchemy.create_engine(com_lur, encoding='utf-8')  # , echo=True
        tmp_session = sqlalchemy.orm.sessionmaker(bind=self.engine)
        self.sessionclass = sqlalchemy.orm.scoped_session(tmp_session)

    @contextlib.contextmanager
    def session(self) -> sqlalchemy.orm.session.Session:
        # tmp_session = # self.sessionclass()
        session: sqlalchemy.orm.session.Session = sqlalchemy.orm.sessionmaker(bind=self.engine)()
        try:
            yield session
            session.commit()
        except BaseException as err:
            logging.error("%s", err)
            session.rollback()
        finally:
            session.close()


def maim():
    authorizer = ftpauth.DummyAuthorizer()
    addUser(authorizer)

    authorizer.add_anonymous("F:\\doodle")

    handler = ftphand.FTPHandler
    handler.authorizer = authorizer

    handler.banner = "pyftpdlib based ftpd ready."

    address = ("192.168.10.213", 21)
    sevrve = ftpsevers.ThreadedFTPServer(address,handler)
    # sevrve = ftpsevers.FTPServer(address, handler)

    sevrve.max_cons = 256
    sevrve.max_cons_per_ip = 32

    sevrve.serve_forever()


def addUser(authorizer):
    prj = {"dubuxiaoyao": "W:\\",
           "changanhuanjie": "X:\\",
           "dubuxiaoyao3": "V:\\",
           "kuangshenmozun": "T:\\",
           "wanyufengshen": "U:\\"}

    # server_user = script.MySqlComm.selsctCommMysql("myuser", "", "", """SELECT `user`,password FROM `user`""")
    with connSql().engine.connect() as connect:
        server_user = connect.execute("""SELECT `user`,password FROM myuser.`user`""").fetchall()
    for user, pow in server_user:
        for key, value in prj.items():
            authorizer.add_user(f"{key}{pow}", pow, value, perm="elradfmwMT")
    for key, value in prj.items():
        authorizer.add_user(f"{key}", "", value, perm="elradfmwMT")


if __name__ == '__main__':
    # logpath = pathlib.Path("F:/doodle/var/log")
    # if not logpath.exists():
    #     logpath.mkdir(parents=True)

    # config_log = pathlib.Path.cwd()
    # config_log = config_log.joinpath('doodleServerLog.ini')
    # logging.config.fileConfig(config_log)

    # logging.config.dictConfig({"version": 1,
    #                            "formatters": {
    #                                "simple": {
    #                                    "format": "%(asctime)s - %(name)s - %(lineno)d - %(levelname)s - %(message)s"
    #                                }
    #                            },
    #                            "handlers": {
    #                                {
    #                                    "console": {
    #                                        "class": "logging.StreamHandler",
    #                                        "level": "INFO",
    #                                        "formatter": "simple",
    #
    #                                    }}
    #                            }})
    logging.basicConfig(filename='F:/doodle/pyftpd.log', level=logging.INFO)
    maim()
