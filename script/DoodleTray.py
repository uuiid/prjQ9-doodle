# -*- coding: UTF-8 -*-
import logging
import pathlib
import shutil
import subprocess
import sys
import time

import qdarkstyle
from PySide2 import QtCore
from PySide2 import QtWidgets, QtGui

import script.DoodleSynXml
import script.DoodleUpdata
import script.DoodleCoreApp


class SystemTrayIcon(QtWidgets.QSystemTrayIcon, script.DoodleCoreApp.core):
    timeSyn = 900000
    version = 0.410

    def __init__(self, icon, parent=None):
        self.tray = QtWidgets.QSystemTrayIcon.__init__(self, icon, parent)
        self.ta_log = logging
        self.par = parent

        self.timer = QtCore.QTimer(self)
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.file_syns)
        # self.timer.timeout.connect(lambda: self.Updata(lambda: float(self.doodle_set.version) > self.version))
        self.timer.start(self.timeSyn)
        # 添加本地线程服务器
        # self.localServer = script.DoodleLocalConnection.DoodleServer(self.doodle_set)
        # self.localServer.setDaemon(True)
        # self.localServer.start()

        self.setToolTip(f'文件管理系统-{self.version}')
        menu = QtWidgets.QMenu(parent)

        file_sync = menu.addAction('同步文件')
        file_sync.triggered.connect(self.file_syns)

        project = menu.addAction('项目管理器')
        project.triggered.connect(self.doodle_app.openProjectBrowserGUI)

        # <editor-fold desc="动作">
        UEmenu = menu.addMenu('UE动作')

        UE_open = UEmenu.addAction('打开UE')
        UE_open.triggered.connect(self.openUE)

        UE_sync = UEmenu.addAction('同步UE')
        UE_sync.triggered.connect(self.UEsync)
        # </editor-fold>

        install_plug: QtWidgets.QMenu = menu.addMenu("安装插件")
        install_maya: QtWidgets.QAction = install_plug.addAction("安装maya插件")
        install_maya.triggered.connect(self.installMaya)

        install_ue: QtWidgets.QAction = install_plug.addAction("安装ue插件")
        install_ue.triggered.connect(self.installUE)

        setmenu = menu.addAction('设置')
        setmenu.triggered.connect(self.doodle_app.showSet)

        updata = menu.addAction('更新')
        updata.triggered.connect(lambda: self.Updata(True))

        register = menu.addAction("注册")
        register.triggered.connect(self.doodle_app.showRigister)

        exit_ = menu.addAction('退出')
        exit_.triggered.connect(self.doodle_app.DoodleQuery)

        menu.addSeparator()
        self.setContextMenu(menu)

    def file_syns(self):
        if self.doodle_set.department in ['Light', 'VFX']:
            server_syn= self.doodle_set.getsever()
            if self.doodle_set.department in ["VFX"]:
                include_ = ["*\\VFX\\*"]
                file_sync = script.DoodleSynXml.FreeFileSync(doc=self.doodle_set.doc, syn_file=server_syn,
                                                             program=self.doodle_set.FreeFileSync,
                                                             file_name='{}-ep-{}'.format(self.doodle_set.department,
                                                                                         self.doodle_set.synEp),
                                                             user=self.doodle_set.ftpuser, ip_=self.doodle_set.ftpip,
                                                             password=self.doodle_set.password, include=include_)
                file_sync.setVersioningFolder("/03_Workflow/Assets/{}/backup".format(self.doodle_set.department))
                file_sync.run()
            if self.doodle_set.department in ["Light"]:
                file_sync = script.DoodleSynXml.FreeFileSync(doc=self.doodle_set.doc,
                                                             program=self.doodle_set.FreeFileSync,
                                                             file_name='{}-ep-{}'.format(self.doodle_set.department,
                                                                                         self.doodle_set.synEp),
                                                             user=self.doodle_set.ftpuser, ip_=self.doodle_set.ftpip,
                                                             password=self.doodle_set.password,)
                backup__format = "/03_Workflow/Assets/{}/backup".format(self.doodle_set.department)
                file_sync.setVersioningFolder(backup__format)
                file_sync.addInclude(["*"])
                file_sync.addSynFile([{"Left":i["Left"],"Right":i["Right"].replace("Light","VFX")} for i in server_syn[:]])
                for i in range(server_syn.__len__()):
                    file_sync.addSubIncludeExclude(i,["*\\VFX\\*"])
                    file_sync.addSubSynchronize(i,"down",backup__format)

                file_sync.addSynFile(server_syn)
                for i in range(server_syn.__len__(),server_syn.__len__()*2):
                    file_sync.addSubIncludeExclude(i)
                    file_sync.addSubSynchronize(i,"syn",backup__format)
                file_sync.run()

            self.ta_log.info('同步时间: %s', time.asctime(time.localtime(time.time())))

    def UEsync(self):
        if self.doodle_set.department in ['Light', 'VFX', 'modle']:
            synPath = [{'Left': 'D:\\Source\\UnrealEngine', 'Right': 'W:\\data\\Source\\UnrealEngine'}]
            synUE = 'UE_syn'
            script.DoodleSynXml.FreeFileSync(doc=self.doodle_set.doc,
                                             syn_file=synPath,
                                             program=self.doodle_set.FreeFileSync,
                                             file_name=synUE,
                                             user=self.doodle_set.ftpuser,
                                             ip_=self.doodle_set.ftpip,
                                             password=self.doodle_set.password,
                                             include=['\\Engine\\*']).run()

    @staticmethod
    def openUE():
        logging.info('启动UE')
        subprocess.Popen("D:\\Source\\UnrealEngine\\Engine\\Binaries\\Win64\\UE4Editor.exe")

    def Updata(self, unpdata_=True):
        script.DoodleUpdata.downloadThread(self.doodle_set).run()
        sys.exit(self)

    def installMaya(self):
        mode = "+ doodle_main.py 1.1 {_path_}\n" \
               "MYMODULE_LOCATION:= {_path_}\n" \
               "PATH+:= {_path_}/scripts;{_path_}/plug-ins\n" \
               "PYTHONPATH+:= {_path_}/scripts".format(_path_="C:/Program Files/doodle/tools/maya_plug")
        maya_plug_path = self.doodle_set.doc.parent.joinpath("maya", "modules")
        if not maya_plug_path.is_dir():
            maya_plug_path.mkdir(parents=True, exist_ok=True)
        maya_plug_path.joinpath("Doodle.mod").write_text(mode)

    def installUE(self):
        file, file_type = QtWidgets.QFileDialog.getOpenFileName(None,
                                                                "选择ue项目",
                                                                "",
                                                                "files (*.uproject)")
        if file:
            path = pathlib.Path(file)
            QtWidgets.QMessageBox.warning(None, "警告:", f"复制文件需要一些时间,完成后请重启ue4",
                                          QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
            shutil.copytree("tools/uePlug/Plugins",path.parent.joinpath("Plugins"))
            QtWidgets.QMessageBox.warning(None, "警告:", "复制完成",
                                          QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    QtWidgets.QApplication.setQuitOnLastWindowClosed(False)
    # w = QtWidgets.QWidget()
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyside2())

    tray_icon = SystemTrayIcon(QtGui.QIcon("datas/icon.png"), None)
    tray_icon.showMessage('文件管理', 'hello')
    tray_icon.show()

    sys.exit(app.exec_())
