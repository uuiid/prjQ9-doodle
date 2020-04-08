# -*- coding: UTF-8 -*-
import os
import pathlib
import shutil
import sys
from typing import Dict

import pyperclip
import pypinyin
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets

import UiFile.ProjectBrowser
import script.convert
import script.debug
import script.doodle_setting
import script.readServerDiectory
import script.ProjectAnalysis.PathAnalysis


class ProjectBrowserGUI(QtWidgets.QMainWindow, UiFile.ProjectBrowser.Ui_MainWindow):
    file_version: int = 0
    file_path: pathlib.Path = ''
    file_episods: str = ''
    file_shot: str = ''
    file_department: str = ''
    file_type: str = ''
    root: pathlib.Path
    projectAnalysis: script.ProjectAnalysis.PathAnalysis

    def __init__(self, parent=None):
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
        # self.listepisodes.setAcceptDrops

        '''添加右键菜单==================================================='''
        # 添加集数右键菜单
        self.listepisodes.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)

        add_episodes_Folder = QtWidgets.QAction('添加', self)
        add_episodes_Folder.triggered.connect(self.addEpisodesFolder)
        self.listepisodes.addAction(add_episodes_Folder)
        # 添加镜头右键菜单
        self.listshot.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        add_shot_Folder = QtWidgets.QAction('添加', self)
        add_shot_Folder.triggered.connect(self.addShotFolder)
        add_ABshot_Folder = QtWidgets.QAction('添加AB镜', self)
        add_ABshot_Folder.triggered.connect(self.addABshotFolder)
        self.listshot.addAction(add_ABshot_Folder)
        self.listshot.addAction(add_shot_Folder)
        # 添加部门右键菜单
        self.listdepartment.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        add_department = QtWidgets.QAction('添加', self)
        add_department.triggered.connect(self.addDepartmentFolder)
        self.listdepartment.addAction(add_department)
        # 添加类型右键菜单
        self.listdepType.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        add_depType = QtWidgets.QAction('添加', self)
        add_depType.triggered.connect(self.addTypeFolder)
        self.listdepType.addAction(add_depType)

        # 添加文件右键菜单
        self.listfile.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        # 用文件管理器打开文件位置
        open_explorer = QtWidgets.QAction('打开文件管理器', self)
        open_explorer.triggered.connect(self.openExplorer)
        self.listfile.addAction(open_explorer)

        # copy文件名称或者路径到剪切板
        copy_name_to_clip = QtWidgets.QAction('复制名称', self)
        copy_name_to_clip.triggered.connect(self.copyNameToClipboard)
        copy_path_to_clip = QtWidgets.QAction('复制路径', self)
        copy_path_to_clip.triggered.connect(self.copyPathToClipboard)
        self.listfile.addAction(copy_path_to_clip)
        self.listfile.addAction(copy_name_to_clip)
        '''================================================================='''
        # 首先扫描根目录获得集数
        self.listepisodes.addItems(self.getepisodes())
        # 并链接函数处理下一级
        self.listepisodes.itemClicked.connect(self.setShotItem)
        # 在shot文件列表中添加点击事件更改下一级部门列表
        self.listshot.itemClicked.connect(self.setDepartment)
        # 在department中添加下一级的更新事件
        self.listdepartment.itemClicked.connect(self.setdepType)
        # 在类型中添加文件跟新时间

        # 双击打开文件
        self.listfile.doubleClicked.connect(self.openFile)

        self.listdepType.itemClicked.connect(self.setFile)

        # 添加刷新函数
        self.refresh.triggered.connect(self.setepisodex)

    def getRoot(self) -> pathlib.Path:
        # 获得项目目录
        shot_root_ = self.setSour.getseverPrjBrowser()['shotRoot']
        root = pathlib.Path(self.setlocale.setting['project'])
        # 获得根目录
        for myP in shot_root_:
            root = root.joinpath(myP)
        self.root = root
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

    def setepisodex(self):
        self.listepisodes.clear()
        self.listdepartment.clear()
        self.listdepType.clear()
        self.clearListFile()
        self.listshot.clear()

        self.listepisodes.addItems(self.getepisodes())
        # print('ok')

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
                # 获得文件路径并进行复制
                if path.suffix in ['.ma', '.mb', '.fbx', '.hip', '.usd']:
                    # 为防止在没有选择的情况下复制到不知道的位置所以先进行路径测试
                    if self.listdepType and self.getFile():
                        dstFile = self.getFileName(path.suffix)  # type:pathlib.Path
                        shutil.copy2(str(path), str(dstFile))
                        # print(self.getFileName(path.suffix))
                        # print(str(self.getFile()))
                        script.debug.debug('{} ---> {}'.format(str(path), str(dstFile)))
                        self.setFile()
                    self.enableBorder(False)
                    # print(path)
            else:
                pass
        else:
            a0.ignore()

    def getFileName(self, Suffixes: str):
        # 获得本地设置中的制作人名称
        user_ = pypinyin.slug(self.setlocale.setting['user'], pypinyin.NORMAL)
        # 将版本加一复制为新版本
        self.file_version = self.file_version + 1
        # 格式化文件名称和路径
        path = self.file_path.joinpath('shot_{}-{}_{}_{}_v{:0>4d}__{}_{}'.format(self.file_episods,
                                                                                 self.file_shot,
                                                                                 self.file_department,
                                                                                 self.file_type,
                                                                                 self.file_version,
                                                                                 user_,
                                                                                 Suffixes))
        return path

    def addEpisodesFolder(self):
        Episode = QtWidgets.QInputDialog.getInt(self, '输入集数', "ep", 1, 1, 999, 1)[0]
        if Episode:
            root = self.getRoot()
            episodesPath = root.joinpath("ep{:0>2d}".format(Episode))
            if not episodesPath.is_dir():
                episodesPath.mkdir(parents=True, exist_ok=True)
                self.setepisodex()

    def addShotFolder(self):
        shot = QtWidgets.QInputDialog.getInt(self, '输入镜头', "sc", 1, 1, 999, 1)[0]
        if shot:
            if self.listepisodes.selectedItems():
                shotname = '{}-sc{:0>4d}'.format(self.file_episods, shot)
                self.generateShotFolder(shotname, None)

    def generateShotFolder(self, shot, ABshot=None):
        """这个函数负责生成shot文件夹名称并并创建"""
        root = self.getRoot()
        if ABshot:
            shot = '{}{}'.format(shot, ABshot)
        shot = root.joinpath(shot)
        if not shot.is_dir():
            shot.mkdir(parents=True, exist_ok=True)
            self.setShotItem(self.listepisodes.selectedItems()[0])
            for sub_directory in ['Export', 'Playblasts', 'Rendering', 'Scenefiles']:
                sub_dir: pathlib.Path = shot.joinpath(sub_directory)
                sub_dir.mkdir(parents=True, exist_ok=True)

    def addDepartmentFolder(self):
        department = self.setlocale.setting['department']
        if self.listshot.selectedItems():
            shot_Department = self.getdepartment()
            department = shot_Department.joinpath(department)
            if not department.is_dir():
                department.mkdir(parents=True, exist_ok=True)
                self.setDepartment()

    def addTypeFolder(self):
        deptype = QtWidgets.QInputDialog.getText(self, '输入镜头', "文件类型(请用英文或拼音)",
                                                 QtWidgets.QLineEdit.Normal)[0]
        if deptype:
            if self.listdepartment.selectedItems():
                department_type = self.getdepType()
                deptype = department_type.joinpath(deptype)
                if not script.convert.isChinese(deptype):
                    if not deptype.is_dir():
                        deptype.mkdir(parents=True, exist_ok=True)
                        self.setdepType()

    def openFile(self):
        filepath = self.combinationFilePath()
        # subprocess.Popen(str(filepath))
        try:
            os.startfile(str(filepath))
        except:
            pass

    def combinationFilePath(self):
        # 这个用来组合文件和文件命
        filename = self.combinationFileName()
        filepath = self.file_path.joinpath(filename)
        return filepath

    def combinationFileName(self):
        # 这个用来组合文件名称
        indexs = self.listfile.selectedItems()
        item: Dict[str, str] = {}
        item['version'] = indexs[0].text()
        if len(indexs) == 4:
            item['user'] = indexs[2].text()
            item['fileSuffixes'] = indexs[3].text()
        else:
            item['user'] = indexs[1].text()
            item['fileSuffixes'] = indexs[2].text()
        filename = 'shot_{}-{}_{}_{}_{}__{}_{}'.format(self.file_episods,
                                                       self.file_shot,
                                                       self.file_department,
                                                       self.file_type,
                                                       item['version'],
                                                       item['user'],
                                                       item['fileSuffixes'])
        return filename

    def addABshotFolder(self):
        items = ['B', 'C', 'D', 'E']
        shotAB = QtWidgets.QInputDialog.getItem(self, '选择AB镜头', '要先选择镜头才可以', items, 0, False)
        if shotAB:
            if self.listshot.selectedItems() and self.file_shot:
                shotname = '{}-{}'.format(self.file_episods, self.file_shot)
                self.generateShotFolder(shotname, shotAB[0])

    def openExplorer(self):
        filePath = self.file_path
        os.startfile(filePath)

    def copyNameToClipboard(self):
        pyperclip.copy(str(self.combinationFileName()))

    def copyPathToClipboard(self):
        pyperclip.copy(str(self.file_path))


# 添加右键菜单
# def contextMenuEvent(self, event: QtGui.QContextMenuEvent) -> None:
#     menu = QtWidgets.QMenu(self)
#     addFolder = menu.addAction('添加')
#     addFolder.triggered.connect(self.addFolder)
#     action = menu.exec_(self.mapToGlobal(event.pos()))


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = ProjectBrowserGUI()
    w.show()

    sys.exit(app.exec_())
