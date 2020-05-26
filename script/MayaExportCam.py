import logging
import os
import pathlib
import sys
import tempfile
import threading
import subprocess
import shutil

"""import maya.standalone

maya.standalone.initialize(name='python')
import maya.cmds
import maya.mel
import pymel.core
import subprocess
"C:\\Program Files\\Autodesk\\Maya2018\\bin\\mayapy.exe" "C:\\Users\\teXiao\\AppData\\Local\\Temp\\export.py"
maya.cmds.file(new=True, force=True)
maya.cmds.file('C:/Users/teXiao/Documents/test.mb', o=True)
# pymel.core.file('C:/Users/teXiao/Documents/test.mb',o=True)
maya.cmds.select('persp1')
maya.mel.eval('''FBXExport -f "D:/testaa.fbx" -s''')

for export in cmds.ls("::*UE4"):
    maya.cmds.select(export)
    name = export.sp
    print(export)
    maya.mel.eval('''FBXExport -f "D:/testaa.fbx" -s''')"""


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

    def __init__(self, path: pathlib.Path):
        super().__init__()
        if not isinstance(path, pathlib.Path):
            path = pathlib.Path(path)
        self._path = path

    def run(self) -> None:
        self.exportCam()

    def exportCam(self):
        mayapy_path = '"C:\\Program Files\\Autodesk\\Maya2018\\bin\\mayapy.exe"'
        # mayapy_path = "C:\\Program Files\\Autodesk\\Maya2018\\bin\\mayapy.exe"

        sourefile = pathlib.Path("tools/mayaExport.py")
        tmp_path = pathlib.Path(tempfile.gettempdir()).joinpath('export.py')

        shutil.copy2(sourefile, tmp_path)
        # tmp_path.suffix
        logging.info("open %s", mayapy_path)
        logging.info(str(mayapy_path) + ' ' + tmp_path.as_posix() +
f""" --path {self.path.parent.as_posix()} --name {self.path.stem} --version {0} --suffix {self.path.suffix} """)
        os.system(str(mayapy_path) + ''' ''' + tmp_path.as_posix() +
f""" --path {self.path.parent.as_posix()} --name {self.path.stem} --version {0} --suffix {self.path.suffix} """)
        # os.system(str(mayapy_path) + ''' ''' + tmp_path.as_posix())
