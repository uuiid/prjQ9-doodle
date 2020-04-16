# -*- coding: UTF-8 -*-
import pathlib
import shutil
import subprocess
from typing import Iterator, Dict

import script.doodleLog
import script.synXml


# import script.ProjectBrowserGUI

class ProjectAnalysisShot():
    # import script.ProjectBrowserGUI
    # pbg = typing.NewType('pbg',script.ProjectBrowserGUI.ProjectBrowserGUI)

    @staticmethod
    def getEpisodesItems(obj) -> list:
        """获得集数所在的文件夹
        :type obj: script.ProjectBrowserGUI.ProjectBrowserGUI
        """
        root = obj.root
        item = []
        for path in root.iterdir():
            if path.is_dir():
                item.append(path.stem)
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
        root = obj.root.joinpath(obj.file_episods)
        script.doodleLog.ta_log.info("获得镜头所在的文件夹")
        return pathlib.Path(root)

    @staticmethod
    def getShotItems(obj) -> Iterator[str]:
        """获得shot列表
        :type obj: script.ProjectBrowserGUI.ProjectBrowserGUI
        """
        script.doodleLog.ta_log.info("开始获得镜头所在的文件夹")
        episods = obj.file_episods
        paths = obj.file_shot_path

        mitem = []
        for path in paths.iterdir():
            try:
                mitem.append(path.stem)
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
        shotname = '{}\\sc{:0>4d}'.format(obj.file_episods, shot)
        root = obj.root
        if ab_shot:
            shotname = '{}{}'.format(shotname, ab_shot)
        shot = root.joinpath(shotname)

        for sub_directory in obj.setlocale.ProgramFolder:
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
            department = root.joinpath(epis, shot)
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


class ProjectAnalysisAssets():
    @staticmethod
    def getAssFamilyPath(obj) -> pathlib.Path:
        """
        获得各种资产根目录
        :type obj: script.ProjectBrowserGUI.ProjectBrowserGUI
        """
        if obj.assFamily == 'character':
            path = obj.rootAss.joinpath('Character')
            obj.ta_log.info('获得文件夹%s', path)
        elif obj.assFamily == 'scane':
            path = obj.rootAss.joinpath('Scence')
            obj.ta_log.info('获得文件夹%s', path)
        elif obj.assFamily == 'props':
            path = obj.rootAss.joinpath('Prop')
            obj.ta_log.info('获得文件夹%s', path)
        elif obj.assFamily == 'effects':
            path = obj.rootAss.joinpath('Effects')
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
            item.append(path.stem)
        return item

    @staticmethod
    def getAssTypePath(obj) -> pathlib.Path:
        """
        获得资产的下一级类型资产所在目录
        :type obj: script.ProjectBrowserGUI.ProjectBrowserGUI
        """
        possible_path = obj.assFamilyPath.joinpath(obj.asslistSelect, 'Scenefiles')
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
        folder: list[str] = obj.setlocale.assTypeFolder
        for path in ass_type_path.glob('*'):
            if path.is_dir():
                tmp = path.stem
                folder_tmp = folder.copy()
                folder_tmp[2] = folder_tmp[2].format(obj.asslistSelect)
                if tmp in folder_tmp:
                    itmes.append(tmp)
        return itmes

    @staticmethod
    def getAssFilePath(obj) -> pathlib.Path:
        """这个用来获得资产类型所在路径
        :type obj: script.ProjectBrowserGUI.ProjectBrowserGUI
        """
        ass_type_selsct = obj.assTypeSelsct
        ass_file_path = obj.assTypePath.joinpath(ass_type_selsct)
        return ass_file_path

    @staticmethod
    def getAssFileInfo(obj) -> dict:
        """这个用来组合文件名称
        :type obj: script.ProjectBrowserGUI.ProjectBrowserGUI
        """
        script.doodleLog.ta_log.info("开始解析文件名称")
        if not obj.assFilePath.joinpath('backup').is_dir():
            return []
        dep_type_iterdir = obj.assFilePath.joinpath('backup').iterdir()
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
                           'user': None,
                           'version': tmp[1],
                           'fileSuffixes': file['fileSuffixes']
                           }
                except IndexError:
                    script.doodleLog.ta_log.info("资产文件信息变得奇怪了....%s", tmp)
                except:
                    script.doodleLog.ta_log.info("(资产)这是什么鬼┏┛墓┗┓...(((m -__-)m....%s", tmp)
                    pass
                else:
                    information.append(tmp)
        version = len(information)
        for i in obj.assFilePath.iterdir():
            if i.suffix in ['.mb', '.ma', '.max','.fbx', '.uproject']:
                tmp = i.suffix
                information.append({'name': obj.asslistSelect,
                                    'user': None,
                                    'version': "v{:0>4d}".format(version + 1),
                                    'fileSuffixes': tmp})
        script.doodleLog.ta_log.info("文件信息获取完成")
        return information

    @staticmethod
    def getAssFolder(obj, ass_folder) -> list:
        """这个用来获得资产下一级路径,这级路径是程序文件夹
        :type obj: script.ProjectBrowserGUI.ProjectBrowserGUI
        """
        item_path = []
        family_path: pathlib.Path = obj.assFamilyPath
        family_path = family_path.joinpath(ass_folder)
        for it in obj.setlocale.ProgramFolder:
            item_path.append(family_path.joinpath(it))
        return item_path

    @staticmethod
    def assUploadFileHandle(obj, file_path: pathlib.Path):
        """这个用来获得资产下一级路径,这级路径是程序文件夹
        :type obj: script.ProjectBrowserGUI.ProjectBrowserGUI
        """
        backup = obj.assFilePath.joinpath('backup')
        target_file = obj.assFilePath.joinpath('{}{}'.format(obj.asslistSelect, file_path.suffix))
        version_max: int = 1
        if not backup.is_dir():
            backup.mkdir(parents=True, exist_ok=True)
        if target_file.is_file():
            backup_match = backup.glob('*{}*{}'.format(obj.asslistSelect, file_path.suffix))
            for i in backup_match:
                if i.stem.split('_'):
                    version = int(i.stem.split('_')[-1][1:])
                    if version > version_max:
                        version_max = version
        if file_path.suffix in ['.mb', '.ma', '.max']:
            version_max = version_max + 1
            backup_file = backup.joinpath('{}_v{:0>4d}{}'.format(obj.asslistSelect,
                                                                 version_max,
                                                                 file_path.suffix))
            shutil.move(str(target_file), backup_file)
            obj.ta_log.info('文件备份%s ---->  %s', target_file, backup_file)
        shutil.copy2(str(file_path), str(target_file))
        obj.ta_log.info('文件上传%s ---->  %s', file_path, target_file)

        if file_path.suffix in ['.fbx']:
            shutil.copy2(str(file_path), str(target_file))


    @staticmethod
    def assUploadFileUE4Handle(obj, file_path: pathlib.Path):
        """这个用来获得资产下一级路径,这级路径是程序文件夹
        :type obj: script.ProjectBrowserGUI.ProjectBrowserGUI
        """
        backup = obj.assFilePath.joinpath('backup')
        source = file_path.parent
        target = obj.assFilePath
        syn_path = [{'Left':str(source), 'Right':str(target)}]
        syn_file = script.synXml.weiteXml(obj.setlocale.doc,
                                          syn_path,
                                          Include=['*\\Content\\*','*.uproject'],
                                          Exclude=['*\\backup\\'],
                                          VersioningFolder=str(backup),
                                          fileName='UEpriect')
        program = obj.setlocale.FreeFileSync
        subprocess.run('{} "{}"'.format(program, syn_file), shell=True)
