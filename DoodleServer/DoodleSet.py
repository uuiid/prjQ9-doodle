# -*- coding: UTF-8 -*-
import json
import logging
import pathlib
import threading

import psutil

import DoodleServer.DoodleSql as Dolesql
import DoodleServer.DoodleZNCHConvert as DoleConvert
import DoodleServer.DoodleOrm

class Doodlesetting(object):
    _instance_lock = threading.Lock()
    shotRoot: str
    assetsRoot: str
    synSever: str
    version: str
    projectname: str

    def __new__(cls, *args, **kwargs):
        if not hasattr(Doodlesetting, '_instance'):
            with Doodlesetting._instance_lock:
                if not hasattr(Doodlesetting, '_instance'):
                    Doodlesetting._instance = object.__new__(cls)
        return Doodlesetting._instance

    def __init__(self):
        # 初始化设置
        self.user = '未记录'
        self.department = '未记录'
        self.syn = pathlib.Path('D:/ue_prj')
        self.synEp: int = 1
        self.FreeFileSync = 'C:\\PROGRA~1\\FREEFI~1\\FreeFileSync.exe'
        self.projectname = 'dubuxiaoyao'
        self.ProgramFolder = ['Export', 'Playblasts', 'Rendering', 'Scenefiles']
        self.assTypeFolder = ['sourceimages', 'scenes', '{}_UE4', 'rig', "{}_low"]
        self.filestate = ["Error", "Amend", "Complete"]
        self.project = ''
        self.my_sql = Dolesql.commMysql(self.projectname, "", "")
        # self.__register__ = Dolesql.commMysql("myuser", "", "")

        self.__initSetAttr(self.__getString())
        self.__initSetAttr(self.__getseverPrjBrowser())

        self.cache_path = pathlib.Path("C:\\Doodle_cache")
        self.getCacheDiskPath(1)
        self.cache_path.mkdir(parents=True, exist_ok=True)

        self.ftpuser = self.projectname + DoleConvert.isChinese(self.user).easyToEn()
        self.ftpip = "192.168.10.213"

    # <editor-fold desc="属性操作">

    # region 只读属性
    @property
    def doc(self) -> pathlib.Path:
        if not hasattr(self, '_doc'):
            self._doc = pathlib.Path("{}{}".format(pathlib.Path.home(), '\\Documents\\doodle'))
        return self._doc

    @property
    def userland(self) -> pathlib.Path:
        if not hasattr(self, '_userland'):
            self._userland = self.doc.joinpath("doodle_conf.json")
        return self._userland

    # endregion
    @property
    def synEp(self):
        if not hasattr(self, '_synEp'):
            self._synEp = 1
        return self._synEp

    @synEp.setter
    def synEp(self, synEp):
        if not isinstance(synEp, int):
            synEp = int(synEp)
        self._synEp = synEp

    @property
    def projectname(self) -> str:
        return self._projectname

    @projectname.setter
    def projectname(self, projectname: str):
        if not projectname in ["dubuxiaoyao", "changanhuanjie","dubuxiaoyao3"]:
            projectname = "dubuxiaoyao"
        self._projectname = projectname

    _project_: pathlib.Path

    @property
    def project(self):
        if not hasattr(self, '_project_'):
            assert AttributeError("")
        if not isinstance(self._project_, pathlib.Path):
            self._project_ = pathlib.Path(self._project_)
        return self._project_

    @project.setter
    def project(self, project):
        if not isinstance(project, pathlib.Path):
            self._project_ = pathlib.Path(project)
        self._project_ = project

    @property
    def en_user(self) -> str:
        return DoleConvert.isChinese(self.user).easyToEn()

    # </editor-fold>

    @property
    def password(self):
        return DoleConvert.isChinese(self.user).easyToEn()

    def __initSetAttr(self, setDict: dict):
        for key, value in setDict.items():
            setattr(self, key, value)

    def __getString(self) -> dict:
        """
        获得本地设置
        """
        if not self.doc.is_dir():
            logging.info('没有 %s 目录,-->创建', self.doc)
            # 没有目录时创建目录
            self.doc.mkdir()
        if not self.userland.is_file():
            # 具有目录没有文件时创建文件
            self.userland.touch(exist_ok=True)
            self.writeDoodlelocalSet()

            logging.info('没有 %s 文件,-->写入', self.userland)
        if not self.userland.stat().st_size:
            # 文件为空时写入默认
            self.writeDoodlelocalSet()

            logging.info('文件 %s 为空时,-->写入', self.userland)
        itoa = {}
        try:
            logging.info('尝试读取文件')
            itoa = self.userland.read_text(encoding='utf-8')
            logging.info("%s", itoa)
            itoa = json.loads(itoa)
        except:
            self.writeDoodlelocalSet()
            logging.info('读入失败,  写空文件')
        return itoa

    def writeDoodlelocalSet(self):
        """
        写入本地设置

        """
        doodlelocal_set: dict = {
            'user': self.user,
            'department': self.department,
            "syn": str(self.syn),
            "synEp": self.synEp,
            "projectname": str(self.projectname),
            "FreeFileSync": str(self.FreeFileSync)
        }
        my_setting = json.dumps(doodlelocal_set, ensure_ascii=False, indent=4, separators=(',', ':'))
        self.userland.write_text(my_setting, 'utf-8')

    def getsever(self) -> list:
        """
        返回服务器上的 同步目录设置
        """
        # 读取本地部门类型 以及每集类型
        # 获得设置的文件路径
        sql_com = f"SELECT DISTINCT value3, value4 FROM {self._projectname}.`configure` " \
                  f"WHERE name='synpath' AND value='{self.department}' AND value2 ='{self.synEp:0>3d}'"
        with self.my_sql.engine.connect() as connect:
            data = connect.execute(sql_com).fetchall()
        tmp = [data[i:i + 2] for i in range(0, len(data), 2)]
        return [{i[0][0]: self.syn + '/' + i[0][1], i[1][0]: self.synSever + '/' + i[1][1]} for i in tmp]

    # @functools.lru_cache()
    def __getseverPrjBrowser(self) -> dict:
        """
        返回服务器上的project设置
        :return: dict
        """

        sql_com = f"SELECT DISTINCT name,value FROM {self._projectname}.`configure`"
        with self.my_sql.engine.connect() as connect:
            data = connect.execute(sql_com).fetchall()

        in_data_ = {key: value for key, value in data}
        logging.info('服务器上的项目设置(json) %s', json.dumps(in_data_,
                                                      ensure_ascii=False, indent=4, separators=(',', ':')))
        return in_data_

    def getCacheDiskPath(self, disk_index: int):
        try:
            path = psutil.disk_partitions()[disk_index][1]
        except IndexError as err:
            logging.info("无法找到缓存所用磁盘")
        else:
            if disk_index > 4:
                return None
            if psutil.disk_usage(path)[3] > 90:
                self.getCacheDiskPath(disk_index + 1)
            else:
                self.cache_path = pathlib.Path(path).joinpath("Doodle_cache")
        logging.info("找到缓存路径 %s", self.cache_path)

    def FTPconnectIsGood(self) -> bool:
        with self.my_sql.session() as session:
            session.connection(execution_options={"schema_translate_map": {"myuser": "myuser"}})
            server_user = session.query(DoodleServer.DoodleOrm.user).all()
            server_user_ = [s.user for s in server_user]
        if self.user in server_user_:
            return True
        else:
            return False

    def FTP_Register(self):
        with self.my_sql.session() as session:
            session.connection(execution_options={"schema_translate_map": {"myuser": "myuser"}})
            session.add(DoodleServer.DoodleOrm.user(user=self.user,password=self.password))


if __name__ == '__main__':
    pass
