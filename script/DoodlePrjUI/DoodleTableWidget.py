import logging
import os
import pathlib
import re
import typing

import pyperclip
from PySide2 import QtCore, QtGui, QtWidgets

import DoodleServer
import script.DoodleCoreApp


class FileTableWidgetItem(QtWidgets.QTableWidgetItem):
    _file_data_: DoodleServer.DoodleOrm.fileAttributeInfo_

    @property
    def file_data(self):
        if not hasattr(self, '_file_data_'):
            assert AttributeError("filetable没有这个属性!")
        return self._file_data_

    @file_data.setter
    def file_data(self, file_data):
        self._file_data_ = file_data


class FileTableWidget(QtWidgets.QTableWidget, script.DoodleCoreApp.core):
    subInfo = QtCore.Signal(DoodleServer.DoodleOrm.fileAttributeInfo_)
    dowfile = QtCore.Signal(DoodleServer.DoodleOrm.fileAttributeInfo_)

    doodle_refresh = QtCore.Signal()

    def __init__(self, parent):
        super(FileTableWidget, self).__init__(parent=parent)
        self.setAcceptDrops(True)
        self.itemClicked.connect(self.setCore)
        self.itemDoubleClicked.connect(self.openFile)

    def addTableItems(self, labels: typing.List[DoodleServer.DoodleOrm.fileAttributeInfo_]):
        for index, item in enumerate(labels):
            self.insertRow(index)
            # 设置版本号
            version_item = FileTableWidgetItem(f'v{item.version:0>4d}')
            version_item.file_data = item
            self.setItem(index, 0, version_item)
            # 设置概述
            file_infor = [""]
            if item.infor:
                file_infor = re.split(r"\|", item.infor)
            infor_item = FileTableWidgetItem(file_infor[0])
            infor_item.file_data = item
            infor_item.setToolTip("\n".join(file_infor))
            self.setItem(index, 1, infor_item)
            # 设置制作人
            user_item = FileTableWidgetItem(item.user)
            user_item.file_data = item
            self.setItem(index, 2, user_item)
            # 设置后缀
            suffix_item = FileTableWidgetItem(item.fileSuffixes)
            suffix_item.file_data = item
            self.setItem(index, 3, suffix_item)
            # 设置id
            id_item = FileTableWidgetItem(item.id.__str__())
            id_item.file_data = item
            self.setItem(index, 4, id_item)

        logging.info("跟新文件列表")

    @QtCore.Slot()
    def openShotExplorer(self, item: FileTableWidgetItem):
        item = self.currentItem()
        joinpath = self.doodle_set.project.joinpath(item.file_data.file_path.parent)
        try:
            os.startfile(joinpath)
        except FileNotFoundError:
            logging.error("没有这样的目录")
            QtWidgets.QMessageBox.warning(self, "警告:", f"没有找到目录{joinpath.as_posix()}",
                                          QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)

    @QtCore.Slot()
    def openFile(self, item: FileTableWidgetItem):
        joinpath = self.doodle_set.project.joinpath(item.file_data.file_path)
        try:
            os.startfile(joinpath)
        except FileNotFoundError:
            logging.error("没有这样的文件")
            QtWidgets.QMessageBox.warning(self, "警告:", f"没有找到文件{joinpath.as_posix()}",
                                          QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)

    @QtCore.Slot()
    def copyPathToClipboard(self, item: FileTableWidgetItem):
        pyperclip.copy(item.file_data.file_path.parent.as_posix())

    @QtCore.Slot()
    def copyNameToClipboard(self, item: FileTableWidgetItem):
        pyperclip.copy(item.file_data.file_path.name)

    def localuploadFiles(self):
        file, file_type = QtWidgets.QFileDialog.getOpenFileName(self,
                                                                "选择指定文件",
                                                                "",
                                                                "files (*.mb *.ma *.uproject"
                                                                " *.max *.fbx *.png *.tga *.jpg)")
        if file:
            dowclass = DoodleServer.baseClass.doodleFileFactory(self.core, self.currentItem().file_data.fileSuffixes)
            if dowclass:
                dowclass_obj = dowclass(self.core, self.doodle_set)
                QtWidgets.QMessageBox.critical(self, "复制中", "请等待.....")
                dowclass_obj.down(pathlib.Path(file))
            else:
                QtWidgets.QMessageBox.critical(self, "无法下载此文件.....")

    @QtCore.Slot()
    def updataClass(self, item: FileTableWidgetItem):
        remarks_info, is_ok = QtWidgets.QInputDialog.getText(self,
                                                             "填写备注(中文)",
                                                             "备注",
                                                             QtWidgets.QLineEdit.Normal)[0]
        if is_ok:
            item.file_data.infor += remarks_info
            self.core.updataClass(item.file_data)

    def doodleClear(self):
        mrowtmp = self.rowCount()
        while mrowtmp >= 0:
            self.removeRow(mrowtmp)
            mrowtmp = mrowtmp - 1

    def doodleUpdata(self):
        self.addTableItems(self.core.queryFile())

    def setCore(self, item: FileTableWidgetItem):
        self.core.query_file = item.file_data

    @QtCore.Slot()
    def downFile(self):
        path = QtWidgets.QFileDialog.getExistingDirectory(self,
                                                          "选择下载目录",
                                                          "",
                                                          QtWidgets.QFileDialog.ShowDirsOnly)

        dowclass = DoodleServer.baseClass.doodleFileFactory(self.core, self.currentItem().file_data.fileSuffixes)
        if dowclass:
            dowclass_obj = dowclass(self.core, self.doodle_set)
            QtWidgets.QMessageBox.critical(self, "复制中", "请等待.....")
            dowclass_obj.down(pathlib.Path(path))
            os.startfile(path)
        else:
            QtWidgets.QMessageBox.critical(self, "无法下载此文件.....")


class assTableWidget(FileTableWidget):
    appointfile = QtCore.Signal(pathlib.Path)

    # def __init__(self,parent):
    #     super(assTableWidget, self).__init__(parent=parent)
    #     self.itemClicked.connect(self.setCore)

    def contextMenuEvent(self, arg__1):
        menu = QtWidgets.QMenu(self)
        if self.selectedItems():
            if self.selectedItems():
                open_ass_explorer = menu.addAction("打开文件管理器")
                open_ass_explorer.triggered.connect(self.openShotExplorer)
                add_info = menu.addAction("更新概述")
                add_info.triggered.connect(self.updataClass)
                filestate = menu.addAction("标记问题")
                filestate.triggered.connect(lambda: self.subInfo.emit(self.currentItem().file_data))
                add_ass_file_dow = menu.addAction("下载文件")
                add_ass_file_dow.triggered.connect(self.downFile)
            add_ass_file = menu.addAction('上传(同步)文件')
            add_ass_file.triggered.connect(self.subFilePath)
            get_ass_path = menu.addAction('指定文件')
            get_ass_path.triggered.connect(self.appointFilePath)
        menu.move(QtGui.QCursor().pos())
        return menu.show()

    @QtCore.Slot()
    def appointFilePath(self):
        subclass_obj, path = self.__subAndAppoint__()
        if not subclass_obj:
            subclass_obj.appoint(path)
        self.doodle_refresh.emit()

    @QtCore.Slot()
    def subFilePath(self):
        subclass_obj, path = self.__subAndAppoint__()
        if not subclass_obj:
            subclass_obj.upload(path)
        self.doodle_refresh.emit()

    def __subAndAppoint__(self) -> typing.Tuple[DoodleServer.baseClass.assUePrj, pathlib.Path]:
        file, file_type = QtWidgets.QFileDialog.getOpenFileName(self,
                                                                "选择指定文件",
                                                                "",
                                                                "files (*.mb *.ma *.uproject"
                                                                " *.max *.fbx *.png *.tga *.jpg)")
        remarks_info = QtWidgets.QInputDialog.getText(self,
                                                      "填写备注(中文)",
                                                      "备注",
                                                      QtWidgets.QLineEdit.Normal)[0]
        if file:
            path = pathlib.Path(file)
            subclass = DoodleServer.baseClass.doodleFileFactory(self.core, path.suffix)
            if subclass:
                subclass_obj = subclass(self.core, self.doodle_set)
                subclass_obj.infor = remarks_info
                return subclass_obj, path
        return None, None


class shotTableWidget(FileTableWidget):

    # def __init__(self, parent):
    #     super(shotTableWidget, self).__init__(parent=parent)
    #     self.itemClicked.connect(self.setCore)

    def contextMenuEvent(self, arg__1):
        menu = QtWidgets.QMenu(self)
        if self.selectedItems():
            open_explorer = menu.addAction('打开文件管理器')  # 用文件管理器打开文件位置
            open_explorer.triggered.connect(self.openShotExplorer)
            # copy文件名称或者路径到剪切板
            add_info = menu.addAction("更新概述")
            add_info.triggered.connect(self.updataClass)
            filestate = menu.addAction("标记问题")
            filestate.triggered.connect(lambda: self.subInfo.emit(self.currentItem().file_data))
            copy_name_to_clip = menu.addAction('复制名称')
            copy_name_to_clip.triggered.connect(self.copyNameToClipboard)
            copy_path_to_clip = menu.addAction('复制路径')
            copy_path_to_clip.triggered.connect(self.copyPathToClipboard)
            # 导出Fbx和abc选项
            export_maya = menu.addAction("导出maya相机和fbx")
            export_maya.triggered.connect(self.export)
            import_ue = menu.addAction("导入ue")
            import_ue.triggered.connect(lambda: self.imporpUe4.emit(self.currentItem().file_data))
            menu.move(QtGui.QCursor().pos())
        return menu.show()

    # <editor-fold desc="拖拽函数">
    def enableBorder(self, enable):
        if enable:
            self.setStyleSheet("border:3px solid #165E23")
        else:
            self.setStyleSheet('')

    def dragEnterEvent(self, a0: QtGui.QDragEnterEvent) -> None:
        if a0.mimeData().hasUrls():
            a0.acceptProposedAction()
            self.enableBorder(True)
        else:
            a0.ignore()

    def dragLeaveEvent(self, a0: QtGui.QDragLeaveEvent) -> None:
        # 离开时取消高亮
        self.enableBorder(False)

    def dragMoveEvent(self, event):
        # super(shotTableWidget, self).dragMoveEvent(event)
        pass

    def dropEvent(self, a0: QtGui.QDropEvent) -> None:
        super(shotTableWidget, self).dropEvent(a0)
        print("")
        if a0.mimeData().hasUrls():
            # 检测文件路劲和类型,限制拖动
            if len(a0.mimeData().urls()) == 1:
                url = a0.mimeData().urls()[0]
                path = pathlib.Path(url.toLocalFile())
                logging.info('检测到文件%s拖入窗口', path)
                # 获得文件路径并进行复制

                # 创建maya文件并上传
                DoodleServer.baseClass.shotMayaFile(self.core, self.doodle_set).upload(path)

                self.enableBorder(False)
            else:
                pass

        else:
            a0.ignore()

    @QtCore.Slot()
    def export(self, item: FileTableWidgetItem):
        item = self.currentItem()
        self.core.query_file = item.file_data
        DoodleServer.baseClass.shotMayaExportFile(self.core, self.doodle_set).export()

    # </editor-fold>
