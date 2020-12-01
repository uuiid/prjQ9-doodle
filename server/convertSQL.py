import contextlib
import json
import logging
import pathlib
import re
import typing

import DoodleServer.DoodleOrm
import DoodleServer.DoodleSql
import sqlalchemy.orm
import sqlalchemy.sql
import sqlalchemy.ext.declarative
import sqlalchemy.databases

Base = sqlalchemy.ext.declarative.declarative_base()


class baseFile(Base):
    __tablename__ = "baseFile"
    id: int = sqlalchemy.Column(sqlalchemy.BIGINT, primary_key=True, nullable=False, autoincrement=True, unique=True)
    file: str = sqlalchemy.Column(sqlalchemy.VARCHAR(128))
    fileSuffixes: str = sqlalchemy.Column(sqlalchemy.VARCHAR(32))
    user: str = sqlalchemy.Column(sqlalchemy.VARCHAR(128))
    version: int = sqlalchemy.Column(sqlalchemy.databases.mssql.BIGINT)
    _file_path_: str = sqlalchemy.Column(sqlalchemy.VARCHAR(4096))
    infor: str = sqlalchemy.Column(sqlalchemy.VARCHAR(4096))
    filestate = sqlalchemy.Column(sqlalchemy.VARCHAR(64))
    filetime = sqlalchemy.Column(sqlalchemy.DATETIME,
                                 server_default=sqlalchemy.sql.func.now(),
                                 server_onupdate=sqlalchemy.sql.func.now())

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

    assClass_id = sqlalchemy.Column(sqlalchemy.databases.mssql.BIGINT, sqlalchemy.ForeignKey("assclass.id"))
    assClass = sqlalchemy.orm.relationship("assClass", back_populates="baseFile_list")

    assType_id = sqlalchemy.Column(sqlalchemy.databases.mssql.BIGINT, sqlalchemy.ForeignKey("assType.id"))
    assType = sqlalchemy.orm.relationship("assType", back_populates="baseFile_list")

    episodes_id = sqlalchemy.Column(sqlalchemy.databases.mssql.BIGINT, sqlalchemy.ForeignKey("episodes.id"))
    episodes = sqlalchemy.orm.relationship("episodes", back_populates="baseFile_list")

    shots_id = sqlalchemy.Column(sqlalchemy.databases.mssql.BIGINT, sqlalchemy.ForeignKey("shots.id"))
    shots = sqlalchemy.orm.relationship("shots", back_populates="baseFile_list")

    shotClass_id = sqlalchemy.Column(sqlalchemy.databases.mssql.BIGINT, sqlalchemy.ForeignKey("shotclass.id"))
    shotClass = sqlalchemy.orm.relationship("shotClass", back_populates="baseFile_list")

    shotType_id = sqlalchemy.Column(sqlalchemy.databases.mssql.BIGINT, sqlalchemy.ForeignKey("shottype.id"))
    shotType = sqlalchemy.orm.relationship("shotType", back_populates="baseFile_list")

    project_id: int = sqlalchemy.Column(sqlalchemy.databases.mssql.BIGINT, sqlalchemy.ForeignKey("project.id"))
    project = sqlalchemy.orm.relationship("project", back_populates="baseFile_list")


class configure(Base):
    __tablename__ = "configure"
    id: int = sqlalchemy.Column(sqlalchemy.databases.mssql.BIGINT, primary_key=True, nullable=False, autoincrement=True,
                                unique=True)
    name: str = sqlalchemy.Column(sqlalchemy.VARCHAR(128))
    value: str = sqlalchemy.Column(sqlalchemy.VARCHAR(128))

    project_id: int = sqlalchemy.Column(sqlalchemy.databases.mssql.BIGINT, sqlalchemy.ForeignKey("project.id"))
    project = sqlalchemy.orm.relationship("project", back_populates="configure_list")


class user(Base):
    __tablename__ = "user"
    id: int = sqlalchemy.Column(sqlalchemy.databases.mssql.BIGINT, primary_key=True, nullable=False, autoincrement=True,
                                unique=True)
    user: str = sqlalchemy.Column(sqlalchemy.VARCHAR(128), nullable=False)
    password: str = sqlalchemy.Column(sqlalchemy.VARCHAR(1024), nullable=False)


class synFile(Base):
    __tablename__ = "synfile"
    id: int = sqlalchemy.Column(sqlalchemy.databases.mssql.BIGINT, primary_key=True, nullable=False, autoincrement=True,
                                unique=True)
    assClass_id: int = sqlalchemy.Column(sqlalchemy.databases.mssql.BIGINT, sqlalchemy.ForeignKey("assclass.id"))
    project_id: int = sqlalchemy.Column(sqlalchemy.databases.mssql.BIGINT, sqlalchemy.ForeignKey("project.id"))
    episodes_id: int = sqlalchemy.Column(sqlalchemy.databases.mssql.BIGINT, sqlalchemy.ForeignKey("episodes.id"))
    path: str = sqlalchemy.Column(sqlalchemy.VARCHAR(4096), nullable=False)

    project = sqlalchemy.orm.relationship("project", back_populates="synFile_list")
    assClass = sqlalchemy.orm.relationship("assClass", back_populates="synFile_list")
    episodes = sqlalchemy.orm.relationship("episodes", back_populates="synFile_list")


# ass

class assType(Base):
    __tablename__ = "assType"
    id: int = sqlalchemy.Column(sqlalchemy.databases.mssql.BIGINT, primary_key=True, nullable=False, autoincrement=True,
                                unique=True)
    ass_type: str = sqlalchemy.Column(sqlalchemy.VARCHAR(64))

    project_id = sqlalchemy.Column(sqlalchemy.databases.mssql.BIGINT, sqlalchemy.ForeignKey("project.id"))
    project = sqlalchemy.orm.relationship("project", back_populates="assType_list")

    baseFile_list: typing.List[baseFile] = sqlalchemy.orm.relationship(
        "baseFile",
        back_populates="assType"
    )


class ZNch(Base):
    __tablename__ = "znch"
    id: int = sqlalchemy.Column(sqlalchemy.databases.mssql.BIGINT, primary_key=True)
    localname: str = sqlalchemy.Column(sqlalchemy.VARCHAR(128))

    # 添加中文名称
    assClass_id: int = sqlalchemy.Column(sqlalchemy.databases.mssql.BIGINT, sqlalchemy.ForeignKey("assclass.id"),
                                         unique=True)
    assClass = sqlalchemy.orm.relationship("assClass", back_populates="nameZNCH")


class assClass(Base):
    __tablename__ = "assclass"
    id: int = sqlalchemy.Column(sqlalchemy.databases.mssql.BIGINT, primary_key=True, nullable=False, autoincrement=True,
                                unique=True)
    ass_name: str = sqlalchemy.Column(sqlalchemy.VARCHAR(256))

    assdep_id: int = sqlalchemy.Column(sqlalchemy.databases.mssql.BIGINT, sqlalchemy.ForeignKey("assdepartment.id"))
    assdepartment = sqlalchemy.orm.relationship("assdepartment", back_populates="assClass_list")

    baseFile_list: typing.List[baseFile] = sqlalchemy.orm.relationship(
        "baseFile",
        back_populates="assClass"
    )
    synFile_list: typing.List[synFile] = sqlalchemy.orm.relationship(
        "synFile",
        back_populates="assClass"
    )
    nameZNCH = sqlalchemy.orm.relationship("ZNch", uselist=False, back_populates="assClass")


class assdepartment(Base):
    __tablename__ = "assdepartment"
    id: int = sqlalchemy.Column(sqlalchemy.databases.mssql.BIGINT, primary_key=True, nullable=False, autoincrement=True,
                                unique=True)
    ass_dep: str = sqlalchemy.Column(sqlalchemy.VARCHAR(64))

    project_id: int = sqlalchemy.Column(sqlalchemy.databases.mssql.BIGINT, sqlalchemy.ForeignKey("project.id"))
    project = sqlalchemy.orm.relationship("project", back_populates="assdepartment_list")

    assClass_list: typing.List[assClass] = sqlalchemy.orm.relationship(
        "assClass",
        back_populates="assdepartment"
    )


# shot类


class shotType(Base):
    __tablename__ = "shottype"
    id: int = sqlalchemy.Column(sqlalchemy.databases.mssql.BIGINT, primary_key=True, nullable=False, autoincrement=True,
                                unique=True)
    shot_type: str = sqlalchemy.Column(sqlalchemy.VARCHAR(64))

    shotClass_id = sqlalchemy.Column(sqlalchemy.databases.mssql.BIGINT, sqlalchemy.ForeignKey("shotclass.id"))
    shotClass = sqlalchemy.orm.relationship("shotClass", back_populates="shotType_list")

    project_id: int = sqlalchemy.Column(sqlalchemy.databases.mssql.BIGINT, sqlalchemy.ForeignKey("project.id"))
    project = sqlalchemy.orm.relationship("project", back_populates="shotType_list")

    baseFile_list: typing.List[baseFile] = sqlalchemy.orm.relationship(
        "baseFile",
        back_populates="shotType"
    )


class shotClass(Base):
    __tablename__ = "shotclass"
    id: int = sqlalchemy.Column(sqlalchemy.databases.mssql.BIGINT, primary_key=True, nullable=False, autoincrement=True,
                                unique=True)
    shot_class: str = sqlalchemy.Column(sqlalchemy.VARCHAR(64))

    project_id: int = sqlalchemy.Column(sqlalchemy.databases.mssql.BIGINT, sqlalchemy.ForeignKey("project.id"))
    project = sqlalchemy.orm.relationship("project", back_populates="shotClass_list")

    shotType_list: typing.List[shotType] = sqlalchemy.orm.relationship(
        "shotType",
        back_populates="shotClass"
    )
    baseFile_list: typing.List[baseFile] = sqlalchemy.orm.relationship(
        "baseFile",
        back_populates="shotClass"
    )


class shots(Base):
    __tablename__ = "shots"
    id: int = sqlalchemy.Column(sqlalchemy.databases.mssql.BIGINT, primary_key=True, nullable=False, autoincrement=True,
                                unique=True)
    shot: int = sqlalchemy.Column(sqlalchemy.databases.mssql.BIGINT)
    shotab: str = sqlalchemy.Column(sqlalchemy.VARCHAR(64))

    episodes_id = sqlalchemy.Column(sqlalchemy.databases.mssql.BIGINT, sqlalchemy.ForeignKey("episodes.id"))
    episodes = sqlalchemy.orm.relationship("episodes", back_populates="shots_list")

    baseFile_list: typing.List[baseFile] = sqlalchemy.orm.relationship(
        "baseFile",
        back_populates="shots"
    )


class episodes(Base):
    __tablename__ = "episodes"
    id: int = sqlalchemy.Column(sqlalchemy.databases.mssql.BIGINT, primary_key=True, nullable=False, autoincrement=True,
                                unique=True)
    episodes: int = sqlalchemy.Column(sqlalchemy.databases.mssql.BIGINT)

    project_id: int = sqlalchemy.Column(sqlalchemy.databases.mssql.BIGINT, sqlalchemy.ForeignKey("project.id"))
    project = sqlalchemy.orm.relationship("project", back_populates="episodes_list")

    shots_list: typing.List[shots] = sqlalchemy.orm.relationship(
        "shots",
        back_populates="episodes"
    )
    baseFile_list: typing.List[baseFile] = sqlalchemy.orm.relationship(
        "baseFile",
        back_populates="episodes"
    )
    synFile_list: typing.List[synFile] = sqlalchemy.orm.relationship(
        "synFile",
        back_populates="episodes"
    )


class project(Base):
    __tablename__ = "project"
    id: int = sqlalchemy.Column(sqlalchemy.databases.mssql.BIGINT, primary_key=True, nullable=False, autoincrement=True,
                                unique=True)
    name: str = sqlalchemy.Column(sqlalchemy.VARCHAR(128))

    episodes_list: typing.List[episodes] = sqlalchemy.orm.relationship(
        "episodes",
        back_populates="project",
    )

    assdepartment_list: typing.List[assdepartment] = sqlalchemy.orm.relationship(
        "assdepartment",
        back_populates="project",
    )

    assType_list: typing.List[assType] = sqlalchemy.orm.relationship(
        "assType",
        back_populates="project",
    )

    shotType_list: typing.List[shotType] = sqlalchemy.orm.relationship(
        "shotType",
        back_populates="project",
    )

    shotClass_list: typing.List[shotClass] = sqlalchemy.orm.relationship(
        "shotClass",
        back_populates="project",
    )

    baseFile_list: typing.List[baseFile] = sqlalchemy.orm.relationship(
        "baseFile",
        back_populates="project"
    )
    synFile_list: typing.List[synFile] = sqlalchemy.orm.relationship(
        "synFile",
        back_populates="project"
    )
    configure_list: typing.List[configure] = sqlalchemy.orm.relationship(
        "configure",
        back_populates="project"
    )


class convertSql:
    prj_list: typing.List[project] = []

    def __init__(self):
        com_lur = "mysql+mysqlconnector" \
                  "://{_departmen}:{_password}@" \
                  "192.168.10.213:3306/{_mybd}".format(_departmen="Effects", _password="Effects", _mybd="doodle_main")
        self.engine = sqlalchemy.create_engine(com_lur, encoding='utf-8')  # , echo=True
        tmp_session = sqlalchemy.orm.sessionmaker(bind=self.engine)
        self.sessionclass = sqlalchemy.orm.scoped_session(tmp_session)
        self.conn_duo: DoodleServer.DoodleSql.commMysql = None
        self.set = DoodleServer.DoodleSet.Doodlesetting()

        self.assType: typing.List[typing.Dict[str, assType]] = [{}, {}]
        self.shotClass: typing.List[typing.Dict[str, shotClass]] = [{}, {}]
        self.shotType: typing.List[typing.Dict[str, shotType]] = [{}, {}]

    @contextlib.contextmanager
    def session(self) -> sqlalchemy.orm.session.Session:
        # tmp_session = # self.sessionclass()
        session: sqlalchemy.orm.session.Session = sqlalchemy.orm.sessionmaker(bind=self.engine)()
        try:
            yield session
            session.commit()
        except BaseException as err:
            logging.error("%s", err)
            session.rollback()
        finally:
            session.close()

    def run(self):
        # self.conn_old = DoodleServer.DoodleSql.commMysql("dubuxiaoyao3", "", "")
        self.set.projectname = "dubuxiaoyao3"
        self.prj_list.append(project(name="dubuxiaoyao3"))
        self.setConfig(0)
        self.getOldass(0)
        self.getOldShot(0)

        self.prj_list.append(project(name="changanhuanjie"))
        self.set.projectname = "changanhuanjie"
        self.setConfig(1)
        self.getOldass(1)
        self.getOldShot(1)

        self.sub()

    def getOldass(self, prj_index):
        self.ass_old = DoodleServer.DoodleCore.PrjAss(self.set)
        ass_class_old = self.ass_old.queryAssClass()

        # ass class 循环
        for oldAssdep in ass_class_old:
            ass_dep = assdepartment(ass_dep=oldAssdep.file_class)
            self.prj_list[prj_index].assdepartment_list.append(ass_dep)
            # ass name 循环
            for oldAssClass in oldAssdep.addass_class:
                ass_class = assClass(ass_name=oldAssClass.file_name)
                ass_dep.assClass_list.append(ass_class)
                # 中文添加
                if oldAssClass.nameZNCH:
                    ass_class_zn = ZNch(localname=oldAssClass.nameZNCH.localname)
                    ass_class.nameZNCH = ass_class_zn
                # ass type 循环
                for oldAssType in oldAssClass.addfileType:
                    # ass_type = assType(ass_type=oldAssType.file_type)
                    # if re.findall("_UE",oldAssType.file_type):
                    for oldFile in oldAssType.addfileAttributeInfo:
                        ass_file = baseFile(file=oldFile.file, fileSuffixes=oldFile.fileSuffixes,
                                            user=oldFile.user, version=oldFile.version,
                                            _file_path_=oldFile._file_path_,
                                            infor=oldFile.infor,
                                            filestate=oldFile.filestate,
                                            filetime=oldFile.filetime,
                                            )
                        self.prj_list[prj_index].baseFile_list.append(ass_file)
                        # ass_type.baseFile_list.append(ass_file)
                        ass_class.baseFile_list.append(ass_file)
                        if re.findall("_UE4", oldAssType.file_type):
                            self.chickAssType(prj_index, "UE4")
                            self.assType[prj_index]["UE4"].baseFile_list.append(ass_file)
                        elif re.findall("scenes", oldAssType.file_type):
                            self.chickAssType(prj_index, "scenes")
                            self.assType[prj_index]["scenes"].baseFile_list.append(ass_file)
                        elif re.findall("rig", oldAssType.file_type):
                            self.chickAssType(prj_index, "rig")
                            self.assType[prj_index]["rig"].baseFile_list.append(ass_file)
                        elif re.findall("sourceimages", oldAssType.file_type):
                            self.chickAssType(prj_index, "sourceimages")
                            self.assType[prj_index]["sourceimages"].baseFile_list.append(ass_file)
                        elif re.findall("_low", oldAssType.file_type):
                            self.chickAssType(prj_index, "scenes_low")
                            self.assType[prj_index]["scenes_low"].baseFile_list.append(ass_file)
                        elif re.findall("screenshot", oldAssType.file_type):
                            self.chickAssType(prj_index, "screenshot")
                            self.assType[prj_index]["screenshot"].baseFile_list.append(ass_file)
                        else:
                            raise Exception()
        pass

    def chickAssType(self, prj_index, name_type: str):
        if name_type not in self.assType[prj_index]:
            ass_type = assType(ass_type=name_type)
            self.prj_list[prj_index].assType_list.append(ass_type)
            self.assType[prj_index][name_type] = ass_type

    def chickShotClass(self, prj_index, name_type: str):
        if name_type not in self.shotClass[prj_index]:
            shot_class = shotClass(shot_class=name_type)
            self.prj_list[prj_index].shotClass_list.append(shot_class)
            self.shotClass[prj_index][name_type] = shot_class

    def chickShotType(self, prj_index, name_type: str):
        if name_type not in self.shotType[prj_index]:
            shot_type = shotType(shot_type=name_type)
            self.prj_list[prj_index].shotType_list.append(shot_type)
            self.shotType[prj_index][name_type] = shot_type

    def getOldShot(self, prj_index):
        self.shot_old = DoodleServer.DoodleCore.PrjShot(self.set)
        eps_old_all = self.shot_old.queryEps()

        # 集数循环
        for old_eps in eps_old_all:
            eps = episodes(episodes=old_eps.episodes)
            self.prj_list[prj_index].episodes_list.append(eps)
            self.getConfig(eps, prj_index)
            # 镜头循环
            for old_shot in old_eps.addShot:
                shot = shots(shot=old_shot.shot_, shotab=old_shot.shotab)
                eps.shots_list.append(shot)
                # 镜头类别循环
                for old_class in old_shot.addfileClass:
                    # 镜头type循环
                    for old_type in old_class.addfileType:
                        for old_file in old_type.addfileAttributeInfo:
                            base_file = baseFile(file=old_file.file, fileSuffixes=old_file.fileSuffixes,
                                                 user=old_file.user, version=old_file.version,
                                                 _file_path_=old_file._file_path_,
                                                 infor=old_file.infor,
                                                 filestate=old_file.filestate,
                                                 filetime=old_file.filetime, )
                            self.prj_list[prj_index].baseFile_list.append(base_file)
                            eps.baseFile_list.append(base_file)
                            shot.baseFile_list.append(base_file)
                            if re.findall("[A,a]nm", old_class.file_class):
                                self.chickShotClass(prj_index, "Anm")
                                self.shotClass[prj_index]["Anm"].baseFile_list.append(base_file)
                            elif re.findall("VFX", old_class.file_class):
                                self.chickShotClass(prj_index, "VFX")
                                self.shotClass[prj_index]["VFX"].baseFile_list.append(base_file)
                            elif re.findall("Light", old_class.file_class):
                                self.chickShotClass(prj_index, "Light")
                                self.shotClass[prj_index]["Light"].baseFile_list.append(base_file)
                            else:
                                raise Exception()

                            if re.findall("FB_VFX", old_type.file_type):
                                self.chickShotType(prj_index, "flipbook")
                                self.shotType[prj_index]["flipbook"].baseFile_list.append(base_file)


                            elif re.findall("Ani", old_type.file_type):
                                self.chickShotType(prj_index, "Animation")
                                self.shotType[prj_index]["Animation"].baseFile_list.append(base_file)


                            elif re.findall("donghua", old_type.file_type):
                                self.chickShotType(prj_index, "Animation")
                                self.shotType[prj_index]["Animation"].baseFile_list.append(base_file)

                            elif re.findall("anm", old_type.file_type):
                                self.chickShotType(prj_index, "Animation")
                                self.shotType[prj_index]["Animation"].baseFile_list.append(base_file)

                            elif re.findall("[f,F][B,b][x,X]", old_type.file_type):
                                self.chickShotType(prj_index, "Animation")
                                self.shotType[prj_index]["Animation"].baseFile_list.append(base_file)


                            elif re.findall("export", old_type.file_type):
                                self.chickShotType(prj_index, "maya_export")
                                self.shotType[prj_index]["maya_export"].baseFile_list.append(base_file)

                            elif re.findall("FB_Light", old_type.file_type):
                                self.chickShotType(prj_index, "flipbook")
                                self.shotType[prj_index]["flipbook"].baseFile_list.append(base_file)

                            elif re.findall("screenshot", old_class.file_class):
                                self.chickShotType(prj_index, "screenshot")
                                self.shotType[prj_index]["screenshot"].baseFile_list.append(base_file)
                            else:
                                pass
                            # shot_class.baseFile_list.append(base_file)
                            # shot_type.baseFile_list.append(base_file)
                            # if not base_file.shots:
                            #     episodes.shotClass_list.append(shot_type)
        pass

    def getConfig(self, epsNode: episodes, prjIndex):
        self.set.synEp = epsNode.episodes
        path = self.set.getsever_backup()
        synpath = synFile()
        synpath.path = self.convert(path)

        self.prj_list[prjIndex].synFile_list.append(synpath)
        epsNode.synFile_list.append(synpath)

    def setConfig(self, prjIndex):
        pej = self.prj_list[prjIndex]
        pej.configure_list.append(configure(name="shotRoot", value="/03_Workflow/Shots"))
        pej.configure_list.append(configure(name="assetsRoot", value="/03_Workflow/Assets"))
        if prjIndex == 0:
            pej.configure_list.append(configure(name="synSever", value="V:/03_Workflow/Assets"))
            pej.configure_list.append(configure(name="project", value="V:/"))
        if prjIndex == 1:
            pej.configure_list.append(configure(name="synSever", value="X:/03_Workflow/Assets"))
            pej.configure_list.append(configure(name="project", value="X:/"))

    def sub(self):
        with self.session() as session:
            session: sqlalchemy.orm.session.Session
            for prj in self.prj_list:
                session.add(prj)

    def convert(self, _str_: typing.List[typing.Dict]):
        # josn_: typing.List = json.loads(_str_)
        name = []
        for item in _str_:
            name.append({"Left": "{}/{}".format(item["Left"].split("/")[0],item["Left"].split("/")[1]),
                         "Right":  "{}/{}".format(item["Right"].split("/")[0],item["Right"].split("/")[1])})
        return json.dumps(name, ensure_ascii=False, separators=(',', ':'), )

    def patch(self):
        with self.session() as session:
            assert isinstance(session, sqlalchemy.orm.session.Session)
            data: typing.List[synFile] = session.query(synFile).all()
            for i in data:
                i.path = self.convert(i.path)
            session.commit()


if __name__ == '__main__':
    # Base.metadata.create_all(DoodleServer.DoodleSql.commMysql("doodle_main", "", "").engine)
    convertSql().run()
    # convertSql().patch()
