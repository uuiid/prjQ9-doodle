import copy
import logging
import pathlib
import typing
import cachetools

import sqlalchemy
import sqlalchemy.ext.declarative
import sqlalchemy.orm
import script.MySqlComm
import sqlalchemy.sql
import script.convert


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

# <editor-fold desc="数据库类">
class nameTochinese(script.MySqlComm.Base):
    __tablename__ = "nameTochinese"
    id: int = sqlalchemy.Column(sqlalchemy.SMALLINT, primary_key=True)
    name: str = sqlalchemy.Column(sqlalchemy.VARCHAR(128), unique=True)
    localname: str = sqlalchemy.Column(sqlalchemy.VARCHAR(128), unique=True)


class _root(script.MySqlComm.Base):
    __abstract__ = True
    id: int = sqlalchemy.Column(sqlalchemy.SMALLINT, primary_key=True)
    file: str = sqlalchemy.Column(sqlalchemy.VARCHAR(128))
    fileSuffixes: str = sqlalchemy.Column(sqlalchemy.VARCHAR(32))
    user: str = sqlalchemy.Column(sqlalchemy.VARCHAR(128))
    version: int = sqlalchemy.Column(sqlalchemy.SMALLINT)
    filepath: str = sqlalchemy.Column(sqlalchemy.VARCHAR(1024))
    infor: str = sqlalchemy.Column(sqlalchemy.VARCHAR(4096))
    filestate = sqlalchemy.Column(sqlalchemy.VARCHAR(64))
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


# </editor-fold>


class convertMy(object):

    def __init__(self, mysql_lib: str):
        self.comsql = script.MySqlComm.commMysql(mysql_lib)

        self.name = {}
        self.local_name = {}
        self.getnameTochinese()

    def getnameTochinese(self):
        with self.comsql.session() as session:
            assert isinstance(session, sqlalchemy.orm.session.Session)
            names = session.query(nameTochinese.name, nameTochinese.localname).all()
            self.name = {name[0]: name[1] for name in names}
            self.local_name = {name[1]: name[0] for name in names}

    def toEn(self, zn_ch):
        try:
            m_name = self.local_name[zn_ch]
        except KeyError as err:
            logging.error("转换时库中没有键值")
            m_name = script.convert.isChinese(zn_ch).easyToEn()
        return m_name

    def toZnCh(self, en):
        try:
            m_name = self.name[en]
        except KeyError as err:
            logging.error("转换时库中没有键值")
            m_name = en
        return m_name

    def addLocalName(self, en: str, zn_ch):
        sub = nameTochinese(name=en, localname=zn_ch)
        with self.comsql.session() as session:
            session.add(sub)
        self.getnameTochinese()


class PrjCode(object):
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
    filestate: str
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
        self.convertMy = convertMy(mysql_lib=mysql_lib)

    def submitInfo(self, filename: str, suffix: str, user: str, version: int, filepathAndname: str, infor=""):
        """
        提交文件信息
        """
        pass

    def getScreenshot(self):
        """
        获得截图镜头
        """
        pass

    def getScreenshotPath(self):
        """
        获得截图路径
        """
        pass

    def getFileName(self, version: int, user_: str, suffix: str, prefix: str = "") -> str:
        """
        获得文件名称
        """
        pass

    def getFilePath(self, folder_type: str = "Scenefiles") -> pathlib.Path:
        """
        获得文件路径
        """
        pass

    def getMaxVersion(self) -> int:
        """
        获得最大版本
        """
        pass

    def queryFileName(self, id__: int) -> pathlib.Path:
        """
        查询文件名称
        """
        pass

    def queryFlipBook(self, ass_type: str) -> pathlib.Path:
        """
        查询拍屏
        """
        pass

    def undataInformation(self, query_id: int):
        """
        更新信息
        """
        pass

    def getFileState(self, flag) -> sqlalchemy.orm.query.Query:
        """
        获得文件状态
        """
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
        with self.comsql.session() as session:
            # assert isinstance(session, sqlalchemy.orm.session.Session)
            eps = session.query(_shot.episodes).order_by(_episodes.episodes).all()

        return ['ep{:0>3d}'.format(ep[0]) for ep in eps]

    def getShot(self) -> list:
        """
        获得shot列表
        :return: list
        """
        _shot.__table__.name = f"ep{self.episodes:0>3d}"
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
        """
        组合镜头信息, 返回文件路径
        """
        path = self._root.joinpath(f'ep{self.episodes:0>3d}',
                                   f'sc{self.shot:0>4d}{self.shotab}',
                                   folder_type,
                                   self.department,
                                   self.Type
                                   )
        return path

    def getFileName(self, version: int, user_: str, suffix: str, prefix: str = "") -> str:
        """
        组合文件信息,  生成文件名称
        """
        name = f"{prefix}shot_ep{self.episodes:0>3d}_sc{self.shot:0>4d}{self.shotab}_" \
               f"{self.department}_" \
               f"{self.Type}_v{version:0>4d}" \
               f"__{user_}_{suffix}"
        return name

    def getMaxVersion(self) -> int:
        """
        查询库, 获得最大的文件版本
        """
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
        """
        提交集数,  比较特殊,  因为集数是分片表
        """
        _shot.__table__.name = f"ep{episodes:0>3d}"
        _shot.__table__.create(self.comsql.engine)

        self.episodes = episodes

        with self.comsql.sessionOne() as session:
            session.add(_episodes(episodes=self.episodes))

    def queryFileName(self, id__: int) -> pathlib.Path:
        """
        查询文件名称
        """
        with self.comsql.session() as session:
            assert isinstance(session, sqlalchemy.orm.session.Session)
            file_data = session.query(_shot.filepath).filter(_shot.id == id__).one()

        try:
            file_data = file_data.filepath
        except:
            file_data = ""
        return pathlib.Path(file_data)

    def getScreenshot(self) -> pathlib.Path:
        """
        查询截图路径和名称
        """
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
        """
        获得截图路径
        """
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
        """
        获得拍屏路径
        """
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
        """
        最新拍屏, 按镜头分的最新拍屏
        """
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

    def querFlipBookShotTotal(self, department) -> typing.List[pathlib.Path]:
        with self.comsql.session() as session:
            assert isinstance(session, sqlalchemy.orm.session.Session)
            # .filter(_shot.department == department)
            path = session.query(_shot).filter(_shot.fileSuffixes == ".mp4").order_by(
                _shot.filetime).from_self().group_by(_shot.shot, _shot.shotab).order_by(_shot.shot)
        try:

            path = [pathlib.Path(p.filepath) for p in path]
        except IndexError:
            path = []
        return path

    def undataInformation(self, query_id: int):
        """
        更新拍屏信息以及文件状态
        """
        with self.comsql.session() as session:
            # assert isinstance(session, sqlalchemy.orm.session.Session)
            data: _shot = session.query(_shot).get(query_id)
            data.infor = self.infor
            data.filestate = self.filestate

    def getFileState(self, flag) -> sqlalchemy.orm.query.Query:
        """
        获得文件状态
        """
        with self.comsql.session() as session:
            # assert isinstance(session, sqlalchemy.orm.session.Session)
            data = session.query(_shot).filter(_shot.filestate.isnot(None))
            try:
                data = getattr(self, f"_getFileState{flag}")(data)
            except BaseException as err:
                logging.info("%s", err)
        return data

    def _getFileStateShot(self, data: sqlalchemy.orm.query.Query) -> sqlalchemy.orm.query.Query:
        # 查询条件组合  约束集数变量
        return data.filter(_shot.episodes == self.episodes)

    def _getFileStateDep(self, data: sqlalchemy.orm.query.Query) -> sqlalchemy.orm.query.Query:
        # 约束镜头变量
        data = self._getFileStateShot(data).filter(_shot.shot == self.shot).filter(_shot.shotab == self.shotab)
        return data

    def _getFileStateDepType(self, data: sqlalchemy.orm.query.Query) -> sqlalchemy.orm.query.Query:
        # 约束部门变量
        data = self._getFileStateDep(data).filter(_shot.department == self.department)
        return data

    def _getFileStateFile(self, data: sqlalchemy.orm.query.Query) -> sqlalchemy.orm.query.Query:
        # 约束镜头类型
        data = self._getFileStateDepType(data).filter(_shot.Type == self.Type)
        return data


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
        """
        组合文件信息, 返回路径变量
        """

        path = self._root.joinpath(self.sort,
                                   self.name,
                                   folder_type,
                                   self.Type
                                   )
        return path

    def getFileName(self, version: int, user_: str, suffix: str, prefix: str = "") -> str:
        """
        组合文件名称
        """
        add_suffix = ""
        if self.Type in ["rig"]:
            add_suffix = "_rig"
        name = "{prefix}{cl}{su}{suffix}".format(cl=self.name, su=add_suffix,
                                                 suffix=suffix, prefix=prefix)
        return name

    def getMaxVersion(self) -> int:
        """
        获得文件最高版本
        """
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
        """
        提交截屏
        """
        sub = _ass(name=self.name, type=self.Type, file=self.file, fileSuffixes=self.fileSuffixes,
                   user=self.user, version=self.version, filepath=self.filepath, infor=self.infor)
        sub.__table__.name = self.sort
        with self.comsql.session() as session:
            session.add(sub)

    def queryFileName(self, id__: int) -> pathlib.Path:
        """
        查询文件路径
        """
        with self.comsql.session() as session:
            # assert isinstance(session, sqlalchemy.orm.session.Session)
            file_data = session.query(_ass.filepath).filter(_ass.id == id__).one()
        try:
            file_data = file_data[0]
        except:
            file_data = ""
        return pathlib.Path(file_data)

    def getScreenshot(self) -> pathlib.Path:
        """
        获得截图名称
        """
        path: pathlib.Path = self._root.joinpath(self.sort,
                                                 self.name,
                                                 'Playblasts',
                                                 self.Type,
                                                 "Screenshot",
                                                 f"{self.name}_{self.Type}.jpg"
                                                 )
        return path

    def getScreenshotPath(self) -> pathlib.Path:
        """
        查询截屏路径
        """
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
        """
        查询拍屏,  约束条件是名称和类型
        """
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

    def undataInformation(self, query_id: int):
        """
        更新资产信息
        """
        with self.comsql.session() as session:
            # assert isinstance(session, sqlalchemy.orm.session.Session)
            data: _ass = session.query(_ass).get(query_id)
            if hasattr(self, "infor"):
                data.infor = self.infor
            if hasattr(self, "filestate"):
                data.filestate = self.filestate

    def getFileState(self, flag) -> sqlalchemy.orm.query.Query:
        """
        查询文件状态
        """
        with self.comsql.session() as session:
            # assert isinstance(session, sqlalchemy.orm.session.Session)
            data = session.query(_ass).filter(_ass.filestate.isnot(None))
            try:
                data = getattr(self, f"_getFileState{flag}")(data)
            except AttributeError as err:
                logging.error("查询文件状态时，类中没有这个属性 %s", err)
        return data

    def _getFileStateClass(self, data: sqlalchemy.orm.query.Query) -> sqlalchemy.orm.query.Query:
        data = data
        return data

    def _getFileStateType(self, data: sqlalchemy.orm.query.Query) -> sqlalchemy.orm.query.Query:
        data = data.filter(_ass.name == self.name)
        return data

    def _getFileStateFile(self, data: sqlalchemy.orm.query.Query) -> sqlalchemy.orm.query.Query:
        data = self._getFileStateType(data).filter(_ass.type == self.Type)
        return data
