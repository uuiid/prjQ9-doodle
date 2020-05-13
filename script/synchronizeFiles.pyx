import os
import shutil
import sqlite3
import pathlib
import sqlalchemy
import sqlalchemy.ext.declarative
import sqlalchemy.orm

Base = sqlalchemy.ext.declarative.declarative_base()


class fileinfo(Base):
    __abstract__ = True
    id = sqlalchemy.Column(sqlalchemy.INT, primary_key=True)
    filepath = sqlalchemy.Column(sqlalchemy.TEXT, unique=True)
    filesize = sqlalchemy.Column(sqlalchemy.FLOAT)
    file_m_time = sqlalchemy.Column(sqlalchemy.FLOAT)
    direction = sqlalchemy.Column(sqlalchemy.TEXT)
    synTime = sqlalchemy.Column(sqlalchemy.FLOAT)

class sourefileinfo(fileinfo):
    __tablename__ = "sourefileinfo"


class trangefileinfo(fileinfo):
    __tablename__ = "trangefileinfo"

def copyfile(str soure, str trange):
    cdef str join, path
    cdef object cursor, db_
    cdef object my_session
    for path in [soure, trange]:
        join = os.path.join(path, "stn_py.db")
        if os.path.isfile(join):
            break
    else:
        join = os.path.join(soure, "stn_py.db")

    engine = sqlalchemy.create_engine('sqlite+pysqlcipher:///{}stn_py.db'.format(join))
    session_class = sqlalchemy.orm.sessionmaker(bind=engine)
    my_session = session_class()


    cdef str root, dirs, files, file, f_path, path_join
    cdef double st_mtime, st_size
    cdef object sql_value
    for root, dirs, files in os.walk(soure):
        for file in files:
            path_join = os.path.join(root, file)
            st_mtime = os.stat(path_join).st_mtime
            st_size = os.stat(path_join).st_size
            f_path = path_join.replace(soure, '')
            sql_value = sourefileinfo(filepath=f_path,filesize=st_size,file_m_time=st_mtime)
            my_session.add(sql_value)

    my_session.commit()

    # print(join)
