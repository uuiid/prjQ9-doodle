import sys
import qdarkstyle
# import script
from PySide2 import QtCore, QtGui, QtWidgets

import UiFile.ProjectBrowser
import DoodleServer
import script.DoodleBrowserGUI
import script.DoodleTray
import script.DoodleSetGui
import script.DoodleRegister
import script.Server


class DoodleMain(QtWidgets.QApplication):
    @property
    def core(self) -> DoodleServer.Core.PrjCore:
        return self._core_

    def __init__(self):
        super(DoodleMain, self).__init__(sys.argv)
        self.doodle_set = DoodleServer.Set.Doodlesetting()
        self._core_ = DoodleServer.Core.PrjShot(self.doodle_set)
        QtWidgets.QApplication.setQuitOnLastWindowClosed(False)
        self.setStyleSheet(qdarkstyle.load_stylesheet_pyside2())

        self.browser = None
        self.tray = None
        self.doodle_set_gui = None
        self.server = script.Server.DoodleServer__()
        self.server.setDaemon(True)
        self.server.start()
        # tray_icon = ProjectBrowserGUI()
        # tray_icon.showMessage('文件管理', 'hello')
        #
        # self.openProjectBrowserGUI()
        # sys.exit(self.exec_())

    def codeToShot(self):
        self._core_ = DoodleServer.Core.PrjShot(self.doodle_set)

    def codeToAss(self):
        self._core_ = DoodleServer.Core.PrjAss(self.doodle_set)

    def DoodleQuery(self):
        self.tray.setVisible(False)
        self.tray = None
        sys.exit()

    def openProjectBrowserGUI(self):
        self.browser = script.DoodleBrowserGUI.ProjectBrowserGUI()
        self.browser.show()

    def showSet(self):
        self.doodle_set_gui = script.DoodleSetGui.DoodlesettingGUI()
        self.doodle_set_gui.show()

    def showTray(self):
        self.tray = script.DoodleTray.SystemTrayIcon(QtGui.QIcon("datas/icon.png"), None)
        self.tray.showMessage('文件管理', 'hello')
        self.tray.show()

    def showRigister(self):
        script.DoodleRegister.Rigister(self.doodle_set).show()
# m = DoodleMain()
# m.showTray()
# m.exec_()
