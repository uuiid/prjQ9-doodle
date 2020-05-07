import logging
import os
import pathlib
import sys
import tempfile
import subprocess

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


class export(object):
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
        if not isinstance(path, pathlib.Path):
            path = pathlib.Path(path)
        self._path = path

    def exportCam(self):
        # mayapy_path = '"C:\\Program Files\\Autodesk\\Maya2018\\bin\\mayapy.exe"'
        mayapy_path = "C:\\Program Files\\Autodesk\\Maya2018\\bin\\mayapy.exe"
        out = """
import sys
import os

import maya.standalone
maya.standalone.initialize( name='python' )
import maya.cmds
import maya.mel
import pymel.core
import tempfile
import os
import re

maya.cmds.file(new=True, force=True)
maya.cmds.file('{paths}',o=True)

start = maya.cmds.playbackOptions(query=True, min=True)
end = maya.cmds.playbackOptions(query=True, max=True)

myfile = os.path.join(tempfile.gettempdir(),"doodle_maya_export_log.txt")
exports = cmds.ls("::*UE4")

log = ''
log = log + "dao  chu  wu  ti \\n" + "\\n".join(exports) + "\\n\\n"

for export in exports:
    maya.cmds.select(export)
    mystr = '_'
    log = log + 'ming Lin'+ 'FBXExport -f "{path}/{name}_{{suex=export.split(mystr)[0]}}.fbx" -s' + '\\n'
    mel_name = "{path}/{name}_{{}}.fbx".format(export.split(":")[0].split("_")[0])
    maya.cmds.bakeResults(simulation=True,t=(start,end),hierarchy="below",sampleBy=1,disableImplicitControl=True,preserveOutsideKeys=False, sparseAnimCurveBake=False)
    maya.mel.eval("FBXExportBakeComplexAnimation -v true")
    maya.mel.eval('FBXExport -f "%s" -s' %mel_name)
    log = log + export + "------> OK"

exclude = ".*(front|persp|side|top|camera).*"

cameras = maya.cmds.ls(type='camera',l=True) or []


for camer in cameras:
    ex = True
    for test in filter(None,camer.split("|")):
        if re.findall(exclude,test):
            ex = False
    if ex == True:
        exportCamera = maya.cmds.listRelatives(camer,parent = True,fullPath=True)[0]
        maya.cmds.select(exportCamera)
        maya.cmds.FBXExport("-file", "{path}/{name}_camera_{{}}-{{}}.fbx".format(int(start),int(end)), "-s")

with open(myfile,"a") as f:
    f.write(log)

""".format(paths=str(self.path.as_posix()), path=str(self.path.parent.as_posix()), name=self.path.stem)
        tmp_path = pathlib.Path(tempfile.gettempdir()).joinpath('export.py')
        tmp_path.write_text(out)
        # cmdCom = """set PATH = %PATH%;"C:\Program Files\Autodesk\Maya2018\Python\Lib\site-packages"
        # CALL {} {}""".format(mayapy_path,tmp_path)
        # tmp_path_cmd = pathlib.Path(tempfile.gettempdir()).joinpath('export_cmd.cmd')
        # tmp_path_cmd.write_text(cmdCom)
        logging.info("open %s", mayapy_path)
        # os.system(cmdCom)
        # os.system(str(mayapy_path) + ''' ''' + str(tmp_path))
        # sys.path.append(r"C:\Program Files\Autodesk\Maya2018\Python\Lib\site-packages")
        # subprocess.run([str(mayapy_path), str(tmp_path)])
        # os.system(os.path.join(tempfile.gettempdir(), "doodle_maya_export_log.txt"))
