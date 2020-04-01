# -*- coding: UTF-8 -*-
import pypinyin
import pathlib


def isChinese(strs: pathlib.Path):
    for _Pathchar in strs.parts:
        # print(_Pathchar)
        for _char in _Pathchar:
            # print(_char)
            if '\u4e00' <= _char <= '\u9fff':
                # print(_char)
                return True
    return False




def convertToEn(pathStrs: pathlib.Path) -> pathlib.Path:

    pathlist = pathlib.Path('')
    for i in pathlib.PurePath(pathStrs).parts:
        pathlist = pathlist.joinpath(pypinyin.slug(i, pypinyin.NORMAL))
    return pathlist
