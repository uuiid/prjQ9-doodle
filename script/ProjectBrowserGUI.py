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
        self.listepisodes.itemClicked.connect(self.setShotItem)
        # 在shot文件列表中添加点击事件更改下一级部门列表
        self.listshot.itemClicked.connect(self.setDepartment)
        # 在department中添加下一级的更新事件
        self.listdepartment.itemClicked.connect(self.setdepType)
        # 在类型中添加文件跟新时间
        self.listdepType.itemClicked.connect(self.setFile)

        self.listfile.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.listfile.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)

    def getRoot(self) -> pathlib.Path:
        # 获得项目目录
        shot_root_ = self.setSour.getseverPrjBrowser()['shotRoot']
        root = pathlib.Path(self.setlocale.setting['project'])
        # 获得根目录
        for myP in shot_root_:
            root = root.joinpath(myP)
        return root

    def getepisodes(self):
        '''获得集数'''
        root = self.getRoot()

        item = []
        for path in root.iterdir():
            if path.is_dir():
                item.append(path.stem.split('-')[0])
        item = list(set(item))
        item.sort()
        return item

    def getshot(self, item: QtWidgets.QListWidgetItem):
        '''获得shot镜头'''
        root = self.getRoot()
        shot = root

        return shot

    def setShotItem(self, item: QtWidgets.QListWidgetItem):

        root = self.getshot(item)
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
        mitem = filter(None, mitem)

        self.listdepartment.clear()
        self.listdepType.clear()
        self.listfile.clearContents()

        self.listshot.clear()
        self.listshot.addItems(mitem)

    def getdepartment(self) -> pathlib.Path:
        '''获得部门文件夹'''
        # 获得根文件夹
        root = self.getshot(self.listshot.selectedItems())
        # 获得集数
        epis = self.listepisodes.selectedItems()[0].text()
        # 获得镜头号
        shot = self.listshot.selectedItems()[0].text()
        # 获得部门文件夹
        department = root.joinpath('{}-{}'.format(epis, shot))
        department = department.joinpath('Scenefiles')
        # 添加部门文件夹

        return department

    def setDepartment(self):
        department = self.getdepartment()
        mitem = []
        for mi in department.iterdir():
            mitem.append(mi.stem)

        self.listdepType.clear()
        self.listfile.clearContents()

        self.listdepartment.clear()
        self.listdepartment.addItems(mitem)

    def getdepType(self, ):
        dep = self.getdepartment()
        # department = item.text()
        department = self.listdepartment.selectedItems()[0].text()
        dep = dep.joinpath(department)

        return dep

    def setdepType(self):
        dep = self.getdepType()
        mitem = []
        if dep.iterdir():
            for mi in dep.iterdir():
                if mi.is_dir():
                    mitem.append(mi.stem)
        else:
            return dep

        self.listfile.clearContents()

        self.listdepType.clear()
        self.listdepType.addItems(mitem)

    def getFile(self):
        depType = self.getdepType()
        depType = depType.joinpath(self.listdepType.selectedItems()[0].text())
        dep_type_iterdir = depType.iterdir()

        mitem = []
        if dep_type_iterdir:
            for mFile in dep_type_iterdir:
                if mFile.is_file():
                    mitem.append(mFile.stem)
        else:
            return None
        return mitem

    def setFile(self):
        filePaths = self.getFile()
        ifto = []
        for file in filePaths:
            tmp = file.split('_')
            ifto.append({'Type': tmp[0],
                         'epShot': tmp[1],
                         'department': tmp[2],
                         'depType': tmp[3],
                         'version': tmp[4],
                         'producer': tmp[6]})

        return ifto


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = ProjectBrowserGUI()
    w.show()

    sys.exit(app.exec_())
