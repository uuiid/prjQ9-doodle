# -*- coding: UTF-8 -*-
#coding=utf-8
import os

ROOT = "D:/ueFile"
section = ['Light','Ren','Checkpoint']
content = ['VFX','Light']
keyPath = {'01shot':['shot'],'02works':['Ep'],'03scene':'Sc','04section':section,'05Content':content}

def mkemyFile(paths):
    for path in paths:
        folder = os.path.exists(path)

        if not folder:
            os.makedirs(path)
            print("new folder: {}".format(path))
        else:
            print("cunZhai: {}".format(path))

def shengChengPath(work,scene,root):
    pathLen =  scene*len(content)*len(section)
    print(pathLen)
    Mpaths = []

    for myi in range(1,scene):
        path = keyPath['03scene'] + '{:0>4d}'.format(myi)
        Mpaths.append(path)
    keyPath['03scene'] = Mpaths
    
    keyPath['02works'][0] = keyPath['02works'][0] + '{:0>3d}'.format(work)

    paths = []
    
    for sh in keyPath['01shot']:
        for wo in keyPath['02works']:
            for sc in keyPath['03scene']:
                for se in keyPath['04section']:
                    for co in keyPath['05Content']:
                        if se !='Checkpoint':
                             co = ""
                        tmp = os.path.join(sh,wo,sc,se,co)
                        tmp = os.path.join(root,tmp)
                        paths.append(tmp)

    print(len(paths))
    for i in paths:
        print('folder : {}'.format(i))

    return paths

work = 4
scene = 111
path =  shengChengPath(work,scene,ROOT)
mkemyFile(path)