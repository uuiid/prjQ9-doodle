import urllib.request
import requests
import logging

from PyQt5 import QtCore
from PyQt5 import QtWidgets, QtGui


class downloadThread(QtCore.QThread, QtWidgets.QWidget):
    dowload_proes_signal = QtCore.pyqtSignal(int)
    jindu: int

    def __init__(self, url, fileobj, buffer):
        super().__init__()
        self.url = url
        self.fileobj = fileobj
        self.buffer = buffer

    def run(self) -> None:
        try:
            doodle = requests.get(url=self.url)
            size = int(doodle.headers['Content-Length'])
            speed = 0
            with open(self.fileobj, "wb") as doodle_exe:
                for chunk in doodle.iter_content(chunk_size=10240):
                    if chunk:
                        doodle_exe.write(chunk)
                        speed += 1
                        speed_size = (10240 * speed) / size
                        self.dowload_proes_signal.emit(speed_size)
            # urllib.request.urlretrieve(url=self.url, filename=self.fileobj,
            #                            reporthook=self.updataProgress)

        except BaseException as err:
            logging.error("%s", err)
        self.exit(0)

    def updataProgress(self, num, size, zhong):
        per = 100 * num * size / zhong
        if per > 99:
            per = 100
        # print(per)
        self.jindu = per
        self.dowload_proes_signal.emit(per.__int__())


def undataDoodle(queue, url, fileobj):
    try:
        doodle = requests.get(url=url)
        size = int(doodle.headers['Content-Length'])
        speed = 0
        with open(fileobj, "wb") as doodle_exe:
            for chunk in doodle.iter_content(chunk_size=10240):
                if chunk:
                    doodle_exe.write(chunk)
                    speed += 1
                    speed_size = (10240 * speed) / size
                    queue.put(speed_size*100, block=True, timeout=10)
        # urllib.request.urlretrieve(url=self.url, filename=self.fileobj,
        #                            reporthook=self.updataProgress)

    except BaseException as err:
        logging.error("%s", err)
