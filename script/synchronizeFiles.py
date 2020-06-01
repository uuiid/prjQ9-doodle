import logging
import os
import pathlib
import shutil
import sys
import tempfile
import multiprocessing
import subprocess
import threading
import queue
import ftpsync
import time
import re

import sqlalchemy
import sqlalchemy.ext.declarative
import sqlalchemy.orm
import sqlalchemy.pool
import datetime
import concurrent.futures as cf

Base = sqlalchemy.ext.declarative.declarative_base()

import script.doodle_setting
import script.synXml

_path_my_ = set()


class synInfo(Base):
    __tablename__ = "synInfo"
    id = sqlalchemy.Column(sqlalchemy.INT, primary_key=True)
    synTime: datetime.datetime = sqlalchemy.Column(sqlalchemy.DATETIME)
    sourepath = sqlalchemy.Column(sqlalchemy.TEXT, unique=True)
    trangepath = sqlalchemy.Column(sqlalchemy.TEXT, unique=True)


class fileAction(Base):
    __tablename__ = "fileaction"
    id = sqlalchemy.Column(sqlalchemy.INT, primary_key=True)

    filepath = sqlalchemy.Column(sqlalchemy.TEXT, unique=True)

    direction = sqlalchemy.Column(sqlalchemy.TEXT)

    # synTime: datetime.datetime = sqlalchemy.Column(sqlalchemy.DATETIME)

    conflict = sqlalchemy.Column(sqlalchemy.DATETIME)


class fileinfo(Base):
    __abstract__ = True
    # __tablename__ = "fileinfo"
    id = sqlalchemy.Column(sqlalchemy.INT, primary_key=True)
    filepath = sqlalchemy.Column(sqlalchemy.TEXT, unique=True)
    file_m_time: datetime.datetime = sqlalchemy.Column(sqlalchemy.DATETIME)
    filesize = sqlalchemy.Column(sqlalchemy.TEXT)


class sourefileinfo(fileinfo):
    __tablename__ = "sourefileinfo"


class trangefileinfo(fileinfo):
    __tablename__ = "trangefileinfo"


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
                time = datetime.datetime.fromtimestamp(stat.st_mtime)
                self.queue.put((self.flag, f_path, time, stat.st_size), block=True, timeout=1000)

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
            _path_my_.add(task[1])
            # logging.info("提交数据 %s",task)
        t_session.commit()
        t_session.close()


def FileNotEqual(soure: sourefileinfo, trange: trangefileinfo):
    size_equal = trange.filesize == soure.filesize
    time_equal = trange.file_m_time == soure.file_m_time

    if size_equal and time_equal:
        return False, None
    else:
        if soure.file_m_time > trange.file_m_time:
            return True, soure
        else:
            return True, trange


def exceedSyn(time, syn_time):
    if time > syn_time:
        return True
    else:
        return False


def inspectfile(soure, trange):
    for path in [soure, trange]:
        join = os.path.join(path, "stn_py.db")
        if os.path.isfile(join):
            break
    else:
        join = os.path.join(soure, "stn_py.db")

    engine = sqlalchemy.create_engine('sqlite:///{}'.format(join), connect_args={'check_same_thread': False},
                                      poolclass=sqlalchemy.pool.StaticPool)
    session_class = sqlalchemy.orm.sessionmaker(bind=engine)

    my_session_class = sqlalchemy.orm.scoped_session(session_class)
    if not os.path.isfile(join):
        Base.metadata.create_all(engine)
        my_session: sqlalchemy.orm.Session = my_session_class()
        syn = synInfo(sourepath=soure.as_posix(), trangepath=trange.as_posix())
        my_session.add(syn)
        my_session.commit()

    my_queue = queue.Queue(1000000)

    sour = findFiles(soure, my_queue, sourefileinfo)
    trange_t = findFiles(trange, my_queue, trangefileinfo)
    subinfo = changeSql(my_queue, my_session_class)
    sour.start()
    trange_t.start()
    subinfo.start()
    subinfo.join()

    my_session: sqlalchemy.orm.Session = my_session_class()

    writeSyncFileInfor(my_session)

    my_session.commit()
    syn_info = my_session.query(synInfo).one()

    fileTestConfict(my_session, syn_info)
    return my_session


def fileTestConfict(my_session, syn_info):
    if syn_info.synTime:
        t_path = my_session.query(trangefileinfo.filepath).filter(trangefileinfo.file_m_time > syn_info.synTime).all()
        s_path = my_session.query(sourefileinfo.filepath).filter(sourefileinfo.file_m_time > syn_info.synTime).all()
        com = {i[0] for i in t_path + s_path}
        if com:
            for _p_ in com:
                data_action = my_session.query(fileAction).filter(fileAction.filepath == _p_).one()
                data_action.direction = "com"
    my_session.commit()


def writeSyncFileInfor(my_session):
    for _p_ in _path_my_:
        data_t = my_session.query(trangefileinfo).filter(trangefileinfo.filepath == _p_).all()
        data_s = my_session.query(sourefileinfo).filter(sourefileinfo.filepath == _p_).all()
        data_action = my_session.query(fileAction).filter(fileAction.filepath == _p_).all()
        if not data_action:
            if not data_t:  # 目标路径是空,从来源复制
                action = fileAction(filepath=_p_, direction="s")

            elif not data_s:  # 来源路径是空,从目标复制
                action = fileAction(filepath=_p_, direction="t")

            else:
                data_t = data_t[0]
                data_s = data_s[0]
                not_qeual, file_copy = FileNotEqual(data_s, data_t)
                if not_qeual:
                    action = fileAction(filepath=_p_, direction=file_copy.__class__.__name__[:1])
                else:
                    action = fileAction(filepath=_p_)

            my_session.add(action)
        else:
            data_action = data_action[0]
            if not data_t:  # 目标路径是空,从来源复制
                data_action.direction = "s"
            elif not data_s:  # 来源路径是空,从目标复制
                data_action.direction = "t"
            else:
                data_t = data_t[0]
                data_s = data_s[0]
                not_qeual, file_copy = FileNotEqual(data_s, data_t)
                if not_qeual:
                    data_action.direction = file_copy.__class__.__name__[:1]
                else:
                    data_action.filepath = _p_
                my_session.commit()


def copyFile(soure: str, trange: str):
    for root, dirs, files in os.walk(soure):
        for file in files:
            s_path = os.path.join(root, file)
            t_path = s_path.replace(soure, trange)
            try:
                pathlib.Path(t_path).parent.mkdir(parents=True, exist_ok=True)
            except FileExistsError:
                pass
            copyItem(s_path, t_path)


def robocopy(soure: pathlib.Path, trange: pathlib.Path, ecom=()):
    # /FP 全路径
    # /V 详细信息
    # /L 列出所有
    # /NJH 无表头
    # /NJS 无摘要
    # /NDL 无目录
    # /NS 无大小
    # /E 具有子目录
    # /A 仅存档
    com = ["powershell.exe", "robocopy", soure.as_posix(), trange.as_posix(), "/FP", "/V", "/NJH", "/NJS", "/NDL",
           "/NS"] + list(ecom)
    p = subprocess.Popen(com, stdout=subprocess.PIPE, encoding="gbk")
    out_ = p.stdout.readlines()

    # def NotNone(m_list) -> list:
    #     return [n.strip() for n in m_list if n]
    #
    # out_ = [NotNone(re.split("\\n|\\t", o)) for o in out_]

    return out_


def copyItem(soure: str, trange: str):
    com = ["powershell.exe", "Copy-Item", soure, trange]
    p = subprocess.Popen(com, stdout=subprocess.PIPE, encoding="gbk")
    out_ = p.stdout.readlines()
    return out_


class copyeasily(threading.Thread):
    soure: pathlib.Path
    trange: pathlib.Path

    def __init__(self, soure: pathlib.Path, trange: pathlib.Path):
        super().__init__()
        """来源移动是一个文件, 目标一定是一个目录"""
        self.soure = soure
        self.trange = trange
        if soure.is_file():
            self.copy = getattr(self, f"copy{self.soure.suffix[1:].capitalize()}")
        # try:
        #     trange.iterdir().__next__()
        # except StopIteration:
        #     robocopy(soure, trange)
        #     self.session = None
        # else:
        #     self.session = inspectfile(soure, trange)

    def run(self) -> None:
        self.copy()

    def __getattr__(self, item):
        return self.copyFile

    def copyFile(self):
        return robocopy(self.soure.parent, self.trange.parent, ("/IF", self.soure.name))

    def copyUproject(self):
        tmp = robocopy(self.soure.parent, self.trange.parent, ("/IF", self.soure.name))
        tmp += robocopy(self.soure.parent.joinpath("Content"), self.trange.parent.joinpath("Content"), ("/E",))
        return tmp

if __name__ == '__main__':
    left = pathlib.Path("D:\\ue_project")
    right = pathlib.Path("D:\\ue_project_backup")
    # inspectfile(left, right)
    # copyFile(left.as_posix(), right.as_posix())
