# -*- coding: UTF-8 -*-
import sys
import os
import json
import re
import pymel.core
import UiFile.DleClothToFbx
import pickle

from maya import OpenMayaUI as omui
from PySide2 import QtCore
from PySide2 import QtGui
from PySide2 import QtWidgets

from shiboken2 import wrapInstance
from multiprocessing import connection as Conn

reload(UiFile.DleClothToFbx)
mayaMainWindowPtr = omui.MQtUtil.mainWindow()
mayaMainWindow = wrapInstance(long(mayaMainWindowPtr), QtWidgets.QWidget)


class doodleSet(object):
    url = "getDoodleSet"


class convertSet(object):
    url = ""

    abc_poly_meshname = ""
    abc_obj = ""
    fbx_poly_meshname = ""
    fbx_obj = ""
    bones = 100
    Ifbx_filename = ""
    Ifbx_path = ""
    Iabc_filename = ""
    Iabc_path = ""
    Ofbx_filename = ""
    Ofbx_path = ""
    cluster_iter_num = 10
    global_iter_num = 30
    trans_iter_num = 5
    bind_update_num = 0
    trans_affine = 10
    trans_affine_norm = 4
    weights_iters = 3
    not_zero_bone_num = 8
    weights_smooth = 0.0001
    weights_smooth_step = 1

    @property
    def Ifbx_filepath(self):
        path = os.path.abspath(os.path.join(self.Ifbx_path, self.Ifbx_filename)).replace("\\", "/")
        return path

    @property
    def Iabc_filepath(self):
        path = os.path.abspath(os.path.join(self.Iabc_path, self.Iabc_filename)).replace("\\", "/")
        return path

    @property
    def Ofbx_filepath(self):
        path = os.path.abspath(os.path.join(self.Ofbx_path, self.Ofbx_filename)).replace("\\", "/")
        return path

    def toCommand(self):
        list_com = ["DemBones.exe", "--abc", self.Iabc_filepath, "--init", self.Ifbx_filepath, "--out", self.Ofbx_filepath,
                    "--nBones", self.bones, "--nInitIters", self.cluster_iter_num, "--nIters", self.global_iter_num,
                    "--nTransIters", self.trans_iter_num, "--bindUpdate", self.bind_update_num,
                    "--transAffine", self.trans_affine, "--transAffineNorm", self.trans_affine_norm,
                    "--nWeightsIters", self.weights_iters, "--nnz", self.not_zero_bone_num,
                    "--weightsSmooth", self.weights_smooth, "--weightsSmoothStep", self.weights_smooth_step]
        return list_com

    def to_dict(self):
        return {"Ifbx_filepath":self.Ifbx_filepath,"Iabc_filepath":self.Iabc_filepath,"Ofbx_filepath":self.Ofbx_filepath,
        "Command":self.toCommand()}

    def exportMesh(self, start, end):
        if not os.path.isdir(self.Iabc_path):
            os.makedirs(self.Iabc_path)
        if not os.path.isdir(self.Ifbx_path):
            os.makedirs(self.Ifbx_path)
        pymel.core.select(self.fbx_obj)
        pymel.core.other.FBXExport("-file", self.Ifbx_filepath, "-s")
        abc_mesh = "-root {}".format(self.abc_obj.longName())
        pymel.core.other.AbcExport(
            jobArg="-frameRange {range_start} {range_end}  -worldSpace -dataFormat ogawa {mesh_path} -file {file_path}".format(
                range_start=start, range_end=end, mesh_path=abc_mesh, file_path=self.Iabc_filepath
            ))

    def countBone(self, tranNode):
        num = pymel.core.polyEvaluate(tranNode.name(), vertex=True)
        bone = int(num/100)
        if bone>100:
            index = bone/100
            bone = 100 + int((bone-100)/index)
        self.bones = bone


class DleClothToFbx(QtWidgets.QMainWindow, UiFile.DleClothToFbx.Ui_MainWindow):
    tran = []
    abc = []
    bem_bone = []

    def __init__(self):
        super(DleClothToFbx, self).__init__()
        self.setParent(mayaMainWindow)
        self.setWindowFlags(QtCore.Qt.Window)

        self.setupUi(self)
        # 设置启用
        self.ExportClothAndFbx.setEnabled(False)
        self.getSelectDynamicCloth.setEnabled(False)
        self.selectdynamicClothList.setStyleSheet("background-color: rgb(60,60,60)")
        # 链接获取选择obj
        self.getSelectObj.clicked.connect(self._getSelectMesh)
        # 连接添加动态布料导出obj
        self.getSelectDynamicCloth.clicked.connect(self._getSelectDynamMesh)
        # 解析文件名称
        self._getFileInfo()
        # 链接测试按钮
        self.testing.clicked.connect(self.clicledTesting)
        # 添加客户端
        self.client = Conn.Client(("127.0.0.1", 23369), authkey=b"doodle")

        # 添加导出连接
        self.ExportClothAndFbx.clicked.connect(self.exportButtenClicked)
        # 连接客户端获得必要信息
        self.client.send_bytes(pickle.dumps({"url": "getDoodleSet"}))
        doodleset = pickle.loads(self.client.recv_bytes())
        # 将信息写入实例
        self.cache_path = doodleset["cache_path"]
        self.user = doodleset["user"]
        self.user = doodleset["department"]
        self.projectname = doodleset["projectname"]

        # 添加动态布料启用
        self.dynamicCloth.stateChanged.connect(self._setEnableDynamicCloth)

    def _getSelectMesh(self, a0):
        self.bem_bone=[]
        self.tran = []
        self.tran = pymel.core.ls(sl=True)
        self.selectClothList.clear()
        self.selectClothList.addItems([t.name() for t in self.tran])
        self.ExportClothAndFbx.setEnabled(False)

        for line, tran in enumerate(self.tran):
            bem_bone = convertSet()
            # 获得fbx网格名称和节点
            bem_bone.fbx_poly_meshname = tran.name()
            bem_bone.fbx_obj = tran
            # 如果是动态特网格在一起就直接设置为一种
            bem_bone.abc_poly_meshname = tran.name()
            bem_bone.abc_obj = tran

            bem_bone.Ofbx_filename = tran.name() + u".fbx"
            # 获得路径
            path = os.path.join(self.cache_path, self.getpath()[1:])
            # 填写输出路径和名称
            print(path)
            bem_bone.Ifbx_filename = tran.name() + u"_fbx.fbx"
            bem_bone.Ifbx_path = path

            bem_bone.Iabc_filename = tran.name() + u"_abc.abc"
            bem_bone.Iabc_path = path

            bem_bone.Ofbx_path = path
            bem_bone.countBone(tran)
            self.bem_bone.append(bem_bone)    

    def _getSelectDynamMesh(self):
        self.abc = []
        self.abc = pymel.core.ls(sl=True)
        self.selectdynamicClothList.clear()
        self.selectdynamicClothList.addItems([t.name() for t in self.abc])
        self.ExportClothAndFbx.setEnabled(False)

        for line, tran in enumerate(self.abc):
            bem_bone = self.bem_bone[line]
            # 设置abc信息
            bem_bone.abc_poly_meshname = tran.name()
            bem_bone.abc_obj = tran

            bem_bone.Iabc_filename = tran.name() + u"_abc.abc"
    

    def _getFileInfo(self):
        filename = pymel.core.system.sceneName()
        name_parsing_ep = re.findall("ep\d+", filename)
        name_parsing_shot = re.findall("sc\d+[_BCD]", filename)
        if name_parsing_ep and name_parsing_shot:
            try:
                self._eps = int(name_parsing_ep[0][2:])
            except NameError:
                self._eps = 1
            try:
                self._shot = int(name_parsing_shot[0][2:-1])
                shotab = name_parsing_shot[0][-1:]
                if shotab != "_":
                    self._shotab = shotab
                else:
                    self._shotab = ""
            except NameError:
                self._shot = 1
                self._shotab = ""
            self.episodes.setValue(self._eps)
            self.shot.setValue(self._shot)
            self.shotAb.setCurrentText(self._shotab)
        else:
            self.testing.setStyleSheet("background-color: darkred")
            # print(self.testing.text)
            self.testing.setText(u"检测(无法自动解析,请手动输入)")

    def _setEnableDynamicCloth(self, a0):
        if a0 == 2:

            self.selectdynamicClothList.setStyleSheet("")
            self.getSelectDynamicCloth.setEnabled(True)
        else:
            self.selectdynamicClothList.setStyleSheet("background-color: rgb(60,60,60)")
            self.getSelectDynamicCloth.setEnabled(False)
        self.ExportClothAndFbx.setEnabled(False)
        self.selectdynamicClothList.clear()



    def getpath(self):
        my_dict = pickle.dumps(dict({"url": "getPath", "core": "shot"}, **self.pathInfo()))
        self.client.send_bytes(my_dict)
        return pickle.loads(self.client.recv_bytes())

    def pathInfo(self):
        return {"episodes": self._eps, "shot": self._shot, "shotab": self._shotab, "Type": "clothToFbx",
                "folder_type": "export_clothToFbx"}

    def computeConvertValue(self):
        pass

    def clicledTesting(self):
        self._getFileInfo()
        self.ScaneStartFrame = pymel.core.playbackOptions(query=True, min=True)
        self.ScaneEndFrame = pymel.core.playbackOptions(query=True, max=True)

        self.ExportClothAndFbx.setEnabled(True)

    def closeEvent(self, event):
        """
        关闭窗口时同时断开服务器连接
        :param event:
        :return:
        """
        self.client.send_bytes(b"close")
        self.client.close()

    def exportButtenClicked(self):
        is_export_ok = True
        for bem in self.bem_bone:
            bem.exportMesh(self.ScaneStartFrame, self.ScaneEndFrame)
            if not (os.path.isfile(bem.Ifbx_filepath) and os.path.isfile(bem.Iabc_filepath)):
                is_export_ok = False
        
        if is_export_ok:
            self.client.send_bytes(pickle.dumps(
                {"url":"subInfo","core":"shot","specific":"subClothExport",
                 "info":dict({"filepath":[bem.Ifbx_filepath for bem in self.bem_bone] +
                                         [bem.Iabc_filepath for bem in self.bem_bone]},**self.pathInfo()),
                 "_data_":[bem.to_dict() for bem in self.bem_bone]}))
        self.client.send_bytes(b"close")
        self.client.close()
        self.close()




