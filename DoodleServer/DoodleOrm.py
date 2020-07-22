import json
import pathlib
import typing

import sqlalchemy.orm
import sqlalchemy.sql
import DoodleServer.DoodleDictToObject as dictToObj
import DoodleServer.DoodleSql as DoleSql


def convertData(cls: DoleSql.Base, obj: object):
    kwargs: dict = {}
    for attr in obj.dole_data:
        kwargs[attr] = getattr(obj, attr)
    return cls(**kwargs)


class fileAttributeInfo(DoleSql.Base):
    __tablename__ = "baseFile"
    dole_data = ["file", "fileSuffixes", "user", "version", "filepath", "infor", "filestate"]

    id: int = sqlalchemy.Column(sqlalchemy.SMALLINT, primary_key=True, nullable=False, autoincrement=True, unique=True)
    file: str = sqlalchemy.Column(sqlalchemy.VARCHAR(128))
    fileSuffixes: str = sqlalchemy.Column(sqlalchemy.VARCHAR(32))
    user: str = sqlalchemy.Column(sqlalchemy.VARCHAR(128))
    version: int = sqlalchemy.Column(sqlalchemy.SMALLINT)
    _file_path_: str = sqlalchemy.Column(sqlalchemy.VARCHAR(1024))
    infor: str = sqlalchemy.Column(sqlalchemy.VARCHAR(4096))
    filestate = sqlalchemy.Column(sqlalchemy.VARCHAR(64))
    filetime = sqlalchemy.Column(sqlalchemy.DATETIME,
                                 server_default=sqlalchemy.sql.func.now(),
                                 server_onupdate=sqlalchemy.sql.func.now())
    __tmp_path__: pathlib.Path

    def toDict(self):
        return {"id": self.id, "file": self.file, "fileSuffixes": self.fileSuffixes, "user": self.user,
                "version": self.version, "filepath": self.filepath, "infor": self.infor, "filestate": self.filestate}

    def toObj(self):
        return dictToObj.convertTool().convert(self.toDict())

    @property
    def file_path(self) -> pathlib.Path:
        if not hasattr(self, '__tmp_path__'):
            return pathlib.Path(self._file_path_)
        return self.__tmp_path__

    @file_path.setter
    def file_path(self, file_path: pathlib.Path):
        self._file_path_ = file_path.as_posix()
        self.fileSuffixes = file_path.suffix
        self.__tmp_path__ = file_path

    _file_path_list_: typing.List[pathlib.Path]

    @property
    def file_path_list(self) -> typing.List[pathlib.Path]:
        if not hasattr(self, '_file_path_list_'):
            try:
                pathlist = json.loads(self._file_path_)
            except json.decoder.JSONDecodeError:
                pathlist = [self._file_path_]
            self._file_path_list_ = [pathlib.Path(p) for p in pathlist]
        return self._file_path_list_

    @file_path_list.setter
    def file_path_list(self, file_path_list: typing.List[pathlib.Path]):
        self._file_path_list_ = file_path_list
        self._file_path_ = json.dumps([p.as_posix() for p in file_path_list], ensure_ascii=False, indent=1,
                                      separators=(',', ':'))

    # 集数外键约束
    __episodes__ = sqlalchemy.Column(sqlalchemy.SMALLINT, sqlalchemy.ForeignKey("episodes.id"))
    episodes = sqlalchemy.orm.relationship("Episodes", back_populates="addfileAttributeInfo")

    # 镜头外键
    __shot__ = sqlalchemy.Column(sqlalchemy.SMALLINT, sqlalchemy.ForeignKey("shot.id"))
    shot = sqlalchemy.orm.relationship("Shot", back_populates="addfileAttributeInfo")

    # 添加类型外键
    __file_class__ = sqlalchemy.Column(sqlalchemy.SMALLINT, sqlalchemy.ForeignKey("fileclass.id"))
    file_class = sqlalchemy.orm.relationship("fileClass", back_populates="addfileAttributeInfo")

    # 添加种类外键
    __file_type__ = sqlalchemy.Column(sqlalchemy.SMALLINT, sqlalchemy.ForeignKey("filetype.id"))
    file_type = sqlalchemy.orm.relationship("fileType", back_populates="addfileAttributeInfo")

    # 添加资产名称外键
    __ass_class__ = sqlalchemy.Column(sqlalchemy.SMALLINT, sqlalchemy.ForeignKey("assclass.id"))
    ass_class = sqlalchemy.orm.relationship("assClass", back_populates="addfileAttributeInfo")


class fileType(DoleSql.Base):
    """
    种类
    """
    __tablename__ = "filetype"
    dole_data = ["file_type"]

    id: int = sqlalchemy.Column(sqlalchemy.SMALLINT, primary_key=True, nullable=False, autoincrement=True, unique=True)
    file_type: str = sqlalchemy.Column(sqlalchemy.VARCHAR(64))

    # 添加类型反射和约束
    __file_class__: int = sqlalchemy.Column(sqlalchemy.SMALLINT, sqlalchemy.ForeignKey("fileclass.id"))
    file_class: typing.List = sqlalchemy.orm.relationship("fileClass", back_populates="addfileType")

    # 添加资产名称反射和约束
    __ass_class__: int = sqlalchemy.Column(sqlalchemy.SMALLINT, sqlalchemy.ForeignKey("assclass.id"))
    ass_class: typing.List = sqlalchemy.orm.relationship("assClass", back_populates="addfileType")

    # 添加集数和镜头约束
    __episodes__: int = sqlalchemy.Column(sqlalchemy.SMALLINT, sqlalchemy.ForeignKey("episodes.id"))
    episodes = sqlalchemy.orm.relationship("Episodes", back_populates="addFileType")
    __shot__ = sqlalchemy.Column(sqlalchemy.SMALLINT, sqlalchemy.ForeignKey("shot.id"))
    shot = sqlalchemy.orm.relationship("Shot", back_populates="addfileType")

    # 添加资产ue场景反射
    addfileAttributeInfo: typing.List[fileAttributeInfo] = sqlalchemy.orm.relationship("fileAttributeInfo",
                                                                                       back_populates="file_type",
                                                                                       order_by="fileAttributeInfo.filetime.desc()")


class assClass(DoleSql.Base):
    __tablename__ = "assclass"
    dole_data = ["file_name"]

    id: int = sqlalchemy.Column(sqlalchemy.SMALLINT, primary_key=True, nullable=False, autoincrement=True, unique=True)
    file_name: str = sqlalchemy.Column(sqlalchemy.VARCHAR(256))

    # 添加资产类型反射
    __file_class__: int = sqlalchemy.Column(sqlalchemy.SMALLINT, sqlalchemy.ForeignKey("fileclass.id"))
    file_class = sqlalchemy.orm.relationship("fileClass", back_populates="addass_class")

    # 添加fileType反射
    addfileType: typing.List[fileType] = sqlalchemy.orm.relationship("fileType", back_populates="ass_class")

    # 添加中文
    nameZNCH = sqlalchemy.orm.relationship("ZNch", uselist=False, back_populates="ass_class")

    # file
    addfileAttributeInfo = sqlalchemy.orm.relationship("fileAttributeInfo", back_populates="ass_class")


class fileClass(DoleSql.Base):
    """
    类型
    """
    __tablename__ = "fileclass"
    dole_data = ["file_class"]

    id: int = sqlalchemy.Column(sqlalchemy.SMALLINT, primary_key=True, nullable=False, autoincrement=True, unique=True)
    file_class: str = sqlalchemy.Column(sqlalchemy.VARCHAR(64))

    # 添加镜头约束
    __shot__ = sqlalchemy.Column(sqlalchemy.SMALLINT, sqlalchemy.ForeignKey("shot.id"))
    shot = sqlalchemy.orm.relationship("Shot", back_populates="addfileClass")

    # 添加ep约束
    __episodes__ = sqlalchemy.Column(sqlalchemy.SMALLINT, sqlalchemy.ForeignKey("episodes.id"))
    episodes = sqlalchemy.orm.relationship("Episodes", back_populates="addFileClass")

    # 添加资产名称反射
    addass_class: typing.List[assClass] = sqlalchemy.orm.relationship("assClass", back_populates="file_class",
                                                                      order_by="assClass.file_name")

    # 添加种类反射
    addfileType: typing.List[fileType] = sqlalchemy.orm.relationship("fileType", back_populates="file_class",
                                                                     order_by="fileType.file_type")

    # 添加资产ue场景反射
    addfileAttributeInfo = sqlalchemy.orm.relationship("fileAttributeInfo", back_populates="file_class")


class Shot(DoleSql.Base):
    __tablename__ = "shot"
    dole_data = ["shot_", "shotab"]
    id: int = sqlalchemy.Column(sqlalchemy.SMALLINT, primary_key=True, nullable=False, autoincrement=True, unique=True)

    __episodes__: int = sqlalchemy.Column(sqlalchemy.SMALLINT, sqlalchemy.ForeignKey("episodes.id"))
    episodes = sqlalchemy.orm.relationship("Episodes", back_populates="addShot")

    shot_: int = sqlalchemy.Column(sqlalchemy.SMALLINT)
    shotab: str = sqlalchemy.Column(sqlalchemy.VARCHAR(64))

    # 添加类型反射
    addfileClass: typing.List[fileClass] = sqlalchemy.orm.relationship("fileClass", back_populates="shot",
                                                                       order_by="fileClass.file_class")
    # 添加type反射
    addfileType: typing.List[fileType] = sqlalchemy.orm.relationship("fileType", back_populates="shot",
                                                                     order_by="fileType.file_type")
    # 添加资产ue场景反射
    addfileAttributeInfo = sqlalchemy.orm.relationship("fileAttributeInfo", back_populates="shot")


class Episodes(DoleSql.Base):
    __tablename__ = "episodes"
    dole_data = ["episodes"]
    id: int = sqlalchemy.Column(sqlalchemy.SMALLINT, primary_key=True, nullable=False, autoincrement=True, unique=True)
    episodes: int = sqlalchemy.Column(sqlalchemy.SMALLINT, unique=True)

    # 添加镜头反射
    addShot: typing.List[Shot] = sqlalchemy.orm.relationship("Shot", back_populates="episodes", order_by="Shot.shot_")

    # 添加fileClass约束
    addFileClass: typing.List[fileClass] = sqlalchemy.orm.relationship("fileClass", back_populates="episodes",
                                                                       order_by="fileClass.file_class")
    addFileType: typing.List[fileType] = sqlalchemy.orm.relationship("fileType", back_populates="episodes",
                                                                     order_by="fileType.file_type")
    # 添加资产ue场景反射
    addfileAttributeInfo = sqlalchemy.orm.relationship("fileAttributeInfo", back_populates="episodes")


# =======================================================================


class ZNch(DoleSql.Base):
    __tablename__ = "znch"
    dole_data = ["localname"]
    id: int = sqlalchemy.Column(sqlalchemy.SMALLINT, primary_key=True)
    localname: str = sqlalchemy.Column(sqlalchemy.VARCHAR(128), unique=True)

    # 添加中文名称
    __ass_class__: int = sqlalchemy.Column(sqlalchemy.SMALLINT, sqlalchemy.ForeignKey("assclass.id"), unique=True)
    ass_class = sqlalchemy.orm.relationship("assClass", back_populates="nameZNCH")


class configure(DoleSql.Base):
    __tablename__ = "configure"
    id: int = sqlalchemy.Column(sqlalchemy.SMALLINT, primary_key=True, nullable=False, autoincrement=True, unique=True)
    name: str = sqlalchemy.Column(sqlalchemy.VARCHAR(128))
    value: str = sqlalchemy.Column(sqlalchemy.VARCHAR(128))
    value2: str = sqlalchemy.Column(sqlalchemy.VARCHAR(128))
    value3: str = sqlalchemy.Column(sqlalchemy.VARCHAR(128))
    value4: str = sqlalchemy.Column(sqlalchemy.VARCHAR(128))


class user(DoleSql.Base):
    __tablename__ = "user"
    __table_args__ = {'schema': 'myuser'}

    id: int = sqlalchemy.Column(sqlalchemy.SMALLINT, primary_key=True, nullable=False, autoincrement=True, unique=True)
    user: str = sqlalchemy.Column(sqlalchemy.VARCHAR(128), nullable=False)
    password: str = sqlalchemy.Column(sqlalchemy.VARCHAR(1024), nullable=False)


if __name__ == '__main__':
    # pass
    # test = Episodes(episodes=1)
    print("ok")
    # DoleSql.commMysql("dubuxiaoyao", "", "").createTable()
    # shotFlipBook.filetime.desc()
