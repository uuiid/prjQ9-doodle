import logging
import os
import pathlib
import shutil
import tempfile
import multiprocessing
import sqlalchemy
import sqlalchemy.ext.declarative
import sqlalchemy.orm

Base = sqlalchemy.ext.declarative.declarative_base()

import script.doodle_setting
import script.synXml


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


class findFiles(multiprocessing.Process):
    findpath: str
    session: sqlalchemy.orm.Session
    table: fileinfo

    def __init__(self, findpath, session, table: fileinfo):
        super().__init__()
        self.findpath = findpath
        self.session = session()
        self.table = table

    def run(self) -> None:
        for root, dirs, files in os.walk(self.findpath):
            for file in files:
                path_join = os.path.join(root, file)
                f_path = path_join.replace(self.findpath, '')
                sql_value = self.session.query(fileinfo).filter_by(filepath=f_path).first()
                if not sql_value:
                    sql_value = self.table(filepath=f_path)
                    sql_value.file_m_time = os.stat(path_join).st_mtime
                    sql_value.filesize = os.stat(path_join).st_size
                    sql_value.direction = "to_trange"
                    self.session.add(sql_value)
                sql_value.file_m_time = os.stat(path_join).st_mtime
                sql_value.filesize = os.stat(path_join).st_size
                self.session.flush()
            self.session.commit()
            print(f"子进程执行中  path ->>> {root}")


def copyfile(soure, trange):
    for path in [soure, trange]:
        join = os.path.join(path, "stn_py.db")
        if os.path.isfile(join):
            break
    else:
        join = os.path.join(soure, "stn_py.db")

    engine = sqlalchemy.create_engine('sqlite:///{}'.format(join))
    session_class = sqlalchemy.orm.sessionmaker(bind=engine)
    # my_session: sqlalchemy.orm.Session = session_class()
    if not os.path.isfile(join):
        Base.metadata.create_all(engine)

    sour = findFiles(soure, session_class, sourefileinfo)
    sour.start()

class synFile(object):
    @property
    def left(self) -> pathlib.Path:
        if not hasattr(self, '_left'):
            self._left = ''
        return self._left

    @left.setter
    def left(self, left):
        self._left = left

    @property
    def right(self) -> pathlib.Path:
        if not hasattr(self, '_right'):
            self._right = ''
        return self._right

    @right.setter
    def right(self, right):
        self._right = right

    @property
    def file_db(self) -> pathlib.Path:
        if not hasattr(self, '_file_db'):
            self._file_db = ''
        return self._file_db

    @property
    def ignore(self):
        if not hasattr(self, '_ignore'):
            self._ignore = ''
        return self._ignore

    @ignore.setter
    def ignore(self, ignore):
        self._ignore = ignore

    @property
    def minclude(self):
        if not hasattr(self, '_include'):
            self._include = ['.']
        return self._include

    @minclude.setter
    def minclude(self, minclude):
        self._include = minclude

    @file_db.setter
    def file_db(self, file_db):
        self._file_db = file_db

    def __init__(self, left: pathlib.Path, right: pathlib.Path, ignore=''):
        self.doodleSet = script.doodle_setting.Doodlesetting()
        self._left = left
        self._right = right
        # self._file_db = left.joinpath("Sql_syn_file.db")
        # if self.file_db.is_file():
        #     pass
        # else:
        #     pass

    def getFilePath(self):
        for l_root, dirs, names in os.walk(str(self.left)):
            for name in names:
                r_root = l_root.replace(str(self.left), str(self.right))
                print(f"""{l_root}\\{name}""")
                print(f"""{r_root}\\{name}""")

    def copyAndBakeup(self, is_dir: bool):
        backup = self.right.joinpath("backup")
        tem = pathlib.Path(tempfile.gettempdir())
        synlist = [{"Left": str(self.left), "Right": str(self.right)}]
        if is_dir:
            # pool = multiprocessing.Pool(processes=4)
            for root, dors, files in os.walk(str(self.left)):
                for file in files:
                    left_file = os.path.join(root, file)
                    right_file = left_file.replace(str(self.left), str(self.right))
                    shutil.copy2(left_file, right_file)
                    logging.info("%s-------%s", left_file, right_file)
                    # pool.apply(_copyfile, (left_file, right_file))
            # pool.close()
            # pool.join()
            # synfile = script.synXml.weiteXml(tem,synlist,Exclude=["backup"],VersioningFolder=[str(backup)])
        else:
            if not backup.is_dir():
                backup.mkdir()
            # synfile = script.synXml.weiteXml(tem, synlist, Exclude=["backup"], VersioningFolder=[str(backup)])
        # program = self.doodleSet.FreeFileSync
        # subprocess.run('{} "{}"'.format(program, synfile), shell=True)


if __name__ == '__main__':
    left = pathlib.Path("D:\\ue_project")
    right = pathlib.Path("F:\\ue_project")
    copyfile(left,right)
