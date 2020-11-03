# -*- coding: UTF-8 -*-
import logging
import os
import pathlib
import shutil
import subprocess
import sys
import time
import winreg

import qdarkstyle
from PySide2 import QtCore
from PySide2 import QtWidgets, QtGui

import script.DoodleSynXml
import script.DoodleUpdata
import script.DoodleCoreApp


class SystemTrayIcon(QtWidgets.QSystemTrayIcon, script.DoodleCoreApp.core):
    timeSyn = 900000
    version = 0.411

    def __init__(self, icon, parent=None):
        self.tray = QtWidgets.QSystemTrayIcon.__init__(self, icon, parent)
        self.ta_log = logging
        self.par = parent

        self.timer = QtCore.QTimer(self)
        self.timer.setSingleShot(True)
        # self.timer.timeout.connect(self.file_syns)
        # self.timer.timeout.connect(lambda: self.Updata(lambda: float(self.doodle_set.version) > self.version))
        # self.timer.start(self.timeSyn)
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

        UE_open = UEmenu.addAction('更新ue配置文件')
        UE_open.triggered.connect(self.openUE)

        UE_sync = UEmenu.addAction('清除ue4缓存')
        UE_sync.triggered.connect(self.UEsync)
        # </editor-fold>

        install_plug: QtWidgets.QMenu = menu.addMenu("安装插件")
        install_maya: QtWidgets.QAction = install_plug.addAction("安装maya插件")
        install_maya.triggered.connect(self.installMaya)

        install_ue_425: QtWidgets.QAction = install_plug.addAction("安装ue插件到项目(4.25)")
        install_ue_425.triggered.connect(lambda :self.installUE(425))

        install_ue_426:QtWidgets.QAction = install_plug.addAction("安装ue插件到项目(4.26)")
        install_ue_426.triggered.connect(lambda: self.installUE(426))

        install_ue_app: QtWidgets.QAction = install_plug.addAction("安装ue插件(永久 4.25)")
        install_ue_app.triggered.connect(self.installUEAppPlug)

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
        if pathlib.Path(os.getenv("LOCALAPPDATA")).joinpath("UnrealEngine").exists():
            os.system(r"rmdir /s /q %LOCALAPPDATA%\UnrealEngine")
        # if self.doodle_set.department in ['Light', 'VFX', 'modle']:
        #     synPath = [{'Left': 'D:\\Source\\UnrealEngine', 'Right': 'W:\\data\\Source\\UnrealEngine'}]
        #     synUE = 'UE_syn'
        #     script.DoodleSynXml.FreeFileSync(doc=self.doodle_set.doc,
        #                                      syn_file=synPath,
        #                                      program=self.doodle_set.FreeFileSync,
        #                                      file_name=synUE,
        #                                      user=self.doodle_set.ftpuser,
        #                                      ip_=self.doodle_set.ftpip,
        #                                      password=self.doodle_set.password,
        #                                      include=['\\Engine\\*']).run()

    @staticmethod
    def openUE():
        for i in ["5","6"]:
            try:
                key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,r"SOFTWARE\EpicGames\Unreal Engine\4.2{}".format(i))
            except FileNotFoundError:
                QtWidgets.QMessageBox.warning(None, "警告:", "没有安装 4.2{} 版本 不替换缓存目录".format(i),
                                              QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
            else:
                path = pathlib.Path(winreg.QueryValueEx(key,"InstalledDirectory")[0]).joinpath("Engine","Config")
                file_cong = pathlib.Path("tools/BaseEngine.ini").absolute()
                if path.joinpath("BaseEngine.ini").exists():
                    os.remove(path.joinpath("BaseEngine.ini"))
                shutil.copyfile(file_cong,path.joinpath("BaseEngine.ini"))



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

    def installUE(self,version:int):
        file, file_type = QtWidgets.QFileDialog.getOpenFileName(None,
                                                                "选择ue项目",
                                                                "",
                                                                "files (*.uproject)")
        if file:
            path = pathlib.Path(file)
            if version == 425:
                plug_path_str = "tools/uePlug/4.25/Plugins"
            elif version == 426:
                plug_path_str = "tools/uePlug/4.26/Plugins"
            else:
                plug_path_str = "tools/uePlug/4.25/Plugins"

            if path.parent.joinpath("Plugins", "Doodle").exists():
                os.remove(path.parent.joinpath("Plugins","Doodle"))
            QtWidgets.QMessageBox.warning(None, "警告:", f"复制文件需要一些时间,完成后请重启ue4",
                                          QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
            shutil.copytree(plug_path_str,path.parent.joinpath("Plugins"))
            QtWidgets.QMessageBox.warning(None, "警告:", "复制完成",
                                          QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)

    def installUEAppPlug(self):
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,r"SOFTWARE\EpicGames\Unreal Engine\4.25")
        path = pathlib.Path(winreg.QueryValueEx(key,"InstalledDirectory")[0])
        if path:
            QtWidgets.QMessageBox.warning(None, "警告:", f"复制文件需要一些时间,完成后请重启ue4,"
                                                       f"还有如果 杀软 有拦截极有可能不成功,"
                                                       f"在C盘的话,权限不够也不行",
                                          QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
            if path.joinpath("Engine", "Plugins", "Runtime", "Doodle").exists():
                os.remove(path.joinpath("Engine","Plugins","Runtime","Doodle"))
            shutil.copytree("tools/uePlug/4.25/Plugins/Doodle",
                            path.joinpath("Engine","Plugins","Runtime","Doodle"))
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
