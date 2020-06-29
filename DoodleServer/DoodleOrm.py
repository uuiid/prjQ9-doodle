import typing
import sqlalchemy.orm
import sqlalchemy.sql
# import sqlalchemy
import DoodleServer.DoodleSql as DoleSql
import DoodleServer.DoodleDictToObject as DoleCict


def convertData(cls: DoleSql.Base, obj: object):
    kwargs: dict = {}
    for attr in obj.dole_data:
        kwargs[attr] = getattr(obj, attr)
    return cls(**kwargs)


class _fileAttributeInfo(DoleSql.Base):
    __abstract__ = True
    dole_data = ["file", "fileSuffixes", "user", "version", "filepath", "infor", "filestate"]

    id: int = sqlalchemy.Column(sqlalchemy.SMALLINT, primary_key=True, nullable=False, autoincrement=True, unique=True)
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

    def toDict(self):
        return {"id":self.id,"file":self.file,"fileSuffixes":self.fileSuffixes,"user":self.user,
                "version":self.version,"filepath":self.filepath,"infor":self.infor,"filestate":self.filestate}

    def toObj(self):
        return DoleCict.convertTool().convert(self.toDict())


class assUEScane(_fileAttributeInfo):
    """
    资产ue场景
    """
    __tablename__ = "assUEScane"

    # 添加类型外键
    __file_class__ = sqlalchemy.Column(sqlalchemy.SMALLINT, sqlalchemy.ForeignKey("fileclass.id"))
    file_class = sqlalchemy.orm.relationship("fileClass", back_populates="addassUEScane")

    # 添加种类外键
    __file_type__ = sqlalchemy.Column(sqlalchemy.SMALLINT, sqlalchemy.ForeignKey("filetype.id"))
    file_type = sqlalchemy.orm.relationship("fileType", back_populates="addassUEScane")

    # 添加资产名称外键
    __ass_class__ = sqlalchemy.Column(sqlalchemy.SMALLINT, sqlalchemy.ForeignKey("assclass.id"))
    ass_class = sqlalchemy.orm.relationship("assClass", back_populates="addassUEScane")


class assMayaScane(_fileAttributeInfo):
    __tablename__ = "assMayaScane"
    # 添加类型外键
    __file_class__ = sqlalchemy.Column(sqlalchemy.SMALLINT, sqlalchemy.ForeignKey("fileclass.id"))
    file_class = sqlalchemy.orm.relationship("fileClass", back_populates="addassMayaScane")

    # 添加种类外键
    __file_type__ = sqlalchemy.Column(sqlalchemy.SMALLINT, sqlalchemy.ForeignKey("filetype.id"))
    file_type = sqlalchemy.orm.relationship("fileType", back_populates="addassMayaScane")

    # 添加资产名称外键
    __ass_class__ = sqlalchemy.Column(sqlalchemy.SMALLINT, sqlalchemy.ForeignKey("assclass.id"))
    ass_class = sqlalchemy.orm.relationship("assClass", back_populates="addassMayaScane")


class assUECharacter(_fileAttributeInfo):
    __tablename__ = "assUECharacter"
    # 添加类型外键
    __file_class__ = sqlalchemy.Column(sqlalchemy.SMALLINT, sqlalchemy.ForeignKey("fileclass.id"))
    file_class = sqlalchemy.orm.relationship("fileClass", back_populates="addassUECharacter")

    # 添加种类外键
    __file_type__ = sqlalchemy.Column(sqlalchemy.SMALLINT, sqlalchemy.ForeignKey("filetype.id"))
    file_type = sqlalchemy.orm.relationship("fileType", back_populates="addassUECharacter")

    # 添加资产名称外键
    __ass_class__ = sqlalchemy.Column(sqlalchemy.SMALLINT, sqlalchemy.ForeignKey("assclass.id"))
    ass_class = sqlalchemy.orm.relationship("assClass", back_populates="addassUECharacter")


class assMayaLowModleModel(_fileAttributeInfo):
    __tablename__ = "assMayaLowModleModel"
    # 添加类型外键
    __file_class__ = sqlalchemy.Column(sqlalchemy.SMALLINT, sqlalchemy.ForeignKey("fileclass.id"))
    file_class = sqlalchemy.orm.relationship("fileClass", back_populates="addassMayaLowModleModel")

    # 添加种类外键
    __file_type__ = sqlalchemy.Column(sqlalchemy.SMALLINT, sqlalchemy.ForeignKey("filetype.id"))
    file_type = sqlalchemy.orm.relationship("fileType", back_populates="addassMayaLowModleModel")

    # 添加资产名称外键
    __ass_class__ = sqlalchemy.Column(sqlalchemy.SMALLINT, sqlalchemy.ForeignKey("assclass.id"))
    ass_class = sqlalchemy.orm.relationship("assClass", back_populates="addassMayaLowModleModel")


class assMayaRigModel(_fileAttributeInfo):
    __tablename__ = "assMayaRigModel"
    # 添加类型外键
    __file_class__ = sqlalchemy.Column(sqlalchemy.SMALLINT, sqlalchemy.ForeignKey("fileclass.id"))
    file_class = sqlalchemy.orm.relationship("fileClass", back_populates="addassMayaRigModel")

    # 添加种类外键
    __file_type__ = sqlalchemy.Column(sqlalchemy.SMALLINT, sqlalchemy.ForeignKey("filetype.id"))
    file_type = sqlalchemy.orm.relationship("fileType", back_populates="addassMayaRigModel")

    # 添加资产名称外键
    __ass_class__ = sqlalchemy.Column(sqlalchemy.SMALLINT, sqlalchemy.ForeignKey("assclass.id"))
    ass_class = sqlalchemy.orm.relationship("assClass", back_populates="addassMayaRigModel")


class assMapping(_fileAttributeInfo):
    __tablename__ = "assMapping"
    # 添加类型外键
    __file_class__ = sqlalchemy.Column(sqlalchemy.SMALLINT, sqlalchemy.ForeignKey("fileclass.id"))
    file_class = sqlalchemy.orm.relationship("fileClass", back_populates="addassMapping")

    # 添加种类外键
    __file_type__ = sqlalchemy.Column(sqlalchemy.SMALLINT, sqlalchemy.ForeignKey("filetype.id"))
    file_type = sqlalchemy.orm.relationship("fileType", back_populates="addassMapping")

    # 添加资产名称外键
    __ass_class__ = sqlalchemy.Column(sqlalchemy.SMALLINT, sqlalchemy.ForeignKey("assclass.id"))
    ass_class = sqlalchemy.orm.relationship("assClass", back_populates="addassMapping")


class assFlipBook(_fileAttributeInfo):
    __tablename__ = "assFlipBook"
    # 添加类型外键
    __file_class__ = sqlalchemy.Column(sqlalchemy.SMALLINT, sqlalchemy.ForeignKey("fileclass.id"))
    file_class = sqlalchemy.orm.relationship("fileClass", back_populates="addassFlipBook")

    # 添加种类外键
    __file_type__ = sqlalchemy.Column(sqlalchemy.SMALLINT, sqlalchemy.ForeignKey("filetype.id"))
    file_type = sqlalchemy.orm.relationship("fileType", back_populates="addassFlipBook")

    # 添加资产名称外键
    __ass_class__ = sqlalchemy.Column(sqlalchemy.SMALLINT, sqlalchemy.ForeignKey("assclass.id"))
    ass_class = sqlalchemy.orm.relationship("assClass", back_populates="addassFlipBook")


class assScreenshot(_fileAttributeInfo):
    __tablename__ = "assScreenshot"
    # 添加类型外键
    __file_class__ = sqlalchemy.Column(sqlalchemy.SMALLINT, sqlalchemy.ForeignKey("fileclass.id"))
    file_class = sqlalchemy.orm.relationship("fileClass", back_populates="addassScreenshot")

    # 添加种类外键
    __file_type__ = sqlalchemy.Column(sqlalchemy.SMALLINT, sqlalchemy.ForeignKey("filetype.id"))
    file_type = sqlalchemy.orm.relationship("fileType", back_populates="addassScreenshot")

    # 添加资产名称外键
    __ass_class__ = sqlalchemy.Column(sqlalchemy.SMALLINT, sqlalchemy.ForeignKey("assclass.id"))
    ass_class = sqlalchemy.orm.relationship("assClass", back_populates="addassScreenshot")


class shotUELightScane(_fileAttributeInfo):
    """
    镜头ue灯光场景
    """
    __tablename__ = "shotUELightScane"

    # 集数外键约束
    __episodes__ = sqlalchemy.Column(sqlalchemy.SMALLINT, sqlalchemy.ForeignKey("episodes.id"))
    episodes = sqlalchemy.orm.relationship("Episodes", back_populates="addshotUELightScane")

    # 镜头外键
    __shot__ = sqlalchemy.Column(sqlalchemy.SMALLINT, sqlalchemy.ForeignKey("shot.id"))
    shot = sqlalchemy.orm.relationship("Shot", back_populates="addshotUELightScane")

    # 添加类型外键
    __file_class__ = sqlalchemy.Column(sqlalchemy.SMALLINT, sqlalchemy.ForeignKey("fileclass.id"))
    file_class = sqlalchemy.orm.relationship("fileClass", back_populates="addshotUELightScane")

    # 添加种类外键
    __file_type__ = sqlalchemy.Column(sqlalchemy.SMALLINT, sqlalchemy.ForeignKey("filetype.id"))
    file_type = sqlalchemy.orm.relationship("fileType", back_populates="addshotUELightScane")


class shotUEVFXScane(_fileAttributeInfo):
    """
    镜头ue特效场景
    """
    __tablename__ = "shotUEVFXScane"

    # 集数外键约束
    __episodes__ = sqlalchemy.Column(sqlalchemy.SMALLINT, sqlalchemy.ForeignKey("episodes.id"))
    episodes = sqlalchemy.orm.relationship("Episodes", back_populates="addshotUEVFXScane")

    # 镜头外键
    __shot__ = sqlalchemy.Column(sqlalchemy.SMALLINT, sqlalchemy.ForeignKey("shot.id"))
    shot = sqlalchemy.orm.relationship("Shot", back_populates="addshotUEVFXScane")

    # 添加类型外键
    __file_class__ = sqlalchemy.Column(sqlalchemy.SMALLINT, sqlalchemy.ForeignKey("fileclass.id"))
    file_class = sqlalchemy.orm.relationship("fileClass", back_populates="addshotUEVFXScane")

    # 添加种类外键
    __file_type__ = sqlalchemy.Column(sqlalchemy.SMALLINT, sqlalchemy.ForeignKey("filetype.id"))
    file_type = sqlalchemy.orm.relationship("fileType", back_populates="addshotUEVFXScane")


class shotMayaAnmScane(_fileAttributeInfo):
    """
    镜头maya动画场景
    """
    __tablename__ = "shotmayaanmscane"
    # 集数外键约束
    __episodes__ = sqlalchemy.Column(sqlalchemy.SMALLINT, sqlalchemy.ForeignKey("episodes.id"))
    episodes = sqlalchemy.orm.relationship("Episodes", back_populates="addshotMayaAnmScane")

    # 镜头外键
    __shot__ = sqlalchemy.Column(sqlalchemy.SMALLINT, sqlalchemy.ForeignKey("shot.id"))
    shot = sqlalchemy.orm.relationship("Shot", back_populates="addshotMayaAnmScane")

    # 添加类型外键
    __file_class__ = sqlalchemy.Column(sqlalchemy.SMALLINT, sqlalchemy.ForeignKey("fileclass.id"))
    file_class = sqlalchemy.orm.relationship("fileClass", back_populates="addshotMayaAnmScane")

    # 添加种类外键
    __file_type__ = sqlalchemy.Column(sqlalchemy.SMALLINT, sqlalchemy.ForeignKey("filetype.id"))
    file_type = sqlalchemy.orm.relationship("fileType", back_populates="addshotMayaAnmScane")


class shotMayaAnmExport(_fileAttributeInfo):
    """
    镜头maya动画场景
    """
    __tablename__ = "shotmayaanmexport"
    # 集数外键约束
    __episodes__ = sqlalchemy.Column(sqlalchemy.SMALLINT, sqlalchemy.ForeignKey("episodes.id"))
    episodes: typing.List = sqlalchemy.orm.relationship("Episodes", back_populates="addshotMayaAnmExport")

    # 镜头外键
    __shot__ = sqlalchemy.Column(sqlalchemy.SMALLINT, sqlalchemy.ForeignKey("shot.id"))
    shot: typing.List = sqlalchemy.orm.relationship("Shot", back_populates="addshotMayaAnmExport")

    # 添加类型外键
    __file_class__ = sqlalchemy.Column(sqlalchemy.SMALLINT, sqlalchemy.ForeignKey("fileclass.id"))
    file_class: typing.List = sqlalchemy.orm.relationship("fileClass", back_populates="addshotMayaAnmExport")

    # 添加种类外键
    __file_type__ = sqlalchemy.Column(sqlalchemy.SMALLINT, sqlalchemy.ForeignKey("filetype.id"))
    file_type: typing.List = sqlalchemy.orm.relationship("fileType", back_populates="addshotMayaAnmExport")


class shotSequeueceImage(_fileAttributeInfo):
    __tablename__ = "shotSequeueceImage"
    # 集数外键约束
    __episodes__ = sqlalchemy.Column(sqlalchemy.SMALLINT, sqlalchemy.ForeignKey("episodes.id"))
    episodes = sqlalchemy.orm.relationship("Episodes", back_populates="addshotSequeueceImage")

    # 镜头外键
    __shot__ = sqlalchemy.Column(sqlalchemy.SMALLINT, sqlalchemy.ForeignKey("shot.id"))
    shot = sqlalchemy.orm.relationship("Shot", back_populates="addshotSequeueceImage")

    # 添加类型外键
    __file_class__ = sqlalchemy.Column(sqlalchemy.SMALLINT, sqlalchemy.ForeignKey("fileclass.id"))
    file_class = sqlalchemy.orm.relationship("fileClass", back_populates="addshotSequeueceImage")

    # 添加种类外键
    __file_type__ = sqlalchemy.Column(sqlalchemy.SMALLINT, sqlalchemy.ForeignKey("filetype.id"))
    file_type = sqlalchemy.orm.relationship("fileType", back_populates="addshotSequeueceImage")


class shotFlipBook(_fileAttributeInfo):
    __tablename__ = "shotFlipBook"
    # 集数外键约束
    __episodes__ = sqlalchemy.Column(sqlalchemy.SMALLINT, sqlalchemy.ForeignKey("episodes.id"))
    episodes = sqlalchemy.orm.relationship("Episodes", back_populates="addshotFlipBook")

    # 镜头外键
    __shot__ = sqlalchemy.Column(sqlalchemy.SMALLINT, sqlalchemy.ForeignKey("shot.id"))
    shot = sqlalchemy.orm.relationship("Shot", back_populates="addshotFlipBook")

    # 添加类型外键
    __file_class__ = sqlalchemy.Column(sqlalchemy.SMALLINT, sqlalchemy.ForeignKey("fileclass.id"))
    file_class = sqlalchemy.orm.relationship("fileClass", back_populates="addshotFlipBook")

    # 添加种类外键
    __file_type__ = sqlalchemy.Column(sqlalchemy.SMALLINT, sqlalchemy.ForeignKey("filetype.id"))
    file_type = sqlalchemy.orm.relationship("fileType", back_populates="addshotFlipBook")


class shotScreenshot(_fileAttributeInfo):
    __tablename__ = "shotScreenshot"
    __episodes__ = sqlalchemy.Column(sqlalchemy.SMALLINT, sqlalchemy.ForeignKey("episodes.id"))
    episodes = sqlalchemy.orm.relationship("Episodes", back_populates="addshotScreenshot")

    # 镜头外键
    __shot__ = sqlalchemy.Column(sqlalchemy.SMALLINT, sqlalchemy.ForeignKey("shot.id"))
    shot = sqlalchemy.orm.relationship("Shot", back_populates="addshotScreenshot")

    # 添加类型外键
    __file_class__ = sqlalchemy.Column(sqlalchemy.SMALLINT, sqlalchemy.ForeignKey("fileclass.id"))
    file_class = sqlalchemy.orm.relationship("fileClass", back_populates="addshotScreenshot")

    # 添加种类外键
    __file_type__ = sqlalchemy.Column(sqlalchemy.SMALLINT, sqlalchemy.ForeignKey("filetype.id"))
    file_type = sqlalchemy.orm.relationship("fileType", back_populates="addshotScreenshot")


class fileType(DoleSql.Base):
    """
    种类
    """
    __tablename__ = "filetype"
    dole_data = ["file_type"]

    id: int = sqlalchemy.Column(sqlalchemy.SMALLINT, primary_key=True, nullable=False, autoincrement=True, unique=True)
    file_type: str = sqlalchemy.Column(sqlalchemy.VARCHAR(64))

    # 添加类型反射
    __file_class__: int = sqlalchemy.Column(sqlalchemy.SMALLINT, sqlalchemy.ForeignKey("fileclass.id"))

    file_class: typing.List = sqlalchemy.orm.relationship("fileClass", back_populates="addfileType")

    # 添加资产ue场景反射
    addassUEScane = sqlalchemy.orm.relationship("assUEScane", back_populates="file_type",
                                                order_by="assUEScane.filetime.desc()")
    addassMayaScane = sqlalchemy.orm.relationship("assMayaScane", back_populates="file_type",
                                                  order_by="assMayaScane.filetime.desc()")
    addassUECharacter = sqlalchemy.orm.relationship("assUECharacter", back_populates="file_type",
                                                    order_by="assUECharacter.filetime.desc()")
    addassMayaLowModleModel = sqlalchemy.orm.relationship("assMayaLowModleModel", back_populates="file_type",
                                                          order_by="assMayaLowModleModel.filetime.desc()")
    addassMayaRigModel = sqlalchemy.orm.relationship("assMayaRigModel", back_populates="file_type",
                                                     order_by="assMayaRigModel.filetime.desc()")
    addassMapping = sqlalchemy.orm.relationship("assMapping", back_populates="file_type",
                                                order_by="assMapping.filetime.desc()")
    addassFlipBook = sqlalchemy.orm.relationship("assFlipBook", back_populates="file_type",
                                                 order_by="assFlipBook.filetime.desc()")
    addassScreenshot = sqlalchemy.orm.relationship("assScreenshot", back_populates="file_type",
                                                   order_by="assScreenshot.filetime.desc()")
    # 添加灯光镜头反射
    addshotUELightScane = sqlalchemy.orm.relationship("shotUELightScane", back_populates="file_type",
                                                      order_by="shotUELightScane.filetime.desc()")
    # 添加特效镜头反射
    addshotUEVFXScane = sqlalchemy.orm.relationship("shotUEVFXScane", back_populates="file_type",
                                                    order_by="shotUEVFXScane.filetime.desc()")
    # 添加特效镜头反射
    addshotMayaAnmScane = sqlalchemy.orm.relationship("shotMayaAnmScane", back_populates="file_type",
                                                      order_by="shotMayaAnmScane.filetime.desc()")
    addshotSequeueceImage = sqlalchemy.orm.relationship("shotSequeueceImage", back_populates="file_type",
                                                        order_by="shotSequeueceImage.filetime.desc()")
    addshotFlipBook = sqlalchemy.orm.relationship("shotFlipBook", back_populates="file_type",
                                                  order_by="shotFlipBook.filetime.desc()")
    addshotScreenshot = sqlalchemy.orm.relationship("shotScreenshot", back_populates="file_type",
                                                    order_by="shotScreenshot.filetime.desc()")
    addshotMayaAnmExport = sqlalchemy.orm.relationship("shotMayaAnmExport", back_populates="file_type",
                                                       order_by="shotMayaAnmExport.filetime.desc()")


class assClass(DoleSql.Base):
    __tablename__ = "assclass"
    dole_data = ["file_name"]

    id: int = sqlalchemy.Column(sqlalchemy.SMALLINT, primary_key=True, nullable=False, autoincrement=True, unique=True)
    file_name: str = sqlalchemy.Column(sqlalchemy.VARCHAR(256))

    # 添加资产类型反射
    __file_class__: int = sqlalchemy.Column(sqlalchemy.SMALLINT, sqlalchemy.ForeignKey("fileclass.id"))
    file_class = sqlalchemy.orm.relationship("fileClass", back_populates="addass_class")

    # 添加中文
    nameZNCH = sqlalchemy.orm.relationship("ZNch", uselist=False, back_populates="ass_class")

    # 添加ue场景
    addassUEScane = sqlalchemy.orm.relationship("assUEScane", back_populates="ass_class")
    # 添加maya场景映射
    addassMayaScane = sqlalchemy.orm.relationship("assMayaScane", back_populates="ass_class")
    addassUECharacter = sqlalchemy.orm.relationship("assUECharacter", back_populates="ass_class")
    addassMayaLowModleModel = sqlalchemy.orm.relationship("assMayaLowModleModel", back_populates="ass_class")
    addassMayaRigModel = sqlalchemy.orm.relationship("assMayaRigModel", back_populates="ass_class")
    addassMapping = sqlalchemy.orm.relationship("assMapping", back_populates="ass_class")
    addassFlipBook = sqlalchemy.orm.relationship("assFlipBook", back_populates="ass_class")
    addassScreenshot = sqlalchemy.orm.relationship("assScreenshot", back_populates="ass_class")


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
    shot = sqlalchemy.orm.relationship("Shot", back_populates="addfile_class")

    # 添加资产名称反射
    addass_class: typing.List = sqlalchemy.orm.relationship("assClass", back_populates="file_class",
                                                            order_by="assClass.file_name")

    # 添加种类反射
    addfileType = sqlalchemy.orm.relationship("fileType", back_populates="file_class", order_by="fileType.file_type")

    # 添加资产ue场景反射
    addassUEScane = sqlalchemy.orm.relationship("assUEScane", back_populates="file_class")
    addassMayaScane = sqlalchemy.orm.relationship("assMayaScane", back_populates="file_class")
    addassUECharacter = sqlalchemy.orm.relationship("assUECharacter", back_populates="file_class")
    addassMayaLowModleModel = sqlalchemy.orm.relationship("assMayaLowModleModel", back_populates="file_class")
    addassMayaRigModel = sqlalchemy.orm.relationship("assMayaRigModel", back_populates="file_class")
    addassMapping = sqlalchemy.orm.relationship("assMapping", back_populates="file_class")
    addassFlipBook = sqlalchemy.orm.relationship("assFlipBook", back_populates="file_class")
    addassScreenshot = sqlalchemy.orm.relationship("assScreenshot", back_populates="file_class")
    # 添加灯光镜头反射
    addshotUELightScane = sqlalchemy.orm.relationship("shotUELightScane", back_populates="file_class")
    # 添加特效镜头反射
    addshotUEVFXScane = sqlalchemy.orm.relationship("shotUEVFXScane", back_populates="file_class")
    # 添加特效镜头反射
    addshotMayaAnmScane = sqlalchemy.orm.relationship("shotMayaAnmScane", back_populates="file_class")
    addshotSequeueceImage = sqlalchemy.orm.relationship("shotSequeueceImage", back_populates="file_class")
    addshotFlipBook = sqlalchemy.orm.relationship("shotFlipBook", back_populates="file_class")
    addshotScreenshot = sqlalchemy.orm.relationship("shotScreenshot", back_populates="file_class")

    addshotMayaAnmExport = sqlalchemy.orm.relationship("shotMayaAnmExport", back_populates="file_class",
                                                       order_by="shotMayaAnmExport.filetime.desc()")


class Shot(DoleSql.Base):
    __tablename__ = "shot"
    dole_data = ["shot_", "shotab"]
    id: int = sqlalchemy.Column(sqlalchemy.SMALLINT, primary_key=True, nullable=False, autoincrement=True, unique=True)

    __episodes__: int = sqlalchemy.Column(sqlalchemy.SMALLINT, sqlalchemy.ForeignKey("episodes.id"))
    episodes = sqlalchemy.orm.relationship("Episodes", back_populates="addShot",
                                           order_by="Episodes.episodes")

    shot_: int = sqlalchemy.Column(sqlalchemy.SMALLINT)
    shotab: str = sqlalchemy.Column(sqlalchemy.VARCHAR(64))

    # 添加类型反射
    addfile_class = sqlalchemy.orm.relationship("fileClass", back_populates="shot",
                                                order_by="fileClass.file_class")

    # 添加灯光镜头反射
    addshotUELightScane = sqlalchemy.orm.relationship("shotUELightScane", back_populates="shot",
                                                      order_by="shotUELightScane.filetime.desc()")
    # 添加特效镜头反射
    addshotUEVFXScane = sqlalchemy.orm.relationship("shotUEVFXScane", back_populates="shot",
                                                    order_by="shotUEVFXScane.filetime.desc()")
    # 添加特效镜头反射
    addshotMayaAnmScane = sqlalchemy.orm.relationship("shotMayaAnmScane", back_populates="shot",
                                                      order_by="shotMayaAnmScane.filetime.desc()")
    addshotSequeueceImage = sqlalchemy.orm.relationship("shotSequeueceImage", back_populates="shot",
                                                        order_by="shotSequeueceImage.filetime.desc()")
    addshotFlipBook = sqlalchemy.orm.relationship("shotFlipBook", back_populates="shot",
                                                  order_by="shotFlipBook.filetime.desc()")
    addshotScreenshot = sqlalchemy.orm.relationship("shotScreenshot", back_populates="shot",
                                                    order_by="shotScreenshot.filetime.desc()")

    addshotMayaAnmExport = sqlalchemy.orm.relationship("shotMayaAnmExport", back_populates="shot",
                                                       order_by="shotMayaAnmExport.filetime.desc()")


class Episodes(DoleSql.Base):
    __tablename__ = "episodes"
    dole_data = ["episodes"]
    id: int = sqlalchemy.Column(sqlalchemy.SMALLINT, primary_key=True, nullable=False, autoincrement=True, unique=True)
    episodes: int = sqlalchemy.Column(sqlalchemy.SMALLINT, unique=True)

    # 添加镜头反射
    addShot: list = sqlalchemy.orm.relationship("Shot", back_populates="episodes", order_by="Shot.shot_")

    # 添加灯光镜头反射
    addshotUELightScane = sqlalchemy.orm.relationship("shotUELightScane", back_populates="episodes",
                                                      order_by="shotUELightScane.filetime.desc()")
    # 添加特效镜头反射
    addshotUEVFXScane = sqlalchemy.orm.relationship("shotUEVFXScane", back_populates="episodes",
                                                    order_by="shotUEVFXScane.filetime.desc()")
    # 添加特效镜头反射
    addshotMayaAnmScane = sqlalchemy.orm.relationship("shotMayaAnmScane", back_populates="episodes",
                                                      order_by="shotMayaAnmScane.filetime.desc()")
    addshotSequeueceImage = sqlalchemy.orm.relationship("shotSequeueceImage", back_populates="episodes",
                                                        order_by="shotMayaAnmScane.filetime.desc()")
    addshotFlipBook = sqlalchemy.orm.relationship("shotFlipBook", back_populates="episodes",
                                                  order_by="shotFlipBook.filetime.desc()")
    addshotScreenshot = sqlalchemy.orm.relationship("shotScreenshot", back_populates="episodes",
                                                    order_by="shotScreenshot.filetime.desc()")
    addshotMayaAnmExport = sqlalchemy.orm.relationship("shotMayaAnmExport", back_populates="episodes",
                                                       order_by="shotMayaAnmExport.filetime.desc()")


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


if __name__ == '__main__':
    # pass
    # test = Episodes(episodes=1)
    # print("ok")
    DoleSql.commMysql("dubuxiaoyao", "", "").createTable()
    # shotFlipBook.filetime.desc()