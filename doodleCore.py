import pathlib
import os
import platform

class doodleCore:
    def __init__(self):
        self.doodleIni = ""

        try:
            self.version = "v0.1"
            self.doodleRoot = pathlib.Path(__file__)

            if platform.system() == "Windows":
                self.userini = ppathlib.Path.home().joinpath('Documents','doodle','doodle.json')
        except:
            print("no")



if __name__ == "__main__":
    print(doodleCore.doodleRoot)