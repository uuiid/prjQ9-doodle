import logging
import os
import pathlib
import shutil
import tempfile
import threading


class export(threading.Thread):
    @property
    def path(self) -> pathlib.Path:
        if not hasattr(self, '_path'):
            self._path = ''
        return self._path

    @path.setter
    def path(self, path):
        if not isinstance(path, pathlib.Path):
            path = pathlib.Path(path)
        self._path = path

    def __init__(self, path: pathlib.Path, version, cache_path: pathlib.Path):
        super().__init__()
        self._path = path
        self.version = version
        self.cache_path = cache_path

    def run(self) -> None:
        self.exportCam()

    def exportCam(self):
        mayapy_path = '"C:\\Program Files\\Autodesk\\Maya2018\\bin\\mayapy.exe"'
        # mayapy_path = "C:\\Program Files\\Autodesk\\Maya2018\\bin\\mayapy.exe"

        sourefile = pathlib.Path("tools/mayaExport.py")
        tmp_path = pathlib.Path(tempfile.gettempdir()).joinpath('export.py')

        shutil.copy2(sourefile, tmp_path)

        logging.info("open %s", mayapy_path)
        self.cache_path.mkdir(parents=True, exist_ok=True)
        command = str(mayapy_path) + ''' ''' + tmp_path.as_posix() + \
                  f""" --path {self.path.parent.as_posix()} --name {self.path.stem} """ \
                  f"""--version {self.version} --suffix {self.path.suffix} """ \
                  f"""--exportpath {self.cache_path.as_posix()}"""
        logging.info(command)
        os.system(command)

        # os.system(str(mayapy_path) + ''' ''' + tmp_path.as_posix())
