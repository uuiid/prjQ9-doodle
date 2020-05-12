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
import script
import sqlalchemy.sql.default_comparator
import sqlalchemy.ext.baked
from cx_Freeze import setup, Executable

base = None
if sys.platform == 'win32':
    base = 'Win32GUI'
includefiles = ["UiFile", "tools", "datas", "config"]
includes = ['urllib3',
            "multiprocessing",
            "script/convert.py",
            "script/doodle_setting.py",
            "script/doodleLog.py",
            "script/doodlePlayer.py",
            "script/DooDlePrjCode.py",
            "script/DoodleUpdata.py",
            "script/MayaExportCam.py",
            "script/MySqlComm.py",
            "script/ProjectBrowserGUI.py",
            "script/synchronizeFiles.py",
            "script/synXml.py",
            "sqlalchemy",
            "sqlalchemy.ext.declarative",
            "sqlalchemy.sql",
            "sqlalchemy.sql.default_comparator.py",
            "sqlalchemy.ext.baked.py"]
options = {
    'build_exe': {
        "build_exe":"dist/doodle_tray",
        'includes': includes,
        "include_files": includefiles
    }
}

executables = [
    Executable('doodle_tray.py', base=base)
]

setup(name='doodle',
      version='0.1',
      description='doodle',
      options=options,
      executables=executables
      )
