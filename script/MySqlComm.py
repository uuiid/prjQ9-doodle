import logging
import threading
import contextlib
import mysql.connector
import sqlalchemy.ext.declarative
import sqlalchemy.orm

Base = sqlalchemy.ext.declarative.declarative_base()


# engine = sqlalchemy.create_engine("mysql+mysqlconnector://Effects:Effects@192.168.10.213:3306/dubuxiaoyao",
#                                   encoding='utf-8')
#
# Base = sqlalchemy.ext.declarative.declarative_base()
# session_class = sqlalchemy.orm.sessionmaker(bind=engine)
# my_session: sqlalchemy.orm.session.Session = session_class()
# my_session.close()


def inserteCommMysql(mybd: str, departmen, password, sql_command):
    data_base = mysql.connector.connect(
        host='192.168.10.213',
        port='3306',
        user='Effects',
        passwd="Effects",
        auth_plugin='caching_sha2_password',
        db=mybd
    )
    cursor = data_base.cursor()
    try:
        cursor.execute(sql_command)
        data_base.commit()
        logging.info('成功%s', sql_command)
    except:
        data_base.rollback()
        logging.exception('失败指令%s', sql_command)

    cursor.close()
    data_base.close()


def selsctCommMysql(mybd: str, departmen, password, sql_command):
    data_base = mysql.connector.connect(
        host='192.168.10.213',
        port='3306',
        user='Effects',
        passwd="Effects",
        auth_plugin='caching_sha2_password',
        db=mybd
    )
    cursor = data_base.cursor()
    try:
        cursor.execute(sql_command)
        date = cursor.fetchall()
    except:
        date = ''
    cursor.close()
    data_base.close()
    return date


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
        self.engine = sqlalchemy.create_engine(com_lur, encoding='utf-8',echo=True)
        tmp_session = sqlalchemy.orm.sessionmaker(bind=self.engine)
        self.sessionclass = sqlalchemy.orm.scoped_session(tmp_session)
        # tmp_session = sqlalchemy.orm.sessionmaker(bind=self.engine)
        # self.session: sqlalchemy.orm.session.Session = tmp_session

    def createTable(self):
        Base.metadata.create_all(self.engine)

    @contextlib.contextmanager
    def session(self) -> sqlalchemy.orm.session.Session:
        tmp_session = sqlalchemy.orm.sessionmaker(bind=self.engine)
        session: sqlalchemy.orm.session.Session = self.sessionclass()
        try:
            yield session
            session.commit()
        except BaseException as err:
            logging.error("%s", err)
            session.rollback()
        finally:
            session.close()
            self.sessionclass().close()

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
            session.close()
