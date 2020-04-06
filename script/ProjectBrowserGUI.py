# -*- coding: UTF-8 -*-
import pathlib
import sys
import shutil
import pypinyin

from PyQt5 import QtWidgets
from PyQt5 import QtGui

import UiFile.ProjectBrowser
import script.doodle_setting
import script.readServerDiectory
import script.convert


class ProjectBrowserGUI(QtWidgets.QMainWindow, UiFile.ProjectBrowser.Ui_MainWindow):
    file_version: int = 0
    file_path: pathlib.Path = ''
    file_episods: str = ''
    file_shot: str = ''
    file_department: str = ''
    file_type: str = ''

    def __init__(self):
        super(ProjectBrowserGUI, self).__init__()
        self.setlocale = script.doodle_setting.Doodlesetting()
        self.setSour = script.readServerDiectory.SeverSetting()
        # 设置UI
        self.setupUi(self)
        # 设置最后的文件编辑器的一些标准动作
        # 设置每行选择
        self.listfile.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        # 设置单选
        self.listfile.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        # 设置注释最大
        self.listfile.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        # 设置不可编辑
        self.listfile.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        # 开启窗口拖拽事件
        self.setAcceptDrops(True)
        # self.listepisodes.setAcceptDrops(False)

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

        try:
            self.file_episods = self.listepisodes.selectedItems()[0].text()
        finally:
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
            self.clearListFile()

            self.listshot.clear()
            self.listshot.addItems(mitem)

    def getdepartment(self) -> pathlib.Path:
        '''获得部门文件夹'''
        # 获得根文件夹
        root = self.getshot(self.listshot.selectedItems())
        try:
            # 获得集数
            epis = self.listepisodes.selectedItems()[0].text()
            # 获得镜头号
            shot = self.listshot.selectedItems()[0].text()
        except:
            department = ''
        else:
            # 获得部门文件夹
            department = root.joinpath('{}-{}'.format(epis, shot))
            department = department.joinpath('Scenefiles')

        # 添加部门文件夹

        return department

    def setDepartment(self):
        try:
            self.file_shot = self.listshot.selectedItems()[0].text()
        finally:
            department = self.getdepartment()
            if department:
                mitem = []
                for mi in department.iterdir():
                    mitem.append(mi.stem)

                self.listdepType.clear()
                self.clearListFile()

                self.listdepartment.clear()
                self.listdepartment.addItems(mitem)

    def getdepType(self, ):
        dep = self.getdepartment()
        if dep:
            # department = item.text()
            department = self.listdepartment.selectedItems()[0].text()
            dep = dep.joinpath(department)

        return dep

    def setdepType(self):
        try:
            self.file_department = self.listdepartment.selectedItems()[0].text()
        finally:
            dep = self.getdepType()
            mitem = []
            if dep.iterdir():
                for mi in dep.iterdir():
                    if mi.is_dir():
                        mitem.append(mi.stem)
            else:
                return dep

            self.clearListFile()

            self.listdepType.clear()
            self.listdepType.addItems(mitem)

    def getFile(self):
        try:
            depType = self.getdepType()
            depType = depType.joinpath(self.listdepType.selectedItems()[0].text())
        except:
            depType = ''

        return depType

    def setFile(self):
        '''设置文件在GUI中的显示'''
        # 清空上一次文件显示和版本记录和文件路径
        self.clearListFile()
        self.file_version = 0
        self.file_path = ''
        try:
            self.file_type = self.listdepType.selectedItems()[0].text()
        finally:
            # 获得文件路径
            file_paths = self.getFile()
            self.file_path = file_paths
            dep_type_iterdir = file_paths.iterdir()
            mitem = []
            if dep_type_iterdir:
                for mFile in dep_type_iterdir:
                    if mFile.is_file():
                        mitem.append({'filename': mFile.stem, 'fileSuffixes': mFile.suffix})
            else:
                return None
            # 迭代获得文件命中包含信息
            if mitem:
                mrow = 0
                for file in mitem:
                    tmp = file['filename'].split('_')
                    try:
                        tmp = {'Type': tmp[0],
                               'epShot': tmp[1],
                               'department': tmp[2],
                               'depType': tmp[3],
                               'version': tmp[4],
                               'producer': tmp[6],
                               'fileSuffixes': file['fileSuffixes']
                               }
                    except IndexError:
                        other = tmp
                    except:
                        pass
                    else:
                        tmp_version_ = int(tmp['version'][1:])
                        if tmp_version_ > self.file_version:
                            self.file_version = tmp_version_
                        self.listfile.insertRow(mrow)
                        # version = QtWidgets.QTableWidgetItem(tmp['version'])
                        # version.setFlags(QtWidgets.Item)
                        self.listfile.setItem(mrow, 0, QtWidgets.QTableWidgetItem(tmp['version']))
                        self.listfile.setItem(mrow, 2, QtWidgets.QTableWidgetItem(tmp['producer']))
                        self.listfile.setItem(mrow, 3, QtWidgets.QTableWidgetItem(tmp['fileSuffixes']))
                        # self.listfile.setSortingEnabled(True)
                        # self.listfile.lin
                        mrow = mrow + 1

    def clearListFile(self):
        mrowtmp = self.listfile.rowCount()
        while mrowtmp >= 0:
            self.listfile.removeRow(mrowtmp)
            mrowtmp = mrowtmp - 1

    def targetPath(self):
        ep = self.listepisodes.selectedItems()[0].text()
        shot = self.listshot.selectedItems()[0].text()
        department = self.listdepartment.selectedItems()[0].text()
        depType = self.listdepType.selectedItems()[0].text()
        producer = self.setlocale.setting['user']

        item = self.listfile.item(self.listfile.rowCount(), 0)
        version = int(item.text()[1:])
        version = version + 1
        depType.joinpath('shot_ep01-sc0001_anm_Animation_v0002__xnn_')

    def enableBorder(self, enable):
        if enable:
            # self.setStyleSheet("MainWidget{border:3px solid green}")
            self.listfile.setStyleSheet("border:3px solid #165E23")
        else:
            self.listfile.setStyleSheet('')

    def dragEnterEvent(self, a0: QtGui.QDragEnterEvent) -> None:
        if a0.mimeData().hasUrls():
            a0.acceptProposedAction()
            self.enableBorder(True)
        else:
            a0.ignore()

    def dragLeaveEvent(self, a0: QtGui.QDragLeaveEvent) -> None:
        # 离开时取消高亮
        print('dragLeaveEvent...')
        self.enableBorder(False)

    def dropEvent(self, a0: QtGui.QDropEvent) -> None:
        if a0.mimeData().hasUrls():
            # 检测文件路劲和类型,限制拖动
            if len(a0.mimeData().urls()) == 1:
                url = a0.mimeData().urls()[0]
                path = pathlib.Path(url.toLocalFile())
                if path.suffix in ['.ma', '.mb', '.fbx', '.hip', '.usd']:
                    if self.listdepType and self.getFile():
                        print(self.getFileName(path.suffix))
                        print(str(self.getFile()))
                    self.enableBorder(False)
                    print(path)
            else:
                pass
        else:
            a0.ignore()

    def getFileName(self, Suffixes: str):

        user_ =pypinyin.slug(self.setlocale.setting['user'],pypinyin.NORMAL)
        path = self.file_path.joinpath('shot_{}-{}_{}_{}_v{:0>4d}__{}_{}'.format(self.file_episods,
                                                                                 self.file_shot,
                                                                                 self.file_department,
                                                                                 self.file_type,
                                                                                 self.file_version,
                                                                                 user_,
                                                                                 Suffixes))
        return path


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = ProjectBrowserGUI()
    w.show()

    sys.exit(app.exec_())
