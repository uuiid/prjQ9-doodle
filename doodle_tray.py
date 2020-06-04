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

import qdarkgraystyle
from PyQt5 import QtCore
from PyQt5 import QtWidgets, QtGui

import script.DoodleUpdata
import script.ProjectBrowserGUI
import script.doodleLog
import script.doodle_setting
import script.synXml
import script.DoodleUpdata


class SystemTrayIcon(QtWidgets.QSystemTrayIcon):
    timeSyn = 7200000
    version = 1.061

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
                                       user=self.doodleSet.projectname,
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
        setwin = script.doodle_setting.DoodlesettingGUI()
        self.ta_log.info('打开了设置')
        setwin.show()

    def UEsync(self):
        if self.doodleSet.department in ['Light', 'VFX', 'modle']:
            synPath = [{'Left': 'D:\\Source\\UnrealEngine', 'Right': 'W:\\data\\Source\\UnrealEngine'}]
            synUE = 'UE_syn'
            script.synXml.FreeFileSync(doc=self.doodleSet.doc,
                                       syn_file=synPath,
                                       program=self.doodleSet.FreeFileSync,
                                       file_name=synUE,
                                       user=self.doodleSet.projectname,
                                       ip_=self.doodleSet.ftpip,
                                       password=self.doodleSet.password,
                                       include=['\\Engine\\*']).run()

    @staticmethod
    def openUE():
        script.doodleLog.ta_log.info('启动UE')
        subprocess.Popen("D:\\Source\\UnrealEngine\\Engine\\Binaries\\Win64\\UE4Editor.exe")

    def openProject(self):
        project_browser = script.ProjectBrowserGUI.ProjectBrowserGUI()
        self.ta_log.info('打开了项目管理器')
        project_browser.show()

    def Updata(self, unpdata_=True):
        doodle = "http://192.168.10.213:8000/dist/doodle.exe"
        # djv = "http://192.168.10.213:8000/dist/DJV.zip"
        # ffmpeg = "http://192.168.10.213:8000/dist/ffmpeg.zip"
        # urls = [doodle, djv, ffmpeg]
        tmp_path = pathlib.Path(tempfile.gettempdir())
        if unpdata_:
            try:
                if tmp_path.joinpath(doodle.split("/")[-1]).as_posix():
                    os.remove(tmp_path.as_posix())
                undata_progress = QtWidgets.QProgressDialog("下载文件", "...", 0, 99, parent=None)
                undata_progress.setWindowModality(QtCore.Qt.WindowModal)
                undata_progress.setMinimumDuration(100)
                undata_progress.forceShow()
                my_q = queue.Queue()
                my_th = threading.Thread(
                    target=script.DoodleUpdata.undataDoodle,
                    args=(my_q, doodle, tmp_path.joinpath(doodle.split("/")[-1]).as_posix()))
                my_th.start()

                # dow = script.DoodleUpdata.downloadThread(doodle, tmp_path.joinpath(doodle.split("/")[-1]), 10240)
                # dow.dowload_proes_signal.connect(self._updata)
                # dow.start()
                while True:
                    try:
                        i = my_q.get(block=True, timeout=1)
                        if i > 99: break
                    except queue.Empty:
                        break
                    else:
                        undata_progress.setValue(i)
                undata_progress.close()
                # for i in range(100):
                #     self.undata_progress.setValue(i)
                #     time.sleep(0.1)
                # undata_progress.setWindowFlags(QtCore.Qt.Main)
                # undata_progress.setValue(dow.jindu)
            except BaseException as err:
                logging.error("%s", err)
            else:
                time.sleep(10)
                subprocess.Popen(str(tmp_path.joinpath(doodle.split("/")[-1])))
                sys.exit(self)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    QtWidgets.QApplication.setQuitOnLastWindowClosed(False)
    # w = QtWidgets.QWidget()
    app.setStyleSheet(qdarkgraystyle.load_stylesheet())

    tray_icon = SystemTrayIcon(QtGui.QIcon('datas/icon.png'), None)
    tray_icon.showMessage('文件管理', 'hello')
    tray_icon.show()

    sys.exit(app.exec_())
