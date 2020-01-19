import pathlib
import os,sys
import platform
import doodleBrowser
from PyQt5 import QtGui,QtCore,QtWidgets

test = pathlib.Path(r"W:\03_Workflow\Shots")

DOODLEROOT = pathlib.Path(__file__).parent.expanduser()


class DoodleCore:
    def __init__(self):
        self.doodleIni = ""

        try:
            self.version = "v0.1"
            self.doodleRoot = DOODLEROOT

            if platform.system() == "Windows":
                self.userini = pathlib.Path.home().joinpath('Documents','doodle','doodle.json')
        except:
            print("no")

    @classmethod
    def getShots(self,shotsDir:pathlib.Path):
        tmpShots = shotsDir.iterdir()
        shots =[]
        for shot in tmpShots:
            if shot.is_dir():
                shots.append(shot.stem)
        return shots

    # @classmethod
    # def test(cls):
    #     print("ok test")


if __name__ == "__main__":
    #DoodleCore.test()
    testdood = DoodleCore()
    print(testdood.doodleRoot)
    print(test)
    print(DoodleCore.getShots(test))
    # app = QtWidgets.QApplication(sys.argv)
    # MainWidow = doodleBrowser.MainDoodle()
    # MainWidow.show()
    # app.exec_()