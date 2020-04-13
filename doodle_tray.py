# -*- coding: UTF-8 -*-
import pathlib
import sys
import time
from subprocess import run
from subprocess import Popen

from PyQt5 import QtCore
from PyQt5 import QtWidgets, QtGui

import script.debug
import script.doodle_setting
import script.readServerDiectory
import script.synXml
import script.ProjectBrowserGUI
import script.doodleLog
import qdarkgraystyle


class SystemTrayIcon(QtWidgets.QSystemTrayIcon):
    timeSyn = 7200000

    def __init__(self, icon, parent=None):
        self.tray = QtWidgets.QSystemTrayIcon.__init__(self, icon, parent)
        self.doodleSet = script.doodle_setting.Doodlesetting()
        self.ta_log = script.doodleLog.get_logger(__name__)

        self.timer = QtCore.QTimer(self)
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.file_syns)
        self.timer.start(self.timeSyn)

        self.setToolTip('文件管理系统-0.2.2')
        menu = QtWidgets.QMenu(parent)

        file_sync = menu.addAction('同步文件')
        file_sync.triggered.connect(self.file_syns)

        project = menu.addAction('项目管理器')
        project.triggered.connect(self.openProject)

        UEmenu = menu.addMenu('UE动作')

        UE_sync = UEmenu.addAction('同步UE')
        UE_sync.triggered.connect(self.UEsync)

        UE_open = UEmenu.addAction('打开UE')
        UE_open.triggered.connect(self.openUE)

        setmenu = menu.addAction('设置')
        setmenu.triggered.connect(self.setGUI)

        exit_ = menu.addAction('退出')
        exit_.triggered.connect(self.myexit)

        menu.addSeparator()
        self.setContextMenu(menu)

    def lookdepartment(self):
        if self.doodleSet.department in ['VFX', 'Light', 'modle']:
            pass

    def file_syns(self):
        if self.doodleSet.department in ['Light', 'VFX']:
            self.ta_log.info('进行同步')
            readServerDiectory = script.readServerDiectory.SeverSetting().setting

            self.ta_log.info('读取服务器中同步目录 %s', readServerDiectory)
            synfile_Name = '{}-ep-{}'.format(self.doodleSet.department, self.doodleSet.synEp)
            synfile = script.synXml.weiteXml(self.doodleSet.doc,
                                             readServerDiectory['ep{:0>3d}Syn'.format(self.doodleSet.synEp)],
                                             fileName=synfile_Name)
            program = pathlib.Path('C:\\PROGRA~1\\FREEFI~1\\FreeFileSync.exe')
            run('{} "{}"'.format(program, synfile), shell=True)

            self.ta_log.info('同步时间: %s', time.asctime(time.localtime(time.time())))
            # script.debug.debug("同步时间: {}\n".format(time.asctime(time.localtime(time.time()))))

    def myexit(self):
        # QtWidgets.QSystemTrayIcon.deleteLater(self)
        self.ta_log.info('系统退出 __时间: %s', time.asctime(time.localtime(time.time())))
        self.setVisible(False)
        self.tray = None
        sys.exit()

    def setGUI(self):
        setwin = script.doodle_setting.DoodlesettingGUI()
        self.ta_log.info('打开了设置')
        setwin.show()

    def UEsync(self):
        if self.doodleSet.department in ['Light', 'VFX', 'modle']:
            synPath = [{'Left': 'D:\\Source\\UnrealEngine', 'Right': 'W:\\data\\Source\\UnrealEngine'}]
            synUE = 'UE_syn'
            synfile = script.synXml.weiteXml(self.doodleSet.doc,
                                             synPath,
                                             Filter={'include': ['\\Engine\\*']},
                                             fileName=synUE)
            program = self.doodleSet.FreeFileSync
            run('{} "{}"'.format(program, synfile), shell=True)

    @staticmethod
    def openUE():
        script.doodleLog.ta_log.info('启动UE')
        Popen("D:\\Source\\UnrealEngine\\Engine\\Binaries\\Win64\\UE4Editor.exe")

    def openProject(self):
        self.project_browser = script.ProjectBrowserGUI.ProjectBrowserGUI()
        self.ta_log.info('打开了项目管理器')
        self.project_browser.show()


def main():
    app = QtWidgets.QApplication(sys.argv)
    QtWidgets.QApplication.setQuitOnLastWindowClosed(False)
    # w = QtWidgets.QWidget()
    app.setStyleSheet(qdarkgraystyle.load_stylesheet())

    tray_icon = SystemTrayIcon(QtGui.QIcon('datas/icon.png'), None)
    tray_icon.showMessage('文件管理', 'hello')
    tray_icon.show()

    sys.exit(app.exec_())


main()
