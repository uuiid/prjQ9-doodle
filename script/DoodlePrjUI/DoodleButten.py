from PySide2 import QtCore, QtWidgets
import typing
import pathlib
import DoodleServer

import script.DoodleCore


class ScreenshotPushButten(QtWidgets.QPushButton, script.DoodleCore.core):
    app: DoodleServer.DoodleCore.Shot
    Screenshot: typing.Any

    @QtCore.Slot()
    def Screenshot(self):
        screenshot = self.Screenshot(self.app.code, self.app.doodle_set)
        with screenshot.upload() as path:
            player_doodle_screenshot = DoodleServer.Player.doodleScreenshot(path=path.as_posix())
            self.app.browser.hide()
            player_doodle_screenshot.exec_()
            self.app.browser.show()


class shotScreenshotPushButten(ScreenshotPushButten):

    def __init__(self, parent):
        super(shotScreenshotPushButten, self).__init__(parent=parent)
        self.Screenshot = DoodleServer.DoodleBaseClass.shotScreenshot
        # 链接截图功能和按钮
        self.clicked.connect(self.Screenshot)


class assScreenshotPushButten(ScreenshotPushButten):
    def __init__(self, parent):
        super(assScreenshotPushButten, self).__init__(parent=parent)
        self.Screenshot = DoodleServer.DoodleBaseClass.assScreenshot
        # 链接截图功能和按钮
        self.clicked.connect(self.Screenshot)


class subFilbBook(QtWidgets.QPushButton):
    flib_book: typing.Any

    @QtCore.Slot()
    def subFlinBook(self):
        file, file_type = QtWidgets.QFileDialog.getOpenFileName(self,
                                                                "选择上传文件",
                                                                "",
                                                                "files (*.mp4 *.avi *.mov *.exr "
                                                                "*.png *.tga *.jpg)")
        flib_book = self.flib_book(self.app.code, self.app.doodle_set)
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
