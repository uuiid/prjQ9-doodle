from PySide2.QtWidgets import *
import sys
from mainUI.mainWindow import Ui_MainWindow
'''
class mymain():
    def __init__(self):
'''
class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow,self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)




if __name__ == "__main__":
    app = QApplication(sys.argv)
    # MainWidow = QMainWindow()
    ui = MainWindow()
    ui.show()
    sys.exit(app.exec_())