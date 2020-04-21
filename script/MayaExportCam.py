import maya.standalone
maya.standalone.initialize( name='python' )
import maya.cmds
import maya.mel
import pymel.core
maya.cmds.file(new=True, force=True)
maya.cmds.file('C:/Users/teXiao/Documents/test.mb',o=True)
pymel.core.file('C:/Users/teXiao/Documents/test.mb',o=True)
maya.cmds.select('persp1')
maya.mel.eval('''FBXExport -f "D:/testaa.fbx" -s''')