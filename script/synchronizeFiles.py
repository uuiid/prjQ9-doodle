import logging
import os
import pathlib
import shutil
import tempfile
import multiprocessing
import threading
import queue
import sqlalchemy
import sqlalchemy.ext.declarative
import sqlalchemy.orm
import sqlalchemy.pool
import datetime

Base = sqlalchemy.ext.declarative.declarative_base()

import script.doodle_setting
import script.synXml


class fileAction(Base):
    __tablename__ = "fileaction"
    id = sqlalchemy.Column(sqlalchemy.INT, primary_key=True)
    soure_id = sqlalchemy.Column(sqlalchemy.INT, sqlalchemy.ForeignKey('sourefileinfo.id'))
    trange_id = sqlalchemy.Column(sqlalchemy.INT, sqlalchemy.ForeignKey('trangefileinfo.id'))
    sourefileinfo = sqlalchemy.orm.relationship("sourefileinfo", back_populates="Action")
    trangefileinfo = sqlalchemy.orm.relationship("trangefileinfo", back_populates="Action")

    direction = sqlalchemy.Column(sqlalchemy.TEXT)
    synTime = sqlalchemy.Column(sqlalchemy.FLOAT)


class fileinfo(Base):
    __abstract__ = True
    # __tablename__ = "fileinfo"
    id = sqlalchemy.Column(sqlalchemy.INT, primary_key=True)
    filepath = sqlalchemy.Column(sqlalchemy.TEXT, unique=True)
    file_m_time = sqlalchemy.Column(sqlalchemy.FLOAT)
    filesize = sqlalchemy.Column(sqlalchemy.FLOAT)


class sourefileinfo(fileinfo):
    __tablename__ = "sourefileinfo"
    Action = sqlalchemy.orm.relationship("fileAction", back_populates="sourefileinfo")


class trangefileinfo(fileinfo):
    __tablename__ = "trangefileinfo"
    Action = sqlalchemy.orm.relationship("fileAction", back_populates="trangefileinfo")


class findFiles(threading.Thread):
    findpath: str
    queue: queue.Queue
    table: fileinfo

    def __init__(self, findpath, queue_, flag):
        super().__init__()
        self.findpath = findpath
        self.queue = queue_
        self.flag = flag

    def run(self) -> None:
        for root, dirs, files in os.walk(self.findpath):
            for file in files:
                path_join = os.path.join(root, file)
                f_path = path_join.replace(self.findpath.__str__(), '')
                stat = os.stat(path_join)
                # time = datetime.datetime.fromtimestamp(stat.st_mtime)
                self.queue.put((self.flag, f_path, stat.st_mtime, stat.st_size), block=True, timeout=1000)
            # print(f"子进程执行中  path ->>> {root}")


#  比较文件时  谁的修改日期大, 谁就是最新修改的

# class comFile(threading.Thread):


class changeSql(threading.Thread):
    queue_: queue.Queue
    thread_stop: bool

    def __init__(self, queue_: queue.Queue, my_session):
        super().__init__()
        self.queue_ = queue_
        self.thread_stop = False
        self.my_session = my_session

    def run(self) -> None:
        t_session = self.my_session()
        while not self.thread_stop:
            try:
                task = self.queue_.get(block=True, timeout=3)
            except queue.Empty:
                logging.info("线程结束")
                self.thread_stop = True
                break
            else:

                sql_value = t_session.query(task[0]).filter_by(filepath=task[1]).first()
                if not sql_value:
                    sql_value = task[0](filepath=task[1], file_m_time=task[2], filesize=task[3])
                    t_session.add(sql_value)
                else:
                    sql_value.file_m_time = task[2]
                    sql_value.filesize = task[3]

                # logging.info("提交数据 %s",task)
        t_session.commit()


def comFile(soure_id, soure_time, soure_size, trange_id, trange_time, trange_size):
    size_equal = soure_size == trange_size
    time_equal = soure_time == trange_time
    if size_equal and time_equal:
        return True, soure_id
    else:
        if soure_time > trange_time:
            return False, soure_id
        else:
            return False, trange_id


def copyfile(soure, trange):
    for path in [soure, trange]:
        join = os.path.join(path, "stn_py.db")
        if os.path.isfile(join):
            break
    else:
        join = os.path.join(soure, "stn_py.db")

    engine = sqlalchemy.create_engine('sqlite:///{}'.format(join), connect_args={'check_same_thread': False},
                                      poolclass=sqlalchemy.pool.StaticPool)
    session_class = sqlalchemy.orm.sessionmaker(bind=engine)
    my_session: sqlalchemy.orm.Session = session_class()
    my_session_class = sqlalchemy.orm.scoped_session(session_class)
    if not os.path.isfile(join):
        Base.metadata.create_all(engine)
    my_queue = queue.Queue(1000000)

    sour = findFiles(soure, my_queue, sourefileinfo)
    trange_t = findFiles(trange, my_queue, trangefileinfo)
    subinfo = changeSql(my_queue, session_class)
    sour.start()
    trange_t.start()
    subinfo.start()
    subinfo.join()

    # if not (sour.is_alive() and trange_t.is_alive()):
    #     my_session_class().commit()


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
    copyfile(left, right)
