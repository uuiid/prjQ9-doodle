import sys

import qdarkstyle
from PySide2 import QtWidgets

import UiFile.register
import script.doodle_setting


class Rigister(QtWidgets.QMainWindow, UiFile.register.Ui_MainWindow):

    def __init__(self, doodle_set: script.doodle_setting.Doodlesetting):
        super().__init__()
        self.setupUi(self)
        self.doodle_set = doodle_set
        self.user_name = ""
        self.userText.textEdited.connect(self.GetUser)
        self.is_ok.setEnabled(False)

        self.is_ok.clicked.connect(self.subUserInfo)
        self.cancel.clicked.connect(lambda: self.close())

    def GetUser(self, text):
        self.doodle_set.user = text
        if not self.doodle_set.FTPconnectIsGood():
            self.is_ok.setEnabled(True)
        else:
            self.is_ok.setEnabled(False)

    def subUserInfo(self):
        if not self.doodle_set.FTPconnectIsGood():
            self.doodle_set.FTP_Register()
        self.doodle_set.writeDoodlelocalSet()
        self.close()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet())
    doodle_set = script.doodle_setting.Doodlesetting()
    w = Rigister(doodle_set)
    w.setWindowTitle("Remer")
    w.show()

    sys.exit(app.exec_())
