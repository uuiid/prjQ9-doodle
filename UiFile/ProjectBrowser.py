# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\teXiao\doodle\UiFile\ProjectBrowser.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1309, 725)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.tab_2)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.scane = QtWidgets.QPushButton(self.tab_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scane.sizePolicy().hasHeightForWidth())
        self.scane.setSizePolicy(sizePolicy)
        self.scane.setMinimumSize(QtCore.QSize(0, 30))
        self.scane.setStyleSheet("")
        self.scane.setCheckable(True)
        self.scane.setChecked(False)
        self.scane.setAutoExclusive(True)
        self.scane.setObjectName("scane")
        self.horizontalLayout_5.addWidget(self.scane)
        self.character = QtWidgets.QPushButton(self.tab_2)
        self.character.setMinimumSize(QtCore.QSize(0, 30))
        self.character.setStyleSheet("")
        self.character.setCheckable(True)
        self.character.setChecked(True)
        self.character.setAutoExclusive(True)
        self.character.setObjectName("character")
        self.horizontalLayout_5.addWidget(self.character)
        self.props = QtWidgets.QPushButton(self.tab_2)
        self.props.setMinimumSize(QtCore.QSize(0, 30))
        self.props.setStyleSheet("")
        self.props.setCheckable(True)
        self.props.setChecked(False)
        self.props.setAutoExclusive(True)
        self.props.setObjectName("props")
        self.horizontalLayout_5.addWidget(self.props)
        self.effects = QtWidgets.QPushButton(self.tab_2)
        self.effects.setMinimumSize(QtCore.QSize(0, 30))
        self.effects.setStyleSheet("")
        self.effects.setCheckable(True)
        self.effects.setChecked(False)
        self.effects.setAutoExclusive(True)
        self.effects.setObjectName("effects")
        self.horizontalLayout_5.addWidget(self.effects)
        self.verticalLayout_6.addLayout(self.horizontalLayout_5)
        self.listAss = QtWidgets.QListWidget(self.tab_2)
        self.listAss.setObjectName("listAss")
        self.verticalLayout_6.addWidget(self.listAss)
        self.verticalLayout_6.setStretch(0, 1)
        self.verticalLayout_6.setStretch(1, 20)
        self.horizontalLayout_2.addLayout(self.verticalLayout_6)
        self.verticalLayout_8 = QtWidgets.QVBoxLayout()
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.label_2 = QtWidgets.QLabel(self.tab_2)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_8.addWidget(self.label_2)
        self.listAssType = QtWidgets.QListWidget(self.tab_2)
        self.listAssType.setObjectName("listAssType")
        self.verticalLayout_8.addWidget(self.listAssType)
        self.verticalLayout_8.setStretch(1, 1)
        self.horizontalLayout_2.addLayout(self.verticalLayout_8)
        self.verticalLayout_7 = QtWidgets.QVBoxLayout()
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.label_4 = QtWidgets.QLabel(self.tab_2)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_7.addWidget(self.label_4)
        self.listAssFile = QtWidgets.QTableWidget(self.tab_2)
        self.listAssFile.setObjectName("listAssFile")
        self.listAssFile.setColumnCount(5)
        self.listAssFile.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.listAssFile.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.listAssFile.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.listAssFile.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.listAssFile.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.listAssFile.setHorizontalHeaderItem(4, item)
        self.verticalLayout_7.addWidget(self.listAssFile)
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.verticalLayout_11 = QtWidgets.QVBoxLayout()
        self.verticalLayout_11.setObjectName("verticalLayout_11")
        self.ass_upload = QtWidgets.QPushButton(self.tab_2)
        self.ass_upload.setObjectName("ass_upload")
        self.verticalLayout_11.addWidget(self.ass_upload)
        self.ass_screenshot = QtWidgets.QPushButton(self.tab_2)
        self.ass_screenshot.setObjectName("ass_screenshot")
        self.verticalLayout_11.addWidget(self.ass_screenshot)
        self.label_3 = QtWidgets.QLabel(self.tab_2)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_11.addWidget(self.label_3)
        self.ass_player = QtWidgets.QPushButton(self.tab_2)
        self.ass_player.setObjectName("ass_player")
        self.verticalLayout_11.addWidget(self.ass_player)
        self.verticalLayout_11.setStretch(2, 1)
        self.horizontalLayout_8.addLayout(self.verticalLayout_11)
        self.ass_thumbnail = QtWidgets.QLabel(self.tab_2)
        self.ass_thumbnail.setObjectName("ass_thumbnail")
        self.horizontalLayout_8.addWidget(self.ass_thumbnail)
        self.horizontalLayout_8.setStretch(1, 1)
        self.verticalLayout_7.addLayout(self.horizontalLayout_8)
        self.verticalLayout_7.setStretch(1, 1)
        self.verticalLayout_7.setStretch(2, 1)
        self.horizontalLayout_2.addLayout(self.verticalLayout_7)
        self.horizontalLayout_2.setStretch(0, 2)
        self.horizontalLayout_2.setStretch(1, 1)
        self.horizontalLayout_2.setStretch(2, 3)
        self.gridLayout_2.addLayout(self.horizontalLayout_2, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab_2, "")
        self.Episodes_shot = QtWidgets.QWidget()
        self.Episodes_shot.setEnabled(True)
        self.Episodes_shot.setObjectName("Episodes_shot")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout(self.Episodes_shot)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.episodes = QtWidgets.QLabel(self.Episodes_shot)
        self.episodes.setObjectName("episodes")
        self.verticalLayout_2.addWidget(self.episodes)
        self.listepisodes = QtWidgets.QListWidget(self.Episodes_shot)
        self.listepisodes.setObjectName("listepisodes")
        self.verticalLayout_2.addWidget(self.listepisodes)
        self.horizontalLayout_6.addLayout(self.verticalLayout_2)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.shot_shot = QtWidgets.QLabel(self.Episodes_shot)
        self.shot_shot.setObjectName("shot_shot")
        self.verticalLayout_3.addWidget(self.shot_shot)
        self.listshot = QtWidgets.QListWidget(self.Episodes_shot)
        self.listshot.setObjectName("listshot")
        self.verticalLayout_3.addWidget(self.listshot)
        self.horizontalLayout_6.addLayout(self.verticalLayout_3)
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.department = QtWidgets.QLabel(self.Episodes_shot)
        self.department.setObjectName("department")
        self.verticalLayout_4.addWidget(self.department)
        self.listdepartment = QtWidgets.QListWidget(self.Episodes_shot)
        self.listdepartment.setObjectName("listdepartment")
        self.verticalLayout_4.addWidget(self.listdepartment)
        self.horizontalLayout.addLayout(self.verticalLayout_4)
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.depType = QtWidgets.QLabel(self.Episodes_shot)
        self.depType.setObjectName("depType")
        self.verticalLayout_5.addWidget(self.depType)
        self.listdepType = QtWidgets.QListWidget(self.Episodes_shot)
        self.listdepType.setObjectName("listdepType")
        self.verticalLayout_5.addWidget(self.listdepType)
        self.horizontalLayout.addLayout(self.verticalLayout_5)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.file = QtWidgets.QLabel(self.Episodes_shot)
        self.file.setObjectName("file")
        self.verticalLayout.addWidget(self.file)
        self.listfile = QtWidgets.QTableWidget(self.Episodes_shot)
        self.listfile.setMaximumSize(QtCore.QSize(120000, 1200))
        self.listfile.setObjectName("listfile")
        self.listfile.setColumnCount(5)
        self.listfile.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.listfile.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.listfile.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.listfile.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.listfile.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.listfile.setHorizontalHeaderItem(4, item)
        self.verticalLayout.addWidget(self.listfile)
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.start_frame = QtWidgets.QSpinBox(self.Episodes_shot)
        self.start_frame.setMinimum(1001)
        self.start_frame.setMaximum(2000)
        self.start_frame.setObjectName("start_frame")
        self.horizontalLayout_10.addWidget(self.start_frame)
        self.end_frame = QtWidgets.QSpinBox(self.Episodes_shot)
        self.end_frame.setMinimum(1000)
        self.end_frame.setMaximum(2000)
        self.end_frame.setProperty("value", 1250)
        self.end_frame.setObjectName("end_frame")
        self.horizontalLayout_10.addWidget(self.end_frame)
        self.fps = QtWidgets.QSpinBox(self.Episodes_shot)
        self.fps.setProperty("value", 25)
        self.fps.setObjectName("fps")
        self.horizontalLayout_10.addWidget(self.fps)
        self.verticalLayout.addLayout(self.horizontalLayout_10)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.horizontalLayout.setStretch(0, 1)
        self.horizontalLayout.setStretch(1, 1)
        self.horizontalLayout.setStretch(2, 5)
        self.verticalLayout_10.addLayout(self.horizontalLayout)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.verticalLayout_9 = QtWidgets.QVBoxLayout()
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.shot_upload = QtWidgets.QPushButton(self.Episodes_shot)
        self.shot_upload.setStyleSheet("")
        self.shot_upload.setCheckable(False)
        self.shot_upload.setAutoRepeat(True)
        self.shot_upload.setAutoExclusive(False)
        self.shot_upload.setObjectName("shot_upload")
        self.verticalLayout_9.addWidget(self.shot_upload)
        self.shot_screenshots = QtWidgets.QPushButton(self.Episodes_shot)
        self.shot_screenshots.setStyleSheet("")
        self.shot_screenshots.setCheckable(False)
        self.shot_screenshots.setAutoRepeat(True)
        self.shot_screenshots.setAutoExclusive(False)
        self.shot_screenshots.setObjectName("shot_screenshots")
        self.verticalLayout_9.addWidget(self.shot_screenshots)
        self.label_6 = QtWidgets.QLabel(self.Episodes_shot)
        self.label_6.setObjectName("label_6")
        self.verticalLayout_9.addWidget(self.label_6)
        self.shot_player = QtWidgets.QPushButton(self.Episodes_shot)
        self.shot_player.setObjectName("shot_player")
        self.verticalLayout_9.addWidget(self.shot_player)
        self.horizontalLayout_4.addLayout(self.verticalLayout_9)
        self.shot_thumbnail = QtWidgets.QLabel(self.Episodes_shot)
        self.shot_thumbnail.setObjectName("shot_thumbnail")
        self.horizontalLayout_4.addWidget(self.shot_thumbnail)
        self.horizontalLayout_4.setStretch(0, 1)
        self.horizontalLayout_4.setStretch(1, 13)
        self.verticalLayout_10.addLayout(self.horizontalLayout_4)
        self.verticalLayout_10.setStretch(0, 1)
        self.verticalLayout_10.setStretch(1, 1)
        self.horizontalLayout_6.addLayout(self.verticalLayout_10)
        self.horizontalLayout_6.setStretch(0, 1)
        self.horizontalLayout_6.setStretch(1, 1)
        self.horizontalLayout_6.setStretch(2, 6)
        self.horizontalLayout_7.addLayout(self.horizontalLayout_6)
        self.tabWidget.addTab(self.Episodes_shot, "")
        self.horizontalLayout_3.addWidget(self.tabWidget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1309, 23))
        self.menubar.setObjectName("menubar")
        self.caoZhuo = QtWidgets.QMenu(self.menubar)
        self.caoZhuo.setObjectName("caoZhuo")
        MainWindow.setMenuBar(self.menubar)
        self.refresh = QtWidgets.QAction(MainWindow)
        self.refresh.setObjectName("refresh")
        self.close_socket = QtWidgets.QAction(MainWindow)
        self.close_socket.setObjectName("close_socket")
        self.actioncom_video = QtWidgets.QAction(MainWindow)
        self.actioncom_video.setObjectName("actioncom_video")
        self.caoZhuo.addAction(self.refresh)
        self.caoZhuo.addAction(self.close_socket)
        self.caoZhuo.addAction(self.actioncom_video)
        self.menubar.addAction(self.caoZhuo.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.listepisodes, self.listshot)
        MainWindow.setTabOrder(self.listshot, self.listdepartment)
        MainWindow.setTabOrder(self.listdepartment, self.listdepType)
        MainWindow.setTabOrder(self.listdepType, self.listfile)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.scane.setText(_translate("MainWindow", "场景"))
        self.character.setText(_translate("MainWindow", "人物"))
        self.props.setText(_translate("MainWindow", "道具"))
        self.effects.setText(_translate("MainWindow", "特效"))
        self.label_2.setText(_translate("MainWindow", "类别"))
        self.label_4.setText(_translate("MainWindow", "文件"))
        item = self.listAssFile.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "版本"))
        item = self.listAssFile.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "概述"))
        item = self.listAssFile.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "制作人"))
        item = self.listAssFile.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "后缀"))
        item = self.listAssFile.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "ID"))
        self.ass_upload.setText(_translate("MainWindow", "转盘"))
        self.ass_screenshot.setText(_translate("MainWindow", "截图"))
        self.label_3.setText(_translate("MainWindow", "预览"))
        self.ass_player.setText(_translate("MainWindow", "播放"))
        self.ass_thumbnail.setText(_translate("MainWindow", "TextLabel"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "资产"))
        self.episodes.setText(_translate("MainWindow", "集数"))
        self.shot_shot.setText(_translate("MainWindow", "镜头"))
        self.department.setText(_translate("MainWindow", "部门"))
        self.depType.setText(_translate("MainWindow", "类型"))
        self.file.setText(_translate("MainWindow", "文件"))
        item = self.listfile.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "版本"))
        item = self.listfile.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "概述"))
        item = self.listfile.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "制作人"))
        item = self.listfile.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "格式"))
        item = self.listfile.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "ID"))
        self.shot_upload.setText(_translate("MainWindow", "上传拍屏"))
        self.shot_screenshots.setToolTip(_translate("MainWindow", "<html><head/><body><p>这个按钮按下时可以截屏</p></body></html>"))
        self.shot_screenshots.setText(_translate("MainWindow", "截屏"))
        self.label_6.setText(_translate("MainWindow", "拍屏"))
        self.shot_player.setText(_translate("MainWindow", "播放"))
        self.shot_thumbnail.setText(_translate("MainWindow", "TextLabel"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Episodes_shot), _translate("MainWindow", "镜头"))
        self.caoZhuo.setTitle(_translate("MainWindow", "操作"))
        self.refresh.setText(_translate("MainWindow", "刷新"))
        self.close_socket.setText(_translate("MainWindow", "关闭ue4链接"))
        self.actioncom_video.setText(_translate("MainWindow", "合成整集拍屏"))
