# -*- coding: UTF-8 -*-
import os
import pathlib
import shutil
import sys
import importlib
import script.MySqlComm
from typing import Dict

import pyperclip
import pypinyin
import qdarkgraystyle
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets

import UiFile.ProjectBrowser

import script.ProjectAnalysis.PathAnalysis
import script.convert
import script.debug
import script.doodleLog
import script.doodle_setting


class ProjectBrowserGUI(QtWidgets.QMainWindow, UiFile.ProjectBrowser.Ui_MainWindow):
    '''这个类用来实现项目管理的属性和UI操作,  其中会有一个项目分析器在外部, 有每个项目分别配置或者使用默认设置

    '''
    projectAnalysisShot: script.ProjectAnalysis.PathAnalysis.ProjectAnalysisShot
    projectAnalysisAss: script.ProjectAnalysis.PathAnalysis.ProjectAnalysisAssets
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

    """ projectAnalysisShot   # 路径解析器
    projectAnalysisAss  # 资产路径解析器"""

    def __init__(self, parent=None):
        super(ProjectBrowserGUI, self).__init__()
        # 获取设置
        self.setlocale = script.doodle_setting.Doodlesetting()
        """======================================================================="""
        # 导入解析项目模块
        prj_module = importlib.import_module('script.ProjectAnalysis.{}'.format(self.setlocale.projectAnalysis))

        """======================================================================="""
        self.projectAnalysisShot = prj_module.ProjectAnalysisShot()
        self.projectAnalysisAss = prj_module.ProjectAnalysisAssets()
        self.ta_log = script.doodleLog.get_logger(__name__)
        # 初始化一些属性
        # self.root = self.getRoot()
        # 设置UI
        self.setupUi(self)

        # self.setToolTip("Remer")
        # 设置最后的文件编辑器的一些标准动作
        # 设置每行选择
        self.listfile.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.listAssFile.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        # 设置单选
        self.listfile.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        # 设置注释最大(资产和镜头都是)
        self.listfile.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        self.listAssFile.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        # 设置不可编辑
        self.listfile.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        # 开启窗口拖拽事件
        self.setAcceptDrops(True)
        # self.listepisodes.setAcceptDrops

        # <editor-fold desc="关于shot的更新操作">
        self.addRightClick()
        # 首先扫描根目录获得集数
        self.setepisodex()
        # 并链接函数处理下一级
        self.listepisodes.itemClicked.connect(self.setShotItem)
        # 在shot文件列表中添加点击事件更改下一级部门列表
        self.listshot.itemClicked.connect(self.setDepartment)
        # 在department中添加下一级的更新事件
        self.listdepartment.itemClicked.connect(self.setdepType)
        # 在depType中添加点击跟新文件事件
        self.listdepType.itemClicked.connect(self.setFile)
        # </editor-fold>

        # 在listAss中添加点击事件生成Ass资产列表
        self.listAss.itemClicked.connect(self.setlistAssTypeItems)
        # 在listType中添加点击事件生成file列表
        self.listAssType.itemClicked.connect(self.setlistAssFileItems)

        # 双击打开文件
        self.listfile.doubleClicked.connect(self.openFile)
        # 添加刷新函数
        self.refresh.triggered.connect(self.setepisodex)

        # 设置ass类型
        self.scane.clicked.connect(lambda: self.setAssTypeAttr('scane'))
        self.props.clicked.connect(lambda: self.setAssTypeAttr('props'))
        self.character.clicked.connect(lambda: self.setAssTypeAttr('character'))
        self.effects.clicked.connect(lambda: self.setAssTypeAttr('effects'))

    # <editor-fold desc="集数和根目录的属性操作">
    @property
    def root(self) -> pathlib.Path:
        shot_root_ = self.setlocale.getseverPrjBrowser()['shotRoot']
        root = pathlib.Path(self.setlocale.project)
        # 获得根目录
        for myP in shot_root_:
            root = root.joinpath(myP)
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
            return self.projectAnalysisShot.getShotPath(self)
        except:
            return None

    # </editor-fold>

    # <editor-fold desc="关于部门的操作">
    @property
    def file_department(self) -> str:
        try:
            return self.listdepartment.selectedItems()[0].text()
        except:
            return None

    @property
    def file_department_path(self):
        try:
            tmp = self.projectAnalysisShot.getdepartmentPath(self)
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
            return self.projectAnalysisShot.getDepTypePath(self)
        except:
            return None

    # </editor-fold>

    # <editor-fold desc="关于文件的操作">
    @property
    def file_path(self):
        try:
            return self.projectAnalysisShot.getFilePath(self)
        except:
            return None

    @property
    def file_name(self):
        try:
            filename = self.projectAnalysisShot.getFileName(self)
            return self.projectAnalysisShot.commFileName(filename)
        except:
            return None

    # </editor-fold>

    # <editor-fold desc="属性操作">
    # <editor-fold desc="资产属性">
    @property
    def rootAss(self) -> pathlib.Path:
        """资产类型的根目录"""
        if not hasattr(self, '_rootAss'):
            shot_root_ = self.setlocale.getseverPrjBrowser()['assetsRoot']
            root = pathlib.Path(self.setlocale.project)
            # 获得根目录
            for myP in shot_root_:
                root = root.joinpath(myP)
            self._rootAss = root
        return self._rootAss

    # region 选择的资产类型
    @property
    def assFamily(self):
        """选择的资产类型<场景,人物,道具,特效等等>"""
        if not hasattr(self, '_assfamily'):
            self._assfamily = 'character'
        return self._assfamily

    @assFamily.setter
    def assFamily(self, assfamily):
        self._assfamily = assfamily

    # endregion

    @property
    def assFamilyPath(self) -> pathlib.Path:
        """资产类型所在根目录"""
        if not hasattr(self, '_assFamilyPath'):
            path = self.setAssFamilyPath()
        else:
            path = self._assFamilyPath
        return path

    @assFamilyPath.setter
    def assFamilyPath(self, ass_family_path):
        self._assFamilyPath = ass_family_path

    @property
    def asslistSelect(self) -> str:
        """资产列表中选中的资产"""
        if not hasattr(self, '_asslistSelect'):
            self._asslistSelect = ''
        else:
            self._asslistSelect = self.listAss.selectedItems()[0].text()
        return self._asslistSelect

    @property
    def assTypeSelsct(self) -> str:
        """资产自己的类型的已选择"""
        if not hasattr(self, '_assTypeSelsct'):
            if not self.listdepType.selectedItems():
                self._assTypeSelsct = ''
        else:
            self.assTypeSelsct = self.listAssType.selectedItems()[0].text()
        return self._assTypeSelsct

    @assTypeSelsct.setter
    def assTypeSelsct(self, assTypeSelsct):
        self._assTypeSelsct = assTypeSelsct

    @property
    def assTypePath(self) -> pathlib.Path:
        """资产自己的类型所在路径"""
        if self.listAss.selectedItems():
            ass_type_path = self.projectAnalysisAss.getAssTypePath(self)
        else:
            ass_type_path = None
        return ass_type_path

    @property
    def assFilePath(self) -> pathlib.Path:
        """资产文件所在路径"""
        if self.listAssType.selectedItems():
            return self.projectAnalysisAss.getAssFilePath(self)
        else:
            return None

    @property
    def recentlyOpenedFolder(self) -> pathlib.Path:
        if not hasattr(self, '_recentlyOpenedFolder'):
            self._recentlyOpenedFolder = ''
        return self._recentlyOpenedFolder

    @recentlyOpenedFolder.setter
    def recentlyOpenedFolder(self, recentlyOpenedFolder: pathlib.Path):
        self._recentlyOpenedFolder = recentlyOpenedFolder

    # </editor-fold>
    # </editor-fold>

    # <editor-fold desc="更新shot视图的各种操作">
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

        # 添加资产文件夹右键菜单
        self.listAss.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        add_ass_folder = QtWidgets.QAction('添加', self)
        add_ass_folder.triggered.connect(self.addAssFolder)
        self.listAss.addAction(add_ass_folder)
        # 添加资产类型右键文件夹
        self.listAssType.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        add_ass_type_folder = QtWidgets.QAction('添加', self)
        add_ass_type_folder.triggered.connect(self.addAssTypeFolder)
        self.listAssType.addAction(add_ass_type_folder)
        # 添加文件右键菜单
        self.listAssFile.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        add_ass_file = QtWidgets.QAction('上传文件', self)
        add_ass_file.triggered.connect(self.uploadFiles)
        self.listAssFile.addAction(add_ass_file)
        '''================================================================='''

    def getRoot(self) -> pathlib.Path:
        # 获得项目目录
        shot_root_ = self.setlocale.getseverPrjBrowser()['shotRoot']
        root = pathlib.Path(self.setlocale.project)
        # 获得根目录
        for myP in shot_root_:
            root = root.joinpath(myP)
        self.ta_log.info('根目录%s', root)
        return root

    def setepisodex(self):
        self.listepisodes.clear()
        self.listdepartment.clear()
        self.listdepType.clear()
        self.clearListFile()
        self.listshot.clear()
        # sql = """select * from mainshot"""
        # data = self.setlocale.getseverPrjBrowser()['mySqlData']
        # eps = script.MySqlComm.selsctCommMysql(data,
        #                                        self.setlocale.department,
        #                                        self.setlocale.department, sql)
        # item = []
        # for ep in eps:
        #     if ep[1] == 0:
        #         item.append('PV')
        #     else:
        #         item.append('ep{:0>3d}'.format(ep[1]))
        item = self.projectAnalysisShot.getEpisodesItems(self)
        self.ta_log.info('更新集数列表')

        self.listepisodes.addItems(item)

    def setShotItem(self):
        mitem = self.projectAnalysisShot.getShotItems(self)

        self.listdepartment.clear()
        self.listdepType.clear()
        self.clearListFile()

        self.listshot.clear()
        self.ta_log.info('更新shot列表')
        self.listshot.addItems(mitem)

    def setDepartment(self):
        department = self.file_department_path
        mitem = self.projectAnalysisShot.getdepartmentItems(self)

        self.listdepType.clear()
        self.clearListFile()

        self.listdepartment.clear()
        self.ta_log.info('更新Department列表')
        self.listdepartment.addItems(mitem)

    def setdepType(self):
        mitem = self.projectAnalysisShot.getDepTypeItems(self)

        self.clearListFile()

        self.listdepType.clear()
        self.ta_log.info('更新depType列表')
        self.listdepType.addItems(mitem)

    def setFile(self):
        '''设置文件在GUI中的显示'''
        # 清空上一次文件显示和版本记录和文件路径
        self.clearListFile()
        self.file_version_max = 0
        for item in self.projectAnalysisShot.fileNameInformation(self):
            mrow = 0
            tmp_version_ = int(item['version'][1:])
            if tmp_version_ > self.file_version_max:
                self.file_version_max = tmp_version_
            self.listfile.insertRow(mrow)
            self.listfile.setItem(mrow, 0, QtWidgets.QTableWidgetItem(item['version']))
            self.listfile.setItem(mrow, 2, QtWidgets.QTableWidgetItem(item['producer']))
            self.listfile.setItem(mrow, 3, QtWidgets.QTableWidgetItem(item['fileSuffixes']))
            mrow = mrow + 1
        self.ta_log.info('更新文件列表')

    def clearListFile(self):
        mrowtmp = self.listfile.rowCount()
        while mrowtmp >= 0:
            self.listfile.removeRow(mrowtmp)
            mrowtmp = mrowtmp - 1

    # </editor-fold>

    # <editor-fold desc="更新ass的各种操作">
    def setAssTypeAttr(self, ass_name: str):

        self.assFamily = ass_name
        self.assFamilyPath = self.setAssFamilyPath()
        self.ta_log.info('将资产类型设置为 %s', ass_name)
        self.setListAssItems()

    def clearListAssFile(self):
        mrowtmp = self.listAssFile.rowCount()
        while mrowtmp >= 0:
            self.listAssFile.removeRow(mrowtmp)
            mrowtmp = mrowtmp - 1

    def setAssFamilyPath(self):
        AssFamilyPath = self.projectAnalysisAss.getAssFamilyPath(self)
        return AssFamilyPath

    def setAssTypeSelet(self):
        self.assTypeSelsct = self.listAssType.selectedItems()[0].text()

    # def setAssFilePath(self):
    #     self.assFilePath = self.projectAnalysisAss.getAssFilePath(self)

    def setListAssItems(self):
        self.listAss.clear()
        self.listAssType.clear()
        self.clearListAssFile()

        item = self.projectAnalysisAss.getAssFamilyItems(self)
        if item:
            self.listAss.addItems(item)

    def setlistAssTypeItems(self):
        self.listAssType.clear()
        self.ta_log.info('清除资产类型中的项数')
        self.clearListAssFile()
        self.ta_log.info('清除资产文件中的项数')
        item = self.projectAnalysisAss.getAssTypeItems(self)
        self.listAssType.addItems(item)

    def setlistAssFileItems(self):
        '''设置文件在GUI中的显示'''
        # 清空上一次文件显示和版本记录和文件路径
        self.clearListAssFile()
        self.Ass_version_max = 0
        for item in self.projectAnalysisAss.getAssFileInfo(self):
            mrow = 0
            tmp_version_ = int(item['version'][1:])
            if tmp_version_ > self.file_version_max:
                self.file_version_max = tmp_version_
            self.listAssFile.insertRow(mrow)
            self.listAssFile.setItem(mrow, 0, QtWidgets.QTableWidgetItem(item['version']))
            self.listAssFile.setItem(mrow, 2, QtWidgets.QTableWidgetItem(item['user']))
            self.listAssFile.setItem(mrow, 3, QtWidgets.QTableWidgetItem(item['fileSuffixes']))
            mrow = mrow + 1
        self.ta_log.info('更新文件列表')
        # return self.projectAnalysisAss.

    # </editor-fold>

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
        self.enableBorder(False)

    def dropEvent(self, a0: QtGui.QDropEvent) -> None:
        if a0.mimeData().hasUrls():
            # 检测文件路劲和类型,限制拖动
            if len(a0.mimeData().urls()) == 1:
                url = a0.mimeData().urls()[0]
                path = pathlib.Path(url.toLocalFile())
                self.ta_log.info('检测到文件%s拖入窗口', path)
                # 获得文件路径并进行复制
                if path.suffix in ['.ma', '.mb', '.hip']:
                    # 为防止在没有选择的情况下复制到不知道的位置所以先进行路径测试
                    if self.listdepType and self.file_path:
                        dstFile = self.getFileName(path.suffix)  # type:pathlib.Path
                        shutil.copy2(str(path), str(dstFile))
                        self.ta_log.info('%s ---> %s', path, dstFile)
                        self.setFile()
                        self.enableBorder(False)
                    # print(path)
                if path.suffix in ['.fbx', '.usd']:
                    if self.listdepType and self.file_path:
                        dstFile = self.getFileName(path.suffix, True)  # type:pathlib.Path
                        shutil.copy2(str(path), str(dstFile))
                        self.ta_log.info('%s ---> %s', path, dstFile)
                        self.setFile()
                        self.enableBorder(False)
            else:
                pass
        else:
            a0.ignore()

    def getFileName(self, Suffixes: str, External: bool = False):
        # 获得本地设置中的制作人名称
        user_ = pypinyin.slug(self.setlocale.user, pypinyin.NORMAL)
        # 格式化文件名称和路径
        filename: Dict[str, str] = {}
        filename['file_episods'] = self.file_episods
        filename['file_shot'] = self.file_shot
        filename['file_department'] = self.file_department
        filename['file_Deptype'] = self.file_Deptype
        filename['user'] = user_
        filename['fileSuffixes'] = Suffixes
        # 将版本加一复制为新版本
        if External:
            filename['version'] = 'v{:0>4d}'.format(self.file_version_max)
        else:
            filename['version'] = 'v{:0>4d}'.format(self.file_version_max + 1)
        path = self.file_path.joinpath(self.projectAnalysisShot.commFileName(filename))
        return path

    # </editor-fold>

    # <editor-fold desc="添加集数文件夹的操作都在这里">
    def addEpisodesFolder(self):
        Episode: int = QtWidgets.QInputDialog.getInt(self, '输入集数', "ep", 1, 1, 999, 1)[0]
        if Episode:
            # root = self.getRoot()
            episodesPath = self.projectAnalysisShot.episodesFolderName(self, Episode)
            for path in episodesPath:
                if not path.is_dir():
                    self.ta_log.info('制作%s', path)
                    path.mkdir(parents=True, exist_ok=True)
            self.setepisodex()

    def addShotFolder(self):
        shot = QtWidgets.QInputDialog.getInt(self, '输入镜头', "sc", 1, 1, 999, 1)[0]
        if shot:
            if self.file_episods:
                for path in self.projectAnalysisShot.shotFolderName(self, shot):
                    if not path.is_dir():
                        self.ta_log.info('制作%s', path)
                        path.mkdir(parents=True, exist_ok=True)
                self.setShotItem()

    def addABshotFolder(self):
        items = ['B', 'C', 'D', 'E']
        shotAB = QtWidgets.QInputDialog.getItem(self, '选择AB镜头', '要先选择镜头才可以', items, 0, False)[0]
        try:
            shot = int(self.file_shot[2:])
        except:
            return
        if shotAB:
            if self.file_shot and self.file_episods:
                for path in self.projectAnalysisShot.shotFolderName(self, shot, shotAB):
                    if not path.is_dir():
                        self.ta_log.info('制作AB镜头%s', path)
                        path.mkdir(parents=True, exist_ok=True)
                self.setShotItem()

    def addDepartmentFolder(self):
        department = self.setlocale.department
        if self.file_shot:
            shot_Department = self.file_department_path
            department = shot_Department.joinpath(department)
            if not department.is_dir():
                self.ta_log.info('制作%s', department)
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
                        self.ta_log.info('制作%s', deptype)
                        deptype.mkdir(parents=True, exist_ok=True)
                        self.setdepType()

    def addAssFolder(self):
        """添加资产类型文件夹"""
        assFolder = QtWidgets.QInputDialog.getText(self, '输入资产类型', "请用英文或拼音",
                                                   QtWidgets.QLineEdit.Normal)[0]
        if assFolder:
            if self.assFamily:
                assPath = self.projectAnalysisAss.getAssFolder(self, assFolder)
                for path in assPath:
                    if not path.is_dir():
                        self.ta_log.info('制作%s', path)
                        path.mkdir(parents=True, exist_ok=True)
                        self.setListAssItems()

    def addAssTypeFolder(self):
        """添加资产文件夹类型"""
        items: list[str] = self.setlocale.assTypeFolder.copy()
        items[2] = items[2].format(self.asslistSelect)
        ass_type = QtWidgets.QInputDialog.getItem(self, '选择资产类型', '要先选择资产', items, 0, False)[0]
        if ass_type:
            if self.assTypePath:
                path = self.assTypePath.joinpath(ass_type)
                if not path.is_dir():
                    self.ta_log.info('制作%s', path)
                    path.mkdir(parents=True, exist_ok=True)
                    self.setlistAssTypeItems()

    def uploadFiles(self):
        """上传资产文件"""
        file, fileType = QtWidgets.QFileDialog.getOpenFileName(self,
                                                               "选择上传文件",
                                                               self.recentlyOpenedFolder,
                                                               "files (*.mb *.ma *.uproject *.max *.fbx)")
        self.recentlyOpenedFolder = file

        if file:
            file = pathlib.Path(file)
            if file.suffix in ['.mb', '.ma', '.max', '.fbx']:
                self.projectAnalysisAss.assUploadFileHandle(self, file)
            elif file.suffix in ['.uproject']:
                self.projectAnalysisAss.assUploadFileUE4Handle(self, file)
            else:
                pass
        self.setlistAssFileItems()

    # </editor-fold>

    # <editor-fold desc="各种对于文件的操作">

    def openFile(self):
        filepath = self.combinationFilePath()
        try:
            os.startfile(str(filepath))
            self.ta_log.info('打开%s', filepath)
        except:
            pass

    def combinationFilePath(self):
        # 这个用来组合文件和文件命
        filename = self.file_name
        filepath = self.file_path.joinpath(filename)
        return filepath

    def openExplorer(self):
        filePath = self.file_path
        self.ta_log.info('打开 %s', filePath)
        os.startfile(filePath)

    def copyNameToClipboard(self):
        pyperclip.copy(str(self.file_name))
        self.ta_log.info('复制 %s 到剪切板', str(self.file_name))

    def copyPathToClipboard(self):
        pyperclip.copy(str(self.file_path))
        self.ta_log.info('复制 %s 到剪切板', str(self.file_path))

    # </editor-fold>


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet(qdarkgraystyle.load_stylesheet())
    w = ProjectBrowserGUI()
    w.setWindowTitle("Remer")
    w.show()

    sys.exit(app.exec_())
