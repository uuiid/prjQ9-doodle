# coding=utf-8
# version = 1.21

import maya.cmds
import maya.mel
import pymel.core
import re
import os

from PySide2 import QtCore
from PySide2 import QtGui
from PySide2 import QtWidgets


def addPlug():
    maya.cmds.loadPlugin('AbcExport.mll')
    maya.cmds.loadPlugin('AbcImport.mll')


def getoutFileName(outtype, older, root):
    exname = ""
    # get name space
    inum = 0
    while inum < len(pymel.core.selected()):
        namesp = pymel.core.selected()[inum].namespace()
        if namesp != "":
            break
        inum = inum + 1
    try:
        namesp = namesp.split(":")[-2].replace("_", "-")
    except:
        namesp = ""
    else:
        print(namesp)

    if outtype not in ["abc", "fbx"]:
        return exname
    older_B = older
    older = "/" + older
    if older == "/cam":
        namesp = ""
        older = ""
    # Get scene name
    print(namesp)
    filename = maya.cmds.file(q=True, sn=True, shn=True)
    filename = filename.split('.')[0]

    print(filename)
    # Get the end and start frames of the scene
    start = maya.cmds.playbackOptions(query=True, min=True)
    end = maya.cmds.playbackOptions(query=True, max=True)

    start = int(start)
    end = int(end)
    print(start)
    print(end)

    name_parsing_ep = re.findall("ep\d+", filename)
    name_parsing_shot = re.findall("sc\d+[_BCD]", filename)
    if name_parsing_ep and name_parsing_shot:
        try:
            _eps = int(name_parsing_ep[0][2:])
        except NameError:
            _eps = 1
        try:
            _shot = int(name_parsing_shot[0][2:-1])
            shotab = name_parsing_shot[0][-1:]
            if shotab != "_":
                _shotab = shotab
            else:
                _shotab = ""
        except NameError:
            _shot = 1
            _shotab = ""
        tfilepath = "{root_}/03_Workflow/shots/ep{eps:0>3d}/" \
                    "sc{shot:0>4d}{shotab}/Scenefiles/{dep}/{aim}".format(eps=_eps,
                                                                          shot=_shot,
                                                                          shotab=_shotab,
                                                                          dep=filename.split("_")[3],
                                                                          aim=filename.split("_")[4],
                                                                          root_=root)
        tfilepath = mkdir(tfilepath)
        filepath = filename.split("_")
        exname = tfilepath + "/" + filepath[0] + "_" + filepath[1] + "_" + filepath[2] + "_" + filepath[
            3] + "_" + filepath[4] \
                 + "_" + "export-" + older_B + "_" + namesp + "_" + "." + str(start) + "-" + str(
            end) + "." + outtype
    return [os.path.abspath(exname), start, end]


def mkdir(path):
    myisExis = os.path.exists(path)
    if not myisExis:
        os.makedirs(path)
        print(path + " ok")
        return path
    else:
        print(path + " yi Zai")
        return path


def export(nump):
    exmashs = maya.cmds.ls(sl=True, long=True)
    if exmashs != "":
        box = QtWidgets.QMessageBox()
        dubu_Butten = QtWidgets.QPushButton()
        dubu_Butten.setText("duBuXiaoYao")
        dubu = box.addButton(dubu_Butten, QtWidgets.QMessageBox.AcceptRole)

        chan_butten = QtWidgets.QPushButton()
        chan_butten.setText("changAnHuanJie")
        chan = box.addButton(chan_butten, QtWidgets.QMessageBox.AcceptRole)
        box.exec_()
        while 1:
            if box.clickedButton() == dubu_Butten:
                root = "V:"
                break
            elif box.clickedButton() == chan_butten:
                root = "X:"
                break
        print(exmashs)
        fileinabc = getoutFileName("abc", "repair", root)
        if nump == "two":
            fileinfbx = getoutFileName("fbx", "repair", root)
            exmashFBX = maya.cmds.duplicate(exmashs)
            exmashFBX = maya.cmds.ls(sl=True, long=True)
            maya.cmds.polyUnite(exmashFBX, n="exfbx")
            exmashFBX = maya.cmds.ls(sl=True, long=True)
            maya.cmds.currentTime(fileinabc[2], update=True, edit=True)
        else:
            fileinfbx = getoutFileName("fbx", "cam", root)
        print(fileinfbx)
        maya.mel.eval("FBXExportBakeComplexAnimation -v true")
        maya.mel.eval("FBXExportSmoothingGroups -v true")
        maya.mel.eval("FBXExportConstraints -v true")
        maya.cmds.FBXExport("-file", fileinfbx[0], "-s")
        if nump == "two":
            maya.cmds.delete(exmashFBX)

        if nump == "two":
            abcexmashs = ""
            print(fileinabc)
            for exmash in exmashs:
                abcexmashs = abcexmashs + "-root " + exmash + " "

            # abcExportCom = 'AbcExport -j "-frameRange ' + str(fileinabc[1]) + " " + str(
            #     fileinabc[2]) + " -worldSpace -dataFormat ogawa " + abcexmashs + "-file " + fileinabc[0].replace("\\",
            #                                                                                                      "/") + '"'   -uvWrite
            abcExportCom = """AbcExport -j "-frameRange {f1} {f2} -uvWrite -writeFaceSets -worldSpace -dataFormat ogawa {mash} -file {f0}" """ \
                .format(f0=fileinabc[0].replace("\\", "/"), f1=fileinabc[1], f2=fileinabc[2], mash=abcexmashs)
            maya.mel.eval(abcExportCom)
            # This is a command to export FBX
    else:
        pass
