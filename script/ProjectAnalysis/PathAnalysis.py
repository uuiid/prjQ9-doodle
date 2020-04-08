# -*- coding: UTF-8 -*-
import os
import pathlib
import shutil
import sys
from typing import Dict

import pyperclip
import pypinyin
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets

import UiFile.ProjectBrowser
import script.convert
import script.debug
import script.doodle_setting
import script.readServerDiectory


class DbxyProjectAnalysis():

    @staticmethod
    def getepisodes(root: pathlib.Path) ->list:
        item = []
        for path in root.iterdir():
            if path.is_dir():
                item.append(path.stem.split('-')[0])
        item = list(set(item))
        item.sort()
        return item


class DbxyProjectAnalysisAssets():
    def __init__(self):
        pass
