# -*- coding: UTF-8 -*-
import codecs
import os
import sys
import time
import script.debug
from pathlib import Path
from subprocess import run
import script.doodle_setting
from PyQt5 import QtCore
from PyQt5 import QtWidgets, QtGui


class SystemTrayIcon(QtWidgets.QSystemTrayIcon):
    # patterns = "*"
    # ignore_patterns = ""
    # ignore_directories = False
    # case_sensitive = True
    # path = ""
    # go_recursively = True
    # my_event_handler = ''
    setting = {}

    def __init__(self, icon, parent=None):
        QtWidgets.QSystemTrayIcon.__init__(self, icon, parent)
        doodle_setting = script.doodle_setting.Doodlesetting()
        self.setting = doodle_setting.getString()
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
        self.timer.start(3600000)

        self.setToolTip('文件管理系统-0.1.1')
        menu = QtWidgets.QMenu(parent)

        file_sync = menu.addAction('同步文件')
        file_sync.triggered.connect(self.file_syns)

        exit_ = menu.addAction('退出')
        exit_.triggered.connect(lambda: sys.exit())

        menu.addSeparator()
        self.setContextMenu(menu)

    # def debug(self, mystr):
    #     log = Path("{}{}".format(Path.home(), '\\Documents\\doodle\\log.txt'))
    #     try:
    #         Path("{}{}".format(Path.home(), '\\Documents\\doodle')).mkdir()
    #     except:
    #         pass
    #     Path.touch(log)
    #     with codecs.open(log, mode='a', encoding="utf-8") as f:
    #         f.write(mystr)
    #     if log.stat().st_size > 1048576:
    #         log.unlink()

    def file_syns(self):
        program = os.path.abspath('C:\\PROGRA~1\\FREEFI~1\\FreeFileSync.exe')
        # os.system('{} W:\\data\\ue_prj\\template.ffs_batch'.format(program))
        run('{} W:\\data\\ue_prj\\template.ffs_batch'.format(program), shell=True)
        script.debug.debug("同步时间: {}\n".format(time.time()))


def main():
    app = QtWidgets.QApplication(sys.argv)
    w = QtWidgets.QWidget()
    tray_icon = SystemTrayIcon(QtGui.QIcon('datas/icon.png'), w)
    tray_icon.show()
    tray_icon.showMessage('文件管理', 'hello')

    sys.exit(app.exec_())


main()
