import os
import shutil
import sqlite3
import pathlib
import sqlalchemy
import sqlalchemy.ext.declarative
import sqlalchemy.orm

Base = sqlalchemy.ext.declarative.declarative_base()


class fileinfo(Base):
    __tablename__ = "trangefileinfo"
    id = sqlalchemy.Column(sqlalchemy.INT, primary_key=True)
    filepath = sqlalchemy.Column(sqlalchemy.TEXT, unique=True)
    filesize = sqlalchemy.Column(sqlalchemy.FLOAT)
    file_m_time = sqlalchemy.Column(sqlalchemy.FLOAT)
    direction = sqlalchemy.Column(sqlalchemy.TEXT)
    synTime = sqlalchemy.Column(sqlalchemy.FLOAT)


def copyfile(soure, trange):
    for path in [soure, trange]:
        join = os.path.join(path, "stn_py.db")
        if os.path.isfile(join):
            break
    else:
        join = os.path.join(soure, "stn_py.db")

    engine = sqlalchemy.create_engine('sqlite:///{}'.format(join))
    session_class = sqlalchemy.orm.sessionmaker(bind=engine)
    my_session: sqlalchemy.orm.Session = session_class()
    if not os.path.isfile(join):
        Base.metadata.create_all(engine)
    scanFile(my_session, soure, fileinfo)
    scanFile(my_session, trange, fileinfo)
    my_session.commit()
    # print(join)


def scanFile(my_session: sqlalchemy.orm.Session, soure, fileinfo: Base):
    for root, dirs, files in os.walk(soure):
        for file in files:
            path_join = os.path.join(root, file)
            f_path = path_join.replace(soure, '')
            sql_value = my_session.query(fileinfo).filter_by(filepath=f_path).first()
            if not sql_value:
                sql_value = fileinfo(filepath=f_path)
                sql_value.file_m_time = os.stat(path_join).st_mtime
                sql_value.filesize = os.stat(path_join).st_size
                sql_value.direction = "to_trange"
                my_session.add(sql_value)
            if sql_value.filesize != os.stat(path_join).st_size:
                if sql_value.file_m_time > os.stat(path_join).st_mtime:
                    pass

            sql_value.file_m_time = os.stat(path_join).st_mtime
            sql_value.filesize = os.stat(path_join).st_size
            my_session.flush()



if __name__ == '__main__':
    copyfile(r"F:\Source", r"D:\Source")
