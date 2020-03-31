# -*- coding: UTF-8 -*-
import pathlib
import sys
import time
from subprocess import run

from PyQt5 import QtCore
from PyQt5 import QtWidgets, QtGui

import script.debug
import script.doodle_setting
import script.readServerDiectory
import script.synXml


class SystemTrayIcon(QtWidgets.QSystemTrayIcon):
    # patterns = "*"
    # ignore_patterns = ""
    # ignore_directories = False
    # case_sensitive = True
    # path = ""
    # go_recursively = True
    # my_event_handler = ''
    setting = {}
    timeSyn = 7200000

    def __init__(self, icon, parent=None):
        self.tray = QtWidgets.QSystemTrayIcon.__init__(self, icon, parent)
        self.doodleSet = script.doodle_setting.Doodlesetting()
        self.setting = self.doodleSet.getString()
        # print(self.setting)
        # self.patterns = '*'
        # self.ignore_patterns = ""
        # self.ignore_directories = False
        # self.case_sensitive = True
        # self.path = "D:\\ue_prj"
        # self.go_recursively = True

        self.timer = QtCore.QTimer(self)
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.file_syns)
        self.timer.start(self.timeSyn)

        self.setToolTip('文件管理系统-0.1.2')
        menu = QtWidgets.QMenu(parent)

        file_sync = menu.addAction('同步文件')
        file_sync.triggered.connect(self.file_syns)

        setmenu = menu.addAction('设置')
        setmenu.triggered.connect(self.setGUI)

        exit_ = menu.addAction('退出')
        exit_.triggered.connect(self.myexit)

        menu.addSeparator()
        self.setContextMenu(menu)

    def file_syns(self):
        if self.setting['department'] == 'Light':
            readServerDiectory = script.readServerDiectory.SeverSetting().getsever()
            synfile_Name = '{}-ep-{}'.format(readServerDiectory["department"], readServerDiectory['ep'])
            synfile = script.synXml.weiteXml(self.doodleSet.doc,
                                             readServerDiectory['Synchronization'],
                                             synfile_Name)
            program = pathlib.Path('C:\\PROGRA~1\\FREEFI~1\\FreeFileSync.exe')
            run('{} "{}"'.format(program, synfile), shell=True)
            script.debug.debug("同步时间: {}\n".format(time.asctime(time.localtime(time.time()))))

    def myexit(self):
        QtWidgets.QSystemTrayIcon.deleteLater(self)
        # self.tray = None
        sys.exit()

    def setGUI(self):
        setwin = script.doodle_setting.DoodlesettingGUI()
        setwin.show()


def main():
    app = QtWidgets.QApplication(sys.argv)
    QtWidgets.QApplication.setQuitOnLastWindowClosed(False)
    # w = QtWidgets.QWidget()
    tray_icon = SystemTrayIcon(QtGui.QIcon('datas/icon.png'), None)
    tray_icon.show()
    tray_icon.showMessage('文件管理', 'hello')

    sys.exit(app.exec_())


main()
