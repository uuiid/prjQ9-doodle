import typing
from PySide2 import QtCore, QtGui, QtWidgets
import DoodleServer
import script.DoodleCoreApp


class ScreenshotQlabel(QtWidgets.QLabel, script.DoodleCoreApp.core):
    screenshot_class: typing.Type[
        typing.Union[DoodleServer.baseClass.shotScreenshot, DoodleServer.baseClass.assScreenshot]]

    def doodleUpdata(self):
        scteenshot_obj = self.screenshot_class(self.core, self.doodle_set)
        path = scteenshot_obj.down()
        pixmap = QtGui.QPixmap()
        if path:
            pixmap.load(path.as_posix())
            pixmap = pixmap.scaled(self.geometry().size()*0.98, QtCore.Qt.KeepAspectRatio)
            self.setPixmap(pixmap)
        else:
            # painter = QtGui.QPainter()
            # painter.setFont()
            self.setText("请截屏  + 上传拍屏")



class shotScreenshotQlabel(ScreenshotQlabel):
    def __init__(self, parent):
        super(shotScreenshotQlabel, self).__init__(parent=parent)
        self.screenshot_class = DoodleServer.baseClass.shotScreenshot


class assScreenshotQlabel(ScreenshotQlabel):
    def __init__(self, parent):
        super(assScreenshotQlabel, self).__init__(parent=parent)
        self.screenshot_class = DoodleServer.baseClass.assScreenshot
