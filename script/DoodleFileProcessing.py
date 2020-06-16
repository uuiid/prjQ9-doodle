import threading
import pathlib
import shutil
import logging
import script.synXml as Syn


class copyeasily(threading.Thread):
    soure: pathlib.Path
    trange: pathlib.Path

    def __init__(self, soure: pathlib.Path, trange: pathlib.Path, doodle_set: object, method="upload"):
        super().__init__()
        """method = down upload syn
        来源一定是一个文件, 目标一定是一个文件"""
        self.soure = soure
        self.trange = trange
        self.setlocale = doodle_set
        self.method = method
        self.syn = Syn.FreeFileSync(doc=doodle_set.cache_path,
                                    file_name=soure.stem,
                                    program=doodle_set.FreeFileSync,
                                    user=doodle_set.ftpuser,
                                    ip_=doodle_set.ftpip,
                                    password=doodle_set.password)
        self.syn.addExclude(["backup"])
        self.copy = getattr(self, f"copy{self.soure.suffix[1:].capitalize()}")

    def run(self) -> None:
        self.__copyfile__()
        self.syn.setSynchronize(self.method)
        self.copy()
        self.syn.run()

    def __getattr__(self, item):
        return self.copyFile

    def copyFile(self):
        self.syn.addSynFile([{"Left": self.soure_cache.parent.as_posix(), "Right": self.trange.parent.as_posix()}])
        self.syn.addInclude([self.soure_cache.name])
        self.syn.setVersioningFolder(self.trange.parent.joinpath("backup").as_posix())
        return self.syn

    def copyUproject(self):
        self.syn.addSynFile([{"Left": self.soure.parent.as_posix(), "Right": self.trange.parent.as_posix()},
                             {"Left": self.soure_cache.parent.as_posix(), "Right": self.trange.parent.as_posix()}])
        self.syn.addInclude([self.soure.name, "Content\\*"])
        self.syn.setVersioningFolder(self.trange.parent.joinpath("backup").as_posix())
        return self.syn

    def addSynFile(self, soure: pathlib.Path, right: pathlib.Path):
        self.syn.addSynFile([{"Left": soure.parent.as_posix(), "Right": right.parent.as_posix()}])
        self.syn.addInclude([soure.name])

    def __copyfile__(self):
        assert isinstance(self.setlocale.cache_path, pathlib.Path)
        if self.method == "down":
            self.soure_cache = self.soure
        elif self.method == "upload":
            # 这个是服务器路径
            trange = self.setlocale.cache_path.joinpath(*self.trange.parts[1:])
            trange.parent.mkdir(parents=True, exist_ok=True)
            try:
                shutil.copy(self.soure.as_posix(), trange.as_posix())
            except shutil.SameFileError:
                logging.info("目标已经在临时目录中")
            self.soure_cache = trange
        else:
            self.soure_cache = self.soure
