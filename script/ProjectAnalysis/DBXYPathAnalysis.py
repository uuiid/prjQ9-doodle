# -*- coding: UTF-8 -*-
import pathlib
from typing import Iterator, Dict, TypeVar

import script.ProjectAnalysis.PathAnalysis
import script.doodleLog

# import script.ProjectBrowserGUI
# import script.doodle_setting


class ProjectAnalysisShot(script.ProjectAnalysis.PathAnalysis.ProjectAnalysisShot):

    @staticmethod
    def getEpisodesItems(obj) -> list:
        """获得集数所在的文件夹
        :type obj: script.ProjectBrowserGUI.ProjectBrowserGUI
        """
        root = obj.root
        item = []
        for path in root.iterdir():
            if path.is_dir():
                item.append(path.stem.split('-')[0])
        item = list(set(item))
        item.sort()
        script.doodleLog.ta_log.info("获得集数所在的文件夹")
        return item

    @staticmethod
    def episodesFolderName(obj, episode: int) -> list:
        """要返回路径对象的列表
        :type obj: script.ProjectBrowserGUI.ProjectBrowserGUI
        """
        tmp = []
        name = "ep{:0>2d}".format(episode)
        name = obj.root.joinpath(name)
        tmp.append(name)
        script.doodleLog.ta_log.info("要返回路径对象的列表")
        return tmp

    @staticmethod
    def getShotPath(obj) -> pathlib.Path:
        """获得镜头所在的文件夹
        :type obj: script.ProjectBrowserGUI.ProjectBrowserGUI
        """
        root = obj.root
        script.doodleLog.ta_log.info("获得镜头所在的文件夹")
        return pathlib.Path(root)

    @staticmethod
    def getShotItems(obj) -> Iterator[str]:
        """获得shot列表
        :type obj: script.ProjectBrowserGUI.ProjectBrowserGUI
        """
        script.doodleLog.ta_log.info("开始获得镜头所在的文件夹")
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
    def shotFolderName(obj, shot: int, ab_shot: str = None) -> list:
        """获得镜头路径文件夹,路径obj的一个列表
        :type obj: script.ProjectBrowserGUI.ProjectBrowserGUI
        """
        script.doodleLog.ta_log.info("开始组合shot文件夹列表")
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
    def getdepartmentPath(obj) -> pathlib.Path:
        """获得部门文件夹
        :type obj: script.ProjectBrowserGUI.ProjectBrowserGUI
        """
        script.doodleLog.ta_log.info("开始寻找部门文件夹")
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
    def getdepartmentItems(obj) -> list:
        """获得部门文件夹的内部项数
        :type obj: script.ProjectBrowserGUI.ProjectBrowserGUI
        """
        script.doodleLog.ta_log.info("开始寻找部门文件夹列表")
        department = obj.file_department_path
        mitem = []
        if department:
            for mi in department.iterdir():
                mitem.append(mi.stem)
        return mitem

    @staticmethod
    def getDepTypePath(obj) -> pathlib.Path:
        """获得类型所在文件夹
        :type obj: script.ProjectBrowserGUI.ProjectBrowserGUI
        """
        script.doodleLog.ta_log.info("开始寻找部门文件夹列表")
        dep = obj.file_department
        if dep:
            department = obj.file_department_path
            dep = department.joinpath(dep)  # type : pathlib.Paht
        return dep

    @staticmethod
    def getDepTypeItems(obj) -> list:
        """获得类型所在文件夹中的项数
        :type obj: script.ProjectBrowserGUI.ProjectBrowserGUI
        """
        script.doodleLog.ta_log.info("开始寻找类型文件夹")
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
    def getFilePath(obj) -> pathlib.Path:
        """获得文件所在位置文件夹
        :type obj: script.ProjectBrowserGUI.ProjectBrowserGUI
        """
        script.doodleLog.ta_log.info("找文件所在文件夹")
        try:
            depType = obj.file_Deptype_path
            depType = depType.joinpath(obj.file_Deptype)
        except:
            raise
        return depType

    @staticmethod
    def fileNameInformation(obj) -> list:
        """获得文件名称中的信息, 并以字典返回
        :type obj: script.ProjectBrowserGUI.ProjectBrowserGUI
        """
        script.doodleLog.ta_log.info("开始解析文件名称")
        dep_type_iterdir = obj.file_path.iterdir()
        mitem = []
        if dep_type_iterdir:
            for mFile in dep_type_iterdir:
                if mFile.is_file():
                    mitem.append({'filename': mFile.stem, 'fileSuffixes': mFile.suffix})
        else:
            script.doodleLog.ta_log.info("他是文件夹?")
        script.doodleLog.ta_log.info("分离文件名称和后缀: %s", mitem)
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
                    script.doodleLog.ta_log.info("文件信息变得奇怪了....%s", tmp)
                except:
                    script.doodleLog.ta_log.info("这是什么鬼┏┛墓┗┓...(((m -__-)m....%s", tmp)
                    pass
                else:
                    information.append(tmp)
        script.doodleLog.ta_log.info("文件信息获取完成")
        return information

    @staticmethod
    def getFileName(obj) -> dict:
        """这个用来分解文件名称中的信息
        :type obj: script.ProjectBrowserGUI.ProjectBrowserGUI
        """
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
        script.doodleLog.ta_log.info("组合文件名称完成%s", item)
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
        script.doodleLog.ta_log.info("真正的文件信息组合完成了....%s", filename)
        return filename


class ProjectAnalysisAssets(script.ProjectAnalysis.PathAnalysis.ProjectAnalysisAssets):
    @staticmethod
    def getAssFamilyPath(obj) -> pathlib.Path:
        """
        获得各种资产根目录
        :type obj: script.ProjectBrowserGUI.ProjectBrowserGUI
        """
        if obj.assFamily == 'character':
            path = obj.rootAss.joinpath('DuBuXiaoYao', 'MoXing', 'Character')
            obj.ta_log.info('获得文件夹%s', path)
        elif obj.assFamily == 'scane':
            path = obj.rootAss.joinpath('DuBuXiaoYao', 'MoXing', 'Scence')
            obj.ta_log.info('获得文件夹%s', path)
        elif obj.assFamily == 'props':
            path = obj.rootAss.joinpath('DuBuXiaoYao', 'MoXing', 'Prop')
            obj.ta_log.info('获得文件夹%s', path)
        elif obj.assFamily == 'effects':
            path = obj.rootAss.joinpath('DuBuXiaoYao', 'MoXing', 'TeXiao')
            obj.ta_log.info('获得文件夹%s', path)
        else:
            path = ''
            obj.ta_log.info('你干了什么? 这是一片荒漠(o_ _)ﾉ')
        return path

    @staticmethod
    def getAssFamilyItems(obj) -> list:
        """
        获得各种资产中的项数
        :type obj: script.ProjectBrowserGUI.ProjectBrowserGUI
        """
        item = []
        for path in obj.assFamilyPath.iterdir():
            if path.match('*ep_*'):
                for children_path in path.iterdir():
                    item.append(children_path.stem)
            else:
                item.append(path.stem)
        return item

    @staticmethod
    def getAssTypePath(obj) -> pathlib.Path:
        """
        获得资产的下一级类型资产所在目录
        :type obj: script.ProjectBrowserGUI.ProjectBrowserGUI
        """
        possible_path = list(obj.assFamilyPath.glob('{}'.format(obj.asslistSelect)))
        if possible_path:
            possible_path = possible_path[0]
        else:
            try:
                possible_path = list(obj.assFamilyPath.glob('*\\{}'.format(obj.asslistSelect)))[0]
            except:
                obj.ta_log.error('找不到资产的下一级类型资产文件夹路径?')
                possible_path = []

        possible_path = possible_path.joinpath('Scenefiles')
        obj.ta_log.info('获得资产类型所在文件夹 %s', possible_path)
        return possible_path

    @staticmethod
    def getAssTypeItems(obj) -> list:
        """
        获得资产的下一级类型资产
        :type obj: script.ProjectBrowserGUI.ProjectBrowserGUI
        """
        itmes: list = []
        ass_type_path = obj.assTypePath
        for path in ass_type_path.glob('*'):
            if path.is_dir():
                tmp = path.stem
                if tmp == 'tietu':
                    tmp = 'sourceimages'
                itmes.append(tmp)

        return itmes

    @staticmethod
    def getAssFilePath(obj) -> pathlib.Path:
        """这个用来获得资产类型所在路径
        :type obj: script.ProjectBrowserGUI.ProjectBrowserGUI
        """
        ass_type_selsct = obj.assTypeSelsct
        if ass_type_selsct == 'sourceimages':
            ass_type_selsct = 'tietu'
        ass_file_path = obj.assTypePath.joinpath(ass_type_selsct)
        return ass_file_path

    @staticmethod
    def getAssFileInfo(obj) -> dict:
        """这个用来组合文件名称
        :type obj: script.ProjectBrowserGUI.ProjectBrowserGUI
        """
        script.doodleLog.ta_log.info("开始解析文件名称")
        dep_type_iterdir = obj.assFilePath.iterdir()
        mitem = []
        if dep_type_iterdir:
            for mFile in dep_type_iterdir:
                if mFile.is_file():
                    mitem.append({'filename': mFile.stem, 'fileSuffixes': mFile.suffix})
                else:
                    script.doodleLog.ta_log.info("他是文件夹?")
        script.doodleLog.ta_log.info("分离文件名称和后缀: %s", mitem)
        # 迭代获得文件命中包含信息
        information: list = []
        if mitem:
            for file in mitem:
                tmp = file['filename'].split('_')
                try:
                    tmp = {'name': tmp[0],
                           'fileType': tmp[1],
                           'version': tmp[2],
                           'user': tmp[4],
                           'fileSuffixes': file['fileSuffixes']
                           }
                except IndexError:
                    script.doodleLog.ta_log.info("资产文件信息变得奇怪了....%s", tmp)
                except:
                    script.doodleLog.ta_log.info("(资产)这是什么鬼┏┛墓┗┓...(((m -__-)m....%s", tmp)
                    pass
                else:
                    information.append(tmp)
        script.doodleLog.ta_log.info("文件信息获取完成")
        return information

    @staticmethod
    def seekRigFile(obj):
        """这个用来寻找绑定文件
        :type obj: script.ProjectBrowserGUI.ProjectBrowserGUI
        """
