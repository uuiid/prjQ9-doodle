# -*- coding: utf-8 -*-

# A simple setup script to create an executable using PyQt5. This also
# demonstrates the method for creating a Windows executable that does not have
# an associated console.
#
# PyQt5app.py is a very simple type of PyQt5 application
#
# Run the build process by running the command 'python setup.py build'
#
# If everything works well you should find a subdirectory in the build
# subdirectory that contains the files needed to run the application

import sys
import pathlib
from cx_Freeze import setup, Executable

def toolspy() -> list:
    path = pathlib.Path("tools")
    # infil = []
    # for p in path.iterdir():
    #     if p.is_file():
    #         infil.append(p)
    return [(p.as_posix(), p.as_posix()) for p in path.iterdir() if p.is_file()]


base = None
if sys.platform == 'win32':
    base = 'Win32GUI'
includefiles = ["UiFile", ("tools/template", "tools/template"),
                ("tools/maya_plug","tools/maya_plug"),
                ("tools/dem_bones","tools/dem_bones"),
                "datas", "config"] + toolspy()
includes = ['urllib3',
            "multiprocessing",
            "script.DoodleUpdata",
            "script.DoodleMain",
            "script.DoodleBrowserGUI",
            "DoodleServer.DoodleBaseClass",
            "DoodleServer.DoodleCore",
            "DoodleServer.DoodleDictToObject",
            "DoodleServer.DoodleLoging",
            "script.DoodlePrjUI",
            "script.DoodlePrjUI.DoodleLabel",
            "UiFile",
            "sqlalchemy",
            "sqlalchemy.ext.declarative",
            "sqlalchemy.sql",
            "sqlalchemy.sql.default_comparator",
            "sqlalchemy.ext.baked"]

mypath = sys.path + ["C:\\Program Files\\Autodesk\\Maya2018\\bin",
                     "C:\\Program Files\\Autodesk\\Maya2018\\Python\\Lib\\site-packages"]
options = {
    'build_exe': {
        "build_exe": "dist/doodle_tray",
        'includes': includes,
        "include_files": includefiles,
        "path": mypath
    }
}

executables = [
    Executable('doodle.py', base=base)
]

setup(name='doodle',
      version='0.1',
      description='doodle',
      options=options,
      executables=executables
      )
