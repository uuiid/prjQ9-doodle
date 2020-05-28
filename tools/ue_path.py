# -*- coding: UTF-8 -*-
# coding=utf-8
import os
import pathlib


class createPath(object):
    ROOT = "D:/"

    def __init__(self, root: str, eps: int, secene: int):
        self._section = ['Light', 'Ren', 'Checkpoint']
        self._content = ['VFX', 'Light']
        self._keyPath = {'01shot': ['shot'], '02works': ['Ep'], '03scene': 'Sc', '04section': self._section,
                         '05Content': self._content}
        self.ROOT = root
        self.eps = eps
        self._secene = secene
        self.paths = ""

    def create(self):
        path = self._shengChengPath(self.eps, self._secene, self.ROOT)
        self._mkemyFile(path)

    def _mkemyFile(self, paths):
        for path in paths:
            folder = os.path.exists(path)

            if not pathlib.Path(path).is_dir():
                pathlib.Path(path).mkdir(parents=True, exist_ok=True)
                # os.makedirs(path)
                print("new folder: {}".format(path))
            else:
                print("cunZhai: {}".format(path))

    def _shengChengPath(self, work, scene, root):
        pathLen = scene * len(self._content) * len(self._section)
        print(pathLen)
        Mpaths = []

        for myi in range(1, scene):
            path = self._keyPath['03scene'] + '{:0>4d}'.format(myi)
            Mpaths.append(path)
        self._keyPath['03scene'] = Mpaths

        self._keyPath['02works'][0] = self._keyPath['02works'][0] + '{:0>3d}'.format(work)

        paths = []

        for sh in self._keyPath['01shot']:
            for wo in self._keyPath['02works']:
                for sc in self._keyPath['03scene']:
                    for se in self._keyPath['04section']:
                        for co in self._keyPath['05Content']:
                            if se != 'Checkpoint':
                                co = ""
                            tmp = os.path.join(sh, wo, sc, se, co)
                            tmp = os.path.abspath(os.path.join(root, tmp))
                            paths.append(tmp)

        print(len(paths))
        for i in paths:
            print('folder : {}'.format(i))

        return paths
