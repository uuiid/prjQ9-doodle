# -*- coding: UTF-8 -*-
import logging
import os
import pathlib
import re
import shutil
import sys
import tempfile
import typing

import potplayer
import pyperclip
import pypinyin
import qdarkgraystyle
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets

import UiFile.ProjectBrowser
import script.DooDlePrjCode
import script.MayaExportCam
import script.MySqlComm
import script.convert
import script.debug
import script.doodleLog
import script.doodlePlayer
import script.doodle_setting
import script.synXml
import script.synchronizeFiles



class ProjectBrowserGUI(QtWidgets.QMainWindow, UiFile.ProjectBrowser.Ui_MainWindow):
    '''
    这个类用来实现项目管理的属性和UI操作,  其中会有一个项目分析器在外部, 有每个项目分别配置或者使用默认设置
    '''

    user: str

    def __init__(self, parent=None):
        super(ProjectBrowserGUI, self).__init__()
        # 获取设置

        self.setlocale = script.doodle_setting.Doodlesetting()
        """======================================================================="""
        # 导入解析项目模块
        self.shot = script.DooDlePrjCode.PrjShot(self.setlocale.projectname,
                                                 self.setlocale.project,
                                                 self.setlocale.shotRoot)
        self.ass = script.DooDlePrjCode.PrjAss(self.setlocale.projectname,
                                               self.setlocale.project,
                                               self.setlocale.assetsRoot)
        """======================================================================="""
        # 初始化一些属性
        self.user = pypinyin.slug(self.setlocale.user, pypinyin.NORMAL)
        self.recentlyOpenedFolder = ""
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
        self.listAssFile.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        # 开启窗口拖拽事件
        self.setAcceptDrops(True)
        # self.listepisodes.setAcceptDrops

        # 设置tabWigget点击清除事件
        self.tabWidget.currentChanged['int'].connect(lambda index: self.tabWigetClick(index))

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
        self.ass_screenshot.clicked.connect(lambda: self.Screenshot("ass", self.ass_thumbnail))
        self.shot_screenshots.clicked.connect(lambda: self.Screenshot("shot", self.shot_thumbnail))
        # 添加上传拍屏功能
        self.shot_upload.clicked.connect(lambda: self.uploadFlipBook(self.shot))
        self.ass_upload.clicked.connect(lambda: self.uploadFlipBook(self.ass))

        # 打开拍屏功能
        self.ass_player.clicked.connect(lambda: self.playerButtenClicked(one_or_mut="one"))
        self.shot_player.clicked.connect(lambda: self.playerButtenClicked(one_or_mut="one"))

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
        self.listfile.itemClicked.connect(self.shotFileClicked)
        # </editor-fold>

        # 设置ass类型
        self.scane.clicked.connect(lambda: self.assClassSortClicked('scane'))
        self.props.clicked.connect(lambda: self.assClassSortClicked('props'))
        self.character.clicked.connect(lambda: self.assClassSortClicked('character'))
        self.effects.clicked.connect(lambda: self.assClassSortClicked('effects'))

        # 在listAss中添加点击事件生成Ass资产列表
        self.listAss.itemClicked.connect(lambda item: self.assClassClicked(item))
        # 在listType中添加点击事件生成file列表
        self.listAssType.itemClicked.connect(self.assClassTypeClicked)
        # 在listassfile中获得资产信息
        self.listAssFile.itemClicked.connect(self.assFileClicked)

        # 双击打开文件
        self.listfile.doubleClicked.connect(self.openShotFile)
        # 添加刷新函数
        self.refresh.triggered.connect(self.setepisodex)

        self.pot_player = potplayer.PlayList()

    def tabWigetClick(self, index: int):
        if index == 0:
            logging.info("点击资产")
            self.setepisodex()
        elif index == 1:
            logging.info("点击镜头")
            self.assClassSortClicked("character")

    # <editor-fold desc="菜单项">
    def menuEpisodes(self, menu):
        add_episodes_folder = menu.addAction('添加')
        add_player = menu.addMenu("播放整集拍屏")
        add_episodes_folder.triggered.connect(self.addEpisodesFolder)
        anm_player = add_player.addAction("播放Anm拍屏")
        vfx_player = add_player.addAction("播放vfx拍屏")
        light_player = add_player.addAction("播放light拍屏")
        anm_player.triggered.connect(lambda: self.playerButtenClicked("mut", "Anm"))
        vfx_player.triggered.connect(lambda: self.playerButtenClicked("mut", "VFX"))
        light_player.triggered.connect(lambda: self.playerButtenClicked("mut", "Light"))
        return menu

    def menuShot(self, menu):
        if self.listepisodes.selectedItems():
            add_shot_folder = menu.addAction('添加', )
            add_shot_folder.triggered.connect(self.addShotFolder)
            add_a_bshot_folder = menu.addAction('添加AB镜')
            add_a_bshot_folder.triggered.connect(self.addABshotFolder)
        return menu

    def menuDepartment(self, menu):
        if self.listshot.selectedItems():
            add_department = menu.addAction('添加')
            add_department.triggered.connect(self.addDepartmentFolder)
        return menu

    def menuDeptype(self, menu):
        add_depType = menu.addAction('添加')
        add_depType.triggered.connect(self.addTypeFolder)
        return menu

    def menuShotfile(self, menu):
        if self.listfile.selectedItems():
            open_explorer = menu.addAction('打开文件管理器')  # 用文件管理器打开文件位置
            open_explorer.triggered.connect(lambda: self.openShotExplorer(self.shot))
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
        return menu

    def menuAsstype(self, menu):
        if self.listAss.selectedItems():  # 添加资产类型右键文件夹
            add_ass_type_folder = menu.addAction('添加')
            add_ass_type_folder.triggered.connect(self.addAssTypeFolder)
        return menu

    def menuAssfile(self, menu):
        if self.listAssType.selectedItems():
            add_ass_file = menu.addAction('上传(提交)文件')
            add_ass_file.triggered.connect(self.uploadFiles)
            get_ass_path = menu.addAction('指定文件')
            get_ass_path.triggered.connect(self.appointFilePath)
            if self.listAssFile.selectedItems():
                add_ass_file_dow = menu.addAction('同步UE文件')
                open_ass_explorer = menu.addAction("打开文件管理器")
                open_ass_explorer.triggered.connect(lambda: self.openShotExplorer(self.ass))
                add_ass_file_dow.triggered.connect(self.downloadUe4)
        return menu

    @script.doodleLog.erorrDecorator
    def addRightClickMenu(self, point: QtCore.QPoint, type: str):
        """添加右键菜单功能"""
        menu = QtWidgets.QMenu(self)
        try:
            menu = getattr(self, "menu" + type.capitalize())(menu)
        except AttributeError as err:
            logging.info("寻找不到属性了 %s", err)
        menu.exec_(point)

    # menu.popup(point)

    # </editor-fold>

    # <editor-fold desc="镜头更新事件">
    def setepisodex(self):
        self.listepisodes.clear()
        self.listshot.clear()
        self.listdepartment.clear()
        self.listdepType.clear()
        self.clearListFile()

        self.shot_thumbnail.clear()

        logging.info('更新集数列表')

        self.listepisodes.addItems(self.shot.getEpsodes())

    def listEpisodesClicked(self):
        items__text = self.listepisodes.selectedItems()[0].text()
        if items__text == 'pv':
            items__text = 0
        else:
            items__text = int(items__text[2:])
        self.shot.episodes = items__text

        self.listdepartment.clear()
        self.listdepType.clear()
        self.clearListFile()

        self.listshot.clear()
        self.shot_thumbnail.clear()

        logging.info('更新shot列表')

        self.listshot.addItems(self.shot.getShot())

    def listshotClicked(self):
        items_shot = self.listshot.selectedItems()[0].text()
        try:
            self.shot.shot = int(items_shot[2:])
            self.shot.shotab = ''
        except:
            self.shot.shot = int(items_shot[2:-1])
            self.shot.shotab = items_shot[-1:]

        self.listdepartment.clear()
        self.listdepType.clear()
        self.clearListFile()
        self.shot_thumbnail.clear()

        logging.info('更新Department列表')

        self.listdepartment.addItems(self.shot.getDepartment())

    def listDepartmenClicked(self):
        self.shot.department = self.listdepartment.selectedItems()[0].text()

        self.clearListFile()
        self.listdepType.clear()
        self.shot_thumbnail.clear()

        self.listdepType.addItems(self.shot.getDepType())

    def listDepTypeClicked(self):
        self.shot.Type = self.listdepType.selectedItems()[0].text()

        # 清空上一次文件显示和版本记录和文件路径
        self.clearListFile()

        self.setFileItem(self.shot.getFile())

        # self.setThumbnail("shot", self.shot_thumbnail)

    def shotFileClicked(self):
        shot_row = self.listfile.currentRow()
        self.shot.version = int(self.listfile.item(shot_row, 0).text()[1:])
        self.shot.suffix = self.listfile.item(shot_row, 3).text()
        self.shot.query_id = int(self.listfile.item(shot_row, 4).text())

    def setFileItem(self, items):
        """
        设置文件在GUI中的显示
        """
        for index, item in enumerate(items):
            self.listfile.insertRow(index)
            self.listfile.setItem(index, 0, QtWidgets.QTableWidgetItem(f'v{item[0]:0>4d}'))
            self.listfile.setItem(index, 1, QtWidgets.QTableWidgetItem(item[1]))
            self.listfile.setItem(index, 2, QtWidgets.QTableWidgetItem(item[2]))
            self.listfile.setItem(index, 3, QtWidgets.QTableWidgetItem(item[3]))
            self.listfile.setItem(index, 4, QtWidgets.QTableWidgetItem(str(item[4])))
        logging.info('更新文件列表')

    def clearListFile(self):
        mrowtmp = self.listfile.rowCount()
        while mrowtmp >= 0:
            self.listfile.removeRow(mrowtmp)
            mrowtmp = mrowtmp - 1

    # </editor-fold>

    # <editor-fold desc="更新ass的各种操作">
    def assClassSortClicked(self, ass_name: str):
        self.ass.sort = ass_name
        # self.assFamilyPath = self.setAssFamilyPath()
        logging.info('将资产类型设置为 %s', ass_name)

        self.listAss.clear()
        self.listAssType.clear()
        self.clearListAssFile()

        self.ass_thumbnail.clear()

        # 通过mySql命令获得数据
        self.listAss.addItems(self.ass.getAssClass())

    def assClassClicked(self, item):
        self.ass.ass_class = item.text()  # self.listAssType.selectedItems()[0].text()

        self.listAssType.clear()
        logging.info('清除资产类型中的项数')
        self.clearListAssFile()
        logging.info('清除资产文件中的项数')

        self.ass_thumbnail.clear()
        self.listAssType.addItems(self.ass.getAssType())

    def assClassTypeClicked(self):
        """资产类别点击事件"""
        self.ass.type = self.listAssType.selectedItems()[0].text()
        self.setThumbnail("ass", self.ass_thumbnail)
        # 清空上一次文件显示和版本记录和文件路径
        self.clearListAssFile()

        self.setAssFileItem(self.ass.getFileInfo())

    def assFileClicked(self):
        ass_row = self.listAssFile.currentRow()
        self.ass.version = int(self.listAssFile.item(ass_row, 0).text()[1:])
        # self.ass.user = self.listAssFile.item(ass_row, 2).text()
        # self.ass.suffixes = self.listAssFile.item(ass_row, 3).text()
        self.ass.query_id = int(self.listAssFile.item(ass_row, 4).text())

    def setAssFileItem(self, file_data):
        """设置资产文件在GUI中的显示"""
        for index, item in enumerate(file_data):
            self.listAssFile.insertRow(index)

            self.listAssFile.setItem(index, 0, QtWidgets.QTableWidgetItem(f'v{item[0]:0>4d}'))
            self.listAssFile.setItem(index, 1, QtWidgets.QTableWidgetItem(item[1]))
            self.listAssFile.setItem(index, 2, QtWidgets.QTableWidgetItem(item[2]))
            self.listAssFile.setItem(index, 3, QtWidgets.QTableWidgetItem(item[3]))
            self.listAssFile.setItem(index, 4, QtWidgets.QTableWidgetItem(str(item[4])))

        logging.info('更新文件列表')

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
                logging.info('检测到文件%s拖入窗口', path)
                # 获得文件路径并进行复制

                version = self.shot.getMaxVersion()
                if path.suffix in ['.ma', '.mb', '.hip']:
                    version += 1

                file_path = self.shot.getFilePath()
                shot_name = self.shot.getFileName(version=version, user_=self.user, suffix=path.suffix)
                dst_file = file_path.joinpath(shot_name)

                # 在这里copy
                file_path.mkdir(parents=True, exist_ok=True)
                shutil.copy2(str(path), str(dst_file))

                logging.info('%s ---> %s', path, dst_file)

                self.shot.file = shot_name
                self.shot.fileSuffixes = path.suffix
                self.shot.user = self.user
                self.shot.version = version
                self.shot.filepath = dst_file.as_posix()
                self.shot.infor = ""
                self.shot.submitInfo()
                # self.shot.submitInfo(filename=shot_name,
                #                      suffix=path.suffix, user=self.user,
                #                      version=version,
                #                      filepathAndname=dst_file.as_posix(),
                #                      infor="")
                self.listDepTypeClicked()
                self.enableBorder(False)
            else:
                pass
        else:
            a0.ignore()

    # </editor-fold>

    # <editor-fold desc="添加集数文件夹的操作都在这里">

    def addEpisodesFolder(self):
        """添加集数文件夹并提交数据库"""
        episode: int = QtWidgets.QInputDialog.getInt(self, '输入集数', "ep", 1, 1, 999, 1)[0]
        if episode:
            self.shot.subEpisodesInfo(episodes=episode)
            self.setepisodex()

    def addShotFolder(self):
        """添加镜头"""
        shot = QtWidgets.QInputDialog.getInt(self, '输入镜头', "sc", 1, 1, 999, 1)[0]
        if shot and self.listepisodes.selectedItems():
            self.listshot.addItem('sc{:0>4d}'.format(shot))

    def addABshotFolder(self):
        """添加ab镜"""
        items = ['B', 'C', 'D', 'E']
        shot_ab = QtWidgets.QInputDialog.getItem(self, '选择AB镜头', '要先选择镜头才可以', items, 0, False)[0]
        shot = self.shot.shot
        if shot_ab and self.listshot.selectedItems():
            self.listshot.addItem('sc{:0>4d}{}'.format(shot, shot_ab))

    def addDepartmentFolder(self):
        """添加部门文件"""
        department = self.setlocale.department
        if self.listshot.selectedItems():
            self.listdepartment.addItem(department)

    def addTypeFolder(self):
        """添加类型文件"""
        deptype = QtWidgets.QInputDialog.getText(self, '输入镜头', "文件类型(请用英文或拼音)",
                                                 QtWidgets.QLineEdit.Normal)[0]
        if deptype and self.listdepartment.selectedItems():
            self.listdepType.addItem(deptype)

    def addAssFolder(self):
        """添加资产类型文件夹"""
        ass_folder = QtWidgets.QInputDialog.getText(self, '输入资产类型', "请用英文或拼音",
                                                    QtWidgets.QLineEdit.Normal)[0]
        if ass_folder:
            self.listAss.addItem(ass_folder)

    def addAssTypeFolder(self):
        """添加资产文件夹类型"""

        items: typing.List[str] = self.setlocale.assTypeFolder.copy()
        items[2] = items[2].format(self.ass.name)
        ass_type = QtWidgets.QInputDialog.getItem(self, '选择资产类型', '要先选择资产', items, 0, False)[0]
        if ass_type and self.listAss.selectedItems():
            self.listAssType.addItem(ass_type)

    def uploadFiles(self):
        """
        上传资产文件 弹出选项框
        :return:
        """
        file, file_type = QtWidgets.QFileDialog.getOpenFileName(self,
                                                                "选择上传文件",
                                                                self.recentlyOpenedFolder,
                                                                "files (*.mb *.ma *.uproject *.max "
                                                                "*.fbx *.png *.tga *.jpg)")
        remarks_info = self.recentlyOpenedFolder = QtWidgets.QInputDialog.getText(self,
                                                                                  "填写备注(中文)",
                                                                                  "备注",
                                                                                  QtWidgets.QLineEdit.Normal)[0]
        self.recentlyOpenedFolder = file
        if file and self.listAssType.selectedItems():
            file = pathlib.Path(file)
            version_max = self.ass.getMaxVersion() + 1
            target_file = self.ass.getFilePath().joinpath(self.ass.getFileName(version=version_max,
                                                                               user_=self.user,
                                                                               suffix=file.suffix))

            if file.suffix in ['.mb', '.ma', '.max']:
                self.backupCopy(file, target_file, version_max)
            elif file.suffix in [".fbx"]:
                version_max -= 1
                self.backupCopy(file, target_file, version_max)
            elif file.suffix in ['.uproject']:
                self.assUploadFileUE4Handle(file, target_file)
            elif file.suffix in ['.png', '.tga', 'jpg']:
                self.assUploadMapHandle(file, target_file, version_max)
            else:
                pass
            self.ass.file = target_file.name
            self.ass.fileSuffixes = target_file.suffix
            self.ass.user = self.user
            self.ass.version = version_max
            self.ass.filepath = target_file.as_posix()
            self.ass.infor = remarks_info
            self.ass.submitInfo(target_file.name, target_file.stem, self.user, version_max,
                                infor=remarks_info, filepath_and_name=target_file.as_posix())

        self.assClassTypeClicked()

    @script.doodleLog.erorrDecorator
    def assUploadMapHandle(self, soure_file: pathlib.Path, target: pathlib.Path, version: int):
        """
        上传贴图文件
        :param version:
        :param target:
        :param soure_file: pathlib.Path
        :return: int
        """
        file_path = soure_file.parent
        file_str = f'^{self.ass.name}_.*_(?:Color|Normal|bump|alpha)$'

        for fi in file_path.iterdir():
            if re.match(file_str, fi.stem):
                tar = target.parent.joinpath(fi.name)
                self.backupCopy(fi, tar, version)

    @script.doodleLog.erorrDecorator
    def backupCopy(self, source: pathlib.Path, target: pathlib.Path, version: int):
        """
        来源和目标必须时文件 + 路径
        :param source: pathlib.Path
        :param target: pathlib.Path
        :param version: int
        :return: Nore
        """
        target_parent = target.parent
        backup = target_parent.joinpath('backup')
        target_parent.mkdir(parents=True, exist_ok=True)
        if not backup.is_dir():
            backup.mkdir(parents=True, exist_ok=True)
        backup_file = backup.joinpath('{}_v{:0>4d}{}'.format(target.stem,
                                                             version,
                                                             target.suffix))
        if target.is_file():
            shutil.move(str(target), str(backup_file))
            logging.info('文件备份%s ---->  %s', target, backup_file)
        shutil.copy2(str(source), str(target))

        logging.info('文件上传%s ---->  %s', source, target)

    def downloadUe4(self):
        pass
        # path = QtWidgets.QFileDialog.getExistingDirectory(self,
        #                                                   "选择同步目录",
        #                                                   self.recentlyOpenedFolder,
        #                                                   QtWidgets.QFileDialog.ShowDirsOnly)

    def assUploadFileUE4Handle(self, source_path: pathlib.Path, target_file: pathlib.Path):
        """
        上传ue4项目
        """
        target: pathlib.Path = target_file.parent
        backup = target.joinpath('backup')
        source = source_path.parent
        syn_path = [{'Left': str(source), 'Right': str(target)}]
        syn_file = script.synXml.weiteXml(self.setlocale.doc,
                                          syn_path,
                                          Include=['*\\Content\\*'],
                                          Exclude=['*\\backup\\'],
                                          VersioningFolder=str(backup),
                                          fileName='UEpriect')
        program = self.setlocale.FreeFileSync
        os.system('{} "{}"'.format(program, syn_file))
        shutil.copy2(str(source_path), str(target_file.stem + '.uproject'))

    def appointFilePath(self):
        """指定文件路径"""
        file, file_type = QtWidgets.QFileDialog.getOpenFileName(self,
                                                                "选择上传文件",
                                                                self.recentlyOpenedFolder,
                                                                "files (*.mb *.ma *.uproject"
                                                                " *.max *.fbx *.png *.tga *.jpg)")

        remarks_info = QtWidgets.QInputDialog.getText(self,
                                                      "填写备注(中文)",
                                                      "备注",
                                                      QtWidgets.QLineEdit.Normal)[0]
        if file and (self.listAssType.selectedItems() or self.listdepType.selectedItems()):
            file = pathlib.Path(file)

            if self.listdepType.selectedItems():
                version: int = self.shot.getMaxVersion() + 1
                self.shot.file = file.name
                self.shot.fileSuffixes = file.suffix
                self.shot.user = self.user
                self.shot.version = version
                self.shot.filepath = file.as_posix()
                self.shot.infor = remarks_info
                self.shot.submitInfo(file.name, file.suffix, self.user, version, file.as_posix(), remarks_info)

            elif self.listAssType.selectedItems():
                version: int = self.ass.getMaxVersion() + 1

                self.ass.file = file.name
                self.ass.fileSuffixes = file.suffix
                self.ass.user = self.user
                self.ass.version = version
                self.ass.filepath = file.as_posix()
                self.ass.infor = remarks_info

                self.ass.submitInfo(file.name, file.suffix, self.user, version,
                                    filepath_and_name=file.as_posix(), infor=remarks_info)

    # </editor-fold>

    # <editor-fold desc="各种对于文件的操作">
    def openShotExplorer(self,core:script.DooDlePrjCode.PrjCode):
        p = core
        file_path = p.queryFileName(p.query_id).parent
        logging.info('打开path %s', file_path)
        try:
            os.startfile(str(file_path))
        except BaseException as err:
            logging.error("%s", err)
        return None

    def openShotFile(self):
        file_path = self.shot.queryFileName(self.shot.query_id)
        os.startfile(str(file_path))

    def copyNameToClipboard(self):
        #
        file_path = self.shot.queryFileName(self.shot.query_id)
        pyperclip.copy(str(file_path.name))
        logging.info('复制 %s 到剪切板', str(file_path.name))

    def copyPathToClipboard(self):
        file_path = self.shot.queryFileName(self.shot.query_id)
        pyperclip.copy(str(file_path.parent))
        logging.info('复制 %s 到剪切板', str(file_path.parent))

    def exportMaya(self):
        file_data = self.shot.queryFileName(self.shot.query_id)

        logging.info(file_data)
        if file_data:
            export_maya = script.MayaExportCam.export(file_data)
            export_maya.exportCam()
            QtWidgets.QMessageBox.warning(self, "点击:", "点击导出 "
                                                       "请点击桌面maya导出快捷方式",
                                          QtWidgets.QMessageBox.Yes)

    def Screenshot(self, my_type: str, thumbnail: QtWidgets.QLabel):
        core:script.DooDlePrjCode.PrjCode = getattr(self, my_type)
        path = core.getScreenshot()
        if not path.parent.is_dir():
            path.parent.mkdir(parents=True, exist_ok=True)

        screen_shot = script.doodlePlayer.doodleScreenshot(path=str(path))
        self.hide()
        screen_shot.exec_()
        self.show()
        if path.is_file():
            core.file = path.name
            core.fileSuffixes = path.suffix
            core.version = 1
            core.filepath = path.as_posix()
            core.infor = "这是截图"
            core.submitInfo(path.name, path.suffix, self.user, 0, path.as_posix(), "这是截图")
        self.setThumbnail(my_type, thumbnail)

    def setThumbnail(self, type_: str, thumbnail: QtWidgets.QLabel):
        core = getattr(self, type_)
        path = core.getScreenshotPath()
        pixmap = QtGui.QPixmap(str(path))
        pixmap = pixmap.scaled(thumbnail.geometry().size(), QtCore.Qt.KeepAspectRatio)
        thumbnail.setPixmap(pixmap)

    def uploadFlipBook(self, code: script.DooDlePrjCode.PrjCode):
        """
        上传拍屏 多线程
        :return: None
        """
        file, file_type = QtWidgets.QFileDialog.getOpenFileName(self,
                                                                "选择上传文件",
                                                                self.recentlyOpenedFolder,
                                                                "files (*.mp4 *.avi *.mov *.exr "
                                                                "*.png *.tga *.jpg)")

        self.recentlyOpenedFolder = file

        version: int = code.getMaxVersion()
        name = code.getFileName(version, self.user, ".mp4", prefix="FB_")
        right_path = code.getFilePath("FlipBook")

        logging.info("获得file %s \n 获得 nmae %s", file, name)
        if file:
            path = pathlib.Path("")
            file = pathlib.Path(file)
            if file.suffix in ['.mov', '.avi']:
                path = file.parent.joinpath("convert", name)
                if path.is_file():
                    os.remove(str(path))
                script.doodlePlayer.videoToMp4(video=file, mp4_path=path)
            elif file.suffix in [".exr", ".png", ".tga", "jpg"]:
                try:
                    path = pathlib.Path(tempfile.gettempdir()).joinpath("temp.mp4")
                    if path.is_file():
                        os.remove(str(path))
                    script.doodlePlayer.imageToMp4(video_path=path, image_path=file)
                except:
                    QtWidgets.QMessageBox.warning(self, "图片命名规则:", "test_####.png "
                                                                   "后缀前有四位数字,表示帧号,前面有下划线",
                                                  QtWidgets.QMessageBox.Yes)
                    return ''

            else:
                path = file

            if not right_path.parent.is_dir():
                right_path.parent.mkdir(parents=True, exist_ok=True)

            logging.info("复制路径到 %s", right_path)

            # self.ass.file = path.name
            # self.ass.fileSuffixes = path.suffix
            # self.ass.user = self.user
            # self.ass.version = version
            # self.ass.filepath = path.as_posix()
            # self.ass.infor = "这是拍屏"
            # self.ass.submitInfo(path.name, path.suffix, self.user,
            #                     version=version, filepath_and_name=path.as_posix(), infor="这是拍屏")
            self.shot.dep_type = "FB_" + self.shot.dep_type
            self.shot.submitInfo(path.name, path.suffix, self.user,
                                 version=version, filepathAndname=path.as_posix(), infor="这是拍屏")
            self.listDepartmenClicked()

    def playerButtenClicked(self, one_or_mut: str, department="Anm"):
        tmp_path = os.path.join(tempfile.gettempdir(), "potplayer_temp.dpl")
        self.pot_player = potplayer.PlayList()
        if one_or_mut == "one":
            path = pathlib.Path("")
            if self.listAssType.selectedItems():
                if self.ass.type[:2] == "FB":
                    my_ass_type = self.ass.type
                else:
                    my_ass_type = "FB_" + self.ass.type
                path = self.ass.queryFlipBook(my_ass_type)
                # self.playerFlipBook("ass", my_ass_type)

            elif self.listdepType.selectedItems():
                if self.shot.Type[:2] == "FB":
                    my_shot_type = self.shot.Type
                else:
                    my_shot_type = "FB_" + self.shot.Type
                path = self.shot.queryFlipBook(my_shot_type)
                # self.playerFlipBook("shot", my_shot_type)
            if path:
                self.pot_player.add(path.as_posix())
        else:
            shots = self.shot.getShot()[:]
            shots_ = [int(s[2:-1]) if s[6:] else int(s[2:]) for s in shots]
            for shot in shots_:
                path = self.shot.queryFlipBookShot(shot)
                if path.as_posix() != '.':
                    logging.info("播放文件路径 %s", path)
                    self.pot_player.add(path)
            # self.playerFlipBook('', '', one_or_mut="mut", department=department)

        self.pot_player.dump(tmp_path)
        potplayer.run(tmp_path)

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
