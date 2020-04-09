# -*- coding: UTF-8 -*-
import pathlib
from typing import Iterator, Dict

import script.ProjectBrowserGUI
import script.doodle_setting


class DbxyProjectAnalysisShot():

    @staticmethod
    def getEpisodesItems(obj: script.ProjectBrowserGUI.ProjectBrowserGUI) -> list:
        """获得集数所在的文件夹"""
        root = obj.root
        item = []
        for path in root.iterdir():
            if path.is_dir():
                item.append(path.stem.split('-')[0])
        item = list(set(item))
        item.sort()
        return item

    @staticmethod
    def episodesFolderName(obj: script.ProjectBrowserGUI.ProjectBrowserGUI, episode: int) -> list:
        """要返回路径对象的列表"""
        tmp = []
        name = "ep{:0>2d}".format(episode)
        name = obj.root.joinpath(name)
        tmp.append(name)
        return tmp

    @staticmethod
    def getShotPath(obj: script.ProjectBrowserGUI.ProjectBrowserGUI) -> pathlib.Path:
        """获得镜头所在的文件夹"""
        root = obj.root
        return pathlib.Path(root)

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
    def shotFolderName(obj: script.ProjectBrowserGUI.ProjectBrowserGUI, shot: int, ab_shot: str = None) -> list:
        """获得镜头路径文件夹,路径obj的一个列表"""
        tmp = []
        shotname = '{}-sc{:0>4d}'.format(obj.file_episods, shot)
        root = obj.root
        if ab_shot:
            shotname = '{}{}'.format(shotname, ab_shot)
        shot = root.joinpath(shotname)

        for sub_directory in ['Export', 'Playblasts', 'Rendering', 'Scenefiles']:
            sub_dir: pathlib.Path = shot.joinpath(sub_directory)
            tmp.append(sub_dir)
        return tmp

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
        """获得部门文件夹的内部项数"""
        department = obj.file_department_path
        mitem = []
        if department:
            for mi in department.iterdir():
                mitem.append(mi.stem)
        return mitem

    @staticmethod
    def getDepTypePath(obj: script.ProjectBrowserGUI.ProjectBrowserGUI) -> pathlib.Path:
        """获得类型所在文件夹"""
        dep = obj.file_department
        if dep:
            # department = item.text()
            department = obj.file_department_path
            dep = department.joinpath(dep)  # type : pathlib.Paht
        return dep

    @staticmethod
    def getDepTypeItems(obj: script.ProjectBrowserGUI.ProjectBrowserGUI) -> list:
        """获得类型所在文件夹中的项数"""
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
        """获得文件所在位置文件夹"""
        try:
            depType = obj.file_Deptype_path
            depType = depType.joinpath(obj.file_Deptype)
        except:
            raise
        return depType

    @staticmethod
    def fileNameInformation(obj: script.ProjectBrowserGUI.ProjectBrowserGUI) -> list:
        """获得文件名称中的信息, 并以字典返回"""
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
        """这个用来组合文件名称"""
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
    def commFileName(item: Dict) -> str:
        """组合字典成为文件名称"""
        filename = 'shot_{}-{}_{}_{}_{}__{}_{}'.format(item['file_episods'],
                                                       item['file_shot'],
                                                       item['file_department'],
                                                       item['file_Deptype'],
                                                       item['version'],
                                                       item['user'],
                                                       item['fileSuffixes'])
        return filename


class DbxyProjectAnalysisAssets():
    def __init__(self):
        pass
