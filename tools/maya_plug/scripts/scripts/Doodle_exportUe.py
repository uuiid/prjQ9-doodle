# coding=utf-8
# version = 1.21

import maya.cmds
import maya.mel
import pymel.core
import os


def addPlug():
    maya.cmds.loadPlugin('AbcExport.mll')
    maya.cmds.loadPlugin('AbcImport.mll')


def getoutFileName(outtype,older):
    exname = ""
    #get name space
    inum = 0
    while inum <len(pymel.core.selected()):
        namesp = pymel.core.selected()[inum].namespace()
        if namesp !="":
            break
        inum = inum + 1
    try:
        namesp = namesp.split(":")[-2].replace("_","-")
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

    filepath = filename.split("_")
    if filepath[0] != "":
        if filepath[1] != "":
            if filepath[2] != "":
                if filepath[3] != "":
                    tfilepath = os.path.join("W:/03_Workflow/", filepath[0] + "s", filepath[1],filepath[2], "Scenefiles", filepath[3], filepath[4])
                    tfilepath = mkdir(tfilepath)

                    exname = tfilepath + "/" + filepath[0] + "_" + filepath[1] + "_" + filepath[2] + "_" + filepath[3] + "_" + filepath[4] \
                        + "_" + "export-" + older_B + "_" + namesp + "_" + "." + str(start) + "-" + str(end) + "." + outtype
    return [os.path.abspath(exname),start,end]

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
        print(exmashs)
        fileinabc = getoutFileName("abc","repair")
        if nump == "two":
            fileinfbx = getoutFileName("fbx","repair")
            exmashFBX = maya.cmds.duplicate(exmashs)
            exmashFBX = maya.cmds.ls(sl=True, long=True)
            maya.cmds.polyUnite(exmashFBX,n="exfbx")
            exmashFBX = maya.cmds.ls(sl=True, long=True)
            maya.cmds.currentTime(fileinabc[2], update=True, edit=True)
        else:
            fileinfbx = getoutFileName("fbx","cam")
        print(fileinfbx)

        maya.cmds.FBXExport("-file", fileinfbx[0], "-s")
        if nump == "two":
            maya.cmds.delete(exmashFBX)
        


        if nump == "two":
            abcexmashs = ""
            print(fileinabc)
            for exmash in exmashs:
                abcexmashs = abcexmashs + "-root " + exmash + " "

            abcExportCom = 'AbcExport -j "-frameRange ' + str(fileinabc[1]) + " " + str(
                fileinabc[2]) + " -worldSpace -dataFormat ogawa " + abcexmashs + "-file " + fileinabc[0].replace("\\","/") + '"' # -uvWrite

            maya.mel.eval(abcExportCom)
            # This is a command to export FBX
    else:
        pass
