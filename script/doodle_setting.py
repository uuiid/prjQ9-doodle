# -*- coding: UTF-8 -*-
import codecs
import json
import pathlib
import sys
import threading
from PyQt5 import QtWidgets

import UiFile.setting
import script.convert
import script.readServerDiectory
import script.doodleLog


class Doodlesetting():
    _setting = {}
    _instance_lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not hasattr(Doodlesetting, '_instance'):
            with Doodlesetting._instance_lock:
                if not hasattr(Doodlesetting, '_instance'):
                    Doodlesetting._instance = object.__new__(cls)
        return Doodlesetting._instance

    def __init__(self) -> object:
        # 初始化设置
        # self.doc = pathlib.Path("{}{}".format(pathlib.Path.home(), '\\Documents\\doodle'))
        # self.userland = self.doc.joinpath("doodle_conf.json")
        self.ta_log = script.doodleLog.get_logger(__name__)
        self.initSetAttr()

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
    def setting(self) -> str:
        if not hasattr(self, '_setting'):
            self._setting = {"user": '未记录',
                             "department": '未记录',
                             "syn": "D:\\ue_prj",
                             "synEp": 1,
                             "synSever": "W:\\data\\ue_prj",
                             "project": "W:\\",
                             'FreeFileSync': 'C:\\PROGRA~1\\FREEFI~1\\FreeFileSync.exe'}
        return Doodlesetting._setting

    @setting.setter
    def setting(self, settmp: dict) -> str:
        Doodlesetting._setting = settmp

    @property
    def user(self) -> str:
        if not hasattr(self, '_user'):
            self._user = '未记录'
        return self._user

    @user.setter
    def user(self, user: pathlib.Path):
        self._user = user

    @property
    def department(self) -> str:
        if not hasattr(self, '_department'):
            self._department = '未记录'
        return self._department

    @department.setter
    def department(self, department: str) -> str:
        self._department = department

    @property
    def syn(self) -> pathlib.Path:
        if not hasattr(self, '_syn'):
            self._syn = 'D:\\ue_prj'
        return self._syn

    @syn.setter
    def syn(self, syn: pathlib.Path) -> pathlib.Path:
        self._syn =pathlib.Path(syn)

    @property
    def synEp(self) -> int:
        if not hasattr(self, '_synEp'):
            self._synEp = 1
        return self._synEp

    @synEp.setter
    def synEp(self, synEp: int):
        self._synEp = synEp

    @property
    def synSever(self) -> pathlib.Path:
        if not hasattr(self, '_synSever'):
            self._syn_sever = 'W:\\data\\ue_prj'
        return self._syn_sever

    @synSever.setter
    def synSever(self, syn_sever: pathlib.Path):
        if isinstance(syn_sever,str):
            self._syn_sever = pathlib.Path(syn_sever)
        else:
            self._syn_sever = syn_sever

    @property
    def project(self) -> pathlib.Path:
        if not hasattr(self, '_project'):
            self._project = 'W:\\'
        return self._project

    @project.setter
    def project(self, project:pathlib.Path):
        if isinstance(project,str):
            self.project = pathlib.Path(project)
        else:
            self._project = project

    # region 同步软件所在目录
    @property
    def FreeFileSync(self) -> pathlib.Path:
        if not hasattr(self, '_FreeFileSync'):
            self._FreeFileSync = 'C:\\PROGRA~1\\FREEFI~1\\FreeFileSync.exe'
        return self._FreeFileSync

    @FreeFileSync.setter
    def FreeFileSync(self, FreeFileSync):
        self._FreeFileSync =pathlib.Path(FreeFileSync)

    # endregion

    # </editor-fold>

    def initSetAttr(self):
        setDict = self.getString()
        for key, value in setDict.items():
            setattr(self, key, value)

    def getString(self) -> dict:
        if not self.doc.is_dir():
            self.ta_log.info('没有 %s 目录,-->创建', self.doc)
            # 没有目录时创建目录
            self.doc.mkdir()
        if not self.userland.is_file():
            # 具有目录没有文件时创建文件
            self.userland.touch(exist_ok=True)
            self.writeDoodlelocalSet()

            self.ta_log.info('没有 %s 文件,-->写入', self.userland)
        if not self.userland.stat().st_size:
            # 文件为空时写入默认
            self.writeDoodlelocalSet()

            self.ta_log.info('文件 %s 为空时,-->写入', self.userland)
        itoa = ''
        try:
            self.ta_log.info('尝试读取文件')
            itoa = self.userland.read_text(encoding='utf-8')
            itoa = json.loads(itoa)
        except:
            self.writeDoodlelocalSet()
            self.ta_log.info('读入失败,  写空文件')
        return itoa

    def writeDoodlelocalSet(self):
        doodlelocal_set: dict = {
            'user': self.user,
            'department': self.department,
            "syn": str(self.syn),
            "synEp": self.synEp,
            "synSever": str(self.synSever),
            "project": str(self.project),
            "FreeFileSync": str(self.FreeFileSync)
        }
        my_setting = json.dumps(doodlelocal_set, ensure_ascii=False, indent=4, separators=(',', ':'))
        self.userland.write_text(my_setting, 'utf-8')


class DoodlesettingGUI(QtWidgets.QMainWindow, UiFile.setting.Ui_MainWindow):
    sever_setting = ''
    setlocale: Doodlesetting

    def __init__(self, parent=None):
        super(DoodlesettingGUI, self).__init__()
        QtWidgets.QMainWindow.__init__(self, parent=parent)
        self.setlocale = Doodlesetting()
        self.sever_setting = script.readServerDiectory.SeverSetting()
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
            lambda: self.editConfZhongWen('syn', pathlib.PurePath(self.synTest.text())))

        # 设置服务器同步目录
        self.synSever.setText(str(self.setlocale.synSever))

        # 设置项目目录
        self.projectTest.setText(str(self.setlocale.project))
        self.projectTest.textChanged.connect(self.projecrEdit)

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
        setattr(self.setlocale,key,newValue)
        self.ta_log_GUI.info('用户将%s更改为%s',key,newValue)
        self.synSeverPath()

    def synSeverPath(self):
        # 将同步目录显示出来
        self.pathSynSever.clear()
        self.pathSynLocale.clear()
        syn_sever_path = self.sever_setting.getsever()
        try:
            syn_sever_path = syn_sever_path['ep{:0>3d}Syn'.format(self.setlocale.synEp)]
            for path in syn_sever_path:
                self.pathSynSever.addItem(path['Left'])
                self.pathSynLocale.addItem(path['Right'])
        except KeyError:
            self.pathSynSever.clear()
            self.pathSynLocale.clear()
        except:
            pass

    def editConfZhongWen(self, key, newValue: pathlib.Path):
        # 有中文时调取这个更改转为拼音
        if script.convert.isChinese(newValue):
            newValue = script.convert.convertToEn(newValue)
        else:
            newValue = newValue
        self.sysTestYing.setText(newValue.as_posix())
        self.ta_log_GUI.info('中文%s更改为%s', key, newValue)
        setattr(self.setlocale,key,newValue.as_posix())
        self.synSeverPath()

    def editSynEp(self):
        self.setlocale.synEp = self.synEp.value()
        self.synSeverPath()

    def saveset(self):
        # 保存到文档的设置文件中
        self.ta_log_GUI.info('设置保存')
        self.setlocale.writeDoodlelocalSet()

    def projecrEdit(self):
        self.setlocale.project = self.projectTest.text()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = DoodlesettingGUI()

    w.show()

    sys.exit(app.exec_())
