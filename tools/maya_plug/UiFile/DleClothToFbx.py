# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\teXiao\doodle\tools\maya_plug\UiFile\DleClothToFbx.ui',
# licensing of 'C:\Users\teXiao\doodle\tools\maya_plug\UiFile\DleClothToFbx.ui' applies.
#
# Created: Sun Jun 21 12:53:32 2020
#      by: pyside2-uic  running on PySide2 5.12.3
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(403, 720)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.getSelectObj = QtWidgets.QPushButton(self.centralwidget)
        self.getSelectObj.setObjectName("getSelectObj")
        self.verticalLayout.addWidget(self.getSelectObj)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_3.addWidget(self.label_2)
        self.selectClothList = QtWidgets.QListWidget(self.centralwidget)
        self.selectClothList.setObjectName("selectClothList")
        self.verticalLayout_3.addWidget(self.selectClothList)
        self.verticalLayout_3.setStretch(1, 1)
        self.horizontalLayout.addLayout(self.verticalLayout_3)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.dynamicCloth = QtWidgets.QCheckBox(self.centralwidget)
        self.dynamicCloth.setObjectName("dynamicCloth")
        self.verticalLayout_2.addWidget(self.dynamicCloth)
        self.selectdynamicClothList = QtWidgets.QListWidget(self.centralwidget)
        self.selectdynamicClothList.setEnabled(True)
        self.selectdynamicClothList.setObjectName("selectdynamicClothList")
        self.verticalLayout_2.addWidget(self.selectdynamicClothList)
        self.getSelectDynamicCloth = QtWidgets.QPushButton(self.centralwidget)
        self.getSelectDynamicCloth.setObjectName("getSelectDynamicCloth")
        self.verticalLayout_2.addWidget(self.getSelectDynamicCloth)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setMaximumSize(QtCore.QSize(120000, 67))
        self.textBrowser.setObjectName("textBrowser")
        self.verticalLayout.addWidget(self.textBrowser)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_2.addWidget(self.label_3)
        self.shot = QtWidgets.QSpinBox(self.centralwidget)
        self.shot.setObjectName("shot")
        self.horizontalLayout_2.addWidget(self.shot)
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_2.addWidget(self.label_4)
        self.episodes = QtWidgets.QSpinBox(self.centralwidget)
        self.episodes.setObjectName("episodes")
        self.horizontalLayout_2.addWidget(self.episodes)
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_2.addWidget(self.label_5)
        self.shotAb = QtWidgets.QComboBox(self.centralwidget)
        self.shotAb.setObjectName("shotAb")
        self.shotAb.addItem("")
        self.shotAb.setItemText(0, "")
        self.shotAb.addItem("")
        self.shotAb.addItem("")
        self.shotAb.addItem("")
        self.horizontalLayout_2.addWidget(self.shotAb)
        self.horizontalLayout_2.setStretch(0, 1)
        self.horizontalLayout_2.setStretch(1, 1)
        self.horizontalLayout_2.setStretch(2, 1)
        self.horizontalLayout_2.setStretch(3, 1)
        self.horizontalLayout_2.setStretch(4, 1)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.testing = QtWidgets.QPushButton(self.centralwidget)
        self.testing.setObjectName("testing")
        self.verticalLayout.addWidget(self.testing)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)
        self.ExportClothAndFbx = QtWidgets.QPushButton(self.centralwidget)
        self.ExportClothAndFbx.setObjectName("ExportClothAndFbx")
        self.gridLayout.addWidget(self.ExportClothAndFbx, 1, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 403, 23))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtWidgets.QApplication.translate("MainWindow", "MainWindow", None, -1))
        self.getSelectObj.setText(QtWidgets.QApplication.translate("MainWindow", "获得选择物体", None, -1))
        self.label_2.setText(QtWidgets.QApplication.translate("MainWindow", "布料", None, -1))
        self.dynamicCloth.setText(QtWidgets.QApplication.translate("MainWindow", "动态布料", None, -1))
        self.getSelectDynamicCloth.setText(QtWidgets.QApplication.translate("MainWindow", "添加动态布料", None, -1))
        self.textBrowser.setHtml(QtWidgets.QApplication.translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'SimSun\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">选择布料, 如果是fbx和abc文件则需要将abc指示为动态布料</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">添加动态布料时请注意选择顺序</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600; color:#ff1150;\">两个列表中的物体必须一一对应</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">将自动根据文件名称获得集数和文件镜头名称,如果没有获得请设置</p></body></html>", None, -1))
        self.label_3.setText(QtWidgets.QApplication.translate("MainWindow", "集数", None, -1))
        self.label_4.setText(QtWidgets.QApplication.translate("MainWindow", "镜头", None, -1))
        self.label_5.setText(QtWidgets.QApplication.translate("MainWindow", "ab镜", None, -1))
        self.shotAb.setItemText(1, QtWidgets.QApplication.translate("MainWindow", "B", None, -1))
        self.shotAb.setItemText(2, QtWidgets.QApplication.translate("MainWindow", "C", None, -1))
        self.shotAb.setItemText(3, QtWidgets.QApplication.translate("MainWindow", "D", None, -1))
        self.testing.setText(QtWidgets.QApplication.translate("MainWindow", "检测", None, -1))
        self.ExportClothAndFbx.setText(QtWidgets.QApplication.translate("MainWindow", "导出", None, -1))

