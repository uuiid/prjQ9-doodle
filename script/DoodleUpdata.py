import urllib.request
import logging
from PyQt5 import QtCore
from PyQt5 import QtWidgets, QtGui


class downloadThread(QtCore.QThread):
    dowload_proes_signal = QtCore.pyqtSignal(int)
    jindu: int

    def __init__(self, url, fileobj, buffer):
        super(downloadThread, self).__init__()
        self.url = url
        self.fileobj = fileobj
        self.buffer = buffer

    def run(self) -> None:
        try:
            urllib.request.urlretrieve(url=self.url, filename=self.fileobj,
                                       reporthook=self.updataProgress)
            self.exit(0)
        except BaseException as err:
            logging.error("%s", err)

    def updataProgress(self, num, size, zhong):
        per = 100 * num * size / zhong
        if per > 99:
            per = 100
        print(per)
        self.jindu = per
        self.dowload_proes_signal.emit(per.__int__())
