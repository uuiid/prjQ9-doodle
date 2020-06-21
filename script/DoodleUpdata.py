import logging
import subprocess

import ftputil
import pathlib
import os


class downloadThread(object):

    def __init__(self, doodle_set):
        self.ftpip = doodle_set.ftpip
        self.cache: pathlib.Path = doodle_set.cache_path

    def run(self) -> None:
        with ftputil.FTPHost(self.ftpip, "anonymous") as host:
            doodle_exe = self.cache.joinpath("Doodle.exe")
            if doodle_exe.is_file():
                os.remove(doodle_exe.as_posix())
            if host.path.isfile("/dist/doodle.exe"):
                host.download("/dist/doodle.exe", doodle_exe.as_posix())
                subprocess.Popen(str(doodle_exe))
                doodle_exe.suffix.split(".")