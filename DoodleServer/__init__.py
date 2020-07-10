import pathlib


def GETDOODLEROOT(paths: pathlib.Path):
    for path in paths.iterdir():
        if path.name == "doodle":
            return path
    return GETDOODLEROOT(paths.parent)


import DoodleServer.DoodleBaseClass as baseClass
import DoodleServer.DoodleSynXml as synXml
import DoodleServer.DoodleSet as Set
import DoodleServer.DoodleOrm as Orm
import DoodleServer.DoodleZNCHConvert as ZNconvert
import DoodleServer.DoodleSql as sqlCon
import DoodleServer.DoodleCore as Core
import DoodleServer.DoodlePlayer as Player

import DoodleServer.DoodleDictToObject as dictToObj
