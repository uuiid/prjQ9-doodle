# -*- coding: UTF-8 -*-
import pathlib
import sys

from PySide2 import QtWidgets

import UiFile.setting
import script.DoodleLog
import DoodleServer


class DoodlesettingGUI(QtWidgets.QMainWindow, UiFile.setting.Ui_MainWindow):

    def __init__(self, parent=None):
        super(DoodlesettingGUI, self).__init__(parent=parent)
        self.setlocale = DoodleServer.Set.Doodlesetting()
        self.ta_log_GUI = script.DoodleLog.get_logger(__name__ + 'GUI')

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
        newValue = DoodleServer.DoodleZNCHConvert.isChinese(newValue).easyToEn()
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
