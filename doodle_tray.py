# -*- coding: UTF-8 -*-
import logging
import os
import pathlib
import subprocess
import sys
import tempfile
import time
import urllib.request

import qdarkgraystyle
import urllib3
from PyQt5 import QtCore
from PyQt5 import QtWidgets, QtGui

import script.DoodleUpdata
import script.ProjectBrowserGUI
import script.debug
import script.doodleLog
import script.doodle_setting
import script.synXml


class SystemTrayIcon(QtWidgets.QSystemTrayIcon):
    timeSyn = 7200000
    version = 1.052

    def __init__(self, icon, parent=None):
        self.tray = QtWidgets.QSystemTrayIcon.__init__(self, icon, parent)
        self.doodleSet = script.doodle_setting.Doodlesetting()
        self.ta_log = logging

        self.timer = QtCore.QTimer(self)
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.file_syns)
        self.timer.timeout.connect(lambda: self.Updata(lambda: float(self.doodleSet.version) > self.version))
        self.timer.start(self.timeSyn)

        self.setToolTip(f'文件管理系统-{self.version}')
        menu = QtWidgets.QMenu(parent)

        file_sync = menu.addAction('同步文件')
        file_sync.triggered.connect(self.file_syns)

        project = menu.addAction('项目管理器')
        project.triggered.connect(self.openProject)

        UEmenu = menu.addMenu('UE动作')

        UE_open = UEmenu.addAction('打开UE')
        UE_open.triggered.connect(self.openUE)

        UE_sync = UEmenu.addAction('同步UE')
        UE_sync.triggered.connect(self.UEsync)

        setmenu = menu.addAction('设置')
        setmenu.triggered.connect(self.setGUI)

        updata = menu.addAction('更新')
        updata.triggered.connect(lambda: self.Updata(True))

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
            include_ = ["*"]
            if self.doodleSet.department in ["VFX"]:
                include_ = ["*\\VFX\\*"]
            readServerDiectory = self.doodleSet.getsever()

            self.ta_log.info('读取服务器中同步目录 %s', readServerDiectory)
            synfile_Name = '{}-ep-{}'.format(self.doodleSet.department, self.doodleSet.synEp)
            synfile = script.synXml.weiteXml(self.doodleSet.doc,
                                             readServerDiectory,
                                             Include=include_,
                                             fileName=synfile_Name)
            program = self.doodleSet.FreeFileSync
            subprocess.run('{} "{}"'.format(program, synfile), shell=True)

            self.ta_log.info('同步时间: %s', time.asctime(time.localtime(time.time())))

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
                                             Include=['\\Engine\\*'],
                                             fileName=synUE)
            program = self.doodleSet.FreeFileSync
            subprocess.run('{} "{}"'.format(program, synfile), shell=True)

    @staticmethod
    def openUE():
        script.doodleLog.ta_log.info('启动UE')
        subprocess.Popen("D:\\Source\\UnrealEngine\\Engine\\Binaries\\Win64\\UE4Editor.exe")

    def openProject(self):
        self.project_browser = script.ProjectBrowserGUI.ProjectBrowserGUI()
        self.ta_log.info('打开了项目管理器')
        self.project_browser.show()

    def Updata(self, unpdata_=True):
        # new_version = float(self.doodleSet.version)
        url = "http://192.168.10.213:8000/dist/doodle.exe"
        tmp_path = pathlib.Path(tempfile.gettempdir()).joinpath('doodle.exe')
        if unpdata_:
            try:
                if tmp_path.is_file():
                    os.remove(tmp_path.as_posix())

                self.undata_progress = QtWidgets.QProgressDialog("下载文件", "...", 0, 100)
                self.undata_progress.show()
                urllib.request.urlretrieve(url=url, filename=tmp_path.as_posix(), reporthook=self.updataProgress)
                # http = urllib3.PoolManager()
                # resp = http.request("GET", url)
                # tmp_path.write_bytes(resp.data)
                # resp.release_conn()
            except:
                pass
            else:
                time.sleep(10)
                subprocess.Popen(str(tmp_path))
                sys.exit(self)

    def updataProgress(self, num, size, zhong):
        per = 100 * num * size / zhong
        if per > 99:
            per = 100
        print(per)
        self.undata_progress.setValue(per)


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
