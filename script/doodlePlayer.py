import logging
import os
import pathlib
import subprocess
import time

from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets


class doodleScreenshot(QtWidgets.QDialog):

    def __init__(self, parent=None, path: str = "C:/"):
        super(doodleScreenshot, self).__init__(parent)
        self.savePath = path
        time.sleep(0.05)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
        self.setStyleSheet("""background-color:black;""")
        self.setWindowOpacity(0.5)
        desktop_rect = QtWidgets.QDesktopWidget().screenGeometry()
        self.setGeometry(desktop_rect)
        self.setCursor(QtCore.Qt.CrossCursor)

        self.blackMask = QtGui.QBitmap(desktop_rect.size())
        self.blackMask.fill(QtCore.Qt.black)
        self.mask = self.blackMask.copy()
        self.isDrawing = True
        self.startPoint = QtCore.QPoint()
        self.endPoint = QtCore.QPoint()

    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        if self.isDrawing:
            self.mask = self.blackMask.copy()
            pp = QtGui.QPainter(self.mask)
            pen = QtGui.QPen()
            pen.setStyle(QtCore.Qt.NoPen)
            pp.setPen(pen)
            brush = QtGui.QBrush(QtCore.Qt.white)
            pp.setBrush(brush)
            pp.drawRect(QtCore.QRect(self.startPoint, self.endPoint))
            self.setMask(QtGui.QBitmap(self.mask))

    def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
        if event.button() == QtCore.Qt.LeftButton:
            self.startPoint = event.pos()
            self.endPoint = self.startPoint
            self.isDrawing = True

    def mouseMoveEvent(self, event: QtGui.QMouseEvent) -> None:
        if self.isDrawing:
            self.endPoint = event.pos()
            self.update()

    def mouseReleaseEvent(self, event: QtGui.QMouseEvent) -> None:
        if event.button() == QtCore.Qt.LeftButton:
            self.endPoint = event.pos()
            screnshhot = QtWidgets.QApplication.primaryScreen().grabWindow(QtWidgets.QApplication.desktop().winId())
            rect = QtCore.QRect(self.startPoint, self.endPoint)
            outputRegion = screnshhot.copy(rect)
            outputRegion.save(self.savePath, format="JPG", quality=100)
            self.close()

# class


def videoToMp4(video: pathlib.Path, mp4_path: pathlib.Path):
    tools_bin_ffmpeg = "tools\\bin\\ffmpeg "
    tools_bin_ffmpeg += " -i " + str(video)
    tools_bin_ffmpeg += " -vcodec h264"
    tools_bin_ffmpeg += " -acodec mp2 -s 1920*1080 " + str(mp4_path)
    if not mp4_path.parent.is_dir():
        mp4_path.parent.mkdir(parents=True, exist_ok=True)
    os.system(tools_bin_ffmpeg)
    #ffmpeg.kill()


def imageToMp4(video_path: pathlib.Path, image_path: pathlib.Path):
    tools_bin_ffmpeg = "tools\\bin\\ffmpeg "
    list = image_path.parent.joinpath("list.txt")
    image = ["file '" + i.as_posix() + "'" for i in image_path.parent.iterdir() if i.suffix in ['.png','.exr','jpg']]
    list.write_text("\n".join(image))
    tools_bin_ffmpeg += "-r 25 -f concat -safe 0 -i " + str(image_path.parent.joinpath(list))
    tools_bin_ffmpeg += ' -c:v libx264 -vf fps=25 -pix_fmt yuv420p -s 1920*1080 ' + str(video_path)
    logging.info("命令ffmpeg %s",tools_bin_ffmpeg)
    if not video_path.parent.is_dir():
        video_path.parent.mkdir(parents=True, exist_ok=True)
    os.system(tools_bin_ffmpeg)


if __name__ == '__main__':
    pass