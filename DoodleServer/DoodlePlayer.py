import logging
import os
import pathlib
import subprocess
import sys
import time
import tempfile
from PySide2 import QtCore
from PySide2 import QtGui
from PySide2 import QtWidgets

import DoodleServer

__FFMPEG__ = str(DoodleServer.GETDOODLEROOT(pathlib.Path(".").absolute()).joinpath("tools","bin","ffmpeg"))
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


def videoToMp4(video: pathlib.Path, mp4_path: pathlib.Path, watermark: str = "none"):

    tools_bin_ffmpeg = __FFMPEG__
    tools_bin_ffmpeg += " -i " + str(video)
    tools_bin_ffmpeg += " -vcodec h264"
    tools_bin_ffmpeg += f""" -filter_complex "drawtext=text='{watermark}': fontcolor=0xc62d1d: fontsize=44: x=10:y=10: shadowx=3: shadowy=3" """
    tools_bin_ffmpeg += "-acodec mp2 -s 1920*1080 " + str(mp4_path)
    checkDirAndFile(mp4_path)
    os.system(tools_bin_ffmpeg)
    # ffmpeg.kill()


def checkDirAndFile(video_path):
    if not video_path.parent.is_dir():
        video_path.parent.mkdir(parents=True, exist_ok=True)
    if video_path.is_file():
        os.remove(video_path)


def imageToMp4(video_path: pathlib.Path, image_path: pathlib.Path, watermark: str = "none"):
    tools_bin_ffmpeg = __FFMPEG__
    my_list_ = image_path.parent.joinpath("my_list_.txt")
    image = ["file '" + i.name + "'" for i in image_path.parent.iterdir() if i.suffix in ['.png', '.exr', 'jpg']]
    my_list_.write_text("\n".join(image))
    tools_bin_ffmpeg += " -r 25 -f concat -safe 0 -i " + my_list_.as_posix()
    tools_bin_ffmpeg += f""" -filter_complex "drawtext=text='{watermark}': fontcolor=0xc62d1d: fontsize=44: x=10:y=10: shadowx=3: shadowy=3" """
    tools_bin_ffmpeg += '-c:v libx264 -pix_fmt yuv420p -s 1920*1080 ' + video_path.as_posix()
    logging.info("命令ffmpeg %s", tools_bin_ffmpeg)
    checkDirAndFile(video_path)
    os.system(tools_bin_ffmpeg)


def comMp4(video_path: pathlib.Path, paths: list):
    """
    for i in *.png; do echo "file '$i'" >> files.txt; echo "file_packet_metadata url=$i" >> files.txt; done

    ffmpeg -r 25 -f concat -safe 0 -i files.txt -filter_complex "drawtext=text='%{metadata:url}':
    fontcolor=0x808080: fontsize=34: x=w-tw- 10:y=h-th-10" -r 12 -c:v libx264 filename.mp4

    Args:
        video_path:
        paths:

    Returns:

    """
    tools_bin_ffmpeg = __FFMPEG__
    my_list_ = pathlib.Path(tempfile.gettempdir()).joinpath("my_list_.txt")
    image = ["file '" + i.as_posix() + "'" for i in paths]
    my_list_.write_text("\n".join(image))
    tools_bin_ffmpeg += " -f concat -safe 0 -i " + str(my_list_)
    # tools_bin_ffmpeg += """ -filter_complex " " """
    tools_bin_ffmpeg += ' -c:v libx264 -pix_fmt yuv420p -s 1920*1080 -movflags +faststart ' + video_path.as_posix()
    logging.info("命令ffmpeg %s", tools_bin_ffmpeg)
    checkDirAndFile(video_path)
    os.system(tools_bin_ffmpeg)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = doodleScreenshot(path=pathlib.Path("D:\\test\\tt.jpg").as_posix())
    w.setWindowTitle("Remer")
    w.show()

    sys.exit(app.exec_())

