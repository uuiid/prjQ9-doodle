import os
import pathlib
import tempfile

"""import maya.standalone

maya.standalone.initialize(name='python')
import maya.cmds
import maya.mel
import pymel.core
import subprocess

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
    def path(self) ->pathlib.Path:
        if not hasattr(self, '_path'):
            self._path = ''
        return self._path

    @path.setter
    def path(self, path):
        if not isinstance(path,pathlib.Path):
            path = pathlib.Path(path)
        self._path = path

    def __init__(self, path:pathlib.Path):
        if not isinstance(path,pathlib.Path):
            path = pathlib.Path(path)
        self._path = path

    def exportCam(self):
        mayapy_path = '"C:\\Program Files\\Autodesk\\Maya2018\\bin\\mayapy.exe"'
        out = """import maya.standalone
maya.standalone.initialize( name='python' )
import maya.cmds
import maya.mel
import pymel.core
import tempfile
import os

maya.cmds.file(new=True, force=True)
maya.cmds.file('{paths}',o=True)

myfile = os.path.join(tempfile.gettempdir(),"doodle_maya_export_log.txt")
exports = cmds.ls("::*UE4")

log = ''
log = log + "dao  chu  wu  ti \\n" + "\\n".join(exports) + "\\n\\n"

for export in exports:
    maya.cmds.select(export)
    mystr = '_'
    log = log + 'ming Lin'+ 'FBXExport -f "{path}/{name}_{{suex=export.split(mystr)[0]}}.fbx" -s' + '\\n'
    mel_name = "{path}/{name}_{{}}.fbx".format(export.split("_")[0])
    maya.mel.eval('FBXExport -f "%s" -s' %mel_name)
    log = log + export + "------> OK"

with open(myfile,"a") as f:
    f.write(log)

""".format(paths=str(self.path.as_posix()),path=str(self.path.parent.as_posix()),name=self.path.stem)
        tmp_path = pathlib.Path(tempfile.gettempdir()).joinpath('export.py')
        tmp_path.write_text(out)
        os.system(mayapy_path + ''' ''' + str(tmp_path))
        os.system(os.path.join(tempfile.gettempdir(),"doodle_maya_export_log.txt"))