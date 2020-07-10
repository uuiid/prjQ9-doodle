from PySide2 import QtCore, QtWidgets
import typing
import pathlib
import DoodleServer

import script.DoodleCoreApp


class ScreenshotPushButten(QtWidgets.QPushButton, script.DoodleCoreApp.core):
    screenshot_class: typing.Any

    @QtCore.Slot()
    def Screenshot(self):
        screenshot = self.screenshot_class(self.core, self.doodle_set)
        with screenshot.upload() as path:
            player_doodle_screenshot = DoodleServer.Player.doodleScreenshot(path=path.as_posix())
            self.doodle_app.browser.hide()
            player_doodle_screenshot.exec_()
            self.doodle_app.browser.show()


class shotScreenshotPushButten(ScreenshotPushButten):

    def __init__(self, parent):
        super(shotScreenshotPushButten, self).__init__(parent=parent)
        self.screenshot_class = DoodleServer.DoodleBaseClass.shotScreenshot
        # 链接截图功能和按钮
        self.clicked.connect(self.Screenshot)


class assScreenshotPushButten(ScreenshotPushButten):
    def __init__(self, parent):
        super(assScreenshotPushButten, self).__init__(parent=parent)
        self.screenshot_class = DoodleServer.DoodleBaseClass.assScreenshot
        # 链接截图功能和按钮
        self.clicked.connect(self.Screenshot)


class subFilbBook(QtWidgets.QPushButton,script.DoodleCoreApp.core):
    flib_book: typing.Any

    @QtCore.Slot()
    def subFlinBook(self):
        file, file_type = QtWidgets.QFileDialog.getOpenFileName(self,
                                                                "选择上传文件",
                                                                "",
                                                                "files (*.mp4 *.avi *.mov *.exr "
                                                                "*.png *.tga *.jpg)")

        flib_book = self.flib_book(self.core, self.doodle_set)

        # assert isinstance(flib_book, DoodleServer.baseClass.shotFBFile)
        if file:
            flib_book.upload(pathlib.Path(file))


class shotSubFilbBook(subFilbBook):

    def __init__(self, parent):
        super(shotSubFilbBook, self).__init__(parent=parent)
        self.flib_book = DoodleServer.baseClass.shotFBFile
        # 链接上传拍屏功能和按钮
        self.clicked.connect(self.subFlinBook)


class assSubFilbBook(subFilbBook):

    def __init__(self, parent):
        super(assSubFilbBook, self).__init__(parent=parent)
        self.flib_book = DoodleServer.baseClass.shotFBFile
        # 链接上传拍屏功能和按钮
        self.clicked.connect(self.subFlinBook)


class assFileClassPushButtem(QtWidgets.QPushButton, script.DoodleCoreApp.core):
    _file_clas_: DoodleServer.DoodleOrm.fileClass

    @property
    def file_clas(self):
        if not hasattr(self, '_file_clas_'):
            assert AttributeError("没有这个属性")
        return self._file_clas_

    @file_clas.setter
    def file_clas(self, file_clas):
        self._file_clas_ = file_clas

    def __init__(self, parent):
        super(assFileClassPushButtem, self).__init__(parent=parent)
        self.clicked.connect(self.setCore)

    @QtCore.Slot()
    def setCore(self):
        self.core.file_class = self._file_clas_
