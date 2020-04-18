# -*- coding: UTF-8 -*-
import os
import pathlib
import shutil
import subprocess
import sys
import importlib
import script.MySqlComm
import re
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
            items__text = self.listepisodes.selectedItems()[0].text()
            if items__text == 'pv':
                items__text = 0
            else:
                items__text = int(items__text[2:])
            return items__text
        except:
            return ''

    @property
    def file_shot(self) -> int:
        # 关于shot的操作属性
        try:
            items__text = self.listshot.selectedItems()[0].text()
            try:
                items__text = int(items__text[2:])
            except:
                items__text = int(items__text[2:-1])
            return items__text
        except:
            return ''

    @property
    def file_shotab(self) -> int:
        # 关于shot的操作属性
        try:
            items__text = self.listshot.selectedItems()[0].text()
            try:
                items__text = int(items__text[2:])
            except:
                items__textab = int(items__text[2:-1])
            return items__textab
        except:
            return ''

    @property
    def file_department(self) -> str:
        # 关于部门的操作
        try:
            return self.listdepartment.selectedItems()[0].text()
        except:
            return None

    @property
    def file_Deptype(self):
        # 部门的下一个类型的操作
        # return self.listdepType.selectedItems()[0].text()
        try:
            return self.listdepType.selectedItems()[0].text()
        except:
            return None

    @property
    def file_path(self):
        try:
            path = self.root.joinpath(f'ep{self.file_episods:0>3d}',
                                      f'sc{self.file_shot:0>4d}',
                                      'Scenefiles',
                                      self.file_department,
                                      self.file_Deptype
                                      )
            return path
        except:
            return ''

    @property
    def file_name(self):
        if not hasattr(self, '_file_name'):
            self._file_name = ''
        return self._file_name

    @file_name.setter
    def file_name(self, file_name):
        self._file_name = file_name

    @property
    def file_suffixes(self):
        if not hasattr(self, '_file_suffixes'):
            self._file_suffixes = ''
        return self._file_suffixes

    @file_suffixes.setter
    def file_suffixes(self, file_suffixes):
        self._file_suffixes = file_suffixes

    # </editor-fold>

    # <editor-fold desc="属性操作">

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
    def assFilePath(self) -> pathlib.Path:
        """资产文件所在路径"""
        if not hasattr(self, '_assFilePath'):
            self._assFilePath = ''
        else:
            self._assFilePath = self.rootAss.joinpath(self.assFamily,
                                                      self.asslistSelect,
                                                      'Scenefiles',
                                                      self.assTypeSelsct,
                                                      )
        return self._assFilePath

    @property
    def assFileVersion(self):
        if not hasattr(self, '_assFileVersion'):
            self._assFileVersion = 0
        return self._assFileVersion

    @assFileVersion.setter
    def assFileVersion(self, assFileVersion):
        self._assFileVersion = assFileVersion

    @property
    def assfilename(self) -> str:
        if not hasattr(self, "_assfilename"):
            self._assfilename = ''
        else:
            name = self.asslistSelect
            if self.assTypeSelsct in ['rig']:
                name = name + '_rig'
            self._assfilename = name
        return self._assfilename

    # </editor-fold>
    @property
    def recentlyOpenedFolder(self) -> pathlib.Path:
        if not hasattr(self, '_recentlyOpenedFolder'):
            self._recentlyOpenedFolder = ''
        return self._recentlyOpenedFolder

    @recentlyOpenedFolder.setter
    def recentlyOpenedFolder(self, recentlyOpenedFolder: pathlib.Path):
        self._recentlyOpenedFolder = recentlyOpenedFolder

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
        add_ass_file = QtWidgets.QAction('上传(提交)文件', self)
        add_ass_file_dow = QtWidgets.QAction('同步UE文件', self)
        get_ass_path = QtWidgets.QAction('指定文件', self)
        add_ass_file.triggered.connect(self.uploadFiles)
        add_ass_file_dow.triggered.connect(self.downloadUe4)
        get_ass_path.triggered.connect(self.appointFilePath)
        self.listAssFile.addAction(add_ass_file)
        self.listAssFile.addAction(add_ass_file_dow)
        self.listAssFile.addAction(get_ass_path)
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

        # region 获得服务器上数据,集数数据
        sql = """select id,episods from mainshot"""
        data = self.setlocale.getseverPrjBrowser()['mySqlData']
        eps = script.MySqlComm.selsctCommMysql(data,
                                               self.setlocale.department,
                                               self.setlocale.department, sql)
        item = []
        for ep in eps:
            if ep[1] == 0:
                item.append('pv')
            else:
                item.append('ep{:0>3d}'.format(ep[1]))
        # endregion

        # item = self.projectAnalysisShot.getEpisodesItems(self)
        self.ta_log.info('更新集数列表')

        self.listepisodes.addItems(item)

    def setShotItem(self):
        # region 获得服务器上数据,镜头数据
        sql = """select distinct shot,shotab from ep{:0>3d}""".format(self.file_episods)
        data = self.setlocale.getseverPrjBrowser()['mySqlData']
        eps = script.MySqlComm.selsctCommMysql(data,
                                               self.setlocale.department,
                                               self.setlocale.department, sql)
        item = []
        for ep in eps:
            try:
                item.append('sc{:0>4d}{}'.format(ep[0], ep[1]))
            except:
                item.append('sc{:0>4d}'.format(ep[0]))

        self.listdepartment.clear()
        self.listdepType.clear()
        self.clearListFile()

        self.listshot.clear()
        self.ta_log.info('更新shot列表')
        self.listshot.addItems(item)

    def setDepartment(self):
        sql = f"""select distinct department from ep{self.file_episods:0>3d}
                where episodes = {self.file_episods} 
                and shot = {self.file_shot}
                and shotab = {self.file_shotab}"""

        data = self.setlocale.getseverPrjBrowser()['mySqlData']
        eps = script.MySqlComm.selsctCommMysql(data,
                                               self.setlocale.department,
                                               self.setlocale.department, sql)
        item = []
        for department in eps:
            item.append(department[0])

        self.listdepType.clear()
        self.clearListFile()

        self.listdepartment.clear()
        self.ta_log.info('更新Department列表')
        self.listdepartment.addItems(item)

    def setdepType(self):
        sql = f"""select distinct Type from ep{self.file_episods:0>3d}
                where episodes = {self.file_episods} 
                and shot = {self.file_shot}
                and shotab = {self.file_shotab}
                and department ='{self.file_department}'"""

        data = self.setlocale.getseverPrjBrowser()['mySqlData']
        eps = script.MySqlComm.selsctCommMysql(data,
                                               self.setlocale.department,
                                               self.setlocale.department, sql)
        item = []
        for depType in eps:
            item.append(depType[0])

        self.clearListFile()

        self.listdepType.clear()
        self.ta_log.info('更新depType列表')
        self.listdepType.addItems(item)

    def setFile(self):
        '''设置文件在GUI中的显示'''
        # 清空上一次文件显示和版本记录和文件路径
        self.clearListFile()
        self.file_version_max = 0

        sql = f"""select version, user, fileSuffixes from ep{self.file_episods:0>3d}
                where episodes = {self.file_episods}
                and shot = {self.file_shot}
                and shotab = {self.file_shotab}
                and department ='{self.file_department}'
                and Type = '{self.file_Deptype}'"""
        data = self.setlocale.getseverPrjBrowser()['mySqlData']
        eps = script.MySqlComm.selsctCommMysql(data,
                                               self.setlocale.department,
                                               self.setlocale.department, sql)

        for item in eps:
            mrow = 0
            tmp_version_ = int(item[0])
            if tmp_version_ > self.file_version_max:
                self.file_version_max = tmp_version_
            self.listfile.insertRow(mrow)
            self.listfile.setItem(mrow, 0, QtWidgets.QTableWidgetItem(f'v{item[0]:0>4d}'))
            self.listfile.setItem(mrow, 2, QtWidgets.QTableWidgetItem(item[1]))
            self.listfile.setItem(mrow, 3, QtWidgets.QTableWidgetItem(item[2]))
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
        # self.assFamilyPath = self.setAssFamilyPath()
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

        ass_data_com = f"""select distinct name from `{self.assFamily}`"""
        data = self.setlocale.getseverPrjBrowser()['mySqlData']
        data = script.MySqlComm.selsctCommMysql(data,
                                                self.setlocale.department,
                                                self.setlocale.department,
                                                ass_data_com)
        item = []
        for assitem in data:
            item.append(assitem[0])
        # item = self.projectAnalysisAss.getAssFamilyItems(self)
        if item:
            self.listAss.addItems(item)

    def setlistAssTypeItems(self):
        self.listAssType.clear()
        self.ta_log.info('清除资产类型中的项数')
        self.clearListAssFile()
        self.ta_log.info('清除资产文件中的项数')

        ass_type_com = f"""select distinct type from `{self.assFamily}`
                            where name = '{self.asslistSelect}'"""
        data = self.setlocale.getseverPrjBrowser()['mySqlData']
        data = script.MySqlComm.selsctCommMysql(data,
                                                self.setlocale.department,
                                                self.setlocale.department,
                                                ass_type_com)
        item = []
        for asstype in data:
            item.append(asstype[0])
        # item = self.projectAnalysisAss.getAssTypeItems(self)
        self.listAssType.addItems(item)

    def setlistAssFileItems(self):
        '''设置文件在GUI中的显示'''
        # 清空上一次文件显示和版本记录和文件路径
        self.clearListAssFile()
        self.Ass_version_max = 0

        ass_type_com = f"""select distinct version,infor,user,fileSuffixes from `{self.assFamily}`
                            where name = '{self.asslistSelect}'
                            and type = '{self.assTypeSelsct}'"""
        data = self.setlocale.getseverPrjBrowser()['mySqlData']
        file_data = script.MySqlComm.selsctCommMysql(data,
                                                     self.setlocale.department,
                                                     self.setlocale.department,
                                                     ass_type_com)
        for item in file_data:
            mrow = 0
            tmp_version_ = item[0]
            if tmp_version_ > self.file_version_max:
                self.file_version_max = tmp_version_
            self.listAssFile.insertRow(mrow)
            self.listAssFile.setItem(mrow, 0, QtWidgets.QTableWidgetItem(f'v{item[0]:0>4d}'))
            self.listAssFile.setItem(mrow, 1, QtWidgets.QTableWidgetItem(item[1]))
            self.listAssFile.setItem(mrow, 2, QtWidgets.QTableWidgetItem(item[2]))
            self.listAssFile.setItem(mrow, 3, QtWidgets.QTableWidgetItem(item[3]))
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
                    if self.file_path:
                        dstFile = self.getFileName(path.suffix)  # type:pathlib.Path
                        self.file_path.mkdir(parents=True, exist_ok=True)
                        shutil.copy2(str(path), str(dstFile))
                        self.ta_log.info('%s ---> %s', path, dstFile)
                        self.subMissionShotInfor(self.file_version_max + 1, path.suffix)
                    # print(path)
                if path.suffix in ['.fbx', '.usd']:
                    if self.file_path:
                        dstFile = self.getFileName(path.suffix, True)  # type:pathlib.Path
                        self.file_path.mkdir(parents=True, exist_ok=True)
                        shutil.copy2(str(path), str(dstFile))
                        self.ta_log.info('%s ---> %s', path, dstFile)
                        self.subMissionShotInfor(self.file_version_max, path.suffix)
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
        filename['file_episods'] = f'ep{self.file_episods:0>3d}'
        filename['file_shot'] = f'sc{self.file_shot:0>4d}'
        filename['file_department'] = self.file_department
        filename['file_Deptype'] = self.file_Deptype
        filename['user'] = user_
        filename['fileSuffixes'] = Suffixes
        # 将版本加一复制为新版本
        if External:
            filename['version'] = f'v{self.file_version_max:0>4d}'
        else:
            filename['version'] = f'v{self.file_version_max + 1:0>4d}'
        filename = f'shot_{filename["file_episods"]}' \
                   f'-{filename["file_shot"]}_' \
                   f'{filename["file_department"]}_' \
                   f'{filename["file_Deptype"]}_' \
                   f'{filename["version"]}__' \
                   f'{filename["user"]}_' \
                   f'{filename["fileSuffixes"]}'
        self.file_name = filename
        path = self.file_path.joinpath(self.file_name)
        return path

    # </editor-fold>
    def subMissionShotInfor(self, version, file_suffixes):
        as_posix = self.file_path.joinpath(self.file_name).as_posix()
        shot_data = f"""insert into ep{self.file_episods:0>3d}(episodes, 
                        shot, 
                        shotab,
                        department, 
                        Type, 
                        file, 
                        fileSuffixes, 
                        user, 
                        version, 
                        filepath) VALUE({self.file_episods},
                        {self.file_shot},
                        '{self.file_shotab}',
                        '{self.file_department}',
                        '{self.file_Deptype}',
                        '{self.file_name}',
                        '{file_suffixes}',
                        '{self.setlocale.user}',
                        {version},
                        '{as_posix}') 
                        """
        script.MySqlComm.inserteCommMysql(self.setlocale.getseverPrjBrowser()['mySqlData'],
                                          '', '', shot_data)

    # <editor-fold desc="添加集数文件夹的操作都在这里">
    def addEpisodesFolder(self):
        episode: int = QtWidgets.QInputDialog.getInt(self, '输入集数', "ep", 1, 1, 999, 1)[0]
        if episode:
            create_date = f"""create table ep{episode:0>3d}(
                                        id smallint primary key not null auto_increment,
                                        episodes smallint,
                                        shot smallint,
                                        shotab varchar(8),
                                        department varchar(128),
                                        Type varchar(128),
                                        file varchar(128),
                                        fileSuffixes varchar(32),
                                        user varchar(128),
                                        version smallint,
                                        filepath varchar(1024),
                                        itfor varchar(4096),
                                        filetime datetime default current_timestamp on update current_timestamp not null 
                                        );"""
            create_date_insert = f"""insert into mainshot(episods)
                                        value ({episode})"""
            script.MySqlComm.inserteCommMysql(self.setlocale.getseverPrjBrowser()['mySqlData'], '', '', create_date)
            script.MySqlComm.inserteCommMysql(self.setlocale.getseverPrjBrowser()['mySqlData'], '', '',
                                              create_date_insert)

            self.setepisodex()

    def addShotFolder(self):
        shot = QtWidgets.QInputDialog.getInt(self, '输入镜头', "sc", 1, 1, 999, 1)[0]
        if shot:
            self.listshot.addItem('sc{:0>4d}'.format(shot))

    def addABshotFolder(self):
        items = ['B', 'C', 'D', 'E']
        shotAB = QtWidgets.QInputDialog.getItem(self, '选择AB镜头', '要先选择镜头才可以', items, 0, False)[0]
        shot = self.file_shot
        if shotAB:
            self.listshot.addItem('sc{:0>4d}{}'.format(shot, shotAB))

    def addDepartmentFolder(self):
        department = self.setlocale.department
        if self.file_shot:
            self.listdepartment.addItem(department)

    def addTypeFolder(self):
        deptype = QtWidgets.QInputDialog.getText(self, '输入镜头', "文件类型(请用英文或拼音)",
                                                 QtWidgets.QLineEdit.Normal)[0]
        if deptype:
            self.listdepType.addItem(deptype)

    def addAssFolder(self):
        """添加资产类型文件夹"""
        assFolder = QtWidgets.QInputDialog.getText(self, '输入资产类型', "请用英文或拼音",
                                                   QtWidgets.QLineEdit.Normal)[0]
        if assFolder:
            self.listAss.addItem(assFolder)

    def addAssTypeFolder(self):
        """添加资产文件夹类型"""
        items: list[str] = self.setlocale.assTypeFolder.copy()
        items[2] = items[2].format(self.asslistSelect)
        ass_type = QtWidgets.QInputDialog.getItem(self, '选择资产类型', '要先选择资产', items, 0, False)[0]
        if ass_type:
            self.listAssType.addItem(ass_type)

    def uploadFiles(self):
        """上传资产文件"""
        file, fileType = QtWidgets.QFileDialog.getOpenFileName(self,
                                                               "选择上传文件",
                                                               self.recentlyOpenedFolder,
                                                               "files (*.mb *.ma *.uproject *.max *.fbx *.png *.tga *.jpg)")
        self.recentlyOpenedFolder = file

        if file:
            file = pathlib.Path(file)
            if file.suffix in ['.mb', '.ma', '.max', '.fbx']:
                self.assUploadFileHandle(file)
            elif file.suffix in ['.uproject']:
                self.assUploadFileUE4Handle(file)
                self.subMissionAssInfor(self.assFileVersion, '\\.uproject', '')
            elif file.suffix in ['.png', '.tga', 'jpg']:
                self.assUploadMapHandle(file)
            else:
                pass
        self.setlistAssFileItems()

    def assUploadMapHandle(self, file: pathlib.Path):
        version = self.getAssMaxVersion() + 1
        file_path = file.parent
        target_file: pathlib.Path = self.assFilePath
        file_str = f'^{self.asslistSelect}_.*_(?:Color|Normal|bump|alpha)$'

        sub = False
        for fi in file_path.iterdir():
            if re.match(file_str, fi.stem):
                tar = target_file.joinpath(fi.name)
                self.backupCopy(fi, tar, version)
                sub = True
        if sub:
            self.subMissionAssInfor(version, file.suffix, '')

    def backupCopy(self, source: pathlib.Path, target: pathlib.Path, version: int):
        """来源和目标必须时文件 + 路径"""
        backup = self.assFilePath.joinpath('backup')
        self.assFilePath.mkdir(parents=True, exist_ok=True)
        if not backup.is_dir():
            backup.mkdir(parents=True, exist_ok=True)
        backup_file = backup.joinpath('{}_v{:0>4d}{}'.format(target.stem,
                                                             version,
                                                             target.suffix))
        if target.is_file():
            shutil.move(str(target), str(backup_file))
            self.ta_log.info('文件备份%s ---->  %s', target, backup_file)
        shutil.copy2(str(source), str(target))

        self.ta_log.info('文件上传%s ---->  %s', source, target)

    def downloadUe4(self):
        path = QtWidgets.QFileDialog.getExistingDirectory(self,
                                                          "选择同步目录",
                                                          self.recentlyOpenedFolder,
                                                          QtWidgets.QFileDialog.ShowDirsOnly)

    def subMissionAssInfor(self, version, file_suffixes, infor):
        as_posix = self.assFilePath.joinpath(self.assfilename + file_suffixes).as_posix()
        ass_data = f"""insert into `{self.assFamily}`( 
                                name, 
                                type,
                                file,
                                fileSuffixes, 
                                user, 
                                version,
                                infor,
                                filepath) VALUE('{self.asslistSelect}',
                                '{self.assTypeSelsct}',
                                '{self.assfilename}',
                                '{file_suffixes}',
                                '{self.setlocale.user}',
                                {version},
                                '{infor}',
                                '{as_posix}'
                                ) 
                                """
        script.MySqlComm.inserteCommMysql(self.setlocale.getseverPrjBrowser()['mySqlData'],
                                          '', '', ass_data)

    def getAssMaxVersion(self):
        ass_type_com = f"""select distinct version from `{self.assFamily}`
                            where name = '{self.asslistSelect}'
                            and type = '{self.assTypeSelsct}'
                            order by version desc;"""
        data = self.setlocale.getseverPrjBrowser()['mySqlData']
        file_data = script.MySqlComm.selsctCommMysql(data,
                                                     self.setlocale.department,
                                                     self.setlocale.department,
                                                     ass_type_com)
        if file_data:
            version_max: int = file_data[0][0]
        else:
            version_max: int = 0
        return version_max

    def assUploadFileHandle(self, file_path: pathlib.Path):
        """这个用来获得资产下一级路径,这级路径是程序文件夹
        :type self: script.ProjectBrowserGUI.ProjectBrowserGUI
        """
        version_max = self.getAssMaxVersion()
        target_file: pathlib.Path = self.assFilePath.joinpath('{}{}'.format(self.asslistSelect,
                                                                            file_path.suffix))

        if file_path.suffix in ['.mb', '.ma', '.max']:
            version_max = version_max + 1
            self.backupCopy(file_path, target_file, version_max)
            self.subMissionAssInfor(version_max, file_path.suffix, '')

        if file_path.suffix in ['.fbx']:
            self.backupCopy(file_path, target_file, version_max)
            self.subMissionAssInfor(version_max, file_path.suffix, '')

    def assUploadFileUE4Handle(self, file_path: pathlib.Path):
        """这个用来获得资产下一级路径,这级路径是程序文件夹
        :type self: script.ProjectBrowserGUI.ProjectBrowserGUI
        """
        version_max = self.getAssMaxVersion() + 1
        backup = self.assFilePath.joinpath('backup')
        source = file_path.parent
        target: pathlib.Path = self.assFilePath
        syn_path = [{'Left': str(source), 'Right': str(target)}]
        syn_file = script.synXml.weiteXml(self.setlocale.doc,
                                          syn_path,
                                          Include=['*\\Content\\*'],
                                          Exclude=['*\\backup\\'],
                                          VersioningFolder=str(backup),
                                          fileName='UEpriect')
        program = self.setlocale.FreeFileSync
        cmd = os.system('{} "{}"'.format(program, syn_file))
        self.assFileVersion = version_max
        shutil.copy2(str(file_path), str(self.assFilePath.joinpath(self.assfilename + '.uproject')))

    def appointFilePath(self):
        """指定文件路径"""
        file, fileType = QtWidgets.QFileDialog.getOpenFileName(self,
                                                               "选择上传文件",
                                                               self.recentlyOpenedFolder,
                                                               "files (*.mb *.ma *.uproject *.max *.fbx *.png *.tga *.jpg)")

        remarks_info = self.recentlyOpenedFolder = QtWidgets.QInputDialog.getText(self,
                                                                                  "填写备注(中文)",
                                                                                  "备注",
                                                                                  QtWidgets.QLineEdit.Normal)[0]
        if file:
            file = pathlib.Path(file)
            self.subMissionAssInfor(1, file.suffix, remarks_info)

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
        # 这个函数不好用记得改
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
