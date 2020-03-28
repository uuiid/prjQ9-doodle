# -*- coding: UTF-8 -*-
import codecs
import os
import sys

from PyQt5 import QtWidgets, QtGui
import script.setting
import json
import pathlib
import script.convert


class Doodlesetting():
    setting = {}
    doc = pathlib.Path("{}{}".format(pathlib.Path.home(), '\\Documents\\doodle'))
    userland = doc.joinpath("doodle_conf.json")

    def __init__(self):

        self.setting = {"user": '未记录',
                        "department": '未记录',
                        "syn": "D:\\ue_prj",
                        'FreeFileSync': 'C:\\PROGRA~1\\FREEFI~1\\FreeFileSync.exe'}

        self.doc = pathlib.Path("{}{}".format(pathlib.Path.home(), '\\Documents\\doodle'))
        self.userland = self.doc.joinpath("doodle_conf.json")
        self.setting = self.getString()

    def getString(self):
        if not self.doc.is_dir():
            os.makedirs(doc)
        if not self.userland.is_file():
            f = codecs.open(self.userland, mode='w', encoding='utf-8')
            f.write("")
            json.dump(self.setting, f, ensure_ascii=False)
            f.close()
        if not self.userland.stat().st_size:
            with codecs.open(self.userland, mode='w', encoding='utf-8') as f:
                json.dump(self.setting, f, ensure_ascii=False)

        try:
            with codecs.open(self.userland, mode='r', encoding='utf-8') as f:
                for key, value in json.load(f).items():
                    self.setting[key] = value
        except:
            with codecs.open(self.userland, mode='w', encoding='utf-8') as f:
                f.write('')
        return self.setting


class DoodlesettingGUI(QtWidgets.QMainWindow, script.setting.Ui_MainWindow, Doodlesetting):

    def __init__(self):
        super(DoodlesettingGUI, self).__init__()
        Doodlesetting.__init__(self)
        QtWidgets.QMainWindow.__init__(self)
        self.setupUi(self)
        # if not self.doc.is_dir():
        #     os.makedirs(doc)
        # if not self.userland.is_file():
        #     f = codecs.open(self.userland, mode='w', encoding='utf-8')
        #     f.write("")
        #     json.dump(self.setting, f, ensure_ascii=False)
        #     f.close()
        # if not self.userland.stat().st_size:
        #     with codecs.open(self.userland, mode='w', encoding='utf-8') as f:
        #         json.dump(self.setting, f, ensure_ascii=False)
        #
        # try:
        #     with codecs.open(self.userland, mode='r', encoding='utf-8') as f:
        #         for key, value in json.load(f).items():
        #             self.setting[key] = value
        # except:
        #     with codecs.open(self.userland, mode='w', encoding='utf-8') as f:
        #         f.write('')

        self.DepartmentTest.setText(self.setting['department'])
        self.DepartmentTest.editingFinished.connect(lambda: self.editconf('department', self.DepartmentTest.text()))

        self.userTest.setText(self.setting['user'])
        self.userTest.editingFinished.connect(lambda: self.editconf('user', self.userTest.text()))

        self.synTest.setText(self.setting['syn'])
        self.synTest.editingFinished.connect(
            lambda: self.editConfZhongWen('syn', pathlib.PurePath(self.synTest.text())))

        self.freeFileSyncButton.setText(self.setting['FreeFileSync'])

        self.save.triggered.connect(self.saveset)

    def editconf(self, key, newValue):
        self.setting[key] = newValue

    def editConfZhongWen(self, key, newValue: pathlib.Path):
        if script.convert.isChinese(newValue):
            newValue = script.convert.convertToEn(newValue)
        self.sysTestYing.setText(newValue.as_posix())
        self.setting[key] = newValue.as_posix()

    def saveset(self):
        with codecs.open(self.userland, "w", 'utf-8') as f:
            json.dump(self.setting, f, ensure_ascii=False)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = DoodlesettingGUI()
    w.show()

    sys.exit(app.exec_())
