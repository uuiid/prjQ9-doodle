from PyQt5 import QtGui,QtCore,QtWidgets
import os
import sys
import pathlib
import doodleCore
from mainUI.mainWindow import Ui_MainWindow

test = pathlib.Path(r"W:\03_Workflow\Shots")

class MainDoodle(Ui_MainWindow,QtWidgets.QMainWindow):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.browseFolder)


    def browseFolder(self,shots:str):
        #self.treeWidget.clear()
        #dirextory = QtWidgets.QFileDialog.getExistingDirectory(self,"pushButton")
        shots = doodleCore.DoodleCore.getShots(test)
        if shots:
            root = QtWidgets.QTreeWidgetItem(self.treeWidget)
            for fileName in shots:
                #if fileName.split("-")[-1]:

                item = QtWidgets.QTreeWidgetItem(root)
                item.setText(0,fileName)
                root.addChild(item)



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWidow = MainDoodle()
    MainWidow.show()
    app.exec_()