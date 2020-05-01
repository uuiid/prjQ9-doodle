import logging
import mysql.connector
import sqlalchemy.ext.declarative
import sqlalchemy.orm

engine = sqlalchemy.create_engine("mysql+mysqlconnector://Effects:Effects@192.168.10.213:3306/dubuxiaoyao",
                                  encoding='utf-8')

Base = sqlalchemy.ext.declarative.declarative_base()
session_class = sqlalchemy.orm.sessionmaker(bind=engine)
my_session: sqlalchemy.orm.session.Session = session_class()


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
