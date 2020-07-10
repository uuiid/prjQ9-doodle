import sys

# import script
from PySide2 import QtCore, QtGui, QtWidgets

import UiFile.ProjectBrowser
import DoodleServer


class ProjectBrowserGUI(QtWidgets.QMainWindow, UiFile.ProjectBrowser.Ui_MainWindow):
    def __init__(self):
        super(ProjectBrowserGUI, self).__init__(parent=None)
        self.setupUi(self)


class DoodleMain(QtWidgets.QApplication):
    @property
    def core(self) -> DoodleServer.Core.PrjCore:
        return self._core_

    def __init__(self):
        super(DoodleMain, self).__init__(sys.argv)
        self.doodle_set = DoodleServer.Set.Doodlesetting()
        self._core_ = DoodleServer.Core.PrjShot(self.doodle_set)

        self.browser = ProjectBrowserGUI()
        # app = QtWidgets.QApplication(sys.argv)
        QtWidgets.QApplication.setQuitOnLastWindowClosed(False)

        # tray_icon = ProjectBrowserGUI()
        # tray_icon.showMessage('文件管理', 'hello')
        self.browser.show()

        sys.exit(self.exec_())

    def codeToShot(self):
        self._core_ = DoodleServer.Core.PrjShot(self.doodle_set)

    def codeToAss(self):
        self._core_ = DoodleServer.Core.PrjAss(self.doodle_set)

    def DoodleQuery(self):
        sys.exit(self.exec_())


DoodleMain()
