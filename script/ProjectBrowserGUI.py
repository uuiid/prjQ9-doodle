# -*- coding: UTF-8 -*-
import pathlib
import sys

from PyQt5 import QtWidgets

import UiFile.ProjectBrowser
import script.doodle_setting
import script.readServerDiectory


class ProjectBrowserGUI(QtWidgets.QMainWindow, UiFile.ProjectBrowser.Ui_MainWindow):
    def __init__(self):
        super(ProjectBrowserGUI, self).__init__()
        self.setlocale = script.doodle_setting.Doodlesetting()
        self.setSour = script.readServerDiectory.SeverSetting()
        self.setupUi(self)
        # 首先扫描根目录获得集数
        self.listepisodes.addItems(self.getepisodes())
        # 并链接函数处理下一级
        self.listepisodes.itemClicked.connect(self.getshot)
        self.listdepartment.itemClicked.connect(self.getdepartment)

    def getepisodes(self):
        '''获得集数'''
        shot_root_ = self.setSour.getseverPrjBrowser()['shotRoot']
        root = pathlib.Path(self.setlocale.setting['project'])

        for myP in shot_root_:
            root = root.joinpath(myP)

        item = []
        for path in root.iterdir():
            if path.is_dir():
                item.append(path.stem.split('-')[0])
        item = list(set(item))
        item.sort()
        return item

    def getshot(self, item: QtWidgets.QLabel):
        '''获得shot镜头'''
        shot_root_ = self.setSour.getseverPrjBrowser()['shotRoot']
        root = pathlib.Path(self.setlocale.setting['project'])

        for myP in shot_root_:
            root = root.joinpath(myP)
        mitem = []
        for path in root.iterdir():
            test = path
            # if path.match('ep01*'):
            if path.match('{}*'.format(item.text())):
                try:
                    mitem.append(path.stem.split('-')[1])
                except:
                    pass
        mitem = list(set(mitem))
        mitem.sort()
        mitem = filter(None,mitem)
        self.listshot.clear()
        self.listdepartment.clear()
        self.listdepType.clear()
        self.listfile.clear()
        self.listshot.addItems(mitem)
        return mitem

    def getdepartment(self):
        '''获得部门文件夹'''
        pass


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = ProjectBrowserGUI()
    w.show()

    sys.exit(app.exec_())
