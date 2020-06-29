import logging
import threading
import contextlib
import mysql.connector
import sqlalchemy.ext.declarative
import sqlalchemy.orm

Base = sqlalchemy.ext.declarative.declarative_base()


class commMysql(object):
    _setting = {}
    _instance_lock = threading.Lock()
    engine: sqlalchemy

    def __new__(cls, *args, **kwargs):
        if not hasattr(commMysql, '_instance'):
            with commMysql._instance_lock:
                if not hasattr(commMysql, '_instance'):
                    commMysql._instance = object.__new__(cls)
        return commMysql._instance

    def __init__(self, mybd: str = '', departmen='', password=''):
        com_lur = "mysql+mysqlconnector" \
                  "://{_departmen}:{_password}@" \
                  "192.168.10.213:3306/{_mybd}".format(_departmen="Effects", _password="Effects", _mybd=mybd)
        self.engine = sqlalchemy.create_engine(com_lur, encoding='utf-8')  # , echo=True
        tmp_session = sqlalchemy.orm.sessionmaker(bind=self.engine)
        self.sessionclass = sqlalchemy.orm.scoped_session(tmp_session)
        # tmp_session = sqlalchemy.orm.sessionmaker(bind=self.engine)
        # self.session: sqlalchemy.orm.session.Session = tmp_session

    def createTable(self):
        Base.metadata.create_all(self.engine)

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

    @contextlib.contextmanager
    def sessionOne(self) -> sqlalchemy.orm.session.Session:
        # self.sessionclass.registry
        session: sqlalchemy.orm.session.Session = self.sessionclass()
        try:
            yield session
            # session.add(self,)
            session.commit()
        except BaseException as err:
            logging.info("%s", err)
            session.rollback()
        finally:
            pass
