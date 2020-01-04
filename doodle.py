from PyQt5 import QtGui,QtCore,QtWidgets
import os
import sys
from mainUI.mainWindow import Ui_MainWindow


class MainDoodle(Ui_MainWindow,QtWidgets.QMainWindow):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.browseFolder)


    def browseFolder(self):
        self.treeWidget.clear()
        dirextory = QtWidgets.QFileDialog.getExistingDirectory(self,"pushButton")

        if dirextory:
            root = QtWidgets.QTreeWidgetItem(self.treeWidget)
            for fileName in os.listdir(dirextory):
                item = QtWidgets.QTreeWidgetItem(root)
                item.setText(0,fileName)
                root.addChild(item)



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWidow = MainDoodle()
    MainWidow.show()
    app.exec_()