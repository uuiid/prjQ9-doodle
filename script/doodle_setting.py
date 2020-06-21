# -*- coding: UTF-8 -*-
import json
import logging
import pathlib
import sys
import threading

import psutil
import sqlalchemy.ext.declarative
from PySide2 import QtWidgets

import UiFile.setting
import script.MySqlComm
import script.convert
import script.doodleLog


class srverSetting(sqlalchemy.ext.declarative.declarative_base()):
    __tablename__ = "configure"
    id = sqlalchemy.Column(sqlalchemy.SMALLINT, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.VARCHAR(128))
    value = sqlalchemy.Column(sqlalchemy.VARCHAR(1024))
    value2 = sqlalchemy.Column(sqlalchemy.VARCHAR(32))
    value3 = sqlalchemy.Column(sqlalchemy.VARCHAR(256))
    value4 = sqlalchemy.Column(sqlalchemy.VARCHAR(1024))


class Doodlesetting():
    _setting = {}
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
        self.__initSetAttr(self.__getString())
        self.__initSetAttr(self.__getseverPrjBrowser())

        self.my_sql = script.MySqlComm.commMysql(self.projectname, "", "")

        self.sever_con = srverSetting()

        self.cache_path = pathlib.Path("C:\\Doodle_cache")
        self.getCacheDiskPath(1)
        self.cache_path.mkdir(parents=True, exist_ok=True)

        self.ftpuser = self.projectname + script.convert.isChinese(self.user).easyToEn()
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
        if not projectname in ["dubuxiaoyao", "changanhuanjie"]:
            projectname = "dubuxiaoyao"
        self._projectname = projectname

    # </editor-fold>

    @property
    def password(self):
        return script.convert.isChinese(self.user).easyToEn()

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
        # self.setlocale = script.doodle_setting.Doodlesetting()
        # 获得设置的文件路径
        sql_com = "SELECT DISTINCT value3, value4 FROM `configure` " \
                  f"WHERE name='synpath' AND value='{self.department}' AND value2 ='{self.synEp:0>3d}'"
        data = script.MySqlComm.selsctCommMysql(self.projectname, self.department, "", sql_command=sql_com)
        # {"Left": [value for key, value in data if key == "Left"],
        #  "Right": [value for key, value in data if key == "Right"]}
        # tmp = [{key: value} for key, value in data]
        tmp = [data[i:i + 2] for i in range(0, len(data), 2)]
        return [{i[0][0]: self.syn + '/' + i[0][1], i[1][0]: self.synSever + '/' + i[1][1]} for i in tmp]

    # @functools.lru_cache()
    def __getseverPrjBrowser(self) -> dict:
        """
        返回服务器上的project设置
        :return: dict
        """

        sql_com = "SELECT DISTINCT name,value FROM `configure`"
        data = script.MySqlComm.selsctCommMysql(self.projectname, self.department, "", sql_command=sql_com)

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
        sql_command = f"""SELECT `user` FROM user"""
        server_user = script.MySqlComm.selsctCommMysql("myuser","","",sql_command)
        server_user_ = [s[0] for s in server_user]
        if self.user in server_user_:
            return True
        else:
            return False

    def FTP_Register(self):
        sql_command = """INSERT INTO `user` (`user`, password) VALUES ('{}','{}')""".format(self.user,self.password)
        script.MySqlComm.inserteCommMysql("myuser","","",sql_command)


class DoodlesettingGUI(QtWidgets.QMainWindow, UiFile.setting.Ui_MainWindow):

    def __init__(self, parent=None):
        super(DoodlesettingGUI, self).__init__()
        # QtWidgets.QMainWindow.__init__(self, parent=parent)
        self.setlocale = Doodlesetting()
        self.ta_log_GUI = script.doodleLog.get_logger(__name__ + 'GUI')

        self.setupUi(self)
        # 设置部门显示
        self.DepartmentTest.setCurrentText(self.setlocale.department)
        self.DepartmentTest.currentIndexChanged.connect(lambda: self.editconf('department',
                                                                              self.DepartmentTest.currentText()))
        # 设置人员名称
        self.userTest.setText(self.setlocale.user)
        self.userTest.textChanged.connect(lambda: self.editconf('user', self.userTest.text()))

        # 设置本地同步目录
        self.synTest.setText(str(self.setlocale.syn))
        self.synTest.textChanged.connect(
            lambda: self.editConfZhongWen('syn', pathlib.Path(self.synTest.text())))

        # 设置服务器同步目录
        self.synSever.setText(str(self.setlocale.synSever))

        # 设置项目目录
        self.projectCombo.setCurrentText(str(self.setlocale.projectname))
        self.projectCombo.currentIndexChanged.connect(self.projecrEdit)

        # 设置同步集数
        self.synEp.setValue(self.setlocale.synEp)
        # 链接同步集数更改命令
        self.synEp.valueChanged.connect(self.editSynEp)

        # 设置同步软件安装目录
        self.freeFileSyncButton.setText(str(self.setlocale.FreeFileSync))

        # 设置同步目录显示
        self.synSeverPath()

        # 设置保存按钮命令
        self.save.triggered.connect(self.saveset)

    def editconf(self, key, newValue):
        # 当设置更改时获得更改
        # self.setlocale.setting[key] = newValue
        setattr(self.setlocale, key, newValue)
        self.ta_log_GUI.info('用户将%s更改为%s', key, newValue)
        self.synSeverPath()

    def synSeverPath(self):
        # 将同步目录显示出来
        self.pathSynSever.clear()
        self.pathSynLocale.clear()
        syn_sever_path = self.setlocale.getsever()
        try:
            for path in syn_sever_path:
                self.pathSynSever.addItem(path['Left'])
                self.pathSynLocale.addItem(path['Right'])
        except KeyError:
            self.pathSynSever.clear()
            self.pathSynLocale.clear()
        except:
            pass

    def editConfZhongWen(self, key, newValue: pathlib.Path):
        newValue = script.convert.isChinese(newValue)
        newValue = newValue.easyToEn()
        self.sysTestYing.setText(newValue.as_posix())
        self.ta_log_GUI.info('中文%s更改为%s', key, newValue)
        setattr(self.setlocale, key, newValue.as_posix())
        self.synSeverPath()

    def editSynEp(self):
        self.setlocale.synEp = int(self.synEp.value())
        self.synSeverPath()

    def saveset(self):
        # 保存到文档的设置文件中
        self.ta_log_GUI.info('设置保存')
        self.setlocale.writeDoodlelocalSet()

    def projecrEdit(self, index):
        self.setlocale.projectname = self.projectCombo.itemText(index)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = DoodlesettingGUI()

    w.show()

    sys.exit(app.exec_())
