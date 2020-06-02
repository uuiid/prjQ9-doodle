import threading
import pathlib
import script.synXml as Syn


class copyeasily(threading.Thread):
    soure: pathlib.Path
    trange: pathlib.Path

    def __init__(self, soure: pathlib.Path, trange: pathlib.Path, doodle_set: object):
        super().__init__()
        """来源移动是一个文件, 目标一定是一个目录"""
        self.soure = soure
        self.trange = trange
        self.syn = Syn.FreeFileSync(doc=doodle_set.doc,
                                    program=doodle_set.FreeFileSync,
                                    user=doodle_set.projectname,
                                    ip_=doodle_set.ftpip,
                                    password=doodle_set.password)
        self.syn.addExclude(["backup"])
        if soure.is_file():
            self.copy = getattr(self, f"copy{self.soure.suffix[1:].capitalize()}")

    def run(self) -> None:
        self.copy()

    def __getattr__(self, item):
        return self.copyFile

    def copyFile(self):
        self.syn.addSynFile([{"Left":self.soure.parent.as_posix(),"Right":self.trange.as_posix()}])
        self.syn.addInclude([self.soure.name])
        self.syn.setVersioningFolder(self.trange.joinpath("backup").as_posix())
        return self.syn.run

    def copyUproject(self):
        self.syn.addSynFile([{"Left": self.soure.parent.as_posix(), "Right": self.trange.as_posix()}])
        self.syn.addInclude([self.soure.name,"Content"])
        self.syn.setVersioningFolder(self.trange.joinpath("backup").as_posix())
        return self.syn.run

    def addSynFile(self, soure:pathlib.Path, right:pathlib.Path):
        self.syn.addSynFile([{"Left":soure.parent.as_posix(), "Right":right.parent.as_posix()}])
        self.syn.addInclude([soure.name])

