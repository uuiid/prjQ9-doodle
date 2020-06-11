import datetime
import logging
import os
import pathlib
import queue
import re
import subprocess
import tempfile
import threading

import mysql.connector
import sqlalchemy
import sqlalchemy.ext.declarative
import sqlalchemy.orm
import sqlalchemy.pool
import xml.etree.ElementTree as Et
import pathlib

Base = sqlalchemy.ext.declarative.declarative_base()

_path_my_ = set()

ok = False


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
    com = ["powershell.exe", "robocopy", soure.as_posix(), trange.as_posix(), "/FP", "/NJH", "/NJS", "/NDL","/NS"] + list(ecom)
    if not ok:
        com += ["/L"]
    p = subprocess.Popen(com, stdout=subprocess.PIPE, encoding="gbk")
    out_ = p.stdout.readlines()

    def NotNone(m_list) -> list:
        return [n.strip() for n in m_list if n]

    out_ = [NotNone(re.split("\\n|\\t", o)) for o in out_]

    return out_


def copyItem(soure: str, trange: str):
    com = ["powershell.exe", "Copy-Item", soure, trange]
    p = subprocess.Popen(com, stdout=subprocess.PIPE, encoding="gbk")
    out_ = p.stdout.readlines()
    return out_


class copyeasily(object):
    soure: pathlib.Path
    trange: pathlib.Path

    def __init__(self, soure: pathlib.Path, trange: pathlib.Path):
        getattr(self, f"copy{self.soure.suffix[1:].capitalize()}")
        try:
            trange.iterdir().__next__()
        except StopIteration:
            robocopy(soure, trange)
            self.session = None
        else:
            self.session = inspectfile(soure, trange)

    def __getattr__(self, item):
        return self.copyFile

    def copyFile(self):
        robocopy(self.soure.parent, self.trange.parent, ("/IF", self.soure.name))

    def copyUproject(self):
        robocopy(self.soure.parent, self.trange.parent, ("/IF", self.soure.name))
        robocopy(self.soure.parent.joinpath("Content"), self.trange.parent.joinpath("Content"), ("/E",))

def indent(elem, level=0):
    i = "\n" + level * "\t"
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "\t"
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level + 1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i

def weiteXml(doc: pathlib.Path, synFile: list,**syn_parameter) -> pathlib.Path:
    '''传入对象是一个写入文件的路径和一个同步列表,
    key : fileName Include Exclude Variant VersioningFolder
    Variant(TwoWay,Update)
    这个列表由一个key是Left和Right的字典构成'''
    template_path = pathlib.Path("template\\temp.ffs_batch")
    tree = Et.parse(str(template_path))
    # 加入同步目录
    for syn in synFile:
        pair = Et.SubElement(tree.findall('./FolderPairs')[0], 'Pair')
        LElement = Et.SubElement(pair, "Left")
        LElement.text = syn['Left']
        RElement = Et.SubElement(pair, "Right")
        RElement.text = syn['Right']

    # 查看是否具有过滤器,如果有就删除原来过滤器后添加传入过滤器
    if 'Include' in syn_parameter.keys():
        includes = syn_parameter['Include']
        include_my = tree.findall('./Filter/Include')[0]
        include_my.remove(include_my.findall('./Item')[0])
        for include_i in includes:
            includepath = Et.SubElement(include_my, 'Item')
            includepath.text = include_i
    if 'Exclude' in syn_parameter.keys():
        exclude = syn_parameter['Exclude']
        exclude_my = tree.findall('./Filter/Exclude')[0]
        for exclude_i in exclude:
            exclude_path = Et.SubElement(exclude_my, 'Item')
            exclude_path.text = exclude_i
    # 设置同步方式
    if 'Variant' in syn_parameter.keys():
        variant = syn_parameter['Variant']
        variant_my = tree.findall('./Synchronize/Variant')[0]
        variant_my.text = variant
    # 设置同步时备份目录
    if 'VersioningFolder' in syn_parameter.keys():
        versioningFolder = syn_parameter['VersioningFolder']
        VersioningFolder_my = tree.findall('./Synchronize/VersioningFolder')[0]
        VersioningFolder_my.text = versioningFolder
    # 将xml文档格式化
    root = tree.getroot()
    indent(root)
    # 获取写入文件路径和文件命
    writePath = doc.joinpath('{}.ffs_batch'.format(syn_parameter['fileName']))
    # 写入文件
    tree.write(writePath.as_posix(), encoding='utf-8', xml_declaration=True)
    return writePath

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


def _backup(trange: pathlib.Path, dubuxiaoyao: str,synwaithpath:pathlib.Path, fujia):
    path = []
    sql2 = """SELECT episodes from mainshot"""

    eps = selsctCommMysql(dubuxiaoyao, "", "", sql2)
    for ep in eps:
        sql = f"""SELECT episodes,shot,shotab,department,Type,filepath FROM (SELECT * FROM `ep{ep[0]:0>3d}` order by version desc limit 10000) as tab group by tab.shot,tab.shotab,tab.department,tab.Type"""
        path += [[p[-1], f"shots\\ep{p[0]:0>3d}\\sc{p[1]:0>4d}{p[2]}\\{p[3]}\\{p[4]}"] for p in
                 selsctCommMysql(dubuxiaoyao, "", "", sql)]
    for ass in ["character", "effects", "props", "scane"]:
        sql3 = f"""SELECT name,type,filepath FROM (SELECT * FROM `{ass}` order by version desc limit 10000) as tab group by tab.name,tab.type"""
        path += [[p[-1], f"ass\\{ass}\\{p[0]}\\{p[1]}"] for p in selsctCommMysql(dubuxiaoyao, "", "", sql3)]

    light = """SELECT value FROM `configure` WHERE name='synSever'"""
    synpath = selsctCommMysql(dubuxiaoyao, "", "", light)[0][0]

    for syn in selsctCommMysql(dubuxiaoyao, "", "", """SELECT DISTINCT value4 FROM `configure`"""):
        if syn[0]:
            path.append([os.path.abspath(os.path.join(synpath, syn[0])), f"ass\\light\\{syn[0]}"])

    # tmp = pathlib.Path(tempfile.gettempdir()).joinpath("testpath.txt")
    # tmp.write_text("\n".join([f"{ii[0]}--->{ii[1]}" for ii in path]),encoding="utf-8")

    com_copy = []
    for p_ in path:
        p = pathlib.Path(p_[0])
        if p.is_file():
            if p.suffix in [".uproject"]:
                com_copy.append(
                    [p.parent.joinpath("Content"), trange.joinpath(p_[1], "Content")])
                com_copy.append([p.parent, trange.joinpath(p_[1])])
            else:
                com_copy.append([p.parent, trange.joinpath(p_[1])])
                # robocopy(p.parent,trange,("/E",""))
        else:
            com_copy.append([p, trange.joinpath(p_[1])])
    fujia(com_copy, trange)

    # syn_dist =[]
    # for t__ in com_copy:
    #     syn_dist.append({"Left":t__[0].as_posix(),"Right":t__[1].as_posix()})
    # for i__ in range((com_copy.__len__()/100).__int__()):
    #     weiteXml(synwaithpath,syn_dist[i__:i__+100],fileName=dubuxiaoyao + f"{i__}")
    synwaithpath.joinpath("test.txt").write_text(
        "\n".join([f"{ii[0]}--->{ii[1]}" for ii in com_copy]),
        encoding="utf-8")
    # for i in com_copy:
    #     out = robocopy(*i)
    #     yield out


def fuJiaDBXX(com_copy, trange):
    com_copy.append([pathlib.Path("Y:\\动画共享资料\\3-进行中的动画项目\\2-独步逍遥\\3-设定\\2-动画设定"), trange.joinpath("原画\\动画设定")])
    com_copy.append([pathlib.Path("Y:\\动画共享资料\\3-进行中的动画项目\\2-独步逍遥\\7-分镜"), trange.joinpath("分镜")])
    com_copy.append([pathlib.Path("Y:\\动画共享资料\\3-进行中的动画项目\\2-独步逍遥\\1-文本"), trange.joinpath("剧本")])
    com_copy.append([pathlib.Path("W:\\03_Workflow\\backup"), trange.joinpath("动画外包")])


if __name__ == '__main__':

    synpath = pathlib.Path("D:\\test\\")

    left = pathlib.Path("E:\\dubuxiaoyao")
    # right = pathlib.Path("E:\\dubuxiaoyao")
    texts = _backup(left, "dubuxiaoyao",synpath, fuJiaDBXX)

    # tmp = pathlib.Path(tempfile.gettempdir()).joinpath("test_out.txt")
    # for text in texts:
    #     with open(tmp,mode="a+",encoding='utf-8') as f:
    #         f.write("\n".join([" --> ".join(t) for t in text if t]))
    # inspectfile(left, right)
    # copyFile(left.as_posix(), right.as_posix())
