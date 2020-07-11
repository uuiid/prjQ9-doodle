import logging
import os
import pathlib
import re
import sys
import abc
import tempfile
import typing

import potplayer
import pyperclip
from PySide2 import QtCore, QtGui, QtWidgets

import DoodleServer
import script.DoodleCoreApp


class DoodleListWidegt(QtWidgets.QListWidget, script.DoodleCoreApp.core):
    # def __init__(self,, parent=None):
    #     super(DoodleListWidegt, self).__init__(parent=parent)
    #
    item_class: typing.Any
    doodle_stting: DoodleServer.DoodleSet.Doodlesetting

    def addFofler(self):
        pass

    def addItems(self, labels: typing.List[DoodleServer.DoodleOrm.fileAttributeInfo_], p_str=None):
        for i in labels:
            item = self.item_class
            item.shot = i
            self.addItem(item)

    def showMessageBox(self):
        QtWidgets.QMessageBox.warning(self, "错误", "警告: 已有重复项", QtWidgets.QMessageBox.Yes)


class EpisodesListWidgetItem(QtWidgets.QListWidgetItem):
    _eps_data_: DoodleServer.DoodleOrm.Episodes

    @property
    def eps_data(self):
        if not hasattr(self, '_eps_data_'):
            assert AttributeError("这个eps小部件没有数据")
        return self._eps_data_

    @eps_data.setter
    def eps_data(self, eps_data):
        self._eps_data_ = eps_data
        self.setText('ep{:0>3d}'.format(self._eps_data_.episodes))


class EpisodesListWidget(DoodleListWidegt):
    player = QtCore.Signal(EpisodesListWidgetItem, str)

    select_item: EpisodesListWidgetItem
    item_class = EpisodesListWidgetItem

    doodle_refresh = QtCore.Signal()

    def __init__(self, parent):
        super(EpisodesListWidget, self).__init__(parent=parent)
        self.itemClicked.connect(self.setCore)

    def contextMenuEvent(self, arg__1: QtGui.QContextMenuEvent):
        # print(arg__1)
        menu = QtWidgets.QMenu(self)
        add_episodes_folder = menu.addAction('添加')
        add_episodes_folder.triggered.connect(self.addFofler)
        com_episdoes_player = menu.addAction("合成整集拍屏")
        com_episdoes_player.triggered.connect(self.comEpsVideo)
        add_player = menu.addMenu("播放整集拍屏")
        anm_player = add_player.addAction("播放Anm拍屏")
        vfx_player = add_player.addAction("播放vfx拍屏")
        light_player = add_player.addAction("播放light拍屏")
        anm_player.triggered.connect(self.playerFlibBook)
        vfx_player.triggered.connect(self.playerFlibBook)
        light_player.triggered.connect(self.playerFlibBook)
        menu.move(QtGui.QCursor().pos())
        return menu.show()

    @QtCore.Slot()
    def addFofler(self):
        episode, is_ok = QtWidgets.QInputDialog.getInt(self, '输入集数', "ep", 1, 1, 999, 1)
        if is_ok:
            item = self.item_class()
            item.eps_data = DoodleServer.DoodleOrm.Episodes(episodes=episode)
            if not self.findItems('ep{:0>3d}'.format(episode), QtCore.Qt.MatchExactly):
                self.addItem(item)
            else:
                self.showMessageBox()

    def addItems(self, labels: typing.List[DoodleServer.DoodleOrm.Episodes], p_str=None):
        for i in labels:
            item = self.item_class()
            item.eps_data = i
            self.addItem(item)

    def doodleUpdata(self):
        self.addItems(self.core.queryEps())

    @QtCore.Slot()
    def playerFlibBook(self):
        path = DoodleServer.DoodleBaseClass.shotFbEpisodesFile(self.core, self.doodle_set).down()
        pot_player = potplayer.PlayList()
        pot_player.add(path.as_posix())
        tmp_path = os.path.join(tempfile.gettempdir(), "potplayer_temp.dpl")
        pot_player.dump(tmp_path)
        potplayer.run(tmp_path)

    @QtCore.Slot()
    def comEpsVideo(self):
        self.core.episodes = self.currentItem().eps_data
        return DoodleServer.DoodleBaseClass.shotFbEpisodesFile(self.core, self.doodle_set).makeEpisodesFlipBook()

    @QtCore.Slot()
    def setCore(self, item: EpisodesListWidgetItem):
        self.core.episodes = item.eps_data


class ShotListWidegtItem(QtWidgets.QListWidgetItem):
    _shot_: DoodleServer.DoodleOrm.Shot

    @property
    def shot(self):
        if not hasattr(self, '_shot_'):
            assert AttributeError("这个Shot小部件没有数据")
        return self._shot_

    @shot.setter
    def shot(self, shot):
        self._shot_ = shot
        self.setText('sc{:0>4d}{}'.format(shot.shot_, shot.shotab))


class ShotListWidget(DoodleListWidegt):
    item_class = ShotListWidegtItem

    def __init__(self, parent):
        super(ShotListWidget, self).__init__(parent=parent)
        self.itemClicked.connect(self.setCore)

    @QtCore.Slot()
    def addFofler(self):
        """添加镜头"""
        shot, is_ok = QtWidgets.QInputDialog.getInt(self, '输入镜头', "sc", 1, 1, 999, 1)
        if is_ok:
            item = self.item_class()
            item.shot = DoodleServer.DoodleOrm.Shot(shot_=shot, shotab="")
            if not self.findItems('sc{:0>4d}'.format(shot), QtCore.Qt.MatchExactly):
                self.addItem(item)
            else:
                self.showMessageBox()

    @QtCore.Slot()
    def addABFolder(self):
        """添加ab镜"""
        items = ['B', 'C', 'D', 'E']
        shot_ab, is_ok = QtWidgets.QInputDialog.getItem(self, '选择AB镜头', '要先选择镜头才可以', items, 0, False)
        shot = self.currentItem().shot.shot_
        print(shot)
        if is_ok:
            item = self.item_class()
            item.shot = DoodleServer.DoodleOrm.Shot(shot_=shot, shotab=shot_ab)
            if not self.findItems('sc{:0>4d}{}'.format(shot, shot_ab), QtCore.Qt.MatchExactly):
                self.addItem(item)

    def contextMenuEvent(self, arg__1):
        menu = QtWidgets.QMenu(self)
        add_shot_folder = menu.addAction('添加')
        add_shot_folder.triggered.connect(self.addFofler)
        add_a_bshot_folder = menu.addAction('添加AB镜')
        add_a_bshot_folder.triggered.connect(self.addABFolder)
        menu.move(QtGui.QCursor().pos())
        return menu.show()

    def addItems(self, labels: typing.List[DoodleServer.DoodleOrm.Shot], p_str=None):
        for i in labels:
            item = self.item_class()
            item.shot = i
            self.addItem(item)

    def doodleUpdata(self):
        self.addItems(self.core.queryShot())

    @QtCore.Slot()
    def setCore(self, item: ShotListWidegtItem):
        self.core.shot = item.shot


class ShotFileClassListWidgetItem(QtWidgets.QListWidgetItem):
    _file_class_: DoodleServer.DoodleOrm.fileClass

    @property
    def file_class(self):
        if not hasattr(self, '_file_class_'):
            assert AttributeError("这个shot_file_class小部件没有数据")
        return self._file_class_

    @file_class.setter
    def file_class(self, file_class):
        self._file_class_ = file_class
        self.setText(self._file_class_.file_class)


class ShotFileClassListWidget(DoodleListWidegt):
    item_class = ShotFileClassListWidgetItem

    def __init__(self, parent):
        super(ShotFileClassListWidget, self).__init__(parent=parent)
        self.itemClicked.connect(self.setCore)

    def contextMenuEvent(self, arg__1):
        menu = QtWidgets.QMenu(self)
        add_department = menu.addAction('添加')
        add_department.triggered.connect(self.addFofler)
        menu.move(QtGui.QCursor().pos())
        return menu.show()

    @QtCore.Slot()
    def addFofler(self, ):
        department = self.doodle_stting.department
        if not self.findItems(department, QtCore.Qt.MatchExactly):
            item = self.item_class()
            item.file_class = DoodleServer.DoodleOrm.fileClass(file_class=department)
            self.addItem(item)
        else:
            self.showMessageBox()

    def addItems(self, labels: typing.List[DoodleServer.DoodleOrm.fileAttributeInfo_], p_str=None):
        for i in labels:
            item = self.item_class()
            item.file_class = i
            self.addItem(item)

    def doodleUpdata(self):
        self.addItems(self.core.queryFileClass())

    @QtCore.Slot()
    def setCore(self, item: ShotFileClassListWidgetItem):
        self.core.file_class = item.file_class


class ShotFileTypeListWidgetItem(QtWidgets.QListWidgetItem):
    _file_type_: DoodleServer.DoodleOrm.fileType

    @property
    def file_type(self):
        if not hasattr(self, '_file_type_'):
            assert AttributeError("小部件shotfileclass没有这个属性")
        return self._file_type_

    @file_type.setter
    def file_type(self, file_type):
        self._file_type_ = file_type
        self.setText(self._file_type_.file_type)


class ShotFileTypeListWidget(DoodleListWidegt):
    item_class = ShotFileTypeListWidgetItem

    def __init__(self, parent):
        super(ShotFileTypeListWidget, self).__init__(parent=parent)
        self.itemClicked.connect(self.setCore)

    def contextMenuEvent(self, arg__1):
        menu = QtWidgets.QMenu(self)
        add_dep_type = menu.addAction('添加')
        add_dep_type.triggered.connect(self.addFofler)
        menu.move(QtGui.QCursor().pos())
        return menu.show()

    @QtCore.Slot()
    def addFofler(self):
        deptype, is_ok = QtWidgets.QInputDialog.getText(self, '输入镜头', "文件类型(请用英文或拼音)",
                                                        QtWidgets.QLineEdit.Normal)
        if is_ok:
            if not self.findItems(deptype, QtCore.Qt.MatchExactly):
                item = ShotFileTypeListWidgetItem()
                item.file_type = DoodleServer.DoodleOrm.fileType(file_type=deptype)
                self.addItem(item)
            else:
                self.showMessageBox()

    def addItems(self, labels: typing.List[DoodleServer.DoodleOrm.fileType], p_str=None):
        for i in labels:
            item = self.item_class()
            item.file_type = i
            self.addItem(item)

    def doodleUpdata(self):
        self.addItems(self.core.queryFileType())

    @QtCore.Slot()
    def setCore(self, item: ShotFileTypeListWidgetItem):
        self.core.file_type = item.file_type


class AssNameListWidgetItem(QtWidgets.QListWidgetItem):
    _ass_name_data_: DoodleServer.DoodleOrm.assClass

    @property
    def ass_name_data(self):
        if not hasattr(self, '_ass_name_data_'):
            assert AttributeError("小部件中没有这个属性")
        return self._ass_name_data_

    @ass_name_data.setter
    def ass_name_data(self, ass_name_data):
        self._ass_name_data_ = ass_name_data
        localname = self._ass_name_data_.nameZNCH
        if not localname:
            localname = self._ass_name_data_.file_name
        else:
            localname = self._ass_name_data_.nameZNCH.localname
        self.setText(localname)


class AssFileTypeListWidgetItem(QtWidgets.QListWidgetItem):
    _file_type_: DoodleServer.DoodleOrm.fileType

    @property
    def file_type(self):
        if not hasattr(self, '_file_type_'):
            assert AttributeError("小部件assfiletype没有这个数据")
        return self._file_type_

    @file_type.setter
    def file_type(self, file_type):
        self._file_type_ = file_type
        self.setText(self._file_type_.file_type)


class AssNameListWidget(DoodleListWidegt):
    addZNCH = QtCore.Signal(DoodleServer.DoodleOrm.ZNch)
    updata = QtCore.Signal(DoodleServer.DoodleOrm.ZNch)
    item_class = AssNameListWidgetItem

    def __init__(self, parent):
        super(AssNameListWidget, self).__init__(parent=parent)
        self.itemClicked.connect(self.setCore)

    def contextMenuEvent(self, arg__1):
        menu = QtWidgets.QMenu(self)
        add_ass_folder = menu.addAction('添加')
        add_ass_folder.triggered.connect(self.addFofler)
        if self.selectedItems():
            rename_folder = menu.addAction("添加中文名称")
            rename_folder.triggered.connect(self.addAssZnChName)
        menu.move(QtGui.QCursor().pos())
        return menu.show()

    def addItems(self, labels: typing.List[DoodleServer.DoodleOrm.assClass], p_str=None):
        for i in labels:
            item = AssNameListWidgetItem()
            item.ass_name_data = i
            self.addItem(item)

    @QtCore.Slot()
    def addFofler(self):
        """添加资产类型文件夹"""
        ass_folder, is_ok = QtWidgets.QInputDialog.getText(self, '输入资产类型', "请用中文",
                                                           QtWidgets.QLineEdit.Normal)
        if is_ok:
            if not self.findItems(ass_folder, QtCore.Qt.MatchExactly):
                item = AssNameListWidgetItem()
                ass_class = DoodleServer.DoodleOrm.assClass(
                    file_name=DoodleServer.DoodleZNCHConvert.isChinese(ass_folder).easyToEn())
                ass_class.nameZNCH = DoodleServer.DoodleOrm.ZNch(localname=ass_folder)
                item.ass_name_data = ass_class
                self.addItem(item)
            else:
                self.showMessageBox()

    @QtCore.Slot()
    def addAssZnChName(self):
        ass_folder, is_ok = QtWidgets.QInputDialog.getText(self, '输入中文名称', "请用中文",
                                                           QtWidgets.QLineEdit.Normal)
        if is_ok:
            is_is = QtWidgets.QMessageBox.warning(self, "请确认", "拼音名称:{}\n中文名:{}".format(
                self.currentItem().text(), ass_folder),
                                                  QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
            if is_is == QtWidgets.QMessageBox.Yes:
                znch = self.currentItem().ass_name_data.nameZNCH
                if znch:
                    self.addZNCH.emit(DoodleServer.DoodleOrm.ZNch(localname=ass_folder))
                else:

                    znch.localname = ass_folder
                    self.updata.emit(znch)

    def doodleUpdata(self):
        self.addItems(self.core.queryAssname())

    @QtCore.Slot()
    def setCore(self, item: AssNameListWidgetItem):
        self.core.ass_class = item.ass_name_data


class AssFileTypeListWidget(DoodleListWidegt):

    def __init__(self, parent):
        super(AssFileTypeListWidget, self).__init__(parent=parent)
        self.itemClicked.connect(self.setCore)

    def contextMenuEvent(self, arg__1):
        menu = QtWidgets.QMenu(self)
        # 添加资产类型右键文件夹
        add_ass_type_folder = menu.addAction('添加')
        add_ass_type_folder.triggered.connect(self.addFofler)
        menu.move(QtGui.QCursor().pos())
        return menu.show()

    def addItems(self, labels: typing.List[DoodleServer.DoodleOrm.fileType], p_str=None):
        for i in labels:
            item = AssFileTypeListWidgetItem()
            item.file_type = i
            self.addItem(item)

    @QtCore.Slot()
    def addFofler(self):
        items: typing.List[str] = self.doodle_stting.assTypeFolder.copy()
        items = [i.format(self.ass.name) for i in items]

        ass_type, is_ok = QtWidgets.QInputDialog.getItem(self, '选择资产类型', '要先选择资产', items, 0, False)
        if is_ok:
            if not self.findItems(ass_type, QtCore.Qt.MatchExactly):
                item = AssFileTypeListWidgetItem()
                item.file_type = DoodleServer.DoodleOrm.fileType(file_type=ass_type)
                self.addItem(item)
            else:
                self.showMessageBox()

    def doodleUpdata(self):
        self.addItems(self.core.queryAssType())

    @QtCore.Slot()
    def setCore(self, item: AssFileTypeListWidgetItem):
        self.core.file_type = item.file_type


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = EpisodesListWidget()
    w.addItems(DoodleServer.Core.PrjShot(DoodleServer.DoodleSet.Doodlesetting()).queryEps())
    w.setWindowTitle("Remer")
    w.show()

    sys.exit(app.exec_())
