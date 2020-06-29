# -*- coding: UTF-8 -*-
import pathlib

import pypinyin

class isChinese(object):

    def __init__(self, test_str):
        self.test_str = test_str
        name = test_str.__class__.__name__
        self.is_zn = getattr(self, "_is" + name)
        self.con = getattr(self,"_con" + name)

    def easyToEn(self):
        if self.isCHZN():
            return self.converEn()
        else:
            return self.test_str

    def isCHZN(self):
        return self.is_zn()

    def converEn(self):
        return self.con()

    def _isstr(self):
        assert isinstance(self.test_str,str)
        for _char in self.test_str:
            # print(_char)
            if '\u4e00' <= _char <= '\u9fff':
                # print(_char)
                return True
        return False

    def _isWindowsPath(self):
        assert isinstance(self.test_str,pathlib.WindowsPath)
        for _Pathchar in self.test_str.parts:
            # print(_Pathchar)
            for _char in _Pathchar:
                # print(_char)
                if '\u4e00' <= _char <= '\u9fff':
                    # print(_char)
                    return True
        return False

    def _constr(self):
        pathlist = pypinyin.slug(self.test_str, pypinyin.NORMAL,separator="")
        return pathlist

    def _conWindowsPath(self):
        pathlist = pathlib.Path('')
        for i in self.test_str.parts:
            pathlist = pathlist.joinpath(pypinyin.slug(i, pypinyin.NORMAL))
        return pathlist

