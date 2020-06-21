import shelfBase
import maya.cmds as cmds

import Doodle_PolyRemesh
import Doodle_exportUe
import Doodle_cam
import Doodle_clear


class DlsShelf(shelfBase._shelf):


    def build(self):
        self.addButon("export_cam",icon="icons/OUTcam.png",command=self.exportCam)
        self.addButon("export_abc",icon="icons/OUTabc.png",command=self.exportAbc)
        self.addButon("back_cam",icon="icons/back_cam.png",command=self.BakeAimCam)
        
        self.addButon("remesh",icon="icons/remesh.png",command=self.polyremesh)

        self.addButon("clear",icon="icons/clear.png",command=self.clearScane)
    
    def polyremesh(self):
        Doodle_PolyRemesh.myRemesh()
    
    def exportCam(self):
        Doodle_exportUe.export("one")
    
    def exportAbc(self):
        Doodle_exportUe.export("two")

    def BakeAimCam(self):
        Doodle_cam.camBakeAim()

    def clearScane(self):
        Doodle_clear.clearAndUpload().clearScane()


class DoodleUIManage(object):
    _instances = set()

    @staticmethod
    def creation():
        shelf = DlsShelf("Doodle")
        DoodleUIManage._instances.add(shelf)

    @staticmethod
    def deleteSelf():
        for inst in tuple(DoodleUIManage._instances):
            if cmds.shelfLayout(inst.name, ex=1):
                try:
                    cmds.deleteUI(inst.name)
                except RuntimeError:
                    pass
            DoodleUIManage._instances.discard(inst)