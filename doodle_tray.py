# -*- coding: UTF-8 -*-
import logging
import os
import pathlib
import subprocess
import sys
import tempfile
import time
import threading
import queue

from PySide2 import QtCore
from PySide2 import QtWidgets, QtGui
import qdarkstyle
import script.DoodleUpdata
import script.ProjectBrowserGUI
import script.doodleLog
import script.doodle_setting
import script.synXml
import script.DoodleUpdata
import script.DoodleRegister
import script.DoodleUpdata
import script.DoodleLocalConnection

class SystemTrayIcon(QtWidgets.QSystemTrayIcon):
    timeSyn = 7200000
    version = 1.100
    setwin: script.doodle_setting.DoodlesettingGUI = None
    project_browser: script.ProjectBrowserGUI.ProjectBrowserGUI = None

    def __init__(self, icon, parent=None):
        self.tray = QtWidgets.QSystemTrayIcon.__init__(self, icon, parent)
        self.doodleSet = script.doodle_setting.Doodlesetting()
        self.ta_log = logging
        self.par = parent

        self.timer = QtCore.QTimer(self)
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.file_syns)
        # self.timer.timeout.connect(lambda: self.Updata(lambda: float(self.doodleSet.version) > self.version))
        self.timer.start(self.timeSyn)
        # 添加本地线程服务器
        self.localServer = script.DoodleLocalConnection.DoodleServer(self.doodleSet)
        self.localServer.setDaemon(True)
        self.localServer.start()


        self.setToolTip(f'文件管理系统-{self.version}')
        menu = QtWidgets.QMenu(parent)

        file_sync = menu.addAction('同步文件')
        file_sync.triggered.connect(self.file_syns)

        project = menu.addAction('项目管理器')
        project.triggered.connect(self.openProject)

        # <editor-fold desc="动作">
        UEmenu = menu.addMenu('UE动作')

        UE_open = UEmenu.addAction('打开UE')
        UE_open.triggered.connect(self.openUE)

        UE_sync = UEmenu.addAction('同步UE')
        UE_sync.triggered.connect(self.UEsync)
        # </editor-fold>

        install_plug:QtWidgets.QMenu = menu.addMenu("安装插件")
        install_maya:QtWidgets.QAction = install_plug.addAction("安装maya插件")
        install_maya.triggered.connect(self.installMaya)

        setmenu = menu.addAction('设置')
        setmenu.triggered.connect(self.setGUI)

        updata = menu.addAction('更新')
        updata.triggered.connect(lambda: self.Updata(True))

        register = menu.addAction("注册")
        register.triggered.connect(self.register)

        exit_ = menu.addAction('退出')
        exit_.triggered.connect(self.myexit)

        menu.addSeparator()
        self.setContextMenu(menu)

        # self.Updata(lambda: float(self.doodleSet.version) > self.version)

    def lookdepartment(self):
        if self.doodleSet.department in ['VFX', 'Light', 'modle']:
            pass

    def file_syns(self):
        if self.doodleSet.department in ['Light', 'VFX']:
            include_ = ["*"]
            if self.doodleSet.department in ["VFX"]:
                include_ = ["*\\VFX\\*"]
            script.synXml.FreeFileSync(doc=self.doodleSet.doc,
                                       syn_file=self.doodleSet.getsever(),
                                       program=self.doodleSet.FreeFileSync,
                                       file_name='{}-ep-{}'.format(self.doodleSet.department, self.doodleSet.synEp),
                                       user=self.doodleSet.ftpuser,
                                       ip_=self.doodleSet.ftpip,
                                       password=self.doodleSet.password,
                                       include=include_).run()

            self.ta_log.info('同步时间: %s', time.asctime(time.localtime(time.time())))

    def myexit(self):
        # QtWidgets.QSystemTrayIcon.deleteLater(self)
        self.ta_log.info('系统退出 __时间: %s', time.asctime(time.localtime(time.time())))
        self.setVisible(False)
        self.tray = None
        sys.exit()

    def setGUI(self):
        if isinstance(self.setwin, script.doodle_setting.DoodlesettingGUI):
            self.setwin.show()
        else:
            self.setwin = script.doodle_setting.DoodlesettingGUI()
            self.setwin.show()
        self.ta_log.info('打开了设置')

    def UEsync(self):
        if self.doodleSet.department in ['Light', 'VFX', 'modle']:
            synPath = [{'Left': 'D:\\Source\\UnrealEngine', 'Right': 'W:\\data\\Source\\UnrealEngine'}]
            synUE = 'UE_syn'
            script.synXml.FreeFileSync(doc=self.doodleSet.doc,
                                       syn_file=synPath,
                                       program=self.doodleSet.FreeFileSync,
                                       file_name=synUE,
                                       user=self.doodleSet.ftpuser,
                                       ip_=self.doodleSet.ftpip,
                                       password=self.doodleSet.password,
                                       include=['\\Engine\\*']).run()

    @staticmethod
    def openUE():
        script.doodleLog.ta_log.info('启动UE')
        subprocess.Popen("D:\\Source\\UnrealEngine\\Engine\\Binaries\\Win64\\UE4Editor.exe")

    def openProject(self):
        if isinstance(self.project_browser, script.ProjectBrowserGUI.ProjectBrowserGUI):
            self.project_browser = script.ProjectBrowserGUI.ProjectBrowserGUI()
            self.project_browser.show()
        else:
            self.project_browser = script.ProjectBrowserGUI.ProjectBrowserGUI()
            self.project_browser.show()
        self.ta_log.info('打开了项目管理器')

    def Updata(self, unpdata_=True):
        script.DoodleUpdata.downloadThread(self.doodleSet).run()
        sys.exit(self)

    def register(self):
        script.DoodleRegister.Rigister(self.doodleSet).show()

    def GUIReinitialize(self):
        self.project_browser = None
        self.setwin = None

    def installMaya(self):
        mode = "+ doodle_main.py 1.1 {_path_}\n" \
               "MYMODULE_LOCATION:= {_path_}\n" \
               "PATH+:= {_path_}/scripts;{_path_}/plug-ins\n" \
               "PYTHONPATH+:= {_path_}/scripts".format(_path_="C:/Program Files/doodle/tools/maya_plug")
        maya_plug_path = self.doodleSet.doc.parent.joinpath("maya","modules")
        if not maya_plug_path.is_dir():
            maya_plug_path.mkdir(parents=True, exist_ok=True)
        maya_plug_path.joinpath("Doodle.mod").write_text(mode)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    QtWidgets.QApplication.setQuitOnLastWindowClosed(False)
    # w = QtWidgets.QWidget()
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyside2())

    tray_icon = SystemTrayIcon(QtGui.QIcon("datas/icon.png"), None)
    tray_icon.showMessage('文件管理', 'hello')
    tray_icon.show()

    sys.exit(app.exec_())
