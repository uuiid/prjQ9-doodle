# -*- coding: UTF-8 -*-
import pathlib
import sys
import logging
from PySide2 import QtWidgets

import UiFile.setting
import DoodleServer
import script.DoodleCoreApp


class DoodlesettingGUI(QtWidgets.QMainWindow, UiFile.setting.Ui_MainWindow, script.DoodleCoreApp.core):

    def __init__(self, parent=None):
        super(DoodlesettingGUI, self).__init__(parent=parent)

        self.setupUi(self)
        # 设置部门显示
        self.DepartmentTest.setCurrentText(self.doodle_set.department)
        self.DepartmentTest.currentIndexChanged.connect(lambda: self.editconf('department',
                                                                              self.DepartmentTest.currentText()))
        # 设置人员名称
        self.userTest.setText(self.doodle_set.user)
        self.userTest.textChanged.connect(lambda: self.editconf('user', self.userTest.text()))

        # 设置本地同步目录
        self.synTest.setText(str(self.doodle_set.syn))
        self.synTest.textChanged.connect(
            lambda: self.editConfZhongWen('syn', pathlib.Path(self.synTest.text())))

        # 设置服务器同步目录
        self.synSever.setText(str(self.doodle_set.synSever))

        # 设置项目目录
        self.projectCombo.setCurrentText(str(self.doodle_set.projectname))
        self.projectCombo.currentIndexChanged.connect(self.projecrEdit)

        # 设置同步集数
        self.synEp.setValue(self.doodle_set.synEp)
        # 链接同步集数更改命令
        self.synEp.valueChanged.connect(self.editSynEp)

        # 设置同步软件安装目录
        self.freeFileSyncButton.setText(str(self.doodle_set.FreeFileSync))

        # 设置同步目录显示
        self.synSeverPath()

        # 设置保存按钮命令
        self.save.triggered.connect(self.saveset)

    def editconf(self, key, newValue):
        # 当设置更改时获得更改
        # self.doodle_set.setting[key] = newValue
        setattr(self.doodle_set, key, newValue)
        logging.info('用户将%s更改为%s', key, newValue)
        self.synSeverPath()

    def synSeverPath(self):
        # 将同步目录显示出来
        self.pathSynSever.clear()
        self.pathSynLocale.clear()
        syn_sever_path = self.doodle_set.getsever()
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
        newValue = DoodleServer.DoodleZNCHConvert.isChinese(newValue).easyToEn()
        self.sysTestYing.setText(newValue.as_posix())
        logging.info('中文%s更改为%s', key, newValue)
        setattr(self.doodle_set, key, newValue.as_posix())
        self.synSeverPath()

    def editSynEp(self):
        self.doodle_set.synEp = int(self.synEp.value())
        self.synSeverPath()

    def saveset(self):
        # 保存到文档的设置文件中
        logging.info('设置保存')
        self.doodle_set.writeDoodlelocalSet()
        self.doodle_set.__init__()

    def projecrEdit(self, index):
        self.doodle_set.projectname = self.projectCombo.itemText(index)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = DoodlesettingGUI()

    w.show()

    sys.exit(app.exec_())
