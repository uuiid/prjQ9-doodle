import os
import pathlib
import shutil
import sys
import time
import logging
import subprocess
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


class videoConvert(object):
    def __init__(self, video_path: pathlib.Path, image_path: pathlib.Path):
        self.video_path = video_path
        self.image_path = image_path

    def videoToImage(self):
        tools_bin_ffmpeg = "tools\\bin\\ffmpeg "
        tools_bin_ffmpeg += "-i " + str(self.video_path) + " "
        tools_bin_ffmpeg += "-f fps=25 -f image2 -c:v png -s 1920*1080 "
        image_path_parent = self.image_path.parent
        tools_bin_ffmpeg += str(image_path_parent.joinpath(self.image_path.stem + "%05d" + ".png"))
        logging.info(tools_bin_ffmpeg)
        print(tools_bin_ffmpeg)
        if not image_path_parent.is_dir():
            image_path_parent.mkdir()
        else:
            for file in image_path_parent.iterdir():
                os.remove(str(file))
        ffmpeg_std = subprocess.Popen(tools_bin_ffmpeg,stdout=subprocess.PIPE)
        while True:
            line = ffmpeg_std.stdout.readline()
            if not line:
                break
            return line


# def doodleShot():
#     window = doodleScreenshot()
#     window.exec_()
if __name__ == '__main__':
    in_filename = pathlib.Path(r'D:\EP01_4.3.mp4')
    file = pathlib.Path(r"D:\test\EP01_.png")
    test = videoConvert(in_filename, file)
    test.videoToImage()
    # file.write_bytes(out)
    # app = QtWidgets.QApplication(sys.argv)
    # win = doodleScreenshot()
    # win.show()
    # app.exec_()
