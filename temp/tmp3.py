import sys

from PySide2 import QtCore
from PySide2 import QtGui
from PySide2 import QtWidgets

box = QtWidgets.QMessageBox()
dubu_Butten = QtWidgets.QPushButton()
dubu_Butten.setText("独步逍遥")
dubu = box.addButton(dubu_Butten, QtWidgets.QMessageBox.AcceptRole)

chan_butten = QtWidgets.QPushButton()
chan_butten.setText("长安幻街")
chan = box.addButton(chan_butten, QtWidgets.QMessageBox.AcceptRole)

if box.clickedButton() == dubu_Butten:
    root = "V:"
elif box.clickedButton() == chan_butten:
    root = "X:"
else:
    root = "W:"
print("W:")
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)


    sys.exit(app.exec_())