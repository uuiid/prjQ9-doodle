# -*- coding: UTF-8 -*-
import logging
import os
import pathlib
import re
import shutil
import subprocess
import sys
import time
from typing import Dict
import enum

import pyperclip
import pypinyin
import qdarkgraystyle
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets

import UiFile.ProjectBrowser
import script.MySqlComm
import script.convert
import script.debug
import script.doodleLog
import script.doodle_setting
import script.synXml
import script.doodlePlayer
import script.MayaExportCam


@enum.unique
class DoodlePrjectState(enum.Enum):
    shot_episodes = "shot_episodes"
    shot_shot = "shot_shot"
    shot_department = "shot_department"
    shot_dep_type = "shot_dep_type"
    shot_file = "shot_file"


class ProjectCore():

    @property
    def id(self):
        if not hasattr(self, '_id'):
            self._id = ''
        return self._id

    @id.setter
    def id(self, id):
        if not isinstance(id, int):
            id = int(id)
        self._id = id

    @property
    def mysqlData(self):
        if not hasattr(self, '_mysqlData'):
            self._mysqlData = ''
        return self._mysqlData

    @mysqlData.setter
    def mysqlData(self, mysqlData):
        self._mysqlData = mysqlData

    @property
    def shot_root(self) -> pathlib.Path:
        if not hasattr(self, '_shot_root'):
            self._shot_root = ''
        return self._shot_root

    @shot_root.setter
    def shot_root(self, shot_root):
        self._shot_root = shot_root

    @property
    def shot_episods(self) -> int:
        if not hasattr(self, '_shot_episods'):
            self._shot_episods = ''
        return self._shot_episods

    @shot_episods.setter
    def shot_episods(self, shot_episods):
        if not isinstance(shot_episods, int):
            shot_episods = int(shot_episods)
        self._shot_episods = shot_episods

    @property
    def shot_shot(self) -> int:
        if not hasattr(self, '_shot_shot'):
            self._shot_shot = ''
        return self._shot_shot

    @shot_shot.setter
    def shot_shot(self, shot_shot):
        self._shot_shot = shot_shot

    @property
    def shot_shotab(self) -> str:
        if not hasattr(self, '_shot_shotab'):
            self._shot_shotab = ''
        return self._shot_shotab

    @shot_shotab.setter
    def shot_shotab(self, shot_shotab):
        self._shot_shotab = shot_shotab

    @property
    def shot_department(self) -> str:
        if not hasattr(self, '_shot_department'):
            self._shot_department = ''
        return self._shot_department

    @shot_department.setter
    def shot_department(self, shot_department):
        self._shot_department = shot_department

    @property
    def shot_dep_type(self) -> str:
        if not hasattr(self, '_shot_dep_type'):
            self._shot_dep_type = ''
        return self._shot_dep_type

    @shot_dep_type.setter
    def shot_dep_type(self, shot_dep_type):
        self._shot_dep_type = shot_dep_type

    @property
    def shot_file_path(self) -> pathlib.Path:
        if not hasattr(self, '_shot_file_path'):
            self._shot_file_path = ''
        return self._shot_file_path

    @shot_file_path.setter
    def shot_file_path(self, shot_file_path):
        self._shot_file_path = shot_file_path

    @property
    def shot_name(self) -> str:
        if not hasattr(self, '_shot_name'):
            self._shot_name = ''
        return self._shot_name

    @shot_name.setter
    def shot_name(self, shot_name):
        self._shot_name = shot_name

    @property
    def shot_user(self):
        if not hasattr(self, '_shot_user'):
            self._shot_user = ''
        return self._shot_user

    @shot_user.setter
    def shot_user(self, shot_user):
        self._shot_user = shot_user

    @property
    def shot_suffixes(self):
        if not hasattr(self, '_shot_suffixes'):
            self._shot_suffixes = ''
        return self._shot_suffixes

    @shot_suffixes.setter
    def shot_suffixes(self, shot_suffixes):
        self._shot_suffixes = shot_suffixes

    @property
    def shot_version(self):
        if not hasattr(self, '_shot_version'):
            self._shot_version = ''
        return self._shot_version

    @shot_version.setter
    def shot_version(self, shot_version):
        if not isinstance(shot_version, int):
            shot_version = int(shot_version)
        self._shot_version = shot_version

    @property
    def ass_root(self):
        if not hasattr(self, '_ass_root'):
            self._ass_root = ''
        return self._ass_root

    @ass_root.setter
    def ass_root(self, ass_root):
        self._ass_root = ass_root

    @property
    def ass_class_sort(self):
        if not hasattr(self, '_ass_class_sort'):
            self._ass_class_sort = ''
        return self._ass_class_sort

    @ass_class_sort.setter
    def ass_class_sort(self, ass_class_sort):
        self._ass_class_sort = ass_class_sort

    @property
    def ass_class(self):
        if not hasattr(self, '_ass_class'):
            self._ass_class = ''
        return self._ass_class

    @ass_class.setter
    def ass_class(self, ass_class):
        self._ass_class = ass_class

    @property
    def ass_class_type(self):
        if not hasattr(self, '_ass_class_type'):
            self._ass_class_type = ''
        return self._ass_class_type

    @ass_class_type.setter
    def ass_class_type(self, ass_class_type):
        self._ass_class_type = ass_class_type

    @property
    def ass_file_name(self):
        if not hasattr(self, '_ass_file_name'):
            self._ass_file_name = ''
        return self._ass_file_name

    @ass_file_name.setter
    def ass_file_name(self, ass_file_name):
        self._ass_file_name = ass_file_name

    @property
    def ass_file_path(self):
        if not hasattr(self, '_ass_file_path'):
            self._ass_file_path = ''
        return self._ass_file_path

    @ass_file_path.setter
    def ass_file_path(self, ass_file_path):
        self._ass_file_path = ass_file_path

    @property
    def ass_version(self):
        if not hasattr(self, '_ass_version'):
            self._ass_version = ''
        return self._ass_version

    @ass_version.setter
    def ass_version(self, ass_version):
        self._ass_version = ass_version

    @property
    def recentlyOpenedFolder(self):
        if not hasattr(self, '_recentlyOpenedFolder'):
            self._recentlyOpenedFolder = ''
        return self._recentlyOpenedFolder

    @recentlyOpenedFolder.setter
    def recentlyOpenedFolder(self, recentlyOpenedFolder):
        self._recentlyOpenedFolder = recentlyOpenedFolder

    @property
    def file_version_max(self) -> int:
        if not hasattr(self, '_file_version_max'):
            self._file_version_max = 0
        return self._file_version_max

    @file_version_max.setter
    def file_version_max(self, file_version_max):
        self._file_version_max = file_version_max

    @property
    def ass_suffixes(self):
        if not hasattr(self, '_ass_suffixes'):
            self._ass_suffixes = ''
        return self._ass_suffixes

    @ass_suffixes.setter
    def ass_suffixes(self, ass_suffixes):
        self._ass_suffixes = ass_suffixes

    @property
    def ass_user(self):
        if not hasattr(self, '_ass_user'):
            self._ass_user = ''
        return self._ass_user

    @ass_user.setter
    def ass_user(self, ass_user):
        self._ass_user = ass_user

    @property
    def Ass_version_max(self):
        if not hasattr(self, '_Ass_version_max'):
            self._Ass_version_max = ''
        return self._Ass_version_max

    @Ass_version_max.setter
    def Ass_version_max(self, Ass_version_max):
        self._Ass_version_max = Ass_version_max

    def getShotRoot(self):
        """获得镜头根目录"""
        pass

    def getAssRoot(self):
        pass

    def ShotItem(self):
        """获得服务器上的镜头项数"""
        pass

    def departmentItem(self):
        pass

    def depTypeItem(self):
        pass

    def fileItem(self):
        pass

    def assClassItem(self):
        pass

    def assClassTypeItems(self):
        pass

    def assFileItems(self):
        pass


class ProjectBrowserGUI(QtWidgets.QMainWindow, UiFile.ProjectBrowser.Ui_MainWindow, ProjectCore):
    '''这个类用来实现项目管理的属性和UI操作,  其中会有一个项目分析器在外部, 有每个项目分别配置或者使用默认设置

    '''

    def __init__(self, parent=None):
        super(ProjectBrowserGUI, self).__init__()
        # 获取设置
        self.setlocale = script.doodle_setting.Doodlesetting()
        """======================================================================="""
        # 导入解析项目模块

        """======================================================================="""
        # 添加log
        self.ta_log = logging
        # 初始化一些属性
        self.shot_root = self.getShotRoot()
        self.ass_root = self.getAssRoot()
        self.mysqlData = self.setlocale.getseverPrjBrowser()['mySqlData']
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

        # <editor-fold desc="添加上下文菜单">
        self.listepisodes.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.listepisodes.customContextMenuRequested.connect(
            lambda pos: self.addRightClickMenu(self.listepisodes.mapToGlobal(pos), 'episodes'))

        self.listshot.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.listshot.customContextMenuRequested.connect(
            lambda pos: self.addRightClickMenu(self.listshot.mapToGlobal(pos), "shot"))

        self.listdepartment.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.listdepartment.customContextMenuRequested.connect(
            lambda pos: self.addRightClickMenu(self.listdepartment.mapToGlobal(pos), "department"))

        self.listdepType.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.listdepType.customContextMenuRequested.connect(
            lambda pos: self.addRightClickMenu(self.listdepType.mapToGlobal(pos), "depType"))

        self.listfile.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.listfile.customContextMenuRequested.connect(
            lambda pos: self.addRightClickMenu(self.listfile.mapToGlobal(pos), "shotFile"))

        self.listAss.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.listAss.customContextMenuRequested.connect(
            lambda pos: self.addRightClickMenu(self.listAss.mapToGlobal(pos), "assFolder"))

        self.listAssType.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.listAssType.customContextMenuRequested.connect(
            lambda pos: self.addRightClickMenu(self.listAssType.mapToGlobal(pos), "assType"))

        self.listAssFile.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.listAssFile.customContextMenuRequested.connect(
            lambda pos: self.addRightClickMenu(self.listAssFile.mapToGlobal(pos), "assFile"))
        # </editor-fold>
        # 添加截图功能
        self.ass_screenshot.clicked.connect(self.Screenshot)

        # <editor-fold desc="关于shot的更新操作">
        # self.addRightClick()
        # 首先扫描根目录获得集数
        self.setepisodex()
        # 并链接函数处理下一级
        self.listepisodes.itemClicked.connect(self.listEpisodesClicked)
        # 在shot文件列表中添加点击事件更改下一级部门列表
        self.listshot.itemClicked.connect(self.listshotClicked)
        # 在department中添加下一级的更新事件
        self.listdepartment.itemClicked.connect(self.listDepartmenClicked)
        # 在depType中添加点击跟新文件事件
        self.listdepType.itemClicked.connect(self.listDepTypeClicked)
        # 在文件中添加点击事件
        self.listfile.itemClicked.connect(self.ClickedUpdataAtt)
        # </editor-fold>

        # 设置ass类型
        self.scane.clicked.connect(lambda: self.assClassSortClicked('scane'))
        self.props.clicked.connect(lambda: self.assClassSortClicked('props'))
        self.character.clicked.connect(lambda: self.assClassSortClicked('character'))
        self.effects.clicked.connect(lambda: self.assClassSortClicked('effects'))

        # 在listAss中添加点击事件生成Ass资产列表
        self.listAss.itemClicked.connect(self.assClassClicked)
        # 在listType中添加点击事件生成file列表
        self.listAssType.itemClicked.connect(self.assClassTypeClicked)
        # 在listassfile中获得资产信息
        self.listAssFile.itemClicked.connect(self.ClickedUpdataAtt)

        # 双击打开文件
        self.listfile.doubleClicked.connect(self.openShotFile)
        # 添加刷新函数
        self.refresh.triggered.connect(self.setepisodex)

    @script.doodleLog.erorrDecorator
    def addRightClickMenu(self, point: QtCore.QPoint, type: str):
        """添加右键菜单功能"""
        menu = QtWidgets.QMenu(self)
        if type == "episodes":  # 添加集数右键菜单
            add_episodes_Folder = menu.addAction('添加')
            add_episodes_Folder.triggered.connect(self.addEpisodesFolder)
        elif type == "shot":  # 添加镜头右键菜单
            if self.listepisodes.selectedItems():
                add_shot_Folder = menu.addAction('添加', )
                add_shot_Folder.triggered.connect(self.addShotFolder)
                add_ABshot_Folder = menu.addAction('添加AB镜')
                add_ABshot_Folder.triggered.connect(self.addABshotFolder)
        elif type == "department":  # 添加部门右键菜单
            if self.listshot.selectedItems():
                add_department = menu.addAction('添加')
                add_department.triggered.connect(self.addDepartmentFolder)
        elif type == "depType":  # 添加类型右键菜单
            if self.listdepartment.selectedItems():
                add_depType = menu.addAction('添加')
                add_depType.triggered.connect(self.addTypeFolder)
        elif type == 'shotFile':  # 添加文件右键菜单
            if self.listfile.selectedItems():
                open_explorer = menu.addAction('打开文件管理器')  # 用文件管理器打开文件位置
                open_explorer.triggered.connect(self.openShotExplorer)
                # copy文件名称或者路径到剪切板
                copy_name_to_clip = menu.addAction('复制名称')
                copy_name_to_clip.triggered.connect(self.copyNameToClipboard)
                copy_path_to_clip = menu.addAction('复制路径')
                copy_path_to_clip.triggered.connect(self.copyPathToClipboard)
                # 导出Fbx和abc选项
                export_maya = menu.addAction("导出")
                export_maya.triggered.connect(self.exportMaya)

        elif type == "assFolder":  # 添加资产文件夹右键菜单
            add_ass_folder = menu.addAction('添加')
            add_ass_folder.triggered.connect(self.addAssFolder)
        elif type == "assType":
            if self.listAss.selectedItems():  # 添加资产类型右键文件夹
                add_ass_type_folder = menu.addAction('添加')
                add_ass_type_folder.triggered.connect(self.addAssTypeFolder)
        elif type == "assFile":  # 添加文件右键菜单
            if self.listAssType.selectedItems():
                add_ass_file = menu.addAction('上传(提交)文件')
                add_ass_file.triggered.connect(self.uploadFiles)
                get_ass_path = menu.addAction('指定文件')
                get_ass_path.triggered.connect(self.appointFilePath)
                if self.listAssFile.selectedItems():
                    add_ass_file_dow = menu.addAction('同步UE文件')
                    open_ass_explorer = menu.addAction("打开文件管理器")
                    open_ass_explorer.triggered.connect(self.openShotExplorer)
                    add_ass_file_dow.triggered.connect(self.downloadUe4)
        else:
            pass
        menu.exec_(point)
        # menu.popup(point)

    @script.doodleLog.erorrDecorator
    def ClickedUpdataAtt(self, ass_name: str = ''):
        """更新自身属性"""
        listfile_selected_items = self.listepisodes.selectedItems()
        if listfile_selected_items:
            self.shot_episods = listfile_selected_items[0].text()[2:]
            if self.listshot.selectedItems():
                items_shot = self.listshot.selectedItems()[0].text()
                try:
                    self.shot_shot = int(items_shot[2:])
                    self.shot_shotab = ''
                except:
                    self.shot_shot = int(items_shot[2:-1])
                    self.shot_shotab = items_shot[-1:]
                if self.listdepartment.selectedItems():
                    self.shot_department = self.listdepartment.selectedItems()[0].text()
                    if self.listdepType.selectedItems():
                        self.shot_dep_type = self.listdepType.selectedItems()[0].text()
                        if self.listfile.selectedItems():
                            shot_row = self.listfile.currentRow()
                            self.shot_version = int(self.listfile.item(shot_row, 0).text()[1:])
                            self.shot_suffixes = self.listfile.item(shot_row, 3).text()
                            self.id = int(self.listfile.item(shot_row, 4).text())
        if ass_name and isinstance(ass_name, str):
            self.ass_class_sort = ass_name
        if self.listAss.selectedItems():
            self.ass_class = self.listAss.selectedItems()[0].text()
            if self.listAssType.selectedItems():
                self.ass_class_type = self.listAssType.selectedItems()[0].text()
                name = self.ass_class
                if self.ass_class_type in ['rig']:
                    name = name + '_rig'
                if self.listAssFile.selectedItems():
                    ass_row = self.listAssFile.currentRow()
                    self.ass_version = int(self.listAssFile.item(ass_row, 0).text()[1:])
                    self.ass_user = self.listAssFile.item(ass_row, 2).text()
                    self.ass_suffixes = self.listAssFile.item(ass_row, 3).text()
                    self.id = int(self.listAssFile.item(ass_row, 4).text())

    def MysqlData(self, table: DoodlePrjectState, modle="get"):
        """mysql命令,  还没完"""

        data = self.mysqlData

        if table == DoodlePrjectState.shot_episodes:
            # 生成查询ep集数命令
            sql_com = """select id,episods from mainshot"""
        elif table == DoodlePrjectState.shot_shot:
            # 生成查询shot镜头命令
            sql_com = """select distinct shot,shotab from `ep{eps:0>3d}`""".format(eps=self.shot_episods)
        elif table == DoodlePrjectState.shot_department:
            # 生成查询dep部门命令
            sql_com = """select distinct department from `ep{eps:0>3d}` where 
                episodes = {eps} and shot = {shot} and shotab = '{shotab}'""".format(
                eps=self.shot_episods,
                shot=self.shot_shot,
                shotab=self.shot_shotab)
        elif table == DoodlePrjectState.shot_dep_type:
            # 生成查询depType部门类型命令
            sql_com = """select distinct Type from `ep{eps:0>3d}` where 
                episodes = {eps} and shot = {shot} and shotab = '{shotab}' and department ='{department}'""".format(
                eps=self.shot_episods,
                shot=self.shot_shot,
                shotab=self.shot_shotab,
                department=self.shot_department)
        elif table == DoodlePrjectState.shot_file:
            sql_com = """select version, infor, user, fileSuffixes, id from `ep{eps:0>3d}` where 
                episodes = {eps} and shot = {shot} and shotab = '{shotab}' 
                and department ='{department}' and Type = '{shot_dep_type}' """.format(
                eps=self.shot_episods,
                shot=self.shot_shot,
                shotab=self.shot_shotab,
                department=self.shot_department,
                shot_dep_type=self.shot_dep_type)
        # 生成查询file文件命令
        elif table == "":
            sql_com = """"""

        file_data = script.MySqlComm.selsctCommMysql(data,
                                                     self.setlocale.department,
                                                     self.setlocale.department, sql_com)
        return file_data

    def getShotRoot(self) -> pathlib.Path:
        # 获得项目目录
        shot_root_ = self.setlocale.getseverPrjBrowser()['shotRoot']
        root = pathlib.Path(self.setlocale.project)
        # 获得根目录
        for myP in shot_root_:
            root = root.joinpath(myP)
        self.ta_log.info('根目录%s', root)
        return root

    def getAssRoot(self):
        shot_root = self.setlocale.getseverPrjBrowser()['assetsRoot']
        root = pathlib.Path(self.setlocale.project)
        for myP in shot_root:
            root = root.joinpath(myP)
        return root

    def setepisodex(self):
        self.listepisodes.clear()
        self.listshot.clear()
        self.listdepartment.clear()
        self.listdepType.clear()
        self.clearListFile()

        # region 获得服务器上数据,集数数据
        eps = self.MysqlData(DoodlePrjectState.shot_episodes)
        item = []
        for ep in eps:
            if ep[1] == 0:
                item.append('pv')
            else:
                item.append('ep{:0>3d}'.format(ep[1]))

        self.ta_log.info('更新集数列表')

        self.listepisodes.addItems(item)

    def listEpisodesClicked(self):
        items__text = self.listepisodes.selectedItems()[0].text()
        if items__text == 'pv':
            items__text = 0
        else:
            items__text = int(items__text[2:])
        self.shot_episods = items__text

        self.listdepartment.clear()
        self.listdepType.clear()
        self.clearListFile()

        self.listshot.clear()

        self.ta_log.info('更新shot列表')
        eps = self.MysqlData(DoodlePrjectState.shot_shot)
        item = []
        for ep in eps:
            try:
                item.append('sc{:0>4d}{}'.format(ep[0], ep[1]))
            except:
                item.append('sc{:0>4d}'.format(ep[0]))
        self.listshot.addItems(item)

    def listshotClicked(self):
        items_shot = self.listshot.selectedItems()[0].text()
        try:
            self.shot_shot = int(items_shot[2:])
            self.shot_shotab = ''
        except:
            self.shot_shot = int(items_shot[2:-1])
            self.shot_shotab = items_shot[-1:]

        self.listdepartment.clear()
        self.listdepType.clear()
        self.clearListFile()
        self.ta_log.info('更新Department列表')
        eps = self.MysqlData(DoodlePrjectState.shot_department)
        item = []
        for department in eps:
            item.append(department[0])

        self.listdepartment.addItems(item)

    def listDepartmenClicked(self):
        self.shot_department = self.listdepartment.selectedItems()[0].text()

        self.clearListFile()
        self.listdepType.clear()

        self.ta_log.info('更新depType列表')
        eps = self.MysqlData(DoodlePrjectState.shot_dep_type)
        item = []
        for depType in eps:
            item.append(depType[0])
        self.listdepType.addItems(item)

    def listDepTypeClicked(self):
        self.shot_dep_type = self.listdepType.selectedItems()[0].text()
        self.shot_file_path = self.shot_root.joinpath(f'ep{self.shot_episods:0>3d}',
                                                      f'sc{self.shot_shot:0>4d}',
                                                      'Scenefiles',
                                                      self.shot_department,
                                                      self.shot_dep_type
                                                      )
        # 清空上一次文件显示和版本记录和文件路径
        self.clearListFile()

        eps = self.MysqlData(DoodlePrjectState.shot_file)
        self.setFileItem(eps)

    def setFileItem(self, items):
        '''设置文件在GUI中的显示'''
        self.file_version_max = 0
        for item in items:
            mrow = 0
            tmp_version_ = int(item[0])
            if tmp_version_ > self.file_version_max:
                self.file_version_max = tmp_version_
            self.listfile.insertRow(mrow)
            self.listfile.setItem(mrow, 0, QtWidgets.QTableWidgetItem(f'v{item[0]:0>4d}'))
            self.listfile.setItem(mrow, 1, QtWidgets.QTableWidgetItem(item[1]))
            self.listfile.setItem(mrow, 2, QtWidgets.QTableWidgetItem(item[2]))
            self.listfile.setItem(mrow, 3, QtWidgets.QTableWidgetItem(item[3]))
            self.listfile.setItem(mrow, 4, QtWidgets.QTableWidgetItem(str(item[4])))
            mrow = mrow + 1
        self.ta_log.info('更新文件列表')

    def clearListFile(self):
        mrowtmp = self.listfile.rowCount()
        while mrowtmp >= 0:
            self.listfile.removeRow(mrowtmp)
            mrowtmp = mrowtmp - 1

    # </editor-fold>

    # <editor-fold desc="更新ass的各种操作">
    def assClassSortClicked(self, ass_name: str):
        self.ClickedUpdataAtt(ass_name)
        # self.assFamilyPath = self.setAssFamilyPath()
        self.ta_log.info('将资产类型设置为 %s', ass_name)

        self.listAss.clear()
        self.listAssType.clear()
        self.clearListAssFile()

        item = self.assClassItem()
        if item:
            self.listAss.addItems(item)

    def assClassClicked(self):
        self.ClickedUpdataAtt()

        self.listAssType.clear()
        self.ta_log.info('清除资产类型中的项数')
        self.clearListAssFile()
        self.ta_log.info('清除资产文件中的项数')

        item = self.assClassTypeItems()
        self.listAssType.addItems(item)

    def assClassTypeClicked(self):
        """资产类别点击事件"""
        self.ClickedUpdataAtt()
        self.ass_file_path = self.ass_root.joinpath(self.ass_class_sort,
                                                    self.ass_class,
                                                    'Scenefiles',
                                                    self.ass_class_type,
                                                    )
        self.setAssThumbnail()
        # 清空上一次文件显示和版本记录和文件路径
        self.clearListAssFile()
        file_data = self.assFileItems
        self.setAssFileItem(file_data)

    def assClassItem(self):
        ass_data_com = f"""select distinct name from `{self.ass_class_sort}` order by name"""
        data = self.mysqlData
        data = script.MySqlComm.selsctCommMysql(data,
                                                self.setlocale.department,
                                                self.setlocale.department,
                                                ass_data_com)
        item = []
        for assitem in data:
            item.append(assitem[0])
        return item

    """获得资产类别选项"""

    def assClassTypeItems(self):
        ass_type_com = f"""select distinct type from `{self.ass_class_sort}`
                                where name = '{self.ass_class}'"""
        data = self.mysqlData
        data = script.MySqlComm.selsctCommMysql(data,
                                                self.setlocale.department,
                                                self.setlocale.department,
                                                ass_type_com)
        item = []
        for asstype in data:
            item.append(asstype[0])
        return item
        # item = self.projectAnalysisAss.getAssTypeItems(self)

    '''获得ass服务器上的文件信息'''

    @property
    def assFileItems(self):
        '''获得ass服务器上的文件信息'''

        ass_type_com = f"""select distinct version,infor,user,fileSuffixes,id from `{self.ass_class_sort}`
                                where name = '{self.ass_class}'
                                and type = '{self.ass_class_type}'"""
        data = self.mysqlData
        file_data = script.MySqlComm.selsctCommMysql(data,
                                                     self.setlocale.department,
                                                     self.setlocale.department,
                                                     ass_type_com)
        return file_data
        # return self.projectAnalysisAss.

    """设置资产文件在GUI中的显示"""

    def setAssFileItem(self, file_data):
        """设置资产文件在GUI中的显示"""
        self.Ass_version_max = 0
        for item in file_data:
            mrow = 0
            tmp_version_ = item[0]
            if tmp_version_ > self.Ass_version_max:
                self.Ass_version_max = tmp_version_
            self.listAssFile.insertRow(mrow)
            self.listAssFile.setItem(mrow, 0, QtWidgets.QTableWidgetItem(f'v{item[0]:0>4d}'))
            self.listAssFile.setItem(mrow, 1, QtWidgets.QTableWidgetItem(item[1]))
            self.listAssFile.setItem(mrow, 2, QtWidgets.QTableWidgetItem(item[2]))
            self.listAssFile.setItem(mrow, 3, QtWidgets.QTableWidgetItem(item[3]))
            self.listAssFile.setItem(mrow, 4, QtWidgets.QTableWidgetItem(str(item[4])))
            mrow = mrow + 1
        self.ta_log.info('更新文件列表')

    """清理资产文件列表"""

    def clearListAssFile(self):
        mrowtmp = self.listAssFile.rowCount()
        while mrowtmp >= 0:
            self.listAssFile.removeRow(mrowtmp)
            mrowtmp = mrowtmp - 1

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
                    if self.shot_file_path:
                        dstFile = self.getFileName(path.suffix)  # type:pathlib.Path
                        self.shot_file_path.mkdir(parents=True, exist_ok=True)
                        shutil.copy2(str(path), str(dstFile))
                        self.ta_log.info('%s ---> %s', path, dstFile)
                        self.subMissionShotInfor(self.file_version_max + 1, path.suffix)
                    # print(path)
                if path.suffix in ['.fbx', '.usd']:
                    if self.shot_file_path:
                        dstFile = self.getFileName(path.suffix, True)  # type:pathlib.Path
                        self.shot_file_path.mkdir(parents=True, exist_ok=True)
                        shutil.copy2(str(path), str(dstFile))
                        self.ta_log.info('%s ---> %s', path, dstFile)
                        self.subMissionShotInfor(self.file_version_max, path.suffix)

                self.listDepTypeClicked()
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
        filename['file_episods'] = f'ep{self.shot_episods:0>3d}'
        filename['file_shot'] = f'sc{self.shot_shot:0>4d}'
        filename['file_department'] = self.shot_department
        filename['file_Deptype'] = self.shot_dep_type
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
        self.shot_name = filename
        print(self.shot_file_path)
        path = self.shot_file_path.joinpath(self.shot_name)
        return path

    # </editor-fold>
    def subMissionShotInfor(self, version, file_suffixes, shot_file_path='', shot_name="", infor=""):
        """提交shot信息"""
        if not shot_file_path:
            shot_file_path = self.shot_file_path
        if not shot_name:
            shot_name = self.shot_name
        as_posix = shot_file_path.joinpath(shot_name).as_posix()
        shot_data = f"""insert into ep{self.shot_episods:0>3d}(episodes, 
                            shot, 
                            shotab,
                            department, 
                            Type, 
                            file, 
                            fileSuffixes, 
                            user, 
                            version, 
                            filepath,
                            infor) VALUE({self.shot_episods},
                            {self.shot_shot},
                            '{self.shot_shotab}',
                            '{self.shot_department}',
                            '{self.shot_dep_type}',
                            '{self.shot_name}',
                            '{file_suffixes}',
                            '{self.setlocale.user}',
                            {version},
                            '{as_posix}',
                            '{infor}') 
                            """
        script.MySqlComm.inserteCommMysql(self.mysqlData,
                                          '', '', shot_data)

    # <editor-fold desc="添加集数文件夹的操作都在这里">

    def addEpisodesFolder(self):
        """添加集数文件夹并提交数据库"""
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
            script.MySqlComm.inserteCommMysql(self.mysqlData, '', '', create_date)
            script.MySqlComm.inserteCommMysql(self.mysqlData, '', '',
                                              create_date_insert)

            self.setepisodex()

    def addShotFolder(self):
        """添加镜头"""
        shot = QtWidgets.QInputDialog.getInt(self, '输入镜头', "sc", 1, 1, 999, 1)[0]
        if shot and self.listepisodes.selectedItems():
            self.listshot.addItem('sc{:0>4d}'.format(shot))

    def addABshotFolder(self):
        """添加ab镜"""
        items = ['B', 'C', 'D', 'E']
        shotAB = QtWidgets.QInputDialog.getItem(self, '选择AB镜头', '要先选择镜头才可以', items, 0, False)[0]
        shot = self.shot_shot
        if shotAB and self.listshot.selectedItems():
            self.listshot.addItem('sc{:0>4d}{}'.format(shot, shotAB))

    def addDepartmentFolder(self):
        """添加部门文件"""
        department = self.setlocale.department
        if self.shot_shot and self.listshot.selectedItems():
            self.listdepartment.addItem(department)

    def addTypeFolder(self):
        """添加类型文件"""
        deptype = QtWidgets.QInputDialog.getText(self, '输入镜头', "文件类型(请用英文或拼音)",
                                                 QtWidgets.QLineEdit.Normal)[0]
        if deptype and self.listdepartment:
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
        items[2] = items[2].format(self.ass_class)
        ass_type = QtWidgets.QInputDialog.getItem(self, '选择资产类型', '要先选择资产', items, 0, False)[0]
        if ass_type and self.listAss.selectedItems():
            self.listAssType.addItem(ass_type)

    def uploadFiles(self):
        """上传资产文件"""
        file, fileType = QtWidgets.QFileDialog.getOpenFileName(self,
                                                               "选择上传文件",
                                                               self.recentlyOpenedFolder,
                                                               "files (*.mb *.ma *.uproject *.max *.fbx *.png *.tga *.jpg)")
        remarks_info = self.recentlyOpenedFolder = QtWidgets.QInputDialog.getText(self,
                                                                                  "填写备注(中文)",
                                                                                  "备注",
                                                                                  QtWidgets.QLineEdit.Normal)[0]

        self.recentlyOpenedFolder = file

        if file and self.listAssType.selectedItems():
            file = pathlib.Path(file)
            if file.suffix in ['.mb', '.ma', '.max', '.fbx']:
                version_max = self.assUploadFileHandle(file)
                self.subMissionAssInfor(version_max, file.suffix, infor=remarks_info)
            elif file.suffix in ['.uproject']:
                self.assUploadFileUE4Handle(file)
                self.subMissionAssInfor(self.file_version_max, '.uproject', infor=remarks_info)
            elif file.suffix in ['.png', '.tga', 'jpg']:
                version_max = self.assUploadMapHandle(file)
                self.subMissionAssInfor(version_max, file.suffix, infor=remarks_info)
            else:
                pass
        self.assClassTypeClicked()

    @script.doodleLog.erorrDecorator
    def assUploadMapHandle(self, file: pathlib.Path):
        version = self.getAssMaxVersion() + 1
        file_path = file.parent
        target_file: pathlib.Path = self.ass_file_path
        file_str = f'^{self.ass_class}_.*_(?:Color|Normal|bump|alpha)$'

        sub = False
        for fi in file_path.iterdir():
            if re.match(file_str, fi.stem):
                tar = target_file.joinpath(fi.name)
                self.backupCopy(fi, tar, version)
                sub = True
        return version

    @script.doodleLog.erorrDecorator
    def backupCopy(self, source: pathlib.Path, target: pathlib.Path, version: int):
        """来源和目标必须时文件 + 路径"""
        backup = self.ass_file_path.joinpath('backup')
        self.ass_file_path.mkdir(parents=True, exist_ok=True)
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

    @script.doodleLog.erorrDecorator
    def subMissionAssInfor(self, version, file_suffixes, ass_file_path="", ass_file_name="", infor=''):
        if not ass_file_name:
            ass_file_name = self.ass_file_name
        if not ass_file_path:
            ass_file_path = self.ass_file_path
        as_path = ass_file_path.joinpath(ass_file_name + file_suffixes).as_posix()
        ass_data = f"""insert into `{self.ass_class_sort}`( name, 
                                    type,
                                    file,
                                    fileSuffixes, 
                                    user, 
                                    version,
                                    infor,
                                    filepath) VALUE('{self.ass_class}',
                                    '{self.ass_class_type}',
                                    '{self.ass_file_name}',
                                    '{file_suffixes}',
                                    '{self.setlocale.user}',
                                    {version},
                                    '{infor}',
                                    '{as_path}'
                                    ) 
                                    """
        script.MySqlComm.inserteCommMysql(self.mysqlData,
                                          '', '', ass_data)

    def getAssMaxVersion(self):
        ass_type_com = f"""select distinct version from `{self.ass_class_sort}`
                                where name = '{self.ass_class}'
                                and type = '{self.ass_class_type}'
                                order by version desc;"""
        data = self.mysqlData
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
        """
        :type self: script.ProjectBrowserGUI.ProjectBrowserGUI
        """
        version_max = self.getAssMaxVersion()
        target_file: pathlib.Path = self.ass_file_path.joinpath('{}{}'.format(self.ass_class,
                                                                              file_path.suffix))

        if file_path.suffix in ['.mb', '.ma', '.max']:
            version_max = version_max + 1
            self.backupCopy(file_path, target_file, version_max)
        if file_path.suffix in ['.fbx']:
            self.backupCopy(file_path, target_file, version_max)
        return version_max

    def assUploadFileUE4Handle(self, file_path: pathlib.Path):
        """
        :type self: script.ProjectBrowserGUI.ProjectBrowserGUI
        """
        version_max = self.getAssMaxVersion() + 1
        backup = self.ass_file_path.joinpath('backup')
        source = file_path.parent
        target: pathlib.Path = self.ass_file_path
        syn_path = [{'Left': str(source), 'Right': str(target)}]
        syn_file = script.synXml.weiteXml(self.setlocale.doc,
                                          syn_path,
                                          Include=['*\\Content\\*'],
                                          Exclude=['*\\backup\\'],
                                          VersioningFolder=str(backup),
                                          fileName='UEpriect')
        program = self.setlocale.FreeFileSync
        cmd = os.system('{} "{}"'.format(program, syn_file))
        self.file_version_max = version_max
        shutil.copy2(str(file_path), str(self.ass_file_path.joinpath(self.ass_file_name + '.uproject')))

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
        if file and (self.listAssType.selectedItems() or self.listdepType.selectedItems()):
            file = pathlib.Path(file)
            if self.listdepType.selectedItems():
                self.subMissionShotInfor(self.file_version_max + 1, file.suffix, file.parent, str(file.stem),
                                         remarks_info)
            elif self.listAssType.selectedItems():
                self.subMissionAssInfor(self.Ass_version_max + 1, file.suffix, file.parent, str(file.stem),
                                        remarks_info)

    # </editor-fold>

    # <editor-fold desc="各种对于文件的操作">

    def combinationFilePath(self):
        # 这个用来组合文件和文件命
        filename = self.shot_name
        filepath = self.shot_file_path.joinpath(filename)
        return filepath

    def openShotExplorer(self):
        filePath = self.getMysqlFileNameAndPath().parent
        self.ta_log.info('打开path %s', filePath)
        os.startfile(str(filePath))
        return None

    def openShotFile(self):
        filePath = self.getMysqlFileNameAndPath()
        os.startfile(str(filePath))

    def getMysqlFileNameAndPath(self):
        if self.listfile.selectedItems():
            shot_path_get = f"""select distinct filepath from `ep{self.shot_episods:0>3d}`
                                    where episodes = {self.shot_episods}
                                    and shot = {self.shot_shot}
                                    and shotab = '{self.shot_shotab}'
                                    and department = '{self.shot_department}'
                                    and Type = '{self.shot_dep_type}'
                                    and version = {self.shot_version}
                                    and fileSuffixes = '{self.shot_suffixes}'
                                    """
            data = self.mysqlData
            file_data = script.MySqlComm.selsctCommMysql(data,
                                                         self.setlocale.department,
                                                         self.setlocale.department,
                                                         shot_path_get)
        else:
            ass_path_get = f"""select distinct filepath from `character`
                                    where name = '{self.ass_class}'
                                    and type = '{self.ass_class_type}'
                                    and version = {self.ass_version}
                                    and user = '{self.ass_user}'
                                    and fileSuffixes = '{self.ass_suffixes}'
                                    """
            data = self.mysqlData
            file_data = script.MySqlComm.selsctCommMysql(data,
                                                         self.setlocale.department,
                                                         self.setlocale.department,
                                                         ass_path_get)
        try:
            filePath = pathlib.Path(file_data[0][0])
        except:
            filePath = pathlib.Path('')
        return filePath

    def copyNameToClipboard(self):
        # 这个函数不好用记得改
        filePath = self.getMysqlFileNameAndPath().parent
        pyperclip.copy(str(filePath.name))
        self.ta_log.info('复制 %s 到剪切板', str(self.shot_name))

    def copyPathToClipboard(self):
        filePath = self.getMysqlFileNameAndPath().parent
        pyperclip.copy(str(filePath.parent))
        self.ta_log.info('复制 %s 到剪切板', str(self.shot_file_path))

    def exportMaya(self):
        sql = """select distinct filepath from `ep{shot_ep:>03d}`
                      where id = '{id}'
                      limit 1""".format(shot_ep=self.shot_episods,
                                        id=self.id)
        logging.info(sql)
        data = self.mysqlData
        file_data = script.MySqlComm.selsctCommMysql(data,
                                                     self.setlocale.department,
                                                     self.setlocale.department,
                                                     sql)
        logging.info(file_data)
        try:
            file_data = file_data[0][0]
        except:
            pass
        else:
            export_maya = script.MayaExportCam.export(file_data)
            export_maya.exportCam()

    def Screenshot(self):
        path: pathlib.Path = self.ass_root.joinpath(self.ass_class_sort,
                                                    self.ass_class,
                                                    'Playblasts',
                                                    self.ass_class_type,
                                                    "Screenshot",
                                                    f"{self.ass_class}_{self.ass_version}.jpg"
                                                    )
        if not path.parent.is_dir():
            path.parent.mkdir(parents=True, exist_ok=True)

        screen_shot = script.doodlePlayer.doodleScreenshot(path=str(path))
        self.hide()
        screen_shot.exec_()
        self.show()
        self.subMissionAssInfor(0, ".jpg", path.parent, path.stem, "这是截图")

    def setAssThumbnail(self):
        sql_com = """select distinct filepath from `{character}`
                      where name = '{name}'
                      and type = '{type}'
                      and fileSuffixes = '{fileSuffixes}'
                      and user = '{user}'
                      limit 1""".format(character=self.ass_class_sort,
                                        name=self.ass_class,
                                        type=self.ass_class_type,
                                        fileSuffixes='.jpg',
                                        user=self.setlocale.user)
        data = self.mysqlData
        file_data = script.MySqlComm.selsctCommMysql(data,
                                                     self.setlocale.department,
                                                     self.setlocale.department,
                                                     sql_com)
        try:
            path: pathlib.Path = file_data[0][0]
        except:
            pass
        else:
            pixmap = QtGui.QPixmap(str(path))
            pixmap = pixmap.scaled(self.ass_thumbnail.geometry().size(), QtCore.Qt.KeepAspectRatio)
            self.ass_thumbnail.setPixmap(pixmap)

    # </editor-fold>


if __name__ == '__main__':
    # department = DoodlePrjectState.shot_department.value
    # print(department)
    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet(qdarkgraystyle.load_stylesheet())
    w = ProjectBrowserGUI()
    w.setWindowTitle("Remer")
    w.show()

    sys.exit(app.exec_())
