import json
import pathlib
import pickle
import re
import threading
import logging
import traceback
import sqlalchemy.orm

# from DoodleServer.DoodleOrm import *
import typing

import DoodleServer.DoodleOrm as DoleOrm
import DoodleServer.DoodleSql as Conect
import DoodleServer.DoodleZNCHConvert
import DoodleServer.DoodleDictToObject
import DoodleServer.DoodleSet as DoodleSet
import zmq
from multiprocessing import connection as Conn
from DoodleServer.DoodleOrm import Shot


class PrjCore(object):
    query_id: int
    query_file: DoleOrm.fileAttributeInfo_

    file_type: DoleOrm.fileType
    file_class: DoleOrm.fileClass

    def __init__(self, doodle_set: DoodleSet.Doodlesetting):
        """
        初始化一些属性
        :param doodle_set: 设置类的传递
        """
        self._prj_root_ = pathlib.Path(doodle_set.project)
        self.mysqllib = doodle_set.projectname
        self.comsql = Conect.commMysql(self.mysqllib)

    def queryMaxVersion(self, sql_class: typing.Type[DoleOrm.fileAttributeInfo_] = None) -> int:
        if not sql_class:
            _sql_class_ = self.decideTypeClass()
        else:
            _sql_class_ = sql_class
        with self.comsql.sessionOne() as session:
            assert isinstance(session, sqlalchemy.orm.session.Session)
            data = session.query(_sql_class_.version) \
                .filter(_sql_class_.__file_type__ == self.file_type.id) \
                .order_by(_sql_class_.filetime.desc()).first()
        if data:
            data = data[0]
        else:
            data = 0
        return data

    def queryFile(self, sql_class: typing.Type[DoleOrm.fileAttributeInfo_] = None) -> typing.List[
        DoleOrm.fileAttributeInfo_]:
        pass

    def commPath(self, folder_type: str = "Scenefiles") -> pathlib.Path:
        pass

    def commName(self, version: int, user_: str, suffix: str = "", prefix: str = "") -> str:
        pass

    def _getClassTypeInfo(self):
        pass

    def subClass(self, base_class: DoleOrm.fileAttributeInfo_):
        with self.comsql.sessionOne() as session:
            assert isinstance(session, sqlalchemy.orm.session.Session)
            session.add(base_class)

    def updataClass(self, base_class: DoleOrm.fileAttributeInfo_):
        with self.comsql.sessionOne() as session:
            assert isinstance(session, sqlalchemy.orm.session.Session)
            session.flush(base_class)

    def quertById(self, base_class: typing.Type[DoleOrm.fileAttributeInfo_],
                  query_id: int = None) -> DoleOrm.fileAttributeInfo_:
        if not query_id:
            if self.query_file:
                query_id = self.query_file.id
            else:
                query_id = self.query_id
        with self.comsql.sessionOne() as session:
            assert isinstance(session, sqlalchemy.orm.session.Session)
            data = session.query(base_class).filter(base_class.id == query_id).one()
        if data:
            data = data
        else:
            data = None
        return data

    def decideTypeClass(self):
        if isinstance(self, PrjShot):
            if re.fullmatch("[a,A]nm", self.file_class.file_class):
                if re.findall("^FB_", self.file_type.file_type):
                    cls = DoleOrm.shotFlipBook
                else:
                    cls = DoleOrm.shotMayaAnmScane
            elif re.fullmatch('VFX', self.file_class.file_class):
                if re.findall("^FB_", self.file_type.file_type):
                    cls = DoleOrm.shotFlipBook
                else:
                    cls = DoleOrm.shotUEVFXScane
            elif re.fullmatch("Light", self.file_class.file_class):
                if re.findall("^FB_", self.file_type.file_type):
                    cls = DoleOrm.shotFlipBook
            if re.findall("^export", self.file_type.file_type):
                cls = DoleOrm.shotMayaAnmExport
            if re.findall("screenshot", self.file_type.file_type):
                cls = DoleOrm.shotScreenshot
        elif isinstance(self, PrjAss):
            if re.findall("sourceimages", self.file_type.file_type):
                cls = DoleOrm.assMapping
            elif re.findall("scenes", self.file_type.file_type):
                cls = DoleOrm.assMayaScane
            elif re.findall("_UE4$", self.file_type.file_type):
                cls = DoleOrm.assUEScane
            elif re.findall("rig", self.file_type.file_type):
                cls = DoleOrm.assMayaRigModel
            elif re.findall("_low$", self.file_type.file_type):
                cls = DoleOrm.assMayaLowModleModel
            if re.findall("^screenshot", self.file_type.file_type):
                cls = DoleOrm.assScreenshot
        return cls

    @staticmethod
    def convertPathToIp(path: pathlib.Path) -> pathlib.Path:
        """
        转换到去除根目录
        :param path:需要转换的路径
        :type path:pathlib.Path
        :return: 转换好的路径
        :rtype:pathlib.Path
        """
        if not path:
            return pathlib.Path("")
        if path.drive:
            if path.drive.__len__() == 2:
                _path = path.as_posix()[2:]
            else:
                strlen = path.as_posix().split("/")[2].__len__() + 2
                _path = path.as_posix()[strlen:]
        else:
            _path = path.as_posix()
        return pathlib.Path(_path)


class PrjShot(PrjCore):

    @property
    def episodes(self) -> DoleOrm.Episodes:
        if not hasattr(self, '_episodes'):
            self._episodes = DoleOrm.Episodes()
        return self._episodes

    @episodes.setter
    def episodes(self, episodes):
        self._episodes = episodes
        self._shot = None
        self._file_class = None
        self._file_type = None
        self.query_file = None

    @property
    def shot(self):
        if not hasattr(self, '_shot'):
            self._shot = DoleOrm.Shot()
        return self._shot

    @shot.setter
    def shot(self, shot):
        self._shot = shot
        self._file_class = None
        self._file_type = None
        self.query_file = None

    @property
    def file_class(self):
        if not hasattr(self, '_file_class'):
            self._file_class = DoleOrm.fileClass()
        return self._file_class

    @file_class.setter
    def file_class(self, file_class):
        self._file_class = file_class
        self._file_type = None
        self.query_file = None

    @property
    def file_type(self):
        if not hasattr(self, '_file_type'):
            self._file_type = DoleOrm.fileType()
        return self._file_type

    @file_type.setter
    def file_type(self, file_type):
        self._file_type = file_type
        self.query_file = None

    def __init__(self, doodle_set: DoodleSet.Doodlesetting):
        super(PrjShot, self).__init__(doodle_set)
        self._root = pathlib.Path(doodle_set.shotRoot)

    def queryEps(self) -> typing.List[DoleOrm.Episodes]:
        """
        获得所有集数信息
        :return:
        """
        with self.comsql.sessionOne() as session:
            assert isinstance(session, sqlalchemy.orm.session.Session)
            data = session.query(DoleOrm.Episodes).order_by(DoleOrm.Episodes.episodes).all()
        return data

    def queryEpsLsit(self) -> typing.List[str]:
        return ['ep{:0>3d}'.format(ep.episodes) for ep in self.queryEps()]

    def queryShot(self) -> typing.List[Shot]:
        """
        获得一集中的镜头信息
        :return:
        """
        with self.comsql.sessionOne() as session:
            assert isinstance(session, sqlalchemy.orm.session.Session)
            data = session.query(DoleOrm.Shot) \
                .filter(DoleOrm.Shot.__episodes__ == self.episodes.id) \
                .order_by(DoleOrm.Shot.shot_).all()

        return data

    def queryShotList(self):
        return ['sc{:0>4d}{}'.format(shot.shot_, shot.shotab) for shot in self.queryShot()]

    def queryFileClass(self) -> typing.List[DoleOrm.fileClass]:
        """
        查询文件类型信息
        :return:
        """
        if self.shot:
            shot_id = self.shot.id
        else:
            shot_id = None
        with self.comsql.sessionOne() as session:
            assert isinstance(session, sqlalchemy.orm.session.Session)

            data = session.query(DoleOrm.fileClass) \
                .filter(DoleOrm.fileClass.__shot__ == shot_id) \
                .order_by(DoleOrm.fileClass.file_class).all()
        return data

    def queryFileClassList(self):
        return [dep.file_class for dep in self.queryFileClass()]

    def queryFileType(self) -> typing.List[DoleOrm.fileType]:
        """
        查询文件种类信息
        :return:
        """
        if self.file_class:
            class_id = self.file_class.id
        else:
            class_id = None
        with self.comsql.sessionOne() as session:
            assert isinstance(session, sqlalchemy.orm.session.Session)

            data = session.query(DoleOrm.fileType) \
                .filter(DoleOrm.fileType.__file_class__ == class_id) \
                .order_by(DoleOrm.fileType.file_type).all()
        return data

    def queryFileTypeList(self):
        return [dep_type.file_type for dep_type in self.queryFileType()]

    def queryFile(self, sql_class: typing.Type[DoleOrm.fileAttributeInfo_] = None) -> typing.List[DoleOrm.DoleSql.Base]:
        """
        查询文件本身信息
        :param sql_class:
        :type sql_class:
        :param base_class:文件类名
        :return:
        """
        if not sql_class:
            _sql_class_ = self.decideTypeClass()
        else:
            _sql_class_ = sql_class
        with self.comsql.sessionOne() as session:
            assert isinstance(session, sqlalchemy.orm.session.Session)
            data = session.query(_sql_class_) \
                .filter(_sql_class_.__file_type__ == self.file_type.id) \
                .order_by(_sql_class_.filetime.desc()).all()
        return data

    def commPath(self, folder_type: str = "Scenefiles") -> pathlib.Path:
        """
        组合镜头信息, 返回文件路径
        """
        episodes, file_class, file_type = self._getClassTypeInfo()
        if self.shot:
            if self.shot.shot_:
                shot = f'sc{self.shot.shot_:0>4d}{self.shot.shotab}'
        else:
            shot = ""
        path = self._root.joinpath(f'ep{episodes:0>3d}',
                                   shot,
                                   folder_type,
                                   file_class,
                                   file_type
                                   )
        return path

    def commName(self, version: int = 0, user_: str = None, suffix: str = "", prefix: str = "") -> str:
        """
        组合文件信息,  生成文件名称
        """
        episodes, file_class, file_type = self._getClassTypeInfo()
        if self.shot:
            if self.shot.shot_:
                shot = "sc{:0>4d}{}".format(self.shot.shot_, self.shot.shotab)
        else:
            shot = ""
        name = f"{prefix}shot_ep{episodes:0>3d}_{shot}_" \
               f"{file_class}_" \
               f"{file_type}_v{version:0>4d}" \
               f"__{user_}_{suffix}"
        return name

    def _getClassTypeInfo(self):
        if self.episodes.episodes:
            episodes = self.episodes.episodes
        else:
            episodes = ""

        if self.file_class.file_class:
            file_class = self.file_class.file_class
        else:
            file_class = ""
        if self.file_type.file_type:
            file_type = self.file_type.file_type
        else:
            file_type = ""
        return episodes, file_class, file_type


class PrjAss(PrjCore):

    @property
    def file_class(self):
        if not hasattr(self, '_file_class'):
            self._file_class = DoleOrm.fileClass()
        return self._file_class

    @file_class.setter
    def file_class(self, file_class):
        self._file_class = file_class
        self._ass_class = None
        self._file_type = None
        self.query_file = None

    @property
    def ass_class(self):
        if not hasattr(self, '_ass_class'):
            self._ass_class = DoleOrm.assClass()
        return self._ass_class

    @ass_class.setter
    def ass_class(self, ass_class):
        self._ass_class = ass_class
        self._file_type = None
        self.query_file = None

    @property
    def file_type(self):
        if not hasattr(self, '_file_type'):
            self._file_type = DoleOrm.fileType()
        return self._file_type

    @file_type.setter
    def file_type(self, file_type):
        self._file_type = file_type
        self.query_file = None

    def __init__(self, doodle_set: DoodleSet.Doodlesetting):
        super(PrjAss, self).__init__(doodle_set)
        self._root = pathlib.Path(doodle_set.assetsRoot)

    def queryAssClass(self) -> typing.List[DoleOrm.fileClass]:
        with self.comsql.sessionOne() as session:
            assert isinstance(session, sqlalchemy.orm.session.Session)
            data = session.query(DoleOrm.fileClass) \
                .order_by(DoleOrm.fileClass.file_class) \
                .filter(DoleOrm.fileClass.__shot__.is_(None))\
                .filter(DoleOrm.fileClass.__episodes__.is_(None)).all()
        return data

    def queryAssname(self) -> typing.List[DoleOrm.assClass]:
        with self.comsql.sessionOne() as session:
            assert isinstance(session, sqlalchemy.orm.session.Session)
            data = session.query(DoleOrm.assClass) \
                .order_by(DoleOrm.assClass.file_name) \
                .filter(DoleOrm.assClass.__file_class__ == self.file_class.id) \
                .all()
        return data

    def queryAssType(self) -> typing.List[DoleOrm.fileType]:
        with self.comsql.sessionOne() as session:
            assert isinstance(session, sqlalchemy.orm.session.Session)
            data = session.query(DoleOrm.fileType) \
                .filter(DoleOrm.fileType.__ass_class__ == self.ass_class.id) \
                .all()
        return data

    def queryFile(self, sql_class: typing.Type[DoleOrm.fileAttributeInfo_] = None) -> typing.List[DoleOrm.DoleSql.Base]:
        if not sql_class:
            _sql_class_ = self.decideTypeClass()
        else:
            _sql_class_ = sql_class
        with self.comsql.sessionOne() as session:
            assert isinstance(session, sqlalchemy.orm.session.Session)
            data = session.query(_sql_class_) \
                .filter(_sql_class_.__file_type__ == self.file_type.id) \
                .order_by(_sql_class_.filetime.desc()).all()
        return data

    def commPath(self, folder_type: str = "Scenefiles") -> pathlib.Path:
        """
        组合文件信息, 返回路径变量
        """
        file_class, file_name, file_type = self._getClassTypeInfo()
        path = self._root.joinpath(file_class,
                                   file_name,
                                   folder_type,
                                   file_type
                                   )
        return path

    def commName(self, version: int, user_: str, suffix: str = "", prefix: str = "") -> str:
        """
        组合文件名称
        """
        file_class, file_name, file_type = self._getClassTypeInfo()
        add_suffix = ""
        if file_type in ["rig"]:
            add_suffix = "_rig"
        name = "{prefix}{cl}{su}{suffix}".format(cl=file_name, su=add_suffix,
                                                 suffix=suffix, prefix=prefix)
        return name

    def _getClassTypeInfo(self):
        if self.file_class.file_class:
            file_class = self.file_class.file_class
        else:
            file_class = ""
        if self.ass_class.file_name:
            file_name = self.ass_class.file_name
        else:
            file_name = ""
        if self.file_type.file_type:
            file_type = self.file_type.file_type
        else:
            file_type = ""
        return file_class, file_name, file_type



if __name__ == '__main__':
    import DoodleServer.DoodleSet as DoleSet

    t = DoodleServer(DoleSet.Doodlesetting())
    t.start()
