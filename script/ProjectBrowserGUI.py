# -*- coding: UTF-8 -*-

import socket
import sys

import potplayer
import pyperclip

from PySide2 import QtCore
from PySide2 import QtGui
from PySide2 import QtWidgets
import qdarkstyle
import UiFile.ProjectBrowser
import script.DooDlePrjCode
import script.MayaExportCam
import script.MySqlComm
import script.convert
import script.doodleLog
import script.doodlePlayer
import script.doodle_setting
import script.synXml
import script.synchronizeFiles

from script.DoodleFileClass import *


class _prjColor(object):
    @staticmethod
    def listItemStateError():
        bush = QtGui.QBrush()
        bush.setColor(QtCore.Qt.red)
        return bush

    @staticmethod
    def listItemStateAmend():
        bush = QtGui.QBrush()
        bush.setColor(QtCore.Qt.darkYellow)
        return bush

    @staticmethod
    def listItemStateComplete():
        bush = QtGui.QBrush()
        bush.setColor(QtCore.Qt.darkGreen)
        return bush

    def __getattr__(self, item):
        bush = QtGui.QBrush()
        bush.setColor(QtCore.Qt.black)
        return bush


class ProjectBrowserGUI(QtWidgets.QMainWindow, UiFile.ProjectBrowser.Ui_MainWindow):
    """
    这个类用来实现项目管理的属性和UI操作,其中shot和ass是两个数据库链接器,  用来在ui和数据库中添加一个中间层
    """

    user: str

    def __init__(self, parent=None):
        super(ProjectBrowserGUI, self).__init__(parent)
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

        self.user = script.convert.isChinese(self.setlocale.user).easyToEn()
        # 加载颜色类
        self._color = _prjColor
        # 最近打开的文件夹
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

        # 链接截图功能和按钮
        self.ass_screenshot.clicked.connect(lambda: self.Screenshot("ass", self.ass_thumbnail))
        self.shot_screenshots.clicked.connect(lambda: self.Screenshot("shot", self.shot_thumbnail))
        # 链接上传拍屏功能和按钮
        self.shot_upload.clicked.connect(lambda: self.uploadFlipBook(self.shot))
        self.ass_upload.clicked.connect(lambda: self.uploadFlipBook(self.ass))

        # 链接播放拍屏的按钮
        self.ass_player.clicked.connect(lambda: self.playerButtenClicked(one_or_mut="one"))
        self.shot_player.clicked.connect(lambda: self.playerButtenClicked(one_or_mut="one"))

        # <editor-fold desc="关于shot的更新操作">

        # 首先扫描根目录获得集数
        self.setepisodex()
        # 并链接函数处理下一级
        self.listepisodes.itemClicked.connect(lambda item: self.listEpisodesClicked(item))
        # 在shot文件列表中添加点击事件更改下一级部门列表
        self.listshot.itemClicked.connect(lambda item: self.listshotClicked(item))
        # 在department中添加下一级的更新事件
        self.listdepartment.itemClicked.connect(lambda item: self.listDepartmenClicked(item))
        # 在depType中添加点击跟新文件事件
        self.listdepType.itemClicked.connect(lambda item: self.listDepTypeClicked(item))
        # 在文件中添加点击事件
        self.listfile.cellClicked.connect(lambda row, column: self.shotFileClicked(row))
        # </editor-fold>

        # 设置ass类型
        self.scane.clicked.connect(lambda: self.assClassSortClicked('scane'))
        self.props.clicked.connect(lambda: self.assClassSortClicked('props'))
        self.character.clicked.connect(lambda: self.assClassSortClicked('character'))
        self.effects.clicked.connect(lambda: self.assClassSortClicked('effects'))

        # 在listAss中添加点击事件生成Ass资产列表
        self.listAss.itemClicked.connect(lambda item: self.assClassClicked(item))
        # 在listType中添加点击事件生成file列表
        self.listAssType.itemClicked.connect(lambda item: self.assClassTypeClicked(item))
        # 在listassfile中获得资产信息
        self.listAssFile.cellClicked.connect(lambda row, colume: self.assFileClicked(row))

        # 双击打开文件
        self.listfile.doubleClicked.connect(self.openShotFile)
        # 添加刷新函数
        self.refresh.triggered.connect(self.setepisodex)
        # 关闭ue链接函数
        self.close_socket.triggered.connect(self.closesocket)
        # 合成拍屏
        self.actioncom_video.triggered.connect(self.comEpsVideo)
        # 转换布料
        self.actionclothToFbx.triggered.connect(self.convertCloth)

        # <editor-fold desc="添加上下文菜单">
        # 添加集数上下文菜单
        self.listepisodes.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.listepisodes.customContextMenuRequested.connect(
            lambda pos: self.addRightClickMenu(self.listepisodes.mapToGlobal(pos), 'episodes'))
        # 添加镜头上下文菜单
        self.listshot.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.listshot.customContextMenuRequested.connect(
            lambda pos: self.addRightClickMenu(self.listshot.mapToGlobal(pos), "shot"))
        # 部门菜单
        self.listdepartment.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.listdepartment.customContextMenuRequested.connect(
            lambda pos: self.addRightClickMenu(self.listdepartment.mapToGlobal(pos), "department"))
        # 部门类型菜单
        self.listdepType.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.listdepType.customContextMenuRequested.connect(
            lambda pos: self.addRightClickMenu(self.listdepType.mapToGlobal(pos), "depType"))

        # 镜头文件菜单
        self.listfile.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.listfile.customContextMenuRequested.connect(
            lambda pos: self.addRightClickMenu(self.listfile.mapToGlobal(pos), "shotFile"))

        # 资产种类菜单
        self.listAss.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.listAss.customContextMenuRequested.connect(
            lambda pos: self.addRightClickMenu(self.listAss.mapToGlobal(pos), "assFolder"))
        # 资产类型菜单
        self.listAssType.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.listAssType.customContextMenuRequested.connect(
            lambda pos: self.addRightClickMenu(self.listAssType.mapToGlobal(pos), "assType"))
        # 资产文件菜单
        self.listAssFile.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.listAssFile.customContextMenuRequested.connect(
            lambda pos: self.addRightClickMenu(self.listAssFile.mapToGlobal(pos), "assFile"))
        # </editor-fold>

        self.pot_player = potplayer.PlayList()

    def tabWigetClick(self, index: int):
        """
        选项卡切换事件
        """
        if index == 0:
            logging.info("点击资产")
            self.setepisodex()
        elif index == 1:
            logging.info("点击镜头")
            self.assClassSortClicked("character")

    # <editor-fold desc="菜单项">
    def menuEpisodes(self, menu):
        """
        集数右键菜单
        """
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
        """
        镜头右键菜单
        """
        if self.listepisodes.selectedItems():
            add_shot_folder = menu.addAction('添加', )
            add_shot_folder.triggered.connect(self.addShotFolder)
            add_a_bshot_folder = menu.addAction('添加AB镜')
            add_a_bshot_folder.triggered.connect(self.addABshotFolder)
        return menu

    def menuDepartment(self, menu):
        """
        镜头部门右键菜单
        """
        if self.listshot.selectedItems():
            add_department = menu.addAction('添加')
            add_department.triggered.connect(self.addDepartmentFolder)
        return menu

    def menuDeptype(self, menu):
        """
        镜头部门类型右键菜单
        """
        add_dep_type = menu.addAction('添加')
        add_dep_type.triggered.connect(self.addTypeFolder)
        return menu

    def menuShotfile(self, menu):
        """
        镜头文件菜单
        """
        if self.listfile.selectedItems():
            open_explorer = menu.addAction('打开文件管理器')  # 用文件管理器打开文件位置
            open_explorer.triggered.connect(lambda: self.openShotExplorer(self.shot))
            # copy文件名称或者路径到剪切板
            add_info = menu.addAction("更新概述")
            add_info.triggered.connect(lambda: self.subInfo(self.shot))
            filestate = menu.addAction("标记问题")
            filestate.triggered.connect(lambda: self.markFileStart(self.shot))
            copy_name_to_clip = menu.addAction('复制名称')
            copy_name_to_clip.triggered.connect(self.copyNameToClipboard)
            copy_path_to_clip = menu.addAction('复制路径')
            copy_path_to_clip.triggered.connect(self.copyPathToClipboard)
            # 导出Fbx和abc选项
            export_maya = menu.addAction("导出maya相机")
            export_maya.triggered.connect(self.exportMaya)
            import_ue = menu.addAction("导入ue")
            import_ue.triggered.connect(self.importUe)
        return menu

    def menuAssfolder(self, menu):
        """
        添加资产种类右键菜单
        """
        add_ass_folder = menu.addAction('添加')
        add_ass_folder.triggered.connect(self.addAssFolder)
        if self.listAss.selectedItems():
            rename_folder = menu.addAction("添加中文名称")
            rename_folder.triggered.connect(self.addAssZnChName)
        return menu

    def menuAsstype(self, menu):
        """
        添加资产类型右键菜单
        """
        if self.listAss.selectedItems():  # 添加资产类型右键文件夹
            add_ass_type_folder = menu.addAction('添加')
            add_ass_type_folder.triggered.connect(self.addAssTypeFolder)
        return menu

    def menuAssfile(self, menu):
        """
        添加资产文件右键菜单
        """
        if self.listAssType.selectedItems():
            if self.listAssFile.selectedItems():
                open_ass_explorer = menu.addAction("打开文件管理器")
                open_ass_explorer.triggered.connect(lambda: self.openShotExplorer(self.ass))
                add_info = menu.addAction("更新概述")
                add_info.triggered.connect(lambda: self.subInfo(self.ass))
                filestate = menu.addAction("标记问题")
                filestate.triggered.connect(lambda: self.markFileStart(self.ass))
                add_ass_file_dow = menu.addAction("下载文件")
                add_ass_file_dow.triggered.connect(lambda: self.download(self.ass))
            add_ass_file = menu.addAction('上传(同步)文件')
            add_ass_file.triggered.connect(self.uploadFiles)
            get_ass_path = menu.addAction('指定文件')
            get_ass_path.triggered.connect(self.appointFilePath)
        return menu

    @script.doodleLog.erorrDecorator
    def addRightClickMenu(self, point: QtCore.QPoint, _type: str):
        """添加右键菜单功能"""
        menu = QtWidgets.QMenu(self)
        try:
            menu = getattr(self, "menu" + _type.capitalize())(menu)
        except AttributeError as err:
            logging.info("寻找不到属性了 %s", err)
        menu.exec_(point)
    # menu.popup(point)

    # </editor-fold>
    @staticmethod
    def _setQlistItemColor(list_: QtWidgets.QListWidget, finds, state_type):
        """设置小部件颜色, 用来显示有问题的"""
        item = list_.findItems(finds, QtCore.Qt.MatchExactly)
        try:
            item = item[0]
        except IndexError as err:
            logging.error("没有找到这个小部件 %s", err)
        else:
            item.setBackground(getattr(_prjColor, f"listItemState{state_type}")())
        # item.setBackground(QtGui.QBrush(QtCore.Qt.red))

    # <editor-fold desc="镜头更新事件">

    def setepisodex(self):
        """
        更新集数
        """
        self.listepisodes.clear()
        self.listshot.clear()
        self.listdepartment.clear()
        self.listdepType.clear()
        self.clearTableFile(self.listfile)

        self.shot_thumbnail.clear()

        logging.info('更新集数列表')
        self.listepisodes.addItems(self.shot.getEpsodes())

    def listEpisodesClicked(self, item):
        """
        集数点击事件
        """
        items__text = item.text()
        if items__text == 'pv':
            items__text = 0
        else:
            items__text = int(items__text[2:])
        self.shot.episodes = items__text

        self.listdepartment.clear()
        self.listdepType.clear()
        self.clearTableFile(self.listfile)

        self.listshot.clear()
        self.shot_thumbnail.clear()

        logging.info('更新shot列表')

        self.listshot.addItems(self.shot.getShot())
        # 设置颜色
        state = self.shot.getFileState("Shot")
        for s in state:
            self._setQlistItemColor(self.listshot, f'sc{s.shot:0>4d}{s.shotab}', s.filestate)

    def listshotClicked(self, item):
        """
        镜头点击事件
        """
        items_shot = item.text()
        try:
            self.shot.shot = int(items_shot[2:])
            self.shot.shotab = ''
        except ValueError:
            self.shot.shot = int(items_shot[2:-1])
            self.shot.shotab = items_shot[-1:]

        self.listdepartment.clear()
        self.listdepType.clear()
        self.clearTableFile(self.listfile)
        self.shot_thumbnail.clear()

        logging.info('更新Department列表')

        self.listdepartment.addItems(self.shot.getDepartment())
        # 设置颜色
        state = self.shot.getFileState("Dep")
        for s in state:
            self._setQlistItemColor(self.listdepartment, self.setlocale.department, s.filestate)

    def listDepartmenClicked(self, item):
        """
        部门点击事件
        """
        self.shot.department = item.text()

        self.clearTableFile(self.listfile)
        self.listdepType.clear()
        self.shot_thumbnail.clear()

        self.listdepType.addItems(self.shot.getDepType())
        # 设置颜色
        state = self.shot.getFileState("DepType")
        for s in state:
            self._setQlistItemColor(self.listdepType, s.Type, s.filestate)

    def listDepTypeClicked(self, item):
        """
        部门类型点击事件
        """
        self.shot.Type = item.text()

        # 清空上一次文件显示和版本记录和文件路径
        self.clearTableFile(self.listfile)
        self._setWidegtItem(self.shot.getFile(), self.listfile)

    def shotFileClicked(self, shot_row):
        """
        镜头文件点击事件
        """
        # shot_row = row
        # shot_row = self.listfile.currentRow()
        self.shot.version = int(self.listfile.item(shot_row, 0).text()[1:])
        self.shot.infor = self.listfile.item(shot_row, 1).text()
        self.shot.fileSuffixes = self.listfile.item(shot_row, 3).text()
        self.shot.query_id = int(self.listfile.item(shot_row, 4).text())

    @staticmethod
    def clearTableFile(table: QtWidgets.QTableWidget):
        """清除列表"""
        mrowtmp = table.rowCount()
        while mrowtmp >= 0:
            table.removeRow(mrowtmp)
            mrowtmp = mrowtmp - 1

    # </editor-fold>

    @staticmethod
    def _setWidegtItem(items: list, table: QtWidgets.QTableWidget):
        """
        设置资产文件在GUI中的显示
        """

        for index, item in enumerate(items):
            table.insertRow(index)
            table.setItem(index, 0, QtWidgets.QTableWidgetItem(f'v{item[0]:0>4d}'))
            file_infor = [""]
            if item[1]:
                file_infor = re.split(r"\|", item[1])
            table.setItem(index, 1, QtWidgets.QTableWidgetItem(file_infor[-1]))  # 设置概述
            table.item(index, 1).setToolTip("\n".join(file_infor))
            table.setItem(index, 2, QtWidgets.QTableWidgetItem(item[2]))
            table.setItem(index, 3, QtWidgets.QTableWidgetItem(item[3]))
            table.setItem(index, 4, QtWidgets.QTableWidgetItem(str(item[4])))
        logging.info('更新文件列表')

    # <editor-fold desc="更新ass的各种操作">
    def assClassSortClicked(self, ass_name: str):
        """
        按钮点击事件, 更新资产种类
        """
        self.ass.sort = ass_name
        logging.info('将资产类型设置为 %s', ass_name)

        self.listAss.clear()
        self.listAssType.clear()
        self.clearTableFile(self.listAssFile)

        self.ass_thumbnail.clear()

        # 通过mySql命令获得数据
        self.listAss.addItems(self.ass.getAssClass())
        # 设置颜色
        state = self.ass.getFileState("Class")
        for s in state:
            self._setQlistItemColor(self.listAss, s.name, s.filestate)

        for name, loa in self.ass.convertMy.name.items():
            try:
                item = self.listAss.findItems(name, QtCore.Qt.MatchExactly)[0]
            except IndexError:
                logging.error("找不到中文项目")
            else:
                item.setText(loa)

    def assClassClicked(self, item):
        """
        资产种类点击事件, 资产类型的更新
        """

        self.ass.name = self.ass.convertMy.toEn(item.text())  # self.listAssType.selectedItems()[0].text()

        self.listAssType.clear()
        logging.info('清除资产类型中的项数')
        self.clearTableFile(self.listAssFile)
        logging.info('清除资产文件中的项数')

        self.ass_thumbnail.clear()
        self.listAssType.addItems(self.ass.getAssType())
        # 设置颜色
        state = self.ass.getFileState("Type")
        for s in state:
            self._setQlistItemColor(self.listAssType, s.type, s.filestate)

    def assClassTypeClicked(self, item):
        """资产类别点击事件, 更新资产文件列表"""
        self.ass.Type = item.text()
        self.setThumbnail("ass", self.ass_thumbnail)
        # 清空上一次文件显示和版本记录和文件路径
        self.clearTableFile(self.listAssFile)
        self._setWidegtItem(self.ass.getFileInfo(), self.listAssFile)

    def assFileClicked(self, ass_row):
        # ass_row = self.listAssFile.currentRow()
        self.ass.version = int(self.listAssFile.item(ass_row, 0).text()[1:])
        self.ass.infor = self.listAssFile.item(ass_row, 1).text()
        self.ass.fileSuffixes = self.listAssFile.item(ass_row, 3).text()
        self.ass.query_id = int(self.listAssFile.item(ass_row, 4).text())

    # </editor-fold>

    # <editor-fold desc="拖放操作函数">
    def enableBorder(self, enable):
        if enable:
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

                # 创建maya文件并上传
                mayafile = shotMayaFile(self.shot, self.setlocale)
                mayafile.upload(path)
                logging.info("上传成功 %s", path)

                self.listDepTypeClicked(self.listdepType.selectedItems()[0])
                self.enableBorder(False)
            else:
                pass
        else:
            a0.ignore()

    # </editor-fold>

    # <editor-fold desc="添加集数文件夹的操作都在这里">

    def addEpisodesFolder(self):
        """添加集数文件夹并提交数据库"""
        episode, is_ok = QtWidgets.QInputDialog.getInt(self, '输入集数', "ep", 1, 1, 999, 1)
        if is_ok:
            self.shot.subEpisodesInfo(episodes=episode)
            self.setepisodex()

    def addShotFolder(self):
        """添加镜头"""
        shot, is_ok = QtWidgets.QInputDialog.getInt(self, '输入镜头', "sc", 1, 1, 999, 1)
        if is_ok and self.listepisodes.selectedItems():
            self.listshot.addItem('sc{:0>4d}'.format(shot))

    def addABshotFolder(self):
        """添加ab镜"""
        items = ['B', 'C', 'D', 'E']
        shot_ab, is_ok = QtWidgets.QInputDialog.getItem(self, '选择AB镜头', '要先选择镜头才可以', items, 0, False)
        shot = self.shot.shot
        if is_ok and self.listshot.selectedItems():
            self.listshot.addItem('sc{:0>4d}{}'.format(shot, shot_ab))

    def addDepartmentFolder(self):
        """添加部门文件"""
        department = self.setlocale.department
        if self.listshot.selectedItems():
            self.listdepartment.addItem(department)

    def addTypeFolder(self):
        """添加类型文件"""
        deptype, is_ok = QtWidgets.QInputDialog.getText(self, '输入镜头', "文件类型(请用英文或拼音)",
                                                        QtWidgets.QLineEdit.Normal)
        if is_ok and self.listdepartment.selectedItems():
            self.listdepType.addItem(deptype)

    def addAssFolder(self):
        """添加资产类型文件夹"""
        ass_folder, is_ok = QtWidgets.QInputDialog.getText(self, '输入资产类型', "请用中文",
                                                           QtWidgets.QLineEdit.Normal)
        if is_ok:
            item = self.listAss.findItems(ass_folder, QtCore.Qt.MatchExactly)
            if item:
                QtWidgets.QMessageBox.warning(self, "错误", "警告: 已有重复项",
                                              QtWidgets.QMessageBox.Yes)
                return None
            self.listAss.addItem(ass_folder)

    def addAssZnChName(self):
        """添加中文别名"""
        ass_folder, is_ok = QtWidgets.QInputDialog.getText(self, '输入中文名称', "请用中文",
                                                           QtWidgets.QLineEdit.Normal)
        if is_ok:
            is_is = QtWidgets.QMessageBox.warning(self, "请确认", "拼音名称:{}\n中文名:{}".format(
                                                  self.listAss.selectedItems()[0].text(),ass_folder),
                                                    QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
            if is_is == QtWidgets.QMessageBox.Yes:
                self.ass.convertMy.addLocalName(self.listAss.selectedItems()[0].text(), ass_folder)
                self.assClassSortClicked(self.ass.sort)

    def addAssTypeFolder(self):
        """添加资产文件夹类型"""

        items: typing.List[str] = self.setlocale.assTypeFolder.copy()
        items = [i.format(self.ass.name) for i in items]

        ass_type, is_ok = QtWidgets.QInputDialog.getItem(self, '选择资产类型', '要先选择资产', items, 0, False)
        if is_ok and self.listAss.selectedItems():
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
            # 使用工厂获得提交类
            sub_class = doodleFileFactory(self.ass, file.suffix)
            if sub_class:
                sub_class = sub_class(self.ass, self.setlocale)
            else:
                return None
            sub_class.infor = remarks_info
            sub_class.upload(file)
        # 如果是中文名称,需要提交中文相对名称
        self.andTranslate()
        # 激活点击事件更新列表
        self.assClassTypeClicked(self.listAssType.selectedItems()[0])

    def assUploadMapHandle(self, soure_file: pathlib.Path, target: pathlib.Path, version: int):
        """
        上传贴图文件
        :param version:
        :param target:
        :param soure_file: pathlib.Path
        :return: Bool
        """
        pass

    def download(self, core: script.DooDlePrjCode.PrjCode):
        path = QtWidgets.QFileDialog.getExistingDirectory(self,
                                                          "选择同步目录",
                                                          self.recentlyOpenedFolder,
                                                          QtWidgets.QFileDialog.ShowDirsOnly)
        pathprj = pathlib.Path(path)
        # is_enpty = True
        # for p in pathprj.iterdir():
        #     is_enpty = False
        #     break
        # if not is_enpty:
        #     QtWidgets.QMessageBox.warning(self, "警告", "请选择空目录",
        #                                   QtWidgets.QMessageBox.Yes)
        #     return None
        if isinstance(core, script.DooDlePrjCode.PrjAss):
            cls_file = doodleFileFactory(self.ass, ".uproject")
            if cls_file:
                cls_file = cls_file(core, self.setlocale)
                cls_file.down(core.query_id, pathprj)

            QtWidgets.QMessageBox.critical(self, "复制中", "请等待.....")
            logging.info(path)

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
            if self.listAssType.selectedItems():
                cls_file = doodleFileFactory(self.ass, file.suffix)
                if cls_file:
                    cls_file = cls_file(self.ass, self.setlocale)
                    cls_file.infor = remarks_info
                    cls_file.appoint(file)
        self.andTranslate()

    def andTranslate(self):
        text = self.listAss.selectedItems()[0].text()
        self.ass.convertMy.getnameTochinese()
        try:
            self.ass.convertMy.local_name[text]
        except KeyError:
            self.ass.convertMy.addLocalName(self.ass.convertMy.toEn(text),text)
        else:
            logging.info("库中已经储存此键值,无需上传中文名称")
    # </editor-fold>

    # <editor-fold desc="各种对于文件的操作">
    @staticmethod
    def openShotExplorer(core: script.DooDlePrjCode.PrjCode):
        """
        打开文件管理器
        """
        p = core
        file_path = p.queryFileName(p.query_id).parent
        logging.info('打开path %s', file_path)
        try:
            os.startfile(str(file_path))
        except BaseException as err:
            logging.error("%s", err)
        return None

    def openShotFile(self):
        """
        打开文件
        """
        file_path = self.shot.queryFileName(self.shot.query_id)
        os.startfile(str(file_path))

    def copyNameToClipboard(self):
        """
        复制文件名称到剪贴板
        """
        file_path = self.shot.queryFileName(self.shot.query_id)
        pyperclip.copy(str(file_path.name))
        logging.info('复制 %s 到剪切板', str(file_path.name))

    def copyPathToClipboard(self):
        """
        复制文件路径到剪贴板
        """
        file_path = self.shot.queryFileName(self.shot.query_id)
        pyperclip.copy(str(file_path.parent))
        logging.info('复制 %s 到剪切板', str(file_path.parent))

    def exportMaya(self):
        """
        导出maya相机和动画FBX
        """
        file_data = self.shot.queryFileName(self.shot.query_id)

        logging.info(file_data)
        if file_data:
            QtWidgets.QMessageBox.warning(self, "警告", "不要关闭弹出窗口",
                                          QtWidgets.QMessageBox.Yes)

            export = shotMayaExportFile(self.shot, self.setlocale)
            export.infor = "这是maya导出文件"
            export.exportRun(file_data)

            self.listDepTypeClicked(self.listdepType.selectedItems()[0])

    def Screenshot(self, my_type: str, thumbnail: QtWidgets.QLabel):
        """
        截图保存动作
        """
        # 获得核心
        core: script.DooDlePrjCode.PrjCode = getattr(self, my_type)
        # 判断类型
        cls_sshot = doodleFileFactory(core,"Screenshot")(core,self.setlocale)
        cls_sshot.infor = "这是截图"
        # 上传截屏
        with cls_sshot.upload() as cache:
            screen_shot = script.doodlePlayer.doodleScreenshot(path=cache.as_posix())
            self.hide()
            screen_shot.exec_()
            self.show()
        self.setThumbnail(my_type, thumbnail)

    def setThumbnail(self, type_: str, thumbnail: QtWidgets.QLabel):
        """
        设置截图显示
        """
        core = getattr(self, type_)
        # 获得截图类
        cls_sshot = doodleFileFactory(core,"Screenshot")(core,self.setlocale)
        # 下载文件
        path = cls_sshot.down()

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
        # 获得拍屏类
        cla_FB = assFBFile(code, self.setlocale)
        cla_FB.infor = "这是拍屏"
        cla_FB.upload(file)
        self.listDepartmenClicked(self.listdepartment.selectedItems()[0])

    def playerButtenClicked(self, one_or_mut: str, department="Anm"):
        """
        打开拍屏
        """
        tmp_path = os.path.join(tempfile.gettempdir(), "potplayer_temp.dpl")
        self.pot_player = potplayer.PlayList()
        if one_or_mut == "one":
            path = pathlib.Path("")
            if self.listAssType.selectedItems():
                code = self.ass
            else:
                code = self.shot
            player = doodleFileFactory(code,"FB")(code,self.setlocale)

            path = player.downPlayer(code.Type)

            while player.syn.is_alive():
                pass

            if path:
                self.pot_player.add(path.as_posix())
        else:
            player = shotMayaFBFile(self.shot,self.setlocale)
            video = player.getEpisodesFlipBook()

            while player.syn.is_alive():
                pass

            if video:
                self.pot_player.add(video)
            else:
                reply = QtWidgets.QMessageBox.warning(self, "警告:", "没有找到转换视频，是否执行自动转换",
                                                      QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
                if reply == QtWidgets.QMessageBox.Yes:
                    # 合成视频
                    video = player.makeEpisodesFlipBook()

                    self.pot_player.dump(video.as_posix())
                else:
                    return None

        self.pot_player.dump(tmp_path)
        try:
            potplayer.run(tmp_path)
        except:
            QtWidgets.QMessageBox.warning(self, "警告:", "警告:请关闭360后重新打开本软件,或者检查安装potplayer",
                                          QtWidgets.QMessageBox.Yes)

    def comEpsVideo(self):
        player = shotMayaFBFile(self.shot,self.setlocale)
        video = player.makeEpisodesFlipBook()
        return video

    def subInfo(self, code: script.DooDlePrjCode.PrjCode):
        """
        修改评论
        """
        info, is_input = QtWidgets.QInputDialog.getText(self, "输入信息", "", QtWidgets.QLineEdit.Normal)
        if is_input:
            if not re.findall(r"\|", info):
                code.infor += "|" + info
                code.undataInformation(code.query_id)

    def markFileStart(self, code: script.DooDlePrjCode.PrjCode):
        """
        标记文件状态
        """
        items = self.setlocale.filestate
        ass_type, is_type = QtWidgets.QInputDialog.getItem(self, "标记文件状态", "要先选中文件", items, 0, False)
        info, is_input = QtWidgets.QInputDialog.getText(self, "输入信息", "", QtWidgets.QLineEdit.Normal)
        if is_type and is_input:
            code.filestate = ass_type
            code.infor = f"| {self.setlocale.user}:  {info}"
            code.undataInformation(code.query_id)
        logging.info("%s , %s", ass_type, info)

    def importUe(self):
        address = ("127.0.0.1", 23335)
        so = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            so.connect(address)
            maya_export = shotMayaExportFile(self.shot,self.setlocale)
            content = maya_export.down(self.shot.query_id)

            data = {"eps": self.shot.episodes, "shot": self.shot.shot, "content": json.loads(content)}

            so.send(json.dumps(data, ensure_ascii=False, indent=4, separators=(',', ':')).encode("utf-8"))
            so.close()
        except ConnectionRefusedError:
            logging.info("导入ue失败")
        else:
            logging.info("成功导入ue")

    @staticmethod
    def closesocket():
        address = ("127.0.0.1", 23335)
        so = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            so.connect(address)
            data = "close"
            so.send(data.encode("utf-8"))
            so.close()
        except ConnectionRefusedError:
            logging.info("关闭链接失败")
        else:
            logging.info("成功关闭链接")

    def convertCloth(self):
        shotMayaClothExportFile(self.shot,self.setlocale).down(self.shot.query_id)
    # </editor-fold>


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet())
    w = ProjectBrowserGUI()
    w.setWindowTitle("Remer")
    w.show()

    sys.exit(app.exec_())
