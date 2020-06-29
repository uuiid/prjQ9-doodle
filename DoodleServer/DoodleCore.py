import pathlib
import threading
import logging
import traceback
import sqlalchemy.orm

from DoodleServer.DoodleOrm import *
import DoodleServer.DoodleSql as Conect
import DoodleServer.DoodleZNCHConvert as Convert
import DoodleServer.DoodleDictToObject as DoleDict
import zmq

from DoodleServer.DoodleOrm import Episodes, Shot


class PrjCore(object):
    query_id: int

    def __init__(self, mysql_lib: str, sort_root: str, prj_root: str):
        """
        初始化一些属性
        :param mysql_lib: str
        :param sort_root: str
        :param prj_root: str
        """
        self._root = pathlib.Path(prj_root)
        self._prj_root_ = pathlib.Path(sort_root)
        self.mysqllib = mysql_lib
        self.comsql = Conect.commMysql(mysql_lib)

    def queryMaxVersion(self, base_class: DoleSql.Base) -> int:
        pass

    def queryFile(self, base_class: DoleSql.Base) -> typing.List[DoleSql.Base]:
        pass

    def subClass(self, base_class: DoleSql.Base):
        with self.comsql.sessionOne() as session:
            assert isinstance(session, sqlalchemy.orm.session.Session)
            session.add(base_class)

    def quertById(self, base_class: DoleSql.Base, query_id: int = -1):
        if query_id < 0:
            query_id = self.query_id
        with self.comsql.sessionOne() as session:
            assert isinstance(session, sqlalchemy.orm.session.Session)
            data = session.query(base_class).filter(base_class.id == query_id).one
        if data:
            data = data[0]
        else:
            data = None
        return data


class PrjShot(PrjCore):
    episodes: int
    shot: int
    shotab: str
    file_class: str
    file_type: str

    eps_obj:Episodes
    shot_obj:Shot
    file_class_obj:fileClass
    file_type_obj:fileType

    def queryEps(self) -> typing.List[str]:
        """
        获得所有集数信息
        :return:
        """
        with self.comsql.sessionOne() as session:
            assert isinstance(session, sqlalchemy.orm.session.Session)
            data = session.query(Episodes.episodes).order_by(Episodes.episodes).all()
        return ['ep{:0>3d}'.format(ep[0]) for ep in data]

    def queryShot(self) -> typing.List[str]:
        """
        获得一集中的镜头信息
        :return:
        """
        with self.comsql.sessionOne() as session:
            assert isinstance(session, sqlalchemy.orm.session.Session)
            data = session.query(Shot.shot_, Shot.shotab) \
                .join(Episodes) \
                .filter(Episodes.episodes == self.episodes).order_by(Shot.shot_).all()

        return ['sc{:0>4d}'.format(shot[0]) if shot[1] == ''
                else 'sc{:0>4d}{}'.format(shot[0], shot[1]) for shot in data]

    def queryFileClass(self) -> typing.List[str]:
        """
        查询文件类型信息
        :return:
        """
        with self.comsql.sessionOne() as session:
            assert isinstance(session, sqlalchemy.orm.session.Session)
            data = session.query(fileClass.file_class) \
                .join(Shot, Episodes) \
                .filter(Shot.shot_ == self.shot) \
                .filter(Shot.shotab == self.shotab) \
                .filter(Episodes.episodes == self.episodes) \
                .order_by(fileClass.file_class).all()
        return [dep[0] for dep in data]

    def queryFileType(self) -> typing.List[str]:
        """
        查询文件种类信息
        :return:
        """
        with self.comsql.sessionOne() as session:
            assert isinstance(session, sqlalchemy.orm.session.Session)
            data = session.query(fileType.file_type) \
                .join(fileClass, Shot, Episodes) \
                .filter(fileClass.file_class == self.file_class) \
                .filter(Shot.shot_ == self.shot) \
                .filter(Shot.shotab == self.shotab) \
                .filter(Episodes.episodes == self.episodes) \
                .order_by(fileClass.file_class).all()
        return [dep_type[0] for dep_type in data]

    def queryFile(self, base_class: DoleSql.Base) -> typing.List[DoleSql.Base]:
        """
        查询文件本身信息
        :param base_class:文件类名
        :return:
        """
        with self.comsql.sessionOne() as session:
            assert isinstance(session, sqlalchemy.orm.session.Session)
            data = session.query(base_class) \
                .join(fileType, fileClass, Shot, Episodes) \
                .filter(fileType.file_type == self.file_type) \
                .filter(fileClass.file_class == self.file_class) \
                .filter(Shot.shot_ == self.shot) \
                .filter(Shot.shotab == self.shotab) \
                .filter(Episodes.episodes == self.episodes) \
                .order_by(base_class.filetime.desc()).all()
        return data

    def queryMaxVersion(self, base_class: DoleSql.Base) -> int:
        with self.comsql.sessionOne() as session:
            assert isinstance(session, sqlalchemy.orm.session.Session)
            data = session.query(base_class.version) \
                .join(fileType, fileClass, Shot, Episodes) \
                .filter(fileType.file_type == self.file_type) \
                .filter(fileClass.file_class == self.file_class) \
                .filter(Shot.shot_ == self.shot) \
                .filter(Shot.shotab == self.shotab) \
                .filter(Episodes.episodes == self.episodes) \
                .order_by(base_class.version).one()
        if data:
            data = data[0]
        else:
            data = 0
        return data

    def commPath(self, folder_type: str = "Scenefiles") -> pathlib.Path:
        """
        组合镜头信息, 返回文件路径
        """
        path = self._root.joinpath(f'ep{self.episodes:0>3d}',
                                   f'sc{self.shot:0>4d}{self.shotab}',
                                   folder_type,
                                   self.file_class,
                                   self.file_type
                                   )
        return path

    def commName(self, version: int, user_: str, suffix: str = "", prefix: str = "") -> str:
        """
        组合文件信息,  生成文件名称
        """
        name = f"{prefix}shot_ep{self.episodes:0>3d}_sc{self.shot:0>4d}{self.shotab}_" \
               f"{self.file_class}_" \
               f"{self.file_type}_v{version:0>4d}" \
               f"__{user_}_{suffix}"
        return name


class PrjAss(PrjCore):
    file_class: str
    ass_name:str
    file_type: str

    file_class_obj: fileClass
    ass_name_obj: assClass
    file_type_obj: fileType

    def queryAssClass(self):
        with self.comsql.sessionOne() as session:
            assert isinstance(session, sqlalchemy.orm.session.Session)
            data = session.query(fileClass.file_class) \
                .order_by(fileClass.file_class) \
                .filter(fileClass.__shot__.is_(None)).all()
        return [d[0] for d in data]

    def queryAssname(self):
        with self.comsql.sessionOne() as session:
            assert isinstance(session, sqlalchemy.orm.session.Session)
            data = session.query(assClass.file_name) \
                .order_by(assClass.file_class) \
                .join(fileClass)\
                .filter(fileClass.file_class == self.file_class)\
                .all()
        return [d[0] for d in data]

    def queryAssType(self):
        with self.comsql.sessionOne() as session:
            assert isinstance(session, sqlalchemy.orm.session.Session)
            data = session.query(fileType.file_type) \
                .join(assClass)\
                .filter(assClass.file_name == self.ass_name) \
                .all()
        return [d[0] for d in data]

    def queryFile(self, base_class: DoleSql.Base) -> typing.List[DoleSql.Base]:
        with self.comsql.sessionOne() as session:
            assert isinstance(session, sqlalchemy.orm.session.Session)
            data = session.query(base_class)\
                .join(assClass,fileType) \
                .filter(assClass.file_name == self.ass_name) \
                .filter(fileType.file_type == self.file_type) \
                .all()
        return data

    def queryMaxVersion(self, base_class: DoleSql.Base) -> int:
        with self.comsql.sessionOne() as session:
            assert isinstance(session, sqlalchemy.orm.session.Session)
            data = session.query(base_class.version)\
                .join(assClass,fileType) \
                .filter(assClass.file_name == self.ass_name) \
                .filter(fileType.file_type == self.file_type) \
                .order_by(base_class.version).one()
        if data:
            data = data[0]
        else:
            data = 0
        return data

class DoodleServer(threading.Thread):
    server = None
    connect: zmq.Context
    socket: zmq.Socket

    def __init__(self, doodle_set):
        super().__init__()
        self.doodle_set = doodle_set
        """=============="""
        # self.shot = script.DooDlePrjCode.PrjShot(self.doodle_set.projectname,
        #                                          self.doodle_set.project,
        #                                          self.doodle_set.shotRoot)
        # self.ass = script.DooDlePrjCode.PrjAss(self.doodle_set.projectname,
        #                                        self.doodle_set.project,
        #                                        self.doodle_set.assetsRoot)

    def run(self):
        self.connect = zmq.Context()
        self.socket = self.connect.socket(zmq.REP)
        self.socket.bind("tcp://127.0.0.1:23369")

        # self.server = Conn.Listener(("127.0.0.1", 23369), authkey=b"doodle")
        while True:
            try:
                self.recv_data = self.socket.recv_pyobj()
                if self.recv_data == b'close':
                    self.socket.send_pyobj(b"close")
                    self.socket.close()
                    break
                self.analysis()
            except EOFError:
                logging.error(traceback.print_exc())
                self.socket.send_pyobj("+++出错了++++")
                break
            finally:
                logging.info("完成了一次转发")

    def analysis(self):
        logging.info("开始分析传入数据")
        try:
            data = DoleDict.convertTool().convert(self.recv_data)
            getattr(self, data.url)(data)
        except EOFError:
            logging.error(traceback.print_exc())

    def getDoodleSet(self, data):
        my_set = {"user": Convert.isChinese(self.doodle_set.user).easyToEn(),
                  "department": self.doodle_set.department,
                  "projectname": self.doodle_set.projectname, "cache_path": self.doodle_set.cache_path.as_posix()}
        self.socket.send_pyobj(my_set, protocol=2)


if __name__ == '__main__':
    import DoodleServer.DoodleSet as DoleSet

    t = DoodleServer(DoleSet.Doodlesetting())
    t.start()
    t.join()
