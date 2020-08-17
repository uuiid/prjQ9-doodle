import shelfBase
import maya.cmds as cmds

import scripts.Doodle_PolyRemesh as Doodle_PolyRemesh
import scripts.Doodle_exportUe as Doodle_exportUe
import scripts.Doodle_cam as Doodle_cam
import scripts.Doodle_clear as Doodle_clear
import scripts.Doodle_dem_bone as Doodle_dem_bone
import scripts.Doodle_deleteSurplusWeight as deleteWeight


class DlsShelf(shelfBase._shelf):

    def __init__(self):
        super(DlsShelf, self).__init__()
        self.cloth_to_fbx = None

    def build(self):
        self.addButon("export_cam", icon="icons/OUTcam.png", command=self.exportCam)
        self.addButon("export_abc", icon="icons/OUTabc.png", command=self.exportAbc)
        self.addButon("back_cam", icon="icons/back_cam.png", command=self.BakeAimCam)

        self.addButon("remesh", icon="icons/remesh.png", command=self.polyremesh)

        self.addButon("clear", icon="icons/clear.png", command=self.clearScane)
        self.addButon("CLoth_to_Fbx", icon="icons/cloth_to_fbx.png", command=self.clothToFbx)
        self.addButon("delect Weight", icon="icons/ue_delete_weight.png", command=self.deleteWeightPoint)

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

    def clothToFbx(self):
        if not self.cloth_to_fbx:
            self.cloth_to_fbx.show()
        else:
            self.cloth_to_fbx = Doodle_dem_bone.DleClothToFbx().show()

    def deleteWeightPoint(self):
        deleteWeight.deleteSurplusWeight().show()


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
