import copy
import pathlib

import sqlalchemy
import sqlalchemy.ext.declarative
import sqlalchemy.orm
import script.MySqlComm
import sqlalchemy.sql


# # 定义类型检查
# def Typed(expected_type, cls=None):
#     if cls is None:
#         return lambda cls: Typed(expected_type, cls)
#     super_set = cls.__set__
#
#     def __set__(self, instance, value):
#         if not isinstance(value, expected_type):
#             raise TypeError('expected ' + str(expected_type))
#         super_set(self, instance, value)
#
#     cls.__set__ = __set__
#     return cls
#
#
# @Typed(int)
# class integer():
#     pass

class _root(script.MySqlComm.Base):
    __abstract__ = True
    id: int = sqlalchemy.Column(sqlalchemy.SMALLINT, primary_key=True)
    file: str = sqlalchemy.Column(sqlalchemy.VARCHAR(128))
    fileSuffixes: str = sqlalchemy.Column(sqlalchemy.VARCHAR(32))
    user: str = sqlalchemy.Column(sqlalchemy.VARCHAR(128))
    version: int = sqlalchemy.Column(sqlalchemy.SMALLINT)
    filepath: str = sqlalchemy.Column(sqlalchemy.VARCHAR(1024))
    infor: str = sqlalchemy.Column(sqlalchemy.VARCHAR(4096))
    filetime = sqlalchemy.Column(sqlalchemy.DATETIME,
                                 server_default=sqlalchemy.sql.func.now(),
                                 server_onupdate=sqlalchemy.sql.func.now())


class _shot(_root):
    __tablename__ = "ep001"
    episodes: int = sqlalchemy.Column(sqlalchemy.SMALLINT)
    shot: int = sqlalchemy.Column(sqlalchemy.SMALLINT)
    shotab: str = sqlalchemy.Column(sqlalchemy.VARCHAR(8))
    department: str = sqlalchemy.Column(sqlalchemy.VARCHAR(128))
    Type: str = sqlalchemy.Column(sqlalchemy.VARCHAR(128))


class _ass(_root):
    __tablename__ = "props"
    name: str = sqlalchemy.Column(sqlalchemy.VARCHAR(256))
    type: str = sqlalchemy.Column(sqlalchemy.VARCHAR(128))


class _episodes(script.MySqlComm.Base):
    __tablename__ = "mainshot"
    id: int = sqlalchemy.Column(sqlalchemy.SMALLINT, primary_key=True)
    episodes: int = sqlalchemy.Column(sqlalchemy.SMALLINT)


class PrjCode():
    mysqllib: str
    _root: pathlib.Path
    query_id: int
    id: int
    Type: str
    file: str
    fileSuffixes: str
    user: str
    version: int
    filepath: str
    infor: str
    filetime: float

    def __init__(self, mysql_lib: str, sort_root: str, prj_root: str):
        """
        初始化一些属性
        :param mysql_lib: str
        :param sort_root: str
        :param prj_root: str
        """
        self._root = pathlib.Path(sort_root).joinpath(prj_root)
        self.mysqllib = mysql_lib
        self.comsql = script.MySqlComm.commMysql(mysql_lib)

    def submitInfo(self, filename: str, suffix: str, user: str, version: int, filepathAndname: str, infor=""):
        pass

    def getScreenshot(self):
        pass

    def getScreenshotPath(self):
        pass

    def getFileName(self, version: int, user_: str, suffix: str, prefix: str = "") -> str:
        pass

    def getFilePath(self, folder_type: str = "Scenefiles") -> pathlib.Path:
        pass

    def getMaxVersion(self) -> int:
        pass

    def queryFileName(self, id__: int) -> pathlib.Path:
        pass

    def queryFlipBook(self, ass_type: str) -> pathlib.Path:
        pass

    def undataInformation(self, query_id: int):
        pass


class PrjShot(PrjCode):
    # <editor-fold desc="Description">
    episodes: int
    shot: int
    shotab: str
    department: str

    # </editor-fold>

    def getEpsodes(self) -> list:
        """
        获得镜头列表
        :return: list
        """

        _shot.__table__.name = "mainshot"
        eps = []

        with self.comsql.session() as session:
            # assert isinstance(session, sqlalchemy.orm.session.Session)
            eps = session.query(_shot.episodes).all()

        return ['ep{:0>3d}'.format(ep[0]) for ep in eps]

    def getShot(self, sort: str = "shot") -> list:
        """
        获得shot列表
        :return: list
        """
        _shot.__table__.name = f"ep{self.episodes:0>3d}"
        shots = []
        with self.comsql.session() as session:
            assert isinstance(session, sqlalchemy.orm.session.Session)
            shots = session.query(_shot.shot, _shot.shotab). \
                order_by(_shot.shot). \
                filter_by(episodes=self.episodes). \
                distinct().all()
        return ['sc{:0>4d}'.format(shot[0]) if shot[1] == ''
                else 'sc{:0>4d}{}'.format(shot[0], shot[1]) for shot in shots]

    def getDepartment(self) -> list:
        """
        获得部门列表
        :return: lsit
        """
        deps = []
        with self.comsql.session() as session:
            # assert isinstance(session, sqlalchemy.orm.session.Session)
            deps = session.query(_shot.department). \
                order_by(_shot.department). \
                filter_by(episodes=self.episodes, shot=self.shot, shotab=self.shotab). \
                distinct().all()
        return [dep[0] for dep in deps]

    def getDepType(self) -> list:
        """
        获得部门类型列表
        :return: list
        """
        dep_types = []
        with self.comsql.session() as session:
            # assert isinstance(session, sqlalchemy.orm.session.Session)
            dep_types = session.query(_shot.Type). \
                order_by(_shot.Type). \
                filter_by(episodes=self.episodes, shot=self.shot, shotab=self.shotab, department=self.department). \
                distinct().all()
        return [dep_type[0] for dep_type in dep_types]

    def getFile(self) -> list:
        """
        获得文件信息(版本,评论,上传者,后缀,id)
        :return:
        """
        files = []
        with self.comsql.session() as session:
            # assert isinstance(session, sqlalchemy.orm.session.Session)
            files = session.query(_shot.version, _shot.infor, _shot.user, _shot.fileSuffixes, _shot.id). \
                filter_by(episodes=self.episodes, shot=self.shot,
                          shotab=self.shotab, department=self.department, Type=self.Type). \
                distinct().all()
        return files

    def getFilePath(self, folder_type: str = "Scenefiles") -> pathlib.Path:
        path = self._root.joinpath(f'ep{self.episodes:0>3d}',
                                   f'sc{self.shot:0>4d}',
                                   folder_type,
                                   self.department,
                                   self.Type
                                   )
        return path

    def getFileName(self, version: int, user_: str, suffix: str, prefix: str = "") -> str:
        name = f"{prefix}shot_ep{self.episodes:0>3d}_sc{self.shot:0>4d}{self.shotab}_" \
               f"{self.department}_" \
               f"{self.Type}_v{version:0>4d}" \
               f"__{user_}_{suffix}"
        return name

    def getMaxVersion(self) -> int:
        with self.comsql.session() as session:
            # assert isinstance(session, sqlalchemy.orm.session.Session)
            file_data = session.query(_shot.version). \
                order_by(sqlalchemy.desc(_shot.version)). \
                filter_by(episodes=self.episodes, shot=self.shot,
                          shotab=self.shotab, department=self.department, Type=self.Type). \
                distinct().first()
        if file_data:
            version_max: int = int(file_data[0])
        else:
            version_max: int = 0
        return version_max

    def submitInfo(self, filename: str = '', suffix: str = '', user: str = '', version: int = 0,
                   filepathAndname: str = '', infor=""):
        """
        提交文件信息
        :param filename: str
        :param suffix:str
        :param user:str
        :param version:int
        :param filepathAndname:str
        :param infor: str
        :return:
        """
        sub = _shot(episodes=self.episodes, shot=self.shot, shotab=self.shotab,
                    department=self.department, Type=self.Type, file=self.file, fileSuffixes=self.fileSuffixes,
                    user=self.user, version=self.version, filepath=self.filepath, infor=self.infor)
        sub.__table__.name = f"ep{self.episodes:0>3d}"
        with self.comsql.session() as session:
            assert isinstance(session, sqlalchemy.orm.session.Session)
            # session.expire_on_commit = False
            session.add(sub)

    def subEpisodesInfo(self, episodes: int):
        _shot.__table__.name = f"ep{episodes:0>3d}"
        _shot.__table__.create(self.comsql.engine)

        self.episodes = episodes

        with self.comsql.sessionOne() as session:
            session.add(_episodes(episodes=self.episodes))

    def queryFileName(self, id__: int) -> pathlib.Path:

        with self.comsql.session() as session:
            assert isinstance(session, sqlalchemy.orm.session.Session)
            file_data = session.query(_shot.filepath).filter(_shot.id == id__).one()

        try:
            file_data = file_data.filepath
        except:
            file_data = ""
        return pathlib.Path(file_data)

    def getScreenshot(self) -> pathlib.Path:
        path: pathlib.Path = self._root.joinpath(f'ep{self.episodes:0>3d}',
                                                 f'sc{self.shot:0>4d}{self.shotab}',
                                                 'Playblasts',
                                                 self.department,
                                                 self.Type,
                                                 "Screenshot",
                                                 f"ep{self.episodes:0>3d}_sc{self.shot:0>4d}{self.shotab}.jpg"
                                                 )
        return path

    def getScreenshotPath(self) -> pathlib.Path:
        with self.comsql.session() as session:
            # assert isinstance(session, sqlalchemy.orm.session.Session)
            file_data = session.query(_shot.filepath). \
                filter_by(episodes=self.episodes, shot=self.shot, shotab=self.shotab,
                          department=self.department, Type=self.Type,
                          fileSuffixes='.jpg'). \
                order_by(sqlalchemy.desc(_shot.filetime)).first()
        try:
            file_data = pathlib.Path(file_data[0])
        except:
            file_data = pathlib.Path("")
        return file_data

    def queryFlipBook(self, ass_type: str) -> pathlib.Path:
        with self.comsql.session() as session:
            # assert isinstance(session, sqlalchemy.orm.session.Session)
            path = session.query(_shot.filepath). \
                filter_by(episodes=self.episodes, shot=self.shot, shotab=self.shotab,
                          department=self.department, Type=ass_type,
                          fileSuffixes='.mp4'). \
                order_by(sqlalchemy.desc(_shot.filetime)).first()
        try:
            path = pathlib.Path(path[0])
        except:
            path = pathlib.Path("")
        return path

    def queryFlipBookShot(self, shot: int) -> pathlib.Path:
        with self.comsql.session() as session:
            assert isinstance(session, sqlalchemy.orm.session.Session)
            path = session.query(_shot.filepath). \
                filter_by(episodes=self.episodes, shot=shot, fileSuffixes='.mp4'). \
                order_by(sqlalchemy.desc(_shot.filetime)).first()
        try:
            path = pathlib.Path(path[0])
        except:
            path = pathlib.Path("")
        return path

    def undataInformation(self, query_id: int):
        with self.comsql.session() as session:
            # assert isinstance(session, sqlalchemy.orm.session.Session)
            data:_shot = session.query(_shot).get(query_id)
            data.infor = self.infor


class PrjAss(PrjCode):
    sort: str
    name: str

    def getAssClass(self) -> list:
        """
        获得资产类型
        :return: list
        """
        _ass.__table__.name = self.sort
        datas = []
        with self.comsql.session() as session:
            datas = session.query(_ass.name).distinct().order_by(_ass.name)
        return [data[0] for data in datas]

    def getAssType(self) -> list:
        """
        获得资产类型细分
        :return:
        """
        datas = []
        with self.comsql.session() as session:
            # assert isinstance(session, sqlalchemy.orm.session.Session)
            datas = session.query(_ass.type).filter_by(name=self.name).distinct()
        return [data[0] for data in datas]

    def getFileInfo(self) -> list:
        """
        获得文件信息(版本,评论,制作人,后缀)
        :return:
        """
        file_data = []
        with self.comsql.session() as session:
            # assert isinstance(session, sqlalchemy.orm.session.Session)
            file_data = session.query(_ass.version, _ass.infor, _ass.user, _ass.fileSuffixes,
                                      _ass.id).filter_by(name=self.name, type=self.Type).distinct().all()
        return file_data

    def getFilePath(self, folder_type: str = "Scenefiles") -> pathlib.Path:
        path = self._root.joinpath(self.sort,
                                   self.name,
                                   folder_type,
                                   self.Type
                                   )
        return path

    def getFileName(self, version: int, user_: str, suffix: str, prefix: str = "") -> str:
        add_suffix = ""
        if self.Type in ["rig"]:
            add_suffix = "_rig"
        name = "{prefix}{cl}{su}{suffix}".format(cl=self.name, su=add_suffix,
                                                 suffix=suffix, prefix=prefix)
        return name

    def getMaxVersion(self) -> int:
        file_data = []
        with self.comsql.session() as session:
            # assert isinstance(session, sqlalchemy.orm.session.Session)
            file_data = session.query(_ass.version). \
                order_by(sqlalchemy.desc(_ass.version)). \
                filter_by(name=self.name, type=self.Type). \
                distinct().first()

        if file_data:
            version_max: int = int(file_data[0])
        else:
            version_max: int = 0
        return version_max

    def submitInfo(self, file_name: str, suffix: str, user: str, version: int,
                   filepath_and_name: str, infor: str = ""):
        sub = _ass(name=self.name, type=self.Type, file=self.file, fileSuffixes=self.fileSuffixes,
                   user=self.user, version=self.version, filepath=self.filepath, infor=self.infor)
        sub.__table__.name = self.sort
        with self.comsql.session() as session:
            session.add(sub)

    def queryFileName(self, id__: int) -> pathlib.Path:
        with self.comsql.session() as session:
            assert isinstance(session, sqlalchemy.orm.session.Session)
            file_data = session.query(_ass.filepath).filter(_ass.id == id__).one()
        try:
            file_data = file_data[0]
        except:
            file_data = ""
        return pathlib.Path(file_data)

    def getScreenshot(self) -> pathlib.Path:
        path: pathlib.Path = self._root.joinpath(self.sort,
                                                 self.name,
                                                 'Playblasts',
                                                 self.Type,
                                                 "Screenshot",
                                                 f"{self.name}_{self.Type}.jpg"
                                                 )
        return path

    def getScreenshotPath(self) -> pathlib.Path:
        with self.comsql.session() as session:
            file_data = session.query(_ass.filepath). \
                filter_by(name=self.name, type=self.Type, fileSuffixes='.jpg'). \
                order_by(sqlalchemy.desc(_ass.filetime)).first()
        try:
            file_data = pathlib.Path(file_data[0])
        except:
            file_data = pathlib.Path("")
        return file_data

    def queryFlipBook(self, ass_type: str) -> pathlib.Path:
        with self.comsql.session() as session:
            assert isinstance(session, sqlalchemy.orm.session.Session)
            path = session.query(_ass.filepath). \
                filter_by(name=self.name, type=ass_type, fileSuffixes=".mp4"). \
                order_by(sqlalchemy.desc(_ass.filetime)).first()
        try:
            path = pathlib.Path(path[0])
        except:
            path = pathlib.Path("")
        return path
