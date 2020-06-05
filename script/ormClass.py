import sqlalchemy.orm
import sqlalchemy.sql

import script.MySqlComm


class Episodes(script.MySqlComm.Base):
    __tablename__ = "episodes"
    id: int = sqlalchemy.Column(sqlalchemy.SMALLINT, primary_key=True, nullable=False, autoincrement=True, unique=True)
    episodes: int = sqlalchemy.Column(sqlalchemy.SMALLINT, unique=True)

    # 添加镜头反射
    addShot = sqlalchemy.orm.relationship("Shot", back_populates="episodes")

    # 添加灯光镜头反射
    addshotUELightScane = sqlalchemy.orm.relationship("shotUELightScane", back_populates="episodes")
    # 添加特效镜头反射
    addshotUEVFXScane = sqlalchemy.orm.relationship("shotUEVFXScane", back_populates="episodes")
    # 添加特效镜头反射
    addshotMayaAnmScane = sqlalchemy.orm.relationship("shotMayaAnmScane", back_populates="episodes")
    addshotSequeueceImage = sqlalchemy.orm.relationship("shotSequeueceImage", back_populates="episodes")
    addshotFlipBook = sqlalchemy.orm.relationship("shotFlipBook", back_populates="episodes")
    addshotScreenshot = sqlalchemy.orm.relationship("shotScreenshot", back_populates="episodes")


class Shot(script.MySqlComm.Base):
    __tablename__ = "shot"
    id: int = sqlalchemy.Column(sqlalchemy.SMALLINT, primary_key=True, nullable=False, autoincrement=True, unique=True)

    episodes__: int = sqlalchemy.Column(sqlalchemy.SMALLINT, sqlalchemy.ForeignKey("episodes.id"))
    episodes = sqlalchemy.orm.relationship("Episodes", back_populates="addShot")

    shot_: int = sqlalchemy.Column(sqlalchemy.SMALLINT)
    shotab: str = sqlalchemy.Column(sqlalchemy.VARCHAR(64))

    # 添加灯光镜头反射
    addshotUELightScane = sqlalchemy.orm.relationship("shotUELightScane", back_populates="shot")
    # 添加特效镜头反射
    addshotUEVFXScane = sqlalchemy.orm.relationship("shotUEVFXScane", back_populates="shot")
    # 添加特效镜头反射
    addshotMayaAnmScane = sqlalchemy.orm.relationship("shotMayaAnmScane", back_populates="shot")
    addshotSequeueceImage = sqlalchemy.orm.relationship("shotSequeueceImage", back_populates="shot")
    addshotFlipBook = sqlalchemy.orm.relationship("shotFlipBook", back_populates="shot")
    addshotScreenshot = sqlalchemy.orm.relationship("shotScreenshot", back_populates="shot")


class fileClass(script.MySqlComm.Base):
    """
    类型
    """
    __tablename__ = "fileclass"

    id: int = sqlalchemy.Column(sqlalchemy.SMALLINT, primary_key=True, nullable=False, autoincrement=True, unique=True)
    file_class: str = sqlalchemy.Column(sqlalchemy.VARCHAR(64), unique=True)
    # 添加种类反射
    addfileType = sqlalchemy.orm.relationship("fileType", back_populates="file_class")

    # 添加资产ue场景反射
    addassUEScane = sqlalchemy.orm.relationship("assUEScane", back_populates="file_class")
    addassMayaCharacter = sqlalchemy.orm.relationship("assMayaCharacter", back_populates="file_class")
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


class fileType(script.MySqlComm.Base):
    """
    种类
    """
    __tablename__ = "filetype"
    id: int = sqlalchemy.Column(sqlalchemy.SMALLINT, primary_key=True, nullable=False, autoincrement=True, unique=True)
    file_type: str = sqlalchemy.Column(sqlalchemy.VARCHAR(64), unique=True)

    # 添加类型反射
    file_class__: int = sqlalchemy.Column(sqlalchemy.VARCHAR(64), sqlalchemy.ForeignKey("fileclass.id"))
    file_class = sqlalchemy.orm.relationship("fileClass", back_populates="addfileType")

    # 添加资产ue场景反射
    addassUEScane = sqlalchemy.orm.relationship("assUEScane", back_populates="file_type")
    addassMayaCharacter = sqlalchemy.orm.relationship("assMayaCharacter", back_populates="file_type")
    addassUECharacter = sqlalchemy.orm.relationship("assUECharacter", back_populates="file_type")
    addassMayaLowModleModel = sqlalchemy.orm.relationship("assMayaLowModleModel", back_populates="file_type")
    addassMayaRigModel = sqlalchemy.orm.relationship("assMayaRigModel", back_populates="file_type")
    addassMapping = sqlalchemy.orm.relationship("assMapping", back_populates="file_type")
    addassFlipBook = sqlalchemy.orm.relationship("assFlipBook", back_populates="file_type")
    addassScreenshot = sqlalchemy.orm.relationship("assScreenshot", back_populates="file_type")
    # 添加灯光镜头反射
    addshotUELightScane = sqlalchemy.orm.relationship("shotUELightScane", back_populates="file_type")
    # 添加特效镜头反射
    addshotUEVFXScane = sqlalchemy.orm.relationship("shotUEVFXScane", back_populates="file_type")
    # 添加特效镜头反射
    addshotMayaAnmScane = sqlalchemy.orm.relationship("shotMayaAnmScane", back_populates="file_type")
    addshotSequeueceImage = sqlalchemy.orm.relationship("shotSequeueceImage", back_populates="file_type")
    addshotFlipBook = sqlalchemy.orm.relationship("shotFlipBook", back_populates="file_type")
    addshotScreenshot = sqlalchemy.orm.relationship("shotScreenshot", back_populates="file_type")


class fileAttributeInfo(script.MySqlComm.Base):
    __abstract__ = True
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


class assUEScane(fileAttributeInfo):
    """
    资产ue场景
    """
    __tablename__ = "assUEScane"

    # 添加类型外键
    file_class__ = sqlalchemy.Column(sqlalchemy.SMALLINT, sqlalchemy.ForeignKey("fileclass.id"))
    file_class = sqlalchemy.orm.relationship("fileClass", back_populates="addassUEScane")

    # 添加种类外键
    file_type__ = sqlalchemy.Column(sqlalchemy.SMALLINT, sqlalchemy.ForeignKey("filetype.id"))
    file_type = sqlalchemy.orm.relationship("fileType", back_populates="addassUEScane")


class assMayaCharacter(fileAttributeInfo):
    __tablename__ = "assMayaCharacter"
    # 添加类型外键
    file_class__ = sqlalchemy.Column(sqlalchemy.SMALLINT, sqlalchemy.ForeignKey("fileclass.id"))
    file_class = sqlalchemy.orm.relationship("fileClass", back_populates="addassMayaCharacter")

    # 添加种类外键
    file_type__ = sqlalchemy.Column(sqlalchemy.SMALLINT, sqlalchemy.ForeignKey("filetype.id"))
    file_type = sqlalchemy.orm.relationship("fileType", back_populates="addassMayaCharacter")


class assUECharacter(fileAttributeInfo):
    __tablename__ = "assUECharacter"
    # 添加类型外键
    file_class__ = sqlalchemy.Column(sqlalchemy.SMALLINT, sqlalchemy.ForeignKey("fileclass.id"))
    file_class = sqlalchemy.orm.relationship("fileClass", back_populates="addassUECharacter")

    # 添加种类外键
    file_type__ = sqlalchemy.Column(sqlalchemy.SMALLINT, sqlalchemy.ForeignKey("filetype.id"))
    file_type = sqlalchemy.orm.relationship("fileType", back_populates="addassUECharacter")


class assMayaLowModleModel(fileAttributeInfo):
    __tablename__ = "assMayaLowModleModel"
    # 添加类型外键
    file_class__ = sqlalchemy.Column(sqlalchemy.SMALLINT, sqlalchemy.ForeignKey("fileclass.id"))
    file_class = sqlalchemy.orm.relationship("fileClass", back_populates="addassMayaLowModleModel")

    # 添加种类外键
    file_type__ = sqlalchemy.Column(sqlalchemy.SMALLINT, sqlalchemy.ForeignKey("filetype.id"))
    file_type = sqlalchemy.orm.relationship("fileType", back_populates="addassMayaLowModleModel")


class assMayaRigModel(fileAttributeInfo):
    __tablename__ = "assMayaRigModel"
    # 添加类型外键
    file_class__ = sqlalchemy.Column(sqlalchemy.SMALLINT, sqlalchemy.ForeignKey("fileclass.id"))
    file_class = sqlalchemy.orm.relationship("fileClass", back_populates="addassMayaRigModel")

    # 添加种类外键
    file_type__ = sqlalchemy.Column(sqlalchemy.SMALLINT, sqlalchemy.ForeignKey("filetype.id"))
    file_type = sqlalchemy.orm.relationship("fileType", back_populates="addassMayaRigModel")


class assMapping(fileAttributeInfo):
    __tablename__ = "assMapping"
    # 添加类型外键
    file_class__ = sqlalchemy.Column(sqlalchemy.SMALLINT, sqlalchemy.ForeignKey("fileclass.id"))
    file_class = sqlalchemy.orm.relationship("fileClass", back_populates="addassMapping")

    # 添加种类外键
    file_type__ = sqlalchemy.Column(sqlalchemy.SMALLINT, sqlalchemy.ForeignKey("filetype.id"))
    file_type = sqlalchemy.orm.relationship("fileType", back_populates="addassMapping")


class assFlipBook(fileAttributeInfo):
    __tablename__ = "assFlipBook"
    # 添加类型外键
    file_class__ = sqlalchemy.Column(sqlalchemy.SMALLINT, sqlalchemy.ForeignKey("fileclass.id"))
    file_class = sqlalchemy.orm.relationship("fileClass", back_populates="addassFlipBook")

    # 添加种类外键
    file_type__ = sqlalchemy.Column(sqlalchemy.SMALLINT, sqlalchemy.ForeignKey("filetype.id"))
    file_type = sqlalchemy.orm.relationship("fileType", back_populates="addassFlipBook")


class assScreenshot(fileAttributeInfo):
    __tablename__ = "assScreenshot"
    # 添加类型外键
    file_class__ = sqlalchemy.Column(sqlalchemy.SMALLINT, sqlalchemy.ForeignKey("fileclass.id"))
    file_class = sqlalchemy.orm.relationship("fileClass", back_populates="addassScreenshot")

    # 添加种类外键
    file_type__ = sqlalchemy.Column(sqlalchemy.SMALLINT, sqlalchemy.ForeignKey("filetype.id"))
    file_type = sqlalchemy.orm.relationship("fileType", back_populates="addassScreenshot")


class shotUELightScane(fileAttributeInfo):
    """
    镜头ue灯光场景
    """
    __tablename__ = "shotUELightScane"

    # 集数外键约束
    episodes__ = sqlalchemy.Column(sqlalchemy.SMALLINT, sqlalchemy.ForeignKey("episodes.id"))
    episodes = sqlalchemy.orm.relationship("Episodes", back_populates="addshotUELightScane")

    # 镜头外键
    shot__ = sqlalchemy.Column(sqlalchemy.SMALLINT, sqlalchemy.ForeignKey("shot.id"))
    shot = sqlalchemy.orm.relationship("Shot", back_populates="addshotUELightScane")

    # 添加类型外键
    file_class__ = sqlalchemy.Column(sqlalchemy.SMALLINT, sqlalchemy.ForeignKey("fileclass.id"))
    file_class = sqlalchemy.orm.relationship("fileClass", back_populates="addshotUELightScane")

    # 添加种类外键
    file_type__ = sqlalchemy.Column(sqlalchemy.SMALLINT, sqlalchemy.ForeignKey("filetype.id"))
    file_type = sqlalchemy.orm.relationship("fileType", back_populates="addshotUELightScane")


class shotUEVFXScane(fileAttributeInfo):
    """
    镜头ue特效场景
    """
    __tablename__ = "shotUEVFXScane"

    # 集数外键约束
    episodes__ = sqlalchemy.Column(sqlalchemy.SMALLINT, sqlalchemy.ForeignKey("episodes.id"))
    episodes = sqlalchemy.orm.relationship("Episodes", back_populates="addshotUEVFXScane")

    # 镜头外键
    shot__ = sqlalchemy.Column(sqlalchemy.SMALLINT, sqlalchemy.ForeignKey("shot.id"))
    shot = sqlalchemy.orm.relationship("Shot", back_populates="addshotUEVFXScane")

    # 添加类型外键
    file_class__ = sqlalchemy.Column(sqlalchemy.SMALLINT, sqlalchemy.ForeignKey("fileclass.id"))
    file_class = sqlalchemy.orm.relationship("fileClass", back_populates="addshotUEVFXScane")

    # 添加种类外键
    file_type__ = sqlalchemy.Column(sqlalchemy.SMALLINT, sqlalchemy.ForeignKey("filetype.id"))
    file_type = sqlalchemy.orm.relationship("fileType", back_populates="addshotUEVFXScane")


class shotMayaAnmScane(fileAttributeInfo):
    """
    镜头maya动画场景
    """
    __tablename__ = "shotMayaAnmScane"
    # 集数外键约束
    episodes__ = sqlalchemy.Column(sqlalchemy.SMALLINT, sqlalchemy.ForeignKey("episodes.id"))
    episodes = sqlalchemy.orm.relationship("Episodes", back_populates="addshotMayaAnmScane")

    # 镜头外键
    shot__ = sqlalchemy.Column(sqlalchemy.SMALLINT, sqlalchemy.ForeignKey("shot.id"))
    shot = sqlalchemy.orm.relationship("Shot", back_populates="addshotMayaAnmScane")

    # 添加类型外键
    file_class__ = sqlalchemy.Column(sqlalchemy.SMALLINT, sqlalchemy.ForeignKey("fileclass.id"))
    file_class = sqlalchemy.orm.relationship("fileClass", back_populates="addshotMayaAnmScane")

    # 添加种类外键
    file_type__ = sqlalchemy.Column(sqlalchemy.SMALLINT, sqlalchemy.ForeignKey("filetype.id"))
    file_type = sqlalchemy.orm.relationship("fileType", back_populates="addshotMayaAnmScane")


class shotSequeueceImage(fileAttributeInfo):
    __tablename__ = "shotSequeueceImage"
    # 集数外键约束
    episodes__ = sqlalchemy.Column(sqlalchemy.SMALLINT, sqlalchemy.ForeignKey("episodes.id"))
    episodes = sqlalchemy.orm.relationship("Episodes", back_populates="addshotSequeueceImage")

    # 镜头外键
    shot__ = sqlalchemy.Column(sqlalchemy.SMALLINT, sqlalchemy.ForeignKey("shot.id"))
    shot = sqlalchemy.orm.relationship("Shot", back_populates="addshotSequeueceImage")

    # 添加类型外键
    file_class__ = sqlalchemy.Column(sqlalchemy.SMALLINT, sqlalchemy.ForeignKey("fileclass.id"))
    file_class = sqlalchemy.orm.relationship("fileClass", back_populates="addshotSequeueceImage")

    # 添加种类外键
    file_type__ = sqlalchemy.Column(sqlalchemy.SMALLINT, sqlalchemy.ForeignKey("filetype.id"))
    file_type = sqlalchemy.orm.relationship("fileType", back_populates="addshotSequeueceImage")


class shotFlipBook(fileAttributeInfo):
    __tablename__ = "shotFlipBook"
    # 集数外键约束
    episodes__ = sqlalchemy.Column(sqlalchemy.SMALLINT, sqlalchemy.ForeignKey("episodes.id"))
    episodes = sqlalchemy.orm.relationship("Episodes", back_populates="addshotFlipBook")

    # 镜头外键
    shot__ = sqlalchemy.Column(sqlalchemy.SMALLINT, sqlalchemy.ForeignKey("shot.id"))
    shot = sqlalchemy.orm.relationship("Shot", back_populates="addshotFlipBook")

    # 添加类型外键
    file_class__ = sqlalchemy.Column(sqlalchemy.SMALLINT, sqlalchemy.ForeignKey("fileclass.id"))
    file_class = sqlalchemy.orm.relationship("fileClass", back_populates="addshotFlipBook")

    # 添加种类外键
    file_type__ = sqlalchemy.Column(sqlalchemy.SMALLINT, sqlalchemy.ForeignKey("filetype.id"))
    file_type = sqlalchemy.orm.relationship("fileType", back_populates="addshotFlipBook")


class shotScreenshot(fileAttributeInfo):
    __tablename__ = "shotScreenshot"
    episodes__ = sqlalchemy.Column(sqlalchemy.SMALLINT, sqlalchemy.ForeignKey("episodes.id"))
    episodes = sqlalchemy.orm.relationship("Episodes", back_populates="addshotScreenshot")

    # 镜头外键
    shot__ = sqlalchemy.Column(sqlalchemy.SMALLINT, sqlalchemy.ForeignKey("shot.id"))
    shot = sqlalchemy.orm.relationship("Shot", back_populates="addshotScreenshot")

    # 添加类型外键
    file_class__ = sqlalchemy.Column(sqlalchemy.SMALLINT, sqlalchemy.ForeignKey("fileclass.id"))
    file_class = sqlalchemy.orm.relationship("fileClass", back_populates="addshotScreenshot")

    # 添加种类外键
    file_type__ = sqlalchemy.Column(sqlalchemy.SMALLINT, sqlalchemy.ForeignKey("filetype.id"))
    file_type = sqlalchemy.orm.relationship("fileType", back_populates="addshotScreenshot")


# =======================================================================


class nameTochinese(script.MySqlComm.Base):
    __tablename__ = "nameTochinese"
    id: int = sqlalchemy.Column(sqlalchemy.SMALLINT, primary_key=True)
    name: str = sqlalchemy.Column(sqlalchemy.VARCHAR(128), unique=True)
    localname: str = sqlalchemy.Column(sqlalchemy.VARCHAR(128), unique=True)
