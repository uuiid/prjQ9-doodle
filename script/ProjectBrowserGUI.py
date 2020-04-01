# -*- coding: UTF-8 -*-
import UiFile.ProjectBrowser
import script.doodle_setting
from PyQt5 import QtWidgets


class ProjectBrowserGUI(QtWidgets.QMainWindow, UiFile.ProjectBrowser.Ui_MainWindow):
    def __init__(self):
        super(ProjectBrowserGUI, self).__init__()
        self.setting = script.doodle_setting.Doodlesetting()

        self.setupUi(self)
