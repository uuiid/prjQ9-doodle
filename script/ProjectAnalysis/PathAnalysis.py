# -*- coding: UTF-8 -*-
import pathlib
from typing import Iterator, Dict

import pypinyin

import script.ProjectBrowserGUI
import script.readServerDiectory
import script.doodle_setting


class DbxyProjectAnalysisShot():

    @staticmethod
    def getEpisodesItems(obj: script.ProjectBrowserGUI.ProjectBrowserGUI) -> list:
        root = obj.root
        item = []
        for path in root.iterdir():
            if path.is_dir():
                item.append(path.stem.split('-')[0])
        item = list(set(item))
        item.sort()
        return item

    @staticmethod
    def getShotPath(obj: script.ProjectBrowserGUI.ProjectBrowserGUI) -> pathlib.Path:
        root = obj.root
        return pathlib.Path(root)
        pass

    @staticmethod
    def getShotItems(obj: script.ProjectBrowserGUI.ProjectBrowserGUI) -> Iterator[str]:
        """获得shot列表"""
        episods = obj.file_episods
        paths = obj.root

        mitem = []
        for path in paths.iterdir():
            if path.match('{}*'.format(episods)):
                try:
                    mitem.append(path.stem.split('-')[1])
                except:
                    pass
        mitem = list(set(mitem))
        mitem.sort()
        mitem = filter(None, mitem)
        return mitem

    @staticmethod
    def getdepartmentPath(obj: script.ProjectBrowserGUI.ProjectBrowserGUI) -> pathlib.Path:
        """获得部门文件夹"""
        # 获得根文件夹
        root = obj.root
        try:
            # 获得集数
            epis = obj.file_episods
            # 获得镜头号
            shot = obj.file_shot
        except:
            department = ''
        else:
            # 获得部门文件夹
            department = root.joinpath('{}-{}'.format(epis, shot))
            department = department.joinpath('Scenefiles')

        return department

    @staticmethod
    def getdepartmentItems(obj: script.ProjectBrowserGUI.ProjectBrowserGUI) -> list:
        department = obj.file_department_path
        mitem = []
        if department:
            for mi in department.iterdir():
                mitem.append(mi.stem)
        return mitem

    @staticmethod
    def getDepTypePath(obj: script.ProjectBrowserGUI.ProjectBrowserGUI) -> pathlib.Path:
        dep = obj.file_department
        if dep:
            # department = item.text()
            department = obj.file_department_path
            dep = department.joinpath(dep)  # type : pathlib.Paht

        return dep


    @staticmethod
    def getDepTypeItems(obj: script.ProjectBrowserGUI.ProjectBrowserGUI) -> list:
        dep = obj.file_Deptype_path
        mitem = []
        if dep.iterdir():
            for mi in dep.iterdir():
                if mi.is_dir():
                    mitem.append(mi.stem)
        else:
            raise
        return mitem

    @staticmethod
    def getFilePath(obj: script.ProjectBrowserGUI.ProjectBrowserGUI) -> pathlib.Path:
        try:
            depType = obj.file_Deptype_path
            depType = depType.joinpath(obj.file_Deptype)
        except:
            raise

        return depType

    @staticmethod
    def fileNameInformation(obj: script.ProjectBrowserGUI.ProjectBrowserGUI) -> list:
        dep_type_iterdir = obj.file_path.iterdir()
        mitem = []
        if dep_type_iterdir:
            for mFile in dep_type_iterdir:
                if mFile.is_file():
                    mitem.append({'filename': mFile.stem, 'fileSuffixes': mFile.suffix})
        else:
            raise
        # 迭代获得文件命中包含信息
        information: list = []
        if mitem:
            for file in mitem:
                tmp = file['filename'].split('_')
                try:
                    tmp = {'Type': tmp[0],
                           'epShot': tmp[1],
                           'department': tmp[2],
                           'depType': tmp[3],
                           'version': tmp[4],
                           'producer': tmp[6],
                           'fileSuffixes': file['fileSuffixes']
                           }
                except IndexError:
                    other = tmp
                except:
                    pass
                else:
                    information.append(tmp)

        return information

    @staticmethod
    def getFileName(obj: script.ProjectBrowserGUI.ProjectBrowserGUI) -> dict:
        # 这个用来组合文件名称
        indexs = obj.listfile.selectedItems()
        item: Dict[str, str] = {'version': indexs[0].text()}
        if len(indexs) == 4:
            item['user'] = indexs[2].text()
            item['fileSuffixes'] = indexs[3].text()
        else:
            item['user'] = indexs[1].text()
            item['fileSuffixes'] = indexs[2].text()

        item['file_episods'] = obj.file_episods
        item['file_shot'] = obj.file_shot
        item['file_department'] = obj.file_department
        item['file_Deptype'] = obj.file_Deptype
        return item

    @staticmethod
    def commFileName(item: Dict):
        filename = 'shot_{}-{}_{}_{}_{}__{}_{}'.format(item['file_episods'],
                                                       item['file_shot'],
                                                       item['file_department'],
                                                       item['file_Deptype'],
                                                       item['version'],
                                                       item['user'],
                                                       item['fileSuffixes'])


class DbxyProjectAnalysisAssets():
    def __init__(self):
        pass
