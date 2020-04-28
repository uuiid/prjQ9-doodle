# -*- coding: UTF-8 -*-
import logging
import os
import pathlib
import re
import shutil
import sys
import time

import enum
import ffmpeg
import tempfile
import pyperclip
import pypinyin
import qdarkgraystyle
import potplayer
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
import script.synchronizeFiles
import script.DooDlePrjCode


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
        self.ass_screenshot.clicked.connect(self.Screenshot)
        self.shot_screenshots.clicked.connect(self.Screenshot)
        # 添加上传拍屏功能
        self.shot_upload.clicked.connect(self.uploadFlipBook)
        self.ass_upload.clicked.connect(self.uploadFlipBook)

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
                open_ass_explorer.triggered.connect(self.openShotExplorer)
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
        self.shot.dep_type = self.listdepType.selectedItems()[0].text()

        # 清空上一次文件显示和版本记录和文件路径
        self.clearListFile()
        self.setThumbnail()

        self.setFileItem(self.shot.getFile())

        self.setThumbnail()

    def setFileItem(self, items):
        '''设置文件在GUI中的显示'''

        for item in items:
            mrow = 0

            self.listfile.insertRow(mrow)
            self.listfile.setItem(mrow, 0, QtWidgets.QTableWidgetItem(f'v{item[0]:0>4d}'))
            self.listfile.setItem(mrow, 1, QtWidgets.QTableWidgetItem(item[1]))
            self.listfile.setItem(mrow, 2, QtWidgets.QTableWidgetItem(item[2]))
            self.listfile.setItem(mrow, 3, QtWidgets.QTableWidgetItem(item[3]))
            self.listfile.setItem(mrow, 4, QtWidgets.QTableWidgetItem(str(item[4])))
            mrow = mrow + 1
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

    def assClassClicked(self):
        self.ass.ass_class = self.listAssType.selectedItems()[0].text()

        self.listAssType.clear()
        logging.info('清除资产类型中的项数')
        self.clearListAssFile()
        logging.info('清除资产文件中的项数')

        self.ass_thumbnail.clear()
        self.listAssType.addItems(self.ass.getAssType())

    def assClassTypeClicked(self):
        """资产类别点击事件"""
        self.ass.ass_type = self.listAssType.selectedItems()[0].text()
        self.setThumbnail()
        # 清空上一次文件显示和版本记录和文件路径
        self.clearListAssFile()

        self.setAssFileItem(self.ass.getFile())

    def setAssFileItem(self, file_data):
        """设置资产文件在GUI中的显示"""
        for item in file_data:
            mrow = 0
            self.listAssFile.insertRow(mrow)

            self.listAssFile.setItem(mrow, 0, QtWidgets.QTableWidgetItem(f'v{item[0]:0>4d}'))
            self.listAssFile.setItem(mrow, 1, QtWidgets.QTableWidgetItem(item[1]))
            self.listAssFile.setItem(mrow, 2, QtWidgets.QTableWidgetItem(item[2]))
            self.listAssFile.setItem(mrow, 3, QtWidgets.QTableWidgetItem(item[3]))
            self.listAssFile.setItem(mrow, 4, QtWidgets.QTableWidgetItem(str(item[4])))
            mrow = mrow + 1
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

                self.shot.submitShotInfo(filename=shot_name,
                                         suffix=path.suffix, user=self.user,
                                         version=version,
                                         filepathAndname=dst_file.as_posix(),
                                         infor="")
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
        assFolder = QtWidgets.QInputDialog.getText(self, '输入资产类型', "请用英文或拼音",
                                                   QtWidgets.QLineEdit.Normal)[0]
        if assFolder:
            self.listAss.addItem(assFolder)

    def addAssTypeFolder(self):
        """添加资产文件夹类型"""
        items: list[str] = self.setlocale.assTypeFolder.copy()
        items[2] = items[2].format(self.ass.ass_class)
        ass_type = QtWidgets.QInputDialog.getItem(self, '选择资产类型', '要先选择资产', items, 0, False)[0]
        if ass_type and self.listAss.selectedItems():
            self.listAssType.addItem(ass_type)

    def uploadFiles(self):
        """
        上传资产文件 弹出选项框
        :return:
        """
        file, fileType = QtWidgets.QFileDialog.getOpenFileName(self,
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

            if file.suffix in ['.mb', '.ma', '.max']:
                target_file = self.ass.getFilePath()
                file_name = self.ass.getFileName()
                self.assUploadFileHandle(file,version_max)
            elif file.suffix in [".fbx"]:
                self.assUploadFileHandle(file,version_max)
            elif file.suffix in ['.uproject']:
                self.assUploadFileUE4Handle(file)
            elif file.suffix in ['.png', '.tga', 'jpg']:
                self.assUploadMapHandle(file)
            else:
                pass
            self.MysqlData(self.ass_class_sort, "set", '', False,
                           name=self.ass_class, type=self.ass_class_type,
                           file=self.ass_file_name, fileSuffixes=file.suffix,
                           user=self.setlocale.user, version=version_max, infor=remarks_info,
                           filepath=file.as_posix())

        self.assClassTypeClicked()

    @script.doodleLog.erorrDecorator
    def assUploadMapHandle(self, file: pathlib.Path):
        """
        上传贴图文件
        :param file: pathlib.Path
        :return: int
        """
        version = self.getMaxVersion() + 1
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
        """
        来源和目标必须时文件 + 路径
        :param source: pathlib.Path
        :param target: pathlib.Path
        :param version: int
        :return: Nore
        """
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

    def assUploadFileHandle(self, file_path: pathlib.Path, version_max):
        """
        上传普通文件
        :param file_path: pathli.Path
        :return: int
        """
        target_file: pathlib.Path = self.ass_file_path.joinpath('{}{}'.format(self.ass_class,
                                                                              file_path.suffix))

        if file_path.suffix in ['.mb', '.ma', '.max']:
            self.backupCopy(file_path, target_file, version_max)
        if file_path.suffix in ['.fbx']:
            self.backupCopy(file_path, target_file, version_max)
        return version_max

    def assUploadFileUE4Handle(self, file_path: pathlib.Path):
        """
        上传ue4项目
        """
        version_max = self.getMaxVersion() + 1
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
        os.system('{} "{}"'.format(program, syn_file))
        shutil.copy2(str(file_path), str(self.ass_file_path.joinpath(self.ass_file_name + '.uproject')))

    def appointFilePath(self):
        """指定文件路径"""
        file, file_type = QtWidgets.QFileDialog.getOpenFileName(self,
                                                                "选择上传文件",
                                                                self.recentlyOpenedFolder,
                                                                "files (*.mb *.ma *.uproject"
                                                                " *.max *.fbx *.png *.tga *.jpg)")

        remarks_info = self.recentlyOpenedFolder = QtWidgets.QInputDialog.getText(self,
                                                                                  "填写备注(中文)",
                                                                                  "备注",
                                                                                  QtWidgets.QLineEdit.Normal)[0]
        if file and (self.listAssType.selectedItems() or self.listdepType.selectedItems()):
            file = pathlib.Path(file)
            version: int = self.getMaxVersion()
            if self.listdepType.selectedItems():

                self.MysqlData(f"ep{self.shot_episods:0>3d}", "set", '', False,
                               episodes=self.shot_episods, shot=self.shot_shot, shotab=self.shot_shotab,
                               department=self.shot_department, Type=self.shot_dep_type,
                               file=self.shot_name, fileSuffixes=file.suffix, user=self.setlocale.user,
                               version=version + 1,
                               filepath=file.as_posix(),
                               infor=remarks_info)

            elif self.listAssType.selectedItems():
                self.MysqlData(self.ass_class_sort, "set", '', False,
                               name=self.ass_class, type=self.ass_class_type,
                               file=self.ass_file_name, fileSuffixes=file.suffix,
                               user=self.setlocale.user, version=version + 1,
                               infor=remarks_info,
                               filepath=file.as_posix())

    # </editor-fold>

    # <editor-fold desc="各种对于文件的操作">

    def combinationFilePath(self):
        # 这个用来组合文件和文件命
        filename = self.shot_name
        filepath = self.shot_file_path.joinpath(filename)
        return filepath

    def openShotExplorer(self):
        file_path = self.getMysqlFileNameAndPath().parent
        self.ta_log.info('打开path %s', file_path)
        os.startfile(str(file_path))
        return None

    def openShotFile(self):
        file_path = self.getMysqlFileNameAndPath()
        os.startfile(str(file_path))

    def getMysqlFileNameAndPath(self):
        if self.listfile.selectedItems():
            table = f"ep{self.shot_episods:0>3d}"
        else:
            table = self.ass_class_sort
        file_data = self.MysqlData(table, "get", '', True, "filepath",
                                   id=self.id)
        try:
            file_path = pathlib.Path(file_data[0][0])
        except:
            file_path = pathlib.Path('')
        return file_path

    def copyNameToClipboard(self):
        #
        file_path = self.getMysqlFileNameAndPath().parent
        pyperclip.copy(str(file_path.name))
        self.ta_log.info('复制 %s 到剪切板', str(self.shot_name))

    def copyPathToClipboard(self):
        file_path = self.getMysqlFileNameAndPath().parent
        pyperclip.copy(str(file_path.parent))
        self.ta_log.info('复制 %s 到剪切板', str(self.shot_file_path))

    def exportMaya(self):
        file_data = self.MysqlData(f"ep{self.shot_episods:0>3d}", "get", '', True, "filepath",
                                   id=self.id)

        logging.info(file_data)
        try:
            file_data = file_data[0][0]
        except:
            pass
        else:
            export_maya = script.MayaExportCam.export(file_data)
            export_maya.exportCam()
            QtWidgets.QMessageBox.warning(self, "点击:", "点击导出 "
                                                           "请点击桌面maya导出快捷方式"
                                          , QtWidgets.QMessageBox.Yes)

    def Screenshot(self):
        path = pathlib.Path("")
        if self.listAssType.selectedItems():
            path: pathlib.Path = self.ass_root.joinpath(self.ass_class_sort,
                                                        self.ass_class,
                                                        'Playblasts',
                                                        self.ass_class_type,
                                                        "Screenshot",
                                                        f"{self.ass_class}_{self.ass_class_type}.jpg"
                                                        )
        elif self.listdepType.selectedItems():
            path: pathlib.Path = self.shot_root.joinpath(f'ep{self.shot_episods:0>3d}',
                                                         f'sc{self.shot_shot:0>4d}',
                                                         'Playblasts',
                                                         self.shot_department,
                                                         self.shot_dep_type,
                                                         "Screenshot",
                                                         f"ep{self.shot_episods:0>3d}_sc{self.shot_shot:0>4d}.jpg"
                                                         )
        if not path.parent.is_dir():
            path.parent.mkdir(parents=True, exist_ok=True)

        screen_shot = script.doodlePlayer.doodleScreenshot(path=str(path))
        self.hide()
        screen_shot.exec_()
        self.show()
        if path.is_file():
            if self.listAssType.selectedItems():
                if not self.listAssFile.item(0, 3).text() == ".jpg":
                    self.MysqlData(self.ass_class_sort, "set", '', False,
                                   name=self.ass_class, type=self.ass_class_type,
                                   file=self.ass_file_name, fileSuffixes=path.suffix,
                                   user=self.setlocale.user, version=0, infor="这是截图",
                                   filepath=path.as_posix())
            elif self.listfile.selectedItems():
                if not self.listfile.item(0, 3).text() == ".jpg":
                    self.MysqlData(f"ep{self.shot_episods:0>3d}", "set", '', False,
                                   episodes=self.shot_episods, shot=self.shot_shot, shotab=self.shot_shotab,
                                   department=self.shot_department, Type=self.shot_dep_type,
                                   file=path.stem, fileSuffixes=path.suffix, user=self.setlocale.user,
                                   version=0,
                                   filepath=path.as_posix(),
                                   infor="这是截图")
        self.setThumbnail()

    def setThumbnail(self):
        file_data: [tuple] = []
        if self.listAssType.selectedItems():
            file_data = self.MysqlData(self.ass_class_sort, "get", '', True, 'filepath',
                                       name=self.ass_class, type=self.ass_class_type,
                                       fileSuffixes='.jpg', user=self.setlocale.user)
        elif self.listdepType.selectedItems():
            file_data = self.MysqlData(f"ep{self.shot_episods:0>3d}", "get", '', True, 'filepath',
                                       episodes=self.shot_episods, shot=self.shot_shot, shotab=self.shot_shotab,
                                       department=self.shot_department, Type=self.shot_dep_type,
                                       fileSuffixes='.jpg')
        try:
            path: pathlib.Path = file_data[0][0]
        except IndexError:
            pass
        else:
            pixmap = QtGui.QPixmap(str(path))

            if self.listAssType.selectedItems():
                pixmap = pixmap.scaled(self.ass_thumbnail.geometry().size(), QtCore.Qt.KeepAspectRatio)
                self.ass_thumbnail.setPixmap(pixmap)
            elif self.listdepType.selectedItems():
                pixmap = pixmap.scaled(self.shot_thumbnail.geometry().size(), QtCore.Qt.KeepAspectRatio)
                self.shot_thumbnail.setPixmap(pixmap)

    def uploadFlipBook(self):
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

        version: int = self.getMaxVersion() + 1
        user_ = pypinyin.slug(self.setlocale.user, pypinyin.NORMAL)
        name = f"ep{self.shot_episods:0>3d}_" \
               f"sc{self.shot_shot:0>4d}" \
               f"_{self.shot_department}_" \
               f"{self.shot_dep_type}_" \
               f"{user_}_v{version:0>4d}.mp4"
        right_path = pathlib.Path("")
        if self.listdepType.selectedItems():
            right_path = self.shot_root.joinpath(f'ep{self.shot_episods:0>3d}',
                                                 f'sc{self.shot_shot:0>4d}',
                                                 'FlipBook',
                                                 self.shot_department,
                                                 self.shot_dep_type,
                                                 f"ep{self.shot_episods:0>3d}_sc{self.shot_shot:0>4d}_{user_}.mp4")
        elif self.listAssType.selectedItems():
            right_path = self.ass_root.joinpath(self.ass_class_sort,
                                                self.ass_class,
                                                'FlipBook',
                                                self.ass_class_type,
                                                f"{self.ass_class}_{self.ass_class_type}_{user_}.mp4")

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
                                                                   "后缀前有四位数字,表示帧号,前面有下划线"
                                                  , QtWidgets.QMessageBox.Yes)
                    return ''

            else:
                path = file

            if self.listdepType.selectedItems():

                if not right_path.parent.is_dir():
                    right_path.parent.mkdir(parents=True, exist_ok=True)

                logging.info("复制路径到 %s", right_path)
                try:
                    shutil.copy2(str(path), str(right_path))
                except:
                    QtWidgets.QMessageBox.warning(self, "警告:", "复制未成功 "
                                                  , QtWidgets.QMessageBox.Yes)
                else:
                    self.MysqlData(f"ep{self.shot_episods:0>3d}", "set", '', False,
                                   episodes=self.shot_episods, shot=self.shot_shot, shotab=self.shot_shotab,
                                   department=self.shot_department, Type="FB_{}".format(self.shot_dep_type),
                                   file=self.shot_name, fileSuffixes='.mp4', user=self.setlocale.user,
                                   version=version,
                                   filepath=right_path.as_posix(),
                                   infor="这是拍屏")
            elif self.listAssType.selectedItems():

                if not right_path.parent.is_dir():
                    right_path.parent.mkdir(parents=True, exist_ok=True)

                logging.info("从  %s 复制路径到 %s", path, right_path)
                try:
                    shutil.copy2(str(path), str(right_path))
                except:
                    QtWidgets.QMessageBox.warning(self, "警告:", "复制未成功 "
                                                  , QtWidgets.QMessageBox.Yes)
                else:
                    self.MysqlData(self.ass_class_sort, "set", '', False,
                                   name=self.ass_class, type="FB_{}".format(self.ass_class_type),
                                   file=self.ass_file_name, fileSuffixes='.mp4',
                                   user=self.setlocale.user, version=version,
                                   infor="这是拍屏",
                                   filepath=right_path.as_posix())
            self.listDepartmenClicked()

    def playerButtenClicked(self, one_or_mut: str, department="Anm"):
        if one_or_mut == "one":
            if self.listAssType.selectedItems():
                if self.ass_class_type[:2] == "FB":
                    my_ass_type = self.ass_class_type
                else:
                    my_ass_type = "FB_" + self.ass_class_type
                self.playerFlipBook("ass", my_ass_type)
            elif self.listdepType.selectedItems():
                if self.shot_dep_type[:2] == "FB":
                    my_ass_type = self.shot_dep_type
                else:
                    my_ass_type = "FB_" + self.shot_dep_type
                self.playerFlipBook("shot", my_ass_type)
        else:
            self.playerFlipBook('', '', one_or_mut="mut", department=department)

    def playerFlipBook(self, ass_or_shot, ass_type, one_or_mut="one", department="Anm"):
        path = pathlib.Path("")
        if one_or_mut == "one":
            if ass_or_shot == "ass":
                path = self.MysqlData(self.ass_class_sort, "get", "filetime", True, "filepath",
                                      name=self.ass_class, type=ass_type,
                                      fileSuffixes=".mp4")
            elif ass_or_shot == "shot":
                path = self.MysqlData(f"ep{self.shot_episods:0>3d}", "get", 'filetime', True, "filepath",
                                      episodes=self.shot_episods, shot=self.shot_shot, shotab=self.shot_shotab,
                                      department=self.shot_department, Type=ass_type,
                                      file=self.shot_name, fileSuffixes='.mp4')
            try:
                if pathlib.Path(path[0][0]).is_file():
                    self.pot_player.add(path[0][0])
                    tmp_path = os.path.join(tempfile.gettempdir(), "potplayer_temp.dpl")
                    self.pot_player.dump(tmp_path)
                    potplayer.run(tmp_path)
            except IndexError:
                pass
        else:
            self.pot_player = potplayer.PlayList()
            for shot in self.MysqlData(f"ep{self.shot_episods:0>3d}", "get", "", False, "shot")[:]:
                try:
                    player_video_path = \
                        self.MysqlData(f"ep{self.shot_episods:0>3d}", "get", "filetime", True, "filepath", shot=shot[0],
                                       department=department, fileSuffixes=".mp4")[0][0]
                except:
                    pass
                else:
                    logging.info("播放文件路径 %s", player_video_path)
                    self.pot_player.add(player_video_path)
            tmp_path: str = os.path.join(tempfile.gettempdir(), "potplayer_temp_long.dpl")
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
