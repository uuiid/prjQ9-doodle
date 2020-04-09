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
    '''这个类用来实现项目管理的属性和UI操作,  其中会有一个项目分析器在外部, 有每个项目分别配置或者使用默认设置

    '''
    file_name: str
    file_version_max: int = 0
    file_path: pathlib.Path  # 文件所在文件夹

    file_episods: str = ''
    root: pathlib.Path  # 根文件夹,也就是集数所在文件夹

    file_shot: str = ''
    file_shot_path: pathlib.Path  # shot所在的文件夹

    file_department: str = ''
    file_department_path: pathlib.Path  # 部门所在的文件夹

    file_Deptype: str = ''
    file_Deptype_path: pathlib.Path  # 文件类型所在的文件夹

    projectAnalysis: script.ProjectAnalysis  # 路径解析器

    def __init__(self, parent=None):
        super(ProjectBrowserGUI, self).__init__()
        self.setlocale = script.doodle_setting.Doodlesetting()
        self.setSour = script.readServerDiectory.SeverSetting()
        self.projectAnalysis = script.ProjectAnalysis.PathAnalysis.DbxyProjectAnalysisShot()
        # 初始化一些属性
        # self.root = self.getRoot()
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

        self.addRightClick()
        # 首先扫描根目录获得集数
        self.listepisodes.addItems(self.projectAnalysis.getEpisodesItems(self))
        # 并链接函数处理下一级
        self.listepisodes.itemClicked.connect(self.setShotItem)
        # 在shot文件列表中添加点击事件更改下一级部门列表
        self.listshot.itemClicked.connect(self.setDepartment)
        # 在department中添加下一级的更新事件
        self.listdepartment.itemClicked.connect(self.setdepType)
        # 在depType中添加点击跟新文件事件
        self.listdepType.itemClicked.connect(self.setFile)

        # 双击打开文件
        self.listfile.doubleClicked.connect(self.openFile)
        # 添加刷新函数
        self.refresh.triggered.connect(self.setepisodex)

    # <editor-fold desc="集数和根目录的属性操作">
    @property
    def root(self) -> pathlib.Path:
        shot_root_ = self.setSour.getseverPrjBrowser()['shotRoot']
        root = pathlib.Path(self.setlocale.setting['project'])
        # 获得根目录
        for myP in shot_root_:
            root = root.joinpath(myP)
        # self.root = root
        return root

    @property
    def file_episods(self):
        try:
            return self.listepisodes.selectedItems()[0].text()
        except:
            return None

    # </editor-fold>

    # <editor-fold desc="关于shot的操作属性">
    @property
    def file_shot(self):
        try:
            return self.listshot.selectedItems()[0].text()
        except:
            return None

    @property
    def file_shot_path(self) -> pathlib.Path:
        try:
            return self.projectAnalysis.getShotPath(self)
        except:
            return None

    # </editor-fold>

    # <editor-fold desc="关于部门的操作">
    @property
    def file_department(self):
        try:
            return self.listdepartment.selectedItems()[0].text()
        except:
            return None

    @property
    def file_department_path(self):
        try:
            tmp = self.projectAnalysis.getdepartmentPath(self)
        except:
            tmp = None
        return tmp

    # </editor-fold>

    # <editor-fold desc="部门的下一个类型的操作">
    @property
    def file_Deptype(self):
        # return self.listdepType.selectedItems()[0].text()
        try:
            return self.listdepType.selectedItems()[0].text()
        except:
            return None

    @property
    def file_Deptype_path(self):
        # return self.projectAnalysis.getDepTypePath(self)
        try:
            return self.projectAnalysis.getDepTypePath(self)
        except:
            return None

    # </editor-fold>

    # <editor-fold desc="关于文件的操作">
    @property
    def file_path(self):
        try:
            return self.projectAnalysis.getFilePath(self)
        except:
            return None

    @property
    def file_name(self):
        try:
            filename = self.projectAnalysis.getFileName(self)
            return self.projectAnalysis.commFileName(filename)
        except:
            return None
    # </editor-fold>

    def addRightClick(self):
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

    def getRoot(self) -> pathlib.Path:
        # 获得项目目录
        shot_root_ = self.setSour.getseverPrjBrowser()['shotRoot']
        root = pathlib.Path(self.setlocale.setting['project'])
        # 获得根目录
        for myP in shot_root_:
            root = root.joinpath(myP)
        return root

    def setepisodex(self):
        self.listepisodes.clear()
        self.listdepartment.clear()
        self.listdepType.clear()
        self.clearListFile()
        self.listshot.clear()

        item = self.projectAnalysis.getEpisodesItems(self)
        self.listepisodes.addItems(item)

    def setShotItem(self):
        mitem = self.projectAnalysis.getShotItems(self)

        self.listdepartment.clear()
        self.listdepType.clear()
        self.clearListFile()

        self.listshot.clear()
        self.listshot.addItems(mitem)

    def setDepartment(self):
        department = self.file_department_path
        mitem  = self.projectAnalysis.getdepartmentItems(self)

        self.listdepType.clear()
        self.clearListFile()

        self.listdepartment.clear()
        self.listdepartment.addItems(mitem)

    def setdepType(self):
        mitem = self.projectAnalysis.getDepTypeItems(self)

        self.clearListFile()

        self.listdepType.clear()
        self.listdepType.addItems(mitem)

    def setFile(self):
        '''设置文件在GUI中的显示'''
        # 清空上一次文件显示和版本记录和文件路径
        self.clearListFile()
        self.file_version_max = 0
        for item in self.projectAnalysis.fileNameInformation(self):
            mrow = 0
            tmp_version_ = int(item['version'][1:])
            if tmp_version_ > self.file_version_max:
                self.file_version_max = tmp_version_
            self.listfile.insertRow(mrow)
            self.listfile.setItem(mrow, 0, QtWidgets.QTableWidgetItem(item['version']))
            self.listfile.setItem(mrow, 2, QtWidgets.QTableWidgetItem(item['producer']))
            self.listfile.setItem(mrow, 3, QtWidgets.QTableWidgetItem(item['fileSuffixes']))
            mrow = mrow + 1

    def clearListFile(self):
        mrowtmp = self.listfile.rowCount()
        while mrowtmp >= 0:
            self.listfile.removeRow(mrowtmp)
            mrowtmp = mrowtmp - 1

    # <editor-fold desc="拖放操作函数">
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
                    if self.listdepType and self.file_path:
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
        self.file_version_max = self.file_version_max + 1
        # 格式化文件名称和路径
        path = self.file_path.joinpath('shot_{}-{}_{}_{}_v{:0>4d}__{}_{}'.format(self.file_episods,
                                                                                 self.file_shot,
                                                                                 self.file_department,
                                                                                 self.file_Deptype,
                                                                                 self.file_version_max,
                                                                                 user_,
                                                                                 Suffixes))
        return path

    # </editor-fold>

    # <editor-fold desc="添加文件夹的操作都在这里">
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
        if self.file_shot:
            shot_Department = self.file_department_path
            department = shot_Department.joinpath(department)
            if not department.is_dir():
                department.mkdir(parents=True, exist_ok=True)
                self.setDepartment()

    def addTypeFolder(self):
        deptype = QtWidgets.QInputDialog.getText(self, '输入镜头', "文件类型(请用英文或拼音)",
                                                 QtWidgets.QLineEdit.Normal)[0]
        if deptype:
            if self.file_department:
                department_type = self.file_Deptype_path
                deptype = department_type.joinpath(deptype)
                if not script.convert.isChinese(deptype):
                    if not deptype.is_dir():
                        deptype.mkdir(parents=True, exist_ok=True)
                        self.setdepType()

    # </editor-fold>

    # <editor-fold desc="各种对于文件的操作">
    def openFile(self):
        filepath = self.combinationFilePath()
        # subprocess.Popen(str(filepath))
        try:
            os.startfile(str(filepath))
        except:
            pass

    def combinationFilePath(self):
        # 这个用来组合文件和文件命
        filename = self.file_name
        filepath = self.file_path.joinpath(filename)
        return filepath

    # def combinationFileName(self):
    #     # 这个用来组合文件名称
    #     indexs = self.listfile.selectedItems()
    #     item: Dict[str, str] = {}
    #     item['version'] = indexs[0].text()
    #     if len(indexs) == 4:
    #         item['user'] = indexs[2].text()
    #         item['fileSuffixes'] = indexs[3].text()
    #     else:
    #         item['user'] = indexs[1].text()
    #         item['fileSuffixes'] = indexs[2].text()
    #     filename = 'shot_{}-{}_{}_{}_{}__{}_{}'.format(self.file_episods,
    #                                                    self.file_shot,
    #                                                    self.file_department,
    #                                                    self.file_Deptype,
    #                                                    item['version'],
    #                                                    item['user'],
    #                                                    item['fileSuffixes'])
    #     return filename

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
        pyperclip.copy(str(self.file_name))

    def copyPathToClipboard(self):
        pyperclip.copy(str(self.file_path))
    # </editor-fold>


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
