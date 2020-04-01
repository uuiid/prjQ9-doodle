# -*- coding: UTF-8 -*-
import codecs
import json
import pathlib
import sys

from PyQt5 import QtWidgets

import UiFile.setting
import script.convert


class Doodlesetting():
    _setting = {}
    doc = pathlib.Path("{}{}".format(pathlib.Path.home(), '\\Documents\\doodle'))
    userland = doc.joinpath("doodle_conf.json")

    def __init__(self):
        # 初始化设置

        self.setting = {"user": '未记录',
                         "department": '未记录',
                         "syn": "D:\\ue_prj",
                         "synSever": "W:\\data\\ue_prj",
                         "project": "W:\\",
                         'FreeFileSync': 'C:\\PROGRA~1\\FREEFI~1\\FreeFileSync.exe'}

        self.doc = pathlib.Path("{}{}".format(pathlib.Path.home(), '\\Documents\\doodle'))
        self.userland = self.doc.joinpath("doodle_conf.json")
        self.setting = self.getString()

    @property
    def setting(self):
        return Doodlesetting._setting

    @setting.setter
    def setting(self, settmp: dict):
        Doodlesetting._setting = settmp

    def getString(self):
        if not self.doc.is_dir():
            # 没有目录时创建目录
            self.doc.mkdir()
        if not self.userland.is_file():
            # 具有目录没有文件时创建文件
            f = codecs.open(self.userland, mode='w', encoding='utf-8')
            f.write("")
            json.dump(self.setting, f, ensure_ascii=False)
            f.close()
        if not self.userland.stat().st_size:
            # 文件为空时写入默认
            with codecs.open(self.userland, mode='w', encoding='utf-8') as f:
                json.dump(self.setting, f, ensure_ascii=False)

        try:
            # 尝试文件读取
            with codecs.open(self.userland, mode='r', encoding='utf-8') as f:
                for key, value in json.load(f).items():
                    # 将文件中有的设置加载进来,  为以后更新做准备
                    self.setting[key] = value
        except:
            with codecs.open(self.userland, mode='w', encoding='utf-8') as f:
                # 否则把文件写空
                f.write('')
        return self.setting


class DoodlesettingGUI(QtWidgets.QMainWindow, UiFile.setting.Ui_MainWindow, Doodlesetting):

    def __init__(self, parent=None):
        super(DoodlesettingGUI, self).__init__()
        Doodlesetting.__init__(self)
        QtWidgets.QMainWindow.__init__(self, parent=parent)
        self.setupUi(self)

        # 设置部门显示
        self.DepartmentTest.setCurrentText(self.setting['department'])
        self.DepartmentTest.currentIndexChanged.connect(lambda: self.editconf('department',
                                                                              self.DepartmentTest.currentText()))
        # 设置人员名称
        self.userTest.setText(self.setting['user'])
        self.userTest.textChanged.connect(lambda: self.editconf('user', self.userTest.text()))

        # 设置本地同步目录
        self.synTest.setText(self.setting['syn'])
        self.synTest.textChanged.connect(
            lambda: self.editConfZhongWen('syn', pathlib.PurePath(self.synTest.text())))

        # 设置服务器同步目录
        self.synSever.setText(self.setting['synSever'])

        # 设置项目目录

        # 设置同步软件安装目录
        self.freeFileSyncButton.setText(self.setting['FreeFileSync'])

        # 设置保存按钮命令
        self.save.triggered.connect(self.saveset)

    def editconf(self, key, newValue):
        # 当设置更改时获得更改

        self.setting[key] = newValue

    def editConfZhongWen(self, key, newValue: pathlib.Path):
        # 有中文时调取这个更改转为拼音

        if script.convert.isChinese(newValue):
            newValue = script.convert.convertToEn(newValue)
        self.sysTestYing.setText(newValue.as_posix())
        self.setting[key] = newValue.as_posix()

    def saveset(self):
        # 保存到文档的设置文件中
        self.setting = json.dumps(self.setting, ensure_ascii=False, indent=4, separators=(',', ':'))
        self.userland.write_text(self.setting, 'utf-8')


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = DoodlesettingGUI()
    w.show()

    sys.exit(app.exec_())
