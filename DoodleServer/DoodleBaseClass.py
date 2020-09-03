import contextlib
import copy
import datetime
import json
import logging
import os
import pathlib
import re
import shutil
import tempfile
import threading
import subprocess
from abc import ABCMeta, abstractmethod

import ftputil
import typing
import uuid

from DoodleServer import DoodleSynXml as Syn
import DoodleServer.DoodleZNCHConvert as DoleConvert
import DoodleServer.DoodleCore as DoleCore
import DoodleServer.DoodleSet as DoleSet
import DoodleServer.DoodleOrm as DoleOrm
import DoodleServer.DoodlePlayer
import DoodleServer


def __None__():
    pass


class MultipleFlipBook(object):
    filepath: typing.List[pathlib.Path]
    shot: typing.List[int]

    def __init__(self):
        self.filepath = []
        self.episodes = []
        self.shot = []

    def addPath(self, filepath: pathlib.Path):
        self.filepath.append(filepath)

    def addShot(self, shot):
        self.shot.append(shot)


class DoodlefilePath(object):

    def __init__(self, local_path: pathlib.Path = None, server_path: pathlib.Path = None, file_name: str = None):
        self.local_path = local_path
        self.server_path = server_path
        self.file_name = file_name

    @property
    def local_path(self):
        if not hasattr(self, '_local_path'):
            self._local_path = pathlib.Path("")
        return self._local_path

    @local_path.setter
    def local_path(self, local_path):
        if not isinstance(local_path, pathlib.Path):
            local_path = pathlib.Path(local_path)
        if not re.match("^[A-Z]:/", local_path.as_posix()):
            raise ValueError("{}必须是本地路径".format(local_path.as_posix()))
        self._local_path = local_path

    @property
    def server_path(self):
        if not hasattr(self, '_server_path'):
            self._server_path = pathlib.Path("")
        return self._server_path

    @server_path.setter
    def server_path(self, server_path):
        if not isinstance(server_path, pathlib.Path):
            server_path = pathlib.Path(server_path)
        if not re.match("^/", server_path.as_posix()):
            raise ValueError("{}必须以'/'开头".format(server_path.as_posix()))
        self._server_path = server_path

    @property
    def file_name(self):
        if not hasattr(self, '_file_name'):
            self._file_name = pathlib.Path("")
        return self._file_name

    @file_name.setter
    def file_name(self, file_name):
        if re.findall("/", file_name):
            raise ValueError("{}必须是文件名称".format(file_name))
        self._file_name = file_name

    def __str__(self):
        return f"{self.server_path.as_posix()}/{self.file_name}"

    @property
    def loacl_file_str(self) -> str:
        return self.local_path.joinpath(self.file_name).as_posix()

    @property
    def server_file_str(self):
        return self.server_path.joinpath(self.file_name).as_posix()


class export(threading.Thread):
    @property
    def path(self) -> pathlib.Path:
        if not hasattr(self, '_path'):
            self._path = pathlib.Path('')
        return self._path

    @path.setter
    def path(self, path):
        if not isinstance(path, pathlib.Path):
            path = pathlib.Path(path)
        self._path = path

    def __init__(self, path: pathlib.Path, version, cache_path: pathlib.Path, shot_maya_export_cls):
        super().__init__()
        self._path = path
        self.version = version
        self.cache_path = cache_path
        self.cls = shot_maya_export_cls
        self.trange_path = shot_maya_export_cls.trange_path.parent

    def run(self) -> None:
        self.exportCam()
        self.cls.MY_upload(self.cache_path.joinpath("doodle_Export.json"), self.trange_path, self.cache_path)

    def exportCam(self):
        mayapy_path = '"C:\\Program Files\\Autodesk\\Maya2018\\bin\\mayapy.exe"'
        # mayapy_path = "C:\\Program Files\\Autodesk\\Maya2018\\bin\\mayapy.exe"

        sourefile = pathlib.Path("tools/mayaExport.py")
        tmp_path = pathlib.Path(tempfile.gettempdir()).joinpath('export.py')

        shutil.copy2(sourefile, tmp_path)

        logging.info("open %s", mayapy_path)
        self.cache_path.mkdir(parents=True, exist_ok=True)
        command = str(mayapy_path) + ''' ''' + tmp_path.as_posix() + \
                  f""" --path {self.path.parent.as_posix()} --name {self.path.stem} """ \
                  f"""--version {self.version} --suffix {self.path.suffix} """ \
                  f"""--exportpath {self.cache_path.as_posix()}"""
        logging.info(command)
        os.system(command)

        # os.system(str(mayapy_path) + ''' ''' + tmp_path.as_posix())


class ftpServer(object):
    _file_: typing.List[DoodlefilePath]

    def __init__(self,
                 user: str,
                 ip_: str,
                 password: str):
        self.user = user
        self.ftpip = ip_
        self.password = password
        self._file_ = []
        self.my_run = __None__

    def run(self):
        self.my_run()
        self.clear()

    def addFile(self, file: DoodlefilePath):
        self._file_.append(file)

    def _down(self):
        logging.info("开始下载 %s", self._file_)
        if not self._file_:
            return None
        with ftputil.FTPHost(self.ftpip, self.user, self.password) as host:
            for file in self._file_:
                # 如果没有存在目录就创建
                self._makeLoaclDir(file.local_path.as_posix())
                if host.path.isfile(file.server_file_str):
                    host.download_if_newer(file.server_file_str, file.loacl_file_str)

    def _upload(self):
        logging.info("开始上传 %s", self._file_)
        now__strftime = datetime.datetime.now().strftime("%y_%b_%d_%h_%M_%S")
        with ftputil.FTPHost(self.ftpip, self.user, self.password) as host:
            for file in self._file_:
                if not host.path.isdir(file.server_path.as_posix()):
                    host.makedirs(file.server_path.as_posix())
                if host.path.isfile(file.server_file_str):
                    tmp_floder = "{}/{}/{}".format(file.server_path.as_posix(), "backup", now__strftime)
                    if not host.path.isdir(tmp_floder):
                        host.makedirs(tmp_floder)
                    host.rename(file.server_file_str, "{}/{}/{}/{}".format(file.server_path.as_posix(),
                                                                           "backup", now__strftime,
                                                                           file.file_name))
                host.upload(file.loacl_file_str, file.server_file_str)

    def _makeLoaclDir(self, path):
        try:
            os.makedirs(path)
        except OSError:
            logging.info("目标已经存在")

    def setRun(self, synchronize: str = "down"):
        """

        Args:
            synchronize: down,upload,syn

        Returns:

        """
        if synchronize == "down":
            self.my_run = self._down
        elif synchronize == "upload":
            self.my_run = self._upload

    def clear(self):
        self._file_.clear()


class _fileclass(object, metaclass=ABCMeta):
    code: DoleCore.PrjCore
    doodle_set: DoleSet.Doodlesetting
    _soure_file = ""
    user: str = ""
    version_max = 0
    file_name = ""
    trange_path: pathlib.Path
    infor = ""
    doodle_file_class: typing.Type[DoleOrm.fileAttributeInfo]

    @property
    def soure_file(self):
        if not hasattr(self, '_soure_file'):
            self._soure_file = pathlib.Path('')
        return self._soure_file

    @soure_file.setter
    def soure_file(self, soure_file):
        if isinstance(soure_file, pathlib.Path):
            soure_file = soure_file
        else:
            soure_file = pathlib.Path(soure_file)
        self._soure_file = soure_file

    def __init__(self, code_shot: DoleCore.PrjCore, doodle_set: DoleSet.Doodlesetting):
        """
        使用doodle初始化
        Args:
            code_shot: DooDlePrjCode._shot
        """

        self.code = copy.copy(code_shot)
        self.doodle_set = doodle_set
        self.user = doodle_set.user
        self._creteThread()
        self._creteFtpServer()
        self.user__easy_to_en = DoleConvert.isChinese(self.doodle_set.user).easyToEn()
        self.doodle_file_class = DoleOrm.fileAttributeInfo

    def _creteThread(self):
        self.syn = Syn.FreeFileSync(doc=self.doodle_set.cache_path,
                                    file_name=uuid.uuid4().__str__().replace("-", ""),
                                    program=self.doodle_set.FreeFileSync,
                                    user=self.doodle_set.ftpuser,
                                    ip_=self.doodle_set.ftpip,
                                    password=self.doodle_set.password)
        self.syn.addExclude(["backup"])

    def _creteFtpServer(self):
        self.ftp = ftpServer(ip_=self.doodle_set.ftpip,
                             user=self.doodle_set.ftpuser,
                             password=self.doodle_set.password)

    def down(self, down_path: pathlib.Path = None):
        # 查询数据库获得文件路径
        path = self.code.quertById(self.doodle_file_class).file_path
        # path = self.code.convertPathToIp(self.code.queryFileName(query_id))
        # 获得下载路径或者输入路径
        if not down_path:
            down_path = self.pathAndCache(path.parent)
        # 添加文件下载路径
        file_tmp = DoodlefilePath(down_path, path.parent, path.name)

        self.ftp.addFile(file_tmp)
        self.ftp.setRun("down")
        # 开始线程
        self.ftp.run()

        return down_path.joinpath(path.name)

    @staticmethod
    def copyToCache(soure: pathlib.Path, trange: pathlib.Path):
        trange.parent.mkdir(parents=True, exist_ok=True)
        try:
            shutil.copy2(soure.as_posix(), trange.as_posix())
        except shutil.SameFileError:
            logging.info("目标已经在临时目录中")
        return trange

    def pathAndCache(self, trange: pathlib.Path) -> pathlib.Path:
        path = trange.as_posix()
        if path[:1] == "/":
            path = path[1:]
        else:
            path = path
        return self.doodle_set.cache_path.joinpath(path)

    def upload(self, soure_file: pathlib.Path):
        self.soure_file = soure_file
        # 获得目标路径
        trange_path = self.code.commPath()
        # 获得缓存路径
        cache_path = self.pathAndCache(trange_path)
        # 获得版本
        self.version_max = self.code.queryMaxVersion(self.doodle_file_class) + 1
        # 获得文件名称
        self.file_name = self.code.commName(version=self.version_max,
                                            user_=self.user__easy_to_en,
                                            suffix=self.soure_file.suffix)

        # 复制文件到缓存路径
        self.copyToCache(self.soure_file, cache_path.joinpath(self.file_name))

        # 添加上传路径
        self.ftp.addFile(DoodlefilePath(cache_path, trange_path, self.file_name))

        # 添加服务器路径
        self.trange_path = trange_path.joinpath(self.file_name)
        # 提交文件到数据库
        self.subInfo()
        # 开始提交线程
        self.ftp.setRun("upload")
        self.ftp.run()

    def subInfo(self):
        sub_class = self.doodle_file_class()  # type DoleOrm.fileAttributeInfo
        sub_class.user = self.user
        sub_class.file = self.file_name
        sub_class.version = self.version_max
        sub_class.file_path = self.trange_path
        sub_class.infor = self.infor
        sub_class = self._addConract_(sub_class)
        self.code.subClass(sub_class)

    @abstractmethod
    def _addConract_(self, sub_class: DoleOrm.fileAttributeInfo):
        return sub_class


class _AssFile(_fileclass):
    code: DoleCore.PrjAss

    def __init__(self, code_shot: DoleCore.PrjAss, doodle_set: DoleSet.Doodlesetting):
        """
        使用doodle初始化
        Args:
            code_shot: DooDlePrjCode._shot
        """

        super(_AssFile, self).__init__(code_shot, doodle_set)

    def appoint(self, soure_file):
        self.soure_file = soure_file
        # 获得版本
        self.version_max = self.code.queryMaxVersion(self.doodle_file_class) + 1
        # 获得文件名称
        self.file_name = self.soure_file.stem
        # 添加服务器路径
        self.trange_path = self.code.convertPathToIp(soure_file)
        # 开始提交
        self.subInfo()


class _Screenshot(_fileclass, metaclass=ABCMeta):

    @contextlib.contextmanager
    def upload(self, soure_file: pathlib.Path = None) -> typing.Iterator[pathlib.Path]:
        self.code.file_type = self._seekScreenshot_()
        trange_path = self.code.commPath("screenshot")
        # 截图直接保存到缓存路径当中
        cache_path = self.pathAndCache(trange_path)
        # 获得版本序列
        self.version_max = self.code.queryMaxVersion(self.doodle_file_class) + 1
        # 文件名称固定为
        self.file_name = self.code.commName(version=self.version_max, user_=self.user__easy_to_en, suffix=".jpg")
        if not cache_path.is_dir():
            cache_path.mkdir(parents=True, exist_ok=True)
        try:
            yield cache_path.joinpath(self.file_name)
        except IOError as err:
            logging.info("保存截图失败")
        else:
            if cache_path.joinpath(self.file_name).is_file():
                # 添加上传文件路径
                self.ftp.addFile(DoodlefilePath(cache_path, trange_path, self.file_name))
                # 更新核心信息后提交
                self.trange_path = trange_path.joinpath(self.file_name)
                self.subInfo()
                # 进行文件复制
                self.ftp.setRun("upload")
                self.ftp.run()
            else:
                logging.error("未发现截图")

    def down(self, down_path: pathlib.Path = None) -> typing.Union[pathlib.Path, None]:
        # 查询数据库获得文件路径
        self.code.file_type = self._seekScreenshot_()
        query_file = self.code.queryFile(self.doodle_file_class)
        if not query_file:
            return None
        else:
            self.code.query_id = query_file[0].id
            path = self.code.convertPathToIp(self.code.quertById(self.doodle_file_class).file_path)
        # if not down_path:
        #     return None
        # 获得下载路径
        down_path_ = self.pathAndCache(self.code.commPath("Screenshot"))
        if down_path_.joinpath(path.name).is_file():
            return down_path_.joinpath(path.name)
        # if not down_path:
        #     down_path_ = pathlib.Path("datas/icon.png")
        # 添加文件下载路径
        self.ftp.addFile(DoodlefilePath(down_path_, path.parent, path.name))

        self.ftp.setRun("down")
        # 开始线程
        self.ftp.run()

        return down_path_.joinpath(path.name)

    @abstractmethod
    def _seekScreenshot_(self):
        pass


class _FlipBook(_fileclass, metaclass=ABCMeta):

    def upload(self, soure_file: pathlib.Path):
        self.soure_file = soure_file
        # 将找到的拍屏类型付给核心中的File_type
        self.code.file_type = self._seekFlibBook_()
        # 获得目标路径
        trange_path = self.code.commPath("FlipBook")
        # 获得缓存路径
        cache_path = self.pathAndCache(trange_path)
        # 获得版本
        self.version_max = self.code.queryMaxVersion(self.doodle_file_class) + 1

        # 获得文件名称
        self.file_name = self.code.commName(version=self.version_max, user_=self.user__easy_to_en,
                                            suffix=".mp4", prefix="FB_")

        # 获得缓存目标
        # 为转换视频做准备
        self.caahe_path = cache_path
        self.converMP4(self.soure_file)
        # 添加上传信息
        self.ftp.addFile(DoodlefilePath(cache_path, trange_path, self.file_name))

        # 开始提交线程
        self.trange_path = trange_path.joinpath(self.file_name)
        self.subInfo()
        self.ftp.setRun("upload")
        self.ftp.run()

    def converMP4(self, file):
        if file:
            file = pathlib.Path(file)
            if file.suffix in ['.mov', '.avi', ".mp4"]:
                path = self.caahe_path.joinpath(self.file_name)
                if path.is_file():
                    os.remove(str(path))
                DoodleServer.DoodlePlayer.videoToMp4(video=file, mp4_path=path, watermark=f"{self.file_name}")
            elif file.suffix in [".exr", ".png", ".tga", "jpg"]:
                try:
                    path = self.caahe_path.joinpath(self.file_name)
                    if path.is_file():
                        os.remove(str(path))
                    DoodleServer.DoodlePlayer.imageToMp4(video_path=path, image_path=file,
                                                         watermark=f"{self.file_name}")
                except:
                    pass

    @abstractmethod
    def _seekFlibBook_(self):
        pass


# <editor-fold desc="Description">
class assUePrj(_AssFile):

    def down(self, down_path: pathlib.Path = None):
        # 查询数据库获得文件路径
        path = self.code.convertPathToIp(self.code.quertById(DoleOrm.fileAttributeInfo).file_path)
        # 获得下载路径或者输入路径
        if down_path:
            down_path_ = down_path.as_posix()  # type: str
        else:
            down_path = self.pathAndCache(self.code.commPath())
            down_path_ = down_path.as_posix()
        # 添加文件下载路径
        self.syn.addSynFile([{"Left": down_path_,
                              "Right": path.parent.as_posix()}])
        # 添加下载名称
        self.syn.addInclude([path.name, "Content\\*"])
        self.syn.addExclude(["*\\backup\\*"])
        self.syn.setVersioningFolder(path.parent.joinpath("backup").as_posix())
        # 设置下载属性
        self.syn.setSynchronize("dow")

        # 开始线程
        self.syn.start()
        return down_path

    def upload(self, soure_file: pathlib.Path):
        self.soure_file = soure_file
        # 获得目标路径
        self.trange_path = self.code.commPath()
        # 获得缓存路径
        cache_path = self.pathAndCache(self.trange_path)
        # 获得版本
        self.version_max = self.code.queryMaxVersion(self.doodle_file_class) + 1
        # 获得文件名称
        self.file_name = self.code.commName(version=self.version_max, user_=self.user__easy_to_en,
                                            suffix=self.soure_file.suffix)

        # 复制文件到缓存路径
        self.copyToCache(self.soure_file, cache_path.joinpath(self.file_name))
        # 添加上传路径
        self.syn.addSynFile([{"Left": cache_path.as_posix(), "Right": self.trange_path.as_posix()}])
        if cache_path != self.soure_file.parent:
            self.syn.addSynFile([{"Left": self.soure_file.parent.as_posix(), "Right": self.trange_path.as_posix()}])

        # 添加上传文件名称
        self.syn.addInclude([self.file_name, "Content\\*"])
        self.syn.addExclude(["*\\backup\\*"])
        self.syn.setVersioningFolder(self.trange_path.joinpath("backup").as_posix())

        # 将目标路径进行组合后提交数据库
        self.trange_path = self.trange_path.joinpath(self.file_name)
        self.subInfo()
        # 开始提交线程
        self.syn.start()

    def _addConract_(self, sub_class: DoleOrm.fileAttributeInfo):
        sub_class.infor = self.infor
        self.code.file_type.ass_class = self.code.ass_class
        self.code.file_type.file_class = self.code.file_class
        self.code.ass_class.file_class = self.code.file_class
        sub_class.file_type = self.code.file_type
        sub_class.file_class = self.code.file_class
        sub_class.ass_class = self.code.ass_class
        return sub_class


class assMapping(_AssFile):
    trange_path_list: typing.List[pathlib.Path]

    def down(self, down_path: pathlib.Path = None):
        path_list = self.code.quertById(self.doodle_file_class)
        if not down_path:
            down_path = self.pathAndCache(self.code.commPath())
        for path in path_list.file_path_list:
            self.ftp.addFile(DoodlefilePath(down_path,path.parent,path.name))
        self.ftp.setRun("down")
        self.ftp.run()

    def upload(self, soure_file: typing.List[pathlib.Path]):
        # 目标路径
        self.trange_path = self.code.commPath()
        # 缓存路径
        cache_path = self.pathAndCache(self.trange_path)
        self.version_max = self.code.queryMaxVersion() + 1

        for path in soure_file:
            # 复制到缓存路径
            self.copyToCache(path, cache_path.joinpath(path.name))
            self.ftp.addFile(DoodlefilePath(cache_path, self.trange_path, path.name))
        self.trange_path_list = [self.trange_path.joinpath(p.name) for p in soure_file]
        self.ftp.setRun("upload")
        self.ftp.run()
        self.subInfo()

    def appoint(self, soure_file: typing.List[pathlib.Path]):
        self.trange_path_list = [self.code.convertPathToIp(p) for p in soure_file]
        self.version_max = self.code.queryMaxVersion() + 1
        self.subInfo()

    def subInfo(self):
        sub_class = self.doodle_file_class()  # type DoleOrm.fileAttributeInfo
        sub_class.user = self.user
        sub_class.file = "doodle_mapping"
        sub_class.version = self.version_max
        sub_class.file_path_list = self.trange_path_list
        sub_class.fileSuffixes = ".png"
        sub_class.infor = self.infor
        sub_class = self._addConract_(sub_class)
        self.code.subClass(sub_class)

    def _addConract_(self, sub_class: DoleOrm.fileAttributeInfo):
        sub_class.infor = self.infor
        self.code.file_type.ass_class = self.code.ass_class
        self.code.file_type.file_class = self.code.file_class
        self.code.ass_class.file_class = self.code.file_class
        sub_class.file_type = self.code.file_type
        sub_class.file_class = self.code.file_class
        sub_class.ass_class = self.code.ass_class
        return sub_class


class assScreenshot(_Screenshot):
    code: DoleCore.PrjAss

    def _addConract_(self, sub_class: DoleOrm.fileAttributeInfo):
        tmp_type = self._seekScreenshot_()

        tmp_type.ass_class = self.code.ass_class
        tmp_type.file_class = self.code.file_class
        self.code.ass_class.file_class = self.code.file_class
        sub_class.file_class = self.code.file_class
        sub_class.ass_class = self.code.ass_class
        sub_class.file_type = tmp_type
        return sub_class

    def _seekScreenshot_(self):
        for tmp_type in self.code.ass_class.addfileType:
            if tmp_type.file_type == "screenshot":
                return tmp_type
        return DoleOrm.fileType(file_type="screenshot")


class assFBFile(_FlipBook):
    code: DoleCore.PrjAss

    def _addConract_(self, sub_class: DoleOrm.fileAttributeInfo):
        tmp_type = self._seekFlibBook_()

        # 添加各种联系
        tmp_type.ass_class = self.code.ass_class
        tmp_type.file_class = self.code.file_class
        self.code.ass_class.file_class = self.code.file_class
        sub_class.file_class = self.code.file_class
        sub_class.ass_class = self.code.ass_class
        sub_class.file_type = tmp_type
        return sub_class

    def _seekFlibBook_(self):
        for tmp_type in self.code.ass_class.addfileType:
            if re.findall("^FB_", tmp_type.file_type):
                return tmp_type
        return DoleOrm.fileType(file_type="FB_{}".format(self.code.ass_class.file_name))

    def down(self, down_path: pathlib.Path = None):
        self.code.file_type = self._seekFlibBook_()
        if self.code.file_type.addassFlipBook:
            self.code.query_file = self.code.file_type.addassFlipBook[0]
        return super(_FlipBook, self).down()


class assMayaFile(_AssFile):
    code: DoleCore.PrjAss

    def upload(self, soure_file: pathlib.Path):
        if soure_file.suffix not in [".ma", ".mb"]:
            raise ValueError("从传入非maya文件")
        else:
            super(assMayaFile, self).upload(soure_file)

    def _addConract_(self, sub_class: DoleOrm.fileAttributeInfo):
        self.code.file_type.ass_class = self.code.ass_class
        self.code.file_type.file_class = self.code.file_class
        self.code.ass_class.file_class = self.code.file_class
        sub_class.file_class = self.code.file_class
        sub_class.ass_class = self.code.ass_class
        sub_class.file_type = self.code.file_type
        return sub_class


class shotMayaFile(_fileclass):
    code: DoleCore.PrjShot

    def _addConract_(self, sub_class: DoleOrm.fileAttributeInfo):
        # shot类约束
        self.code.shot.episodes = self.code.episodes
        # class类约束
        self.code.file_class.episodes = self.code.episodes
        self.code.file_class.shot = self.code.shot
        # type约束
        self.code.file_type.episodes = self.code.episodes
        self.code.file_type.shot = self.code.shot
        self.code.file_type.file_class = self.code.file_class
        # 文件类型约束
        sub_class.episodes = self.code.episodes
        sub_class.shot = self.code.shot
        sub_class.file_class = self.code.file_class
        sub_class.file_type = self.code.file_type
        return sub_class


class shotFBFile(_FlipBook):
    code: DoleCore.PrjShot

    # @contextlib.contextmanager
    # def uploadMultiple(self, soure_file):
    #     self.soure_file = soure_file
    #     mutiple_book = MultipleFlipBook()
    #     my_test_re = re.compile("\d+")
    #     # assert isinstance(self.code, script.DooDlePrjCode.PrjShot)
    #     if self.soure_file.suffix in [".png", ".tga", ".jpg", ".exr"]:
    #         for folder in self.soure_file.parent.parent.iterdir():
    #             self.searchFolder()
    #
    # def searchFolder(self, folders: pathlib.Path, mutiple_book: MultipleFlipBook):
    #     sequence = []
    #     shot = -1
    #     for file in folders.iterdir():
    #         myinfo = list(map(int, filter(None, self.re_test.findall(file.name))))
    #         if (file.suffix in [".png", ".tga", ".jpg", ".exr"]) and myinfo:
    #             if shot < 0:
    #                 shot = myinfo[-2]
    #             else:
    #                 if shot != myinfo[-2]: return None
    #             sequence.append(myinfo[-1])
    #     if sequence:
    #         if (max(sequence) - min(sequence)) == (sequence.__len__() + 1):
    #             mutiple_book.addShot(shot=shot)
    #             mutiple_book.filepath = list(folders.iterdir())

    def down(self, down_path: pathlib.Path = None):
        self.code.file_type = self._seekFlibBook_()
        self.code.query_file = self.code.file_type.addshotFlipBook[0]
        return super(_FlipBook, self).down()

    def _seekFlibBook_(self):
        for tmp_type in self.code.file_class.addfileType:
            if re.findall("^FB_", tmp_type.file_type):
                return tmp_type
        return DoleOrm.fileType(file_type="FB_{}".format(self.code.file_class.file_class))

    def _addConract_(self, sub_class: DoleOrm.fileAttributeInfo):
        sub_class.infor = "这是拍屏"
        # shot类约束
        self.code.shot.episodes = self.code.episodes
        # class类约束
        self.code.file_class.episodes = self.code.episodes
        self.code.file_class.shot = self.code.shot
        # type约束
        self.code.file_type.episodes = self.code.episodes
        self.code.file_type.shot = self.code.shot
        self.code.file_type.file_class = self.code.file_class
        # 文件类型约束
        sub_class.episodes = self.code.episodes
        sub_class.shot = self.code.shot
        sub_class.file_class = self.code.file_class
        sub_class.file_type = self.code.file_type
        return sub_class


class shotFbEpisodesFile(shotFBFile):

    def upload(self, soure_file: pathlib.Path):
        self.soure_file = soure_file
        self.__checkAndSetAttr__()
        # 获得目标路径
        trange_path = self.code.commPath("FlipBook")
        # 获得缓存路径
        cache_path = self.pathAndCache(trange_path)
        # 获得版本
        self.version_max = self.code.queryMaxVersion(self.doodle_file_class) + 1

        # 获得文件名称
        self.file_name = self.code.commName(version=self.version_max, user_=self.user__easy_to_en,
                                            suffix=".mp4", prefix="FB_")

        # 获得缓存目标
        # 复制文件到缓存路径
        self.copyToCache(self.soure_file, cache_path.joinpath(self.file_name))
        # 为转换视频做准备
        self.caahe_path = cache_path
        # 添加上传信息
        self.ftp.clear()
        self.ftp.addFile(DoodlefilePath(cache_path, trange_path, self.file_name))

        # 开始提交线程
        self.trange_path = trange_path.joinpath(self.file_name)
        self.subInfo()
        self.ftp.setRun("upload")
        self.ftp.run()

    def down(self, down_path: pathlib.Path = None):
        self.__checkAndSetAttr__()
        self.code.query_file = self.code.file_type.addfileAttributeInfo[0]
        return super(_FlipBook, self).down()

    def makeEpisodesFlipBook(self) -> pathlib.Path:
        # 获得来源路径
        path = []
        for shot in self.code.episodes.addShot:
            for file_ in shot.addfileAttributeInfo:
                if re.findall("^FB_", file_.file_type.file_type):
                    path.append(file_.file_path)
                    break
        # _shot_ = [for shot in self.code.episodes.addShot if re.findall("^FB_",shot.ad)]
        # path = [fileType.addfileAttributeInfo[0].file_path for fileType in self.code.episodes.addFileType if re.findall("^FB_",fileType.file_type)]
        # 设置各种属性
        self.__checkAndSetAttr__()
        # 获得整集拍屏的服务器路径
        eps_ftp_filepath: pathlib.Path = self.code.commPath()
        # 获得缓存路径
        cache_file = self.pathAndCache(eps_ftp_filepath).joinpath(
            self.code.commName(user_=self.user__easy_to_en, suffix=".mp4")
        )
        path_ = []

        cache_file.parent.mkdir(parents=True, exist_ok=True)
        if cache_file.is_file():
            os.remove(cache_file)

        for fb_path in path:
            path_.append(self.pathAndCache(eps_ftp_filepath).joinpath(fb_path.name))
            self.ftp.addFile(DoodlefilePath(self.pathAndCache(eps_ftp_filepath), fb_path.parent, fb_path.name))
        self.ftp.setRun("down")
        self.ftp.run()
        self.ftp.clear()

        DoodleServer.DoodlePlayer.comMp4(video_path=cache_file, paths=path_)

        self.upload(cache_file)

        return cache_file

    def __checkAndSetAttr__(self):
        self.code.shot = None
        self.code.file_class = self._seekFileClass_()
        self.code.file_type = self._seekFlibBook_()

    def _seekFileClass_(self):
        for tmp_class in self.code.queryFileClass():
            if tmp_class.file_class == self.doodle_set.department:
                return tmp_class
        return DoleOrm.fileClass(file_class=self.doodle_set.department)

    def _seekFlibBook_(self):
        for tmp_type in self.code.file_class.addfileType:
            if re.findall("^FB_", tmp_type.file_type):
                return tmp_type
        return DoleOrm.fileType(file_type="FB_{}".format(self.code.file_class.file_class))

    def _addConract_(self, sub_class: DoleOrm.fileAttributeInfo):
        sub_class.infor = self.infor
        # class类约束
        self.code.file_class.episodes = self.code.episodes
        # type约束
        self.code.file_type.episodes = self.code.episodes
        self.code.file_type.file_class = self.code.file_class
        # 文件类型约束
        sub_class.episodes = self.code.episodes
        sub_class.file_class = self.code.file_class
        sub_class.file_type = self.code.file_type
        return sub_class


# </editor-fold>


class shotMayaExportFile(_fileclass):
    code: DoleCore.PrjShot

    def down(self, down_path: pathlib.Path = None):
        """
        需要下载
        Args:
            query_id:
            down_path:

        Returns:

        """
        file_data = self.code.quertById(self.doodle_file_class)
        path = self.code.convertPathToIp(file_data.file_path)
        cache = self.pathAndCache(path)
        self.ftp.addFile(DoodlefilePath(cache.parent, path.parent, cache.name))

        self.ftp.setRun("down")
        self.ftp.run()

        down_name: list = []
        if cache.is_file():
            json_text = cache.read_text(encoding="utf-8")
            filedow: dict = json.loads(json_text)
            for key, value in filedow.items():
                # value: typing.List[str]
                split_name = value[0].split("/")[-1]
                # down_name.append(split_name)
                filedow[key] = cache.parent.joinpath(split_name).as_posix()
                self.ftp.addFile(DoodlefilePath(cache.parent, path.parent, split_name))

        self.ftp.setRun("down")
        self.ftp.run()
        return cache

    def upload(self, soure_file: pathlib.Path = None):

        self.ftp.addFile(DoodlefilePath(self.cache_path, self.trange_path.parent, self.file_name))
        soure_file = self.cache_path.joinpath(self.file_name)
        if soure_file.is_file():
            maya_export_info: dict = json.loads(soure_file.read_text(encoding="utf-8"))
            # 添加上传文件名称
            for key, value in maya_export_info.items():
                path_value__name = pathlib.Path(value[0]).name
                self.ftp.addFile(DoodlefilePath(self.cache_path, self.trange_path.parent, path_value__name))
                maya_export_info[key] = [self.trange_path.parent.joinpath(path_value__name).as_posix(), value[1]]
            # 将json重新写入
            soure_file.write_text(json.dumps(maya_export_info, ensure_ascii=False, indent=4, separators=(',', ':')))
            # 开始提交线程
            self.ftp.setRun("upload")
            self.ftp.run()

    def subDataToBD(self):
        self.soure_file = super(shotMayaExportFile, self).down()
        # 调整查询类型

        # 获得目标路径
        trange_path = self.code.commPath()
        # 获得缓存路径
        self.cache_path = self.pathAndCache(trange_path)
        # 获得版本
        self.version_max = self._seekFileType_().addfileAttributeInfo.__len__() + 1
        # 获得文件名称
        self.file_name = "doodle_Export.json"
        # 更新目标路径,进行提交
        self.trange_path = trange_path.joinpath(self.file_name)
        self.subInfo()

    def _addConract_(self, sub_class: DoleOrm.fileAttributeInfo):
        sub_class.infor = self.infor
        # shot类约束
        self.code.shot.episodes = self.code.episodes
        # class类约束
        self.code.file_class.episodes = self.code.episodes
        self.code.file_class.shot = self.code.shot
        # type约束
        file_type = self._seekFileType_()
        file_type.episodes = self.code.episodes
        file_type.shot = self.code.shot
        file_type.file_class = self.code.file_class
        # 文件类型约束
        sub_class.episodes = self.code.episodes
        sub_class.shot = self.code.shot
        sub_class.file_class = self.code.file_class
        sub_class.file_type = file_type
        return sub_class

    def _seekFileType_(self):
        for tmp_type in self.code.file_class.addfileType:
            if re.findall("export", tmp_type.file_type):
                return tmp_type
        return DoleOrm.fileType(file_type="export")

    def export(self):
        self.subDataToBD()
        threading.Thread(target=self.run).start()

    def run(self) -> None:
        self._exportCam_()
        self.upload()
        # self.exportRun()

    def _exportCam_(self):
        mayapy_path = '"C:\\Program Files\\Autodesk\\Maya2018\\bin\\mayapy.exe"'
        # mayapy_path = "C:\\Program Files\\Autodesk\\Maya2018\\bin\\mayapy.exe"
        sourefile = DoodleServer.GETDOODLEROOT(pathlib.Path(".").absolute()).joinpath("tools", "mayaExport.py")
        tmp_path = pathlib.Path(tempfile.gettempdir()).joinpath('export.py')

        shutil.copy2(sourefile, tmp_path)

        logging.info("open %s", mayapy_path)
        self.cache_path.mkdir(parents=True, exist_ok=True)
        command = str(mayapy_path) + ''' ''' + tmp_path.as_posix() + \
                  f""" --path {self.soure_file.parent.as_posix()} --name {self.soure_file.stem} """ \
                  f"""--version {self.version_max} --suffix {self.soure_file.suffix} """ \
                  f"""--exportpath {self.cache_path.as_posix()}"""
        logging.info(command)
        os.system(command)


class shotMayaClothExportFile(_fileclass):
    code: DoleCore.PrjShot

    def upload(self, soure_file: typing.List[pathlib.Path]):
        self.code.file_class = self._seekFileClass_()
        self.code.file_type = self._seekFileType_()
        self.soure_file = soure_file[-1]
        self.file_name = soure_file[-1].name
        trange_path = self.code.commPath("export_clothToFbx")
        # 获得版本
        self.version_max = self.code.queryMaxVersion(self.doodle_file_class) + 1
        # 添加多个文件路径
        for path in soure_file:
            self.ftp.addFile(DoodlefilePath(path.parent, trange_path, path.name))

        # 添加服务器路径
        self.trange_path = trange_path.joinpath(self.file_name)
        # 提交文件到数据库
        self.subInfo()
        # 开始提交线程
        self.ftp.setRun("upload")
        self.ftp.run()

    def down(self, down_path: pathlib.Path = None):
        # 获得服务器路径
        path = self.code.quertById(self.doodle_file_class).file_path
        # 添加下载路径
        down_path = self.pathAndCache(path.parent)
        # 添加文件
        file_tmp = DoodlefilePath(down_path, path.parent, path.name)

        self.ftp.addFile(file_tmp)
        self.ftp.setRun("down")
        # 开始线程
        self.ftp.run()

        # 开始其他文件的下载和读取
        data_str = down_path.joinpath(path.name).read_text(encoding="utf-8")
        data = json.loads(data_str)
        for d_ in data:
            Ifbx_path = pathlib.Path(d_["Ifbx_filepath"])
            Iabc_path = pathlib.Path(d_["Iabc_filepath"])
            self.ftp.addFile(DoodlefilePath(down_path, path.parent, Ifbx_path.name))
            self.ftp.addFile(DoodlefilePath(down_path, path.parent, Iabc_path.name))
        self.ftp.setRun("down")
        # 开始线程
        self.ftp.run()

        for d_ in data:
            self.convertCloth(d_["Command"])
        try:
            os.startfile(str(down_path))
        except:
            logging.info("无法打开文件位置")
        return down_path

    @staticmethod
    def convertCloth(comm: list):
        dem_bones = DoodleServer.GETDOODLEROOT(pathlib.Path(".").absolute()).joinpath("tools", "dem_bones")
        comm[0] = str(dem_bones) + comm[0]
        subprocess.Popen(comm[:1] + list(map(lambda x, y: "=".join([str(x), str(y)]), comm[1::2], comm[2::2])),
                         start_new_session=True)

    def _addConract_(self, sub_class: DoleOrm.fileAttributeInfo):
        # shot类约束
        self.code.shot.episodes = self.code.episodes
        # class类约束
        tmp_class = self._seekFileClass_()
        tmp_class.episodes = self.code.episodes
        tmp_class.shot = self.code.shot
        # type约束
        tmp_type = self._seekFileType_()
        tmp_type.episodes = self.code.episodes
        tmp_type.shot = self.code.shot
        tmp_type.file_class = tmp_class
        # 文件类型约束
        sub_class.episodes = self.code.episodes
        sub_class.shot = self.code.shot
        sub_class.file_class = tmp_class
        sub_class.file_type = tmp_type
        return sub_class

    def _seekFileType_(self):
        for tmp_type in self.code.file_class.addfileType:
            if re.findall("^export_cloth", tmp_type.file_type):
                return tmp_type
        return DoleOrm.fileType(file_type="export_cloth_fbx")

    def _seekFileClass_(self):
        for tmp_class in self.code.shot.addfileClass:
            if tmp_class.file_class == self.doodle_set.department:
                return tmp_class
        return DoleOrm.fileClass(file_class=self.doodle_set.department)


class shotScreenshot(_Screenshot):
    code: DoleCore.PrjShot

    def _addConract_(self, sub_class: DoleOrm.fileAttributeInfo):
        tmp_type = self._seekScreenshot_()
        # shot类约束
        self.code.shot.episodes = self.code.episodes
        # class类约束
        self.code.file_class.episodes = self.code.episodes
        self.code.file_class.shot = self.code.shot
        # type约束
        tmp_type.episodes = self.code.episodes
        tmp_type.shot = self.code.shot
        tmp_type.file_class = self.code.file_class
        # 文件类型约束
        sub_class.episodes = self.code.episodes
        sub_class.shot = self.code.shot
        sub_class.file_class = self.code.file_class
        sub_class.file_type = tmp_type
        return sub_class

    def _seekScreenshot_(self):
        if not self.code.file_class:
            self.code.file_class = self._seekFileClass_()
        for tmp_type in self.code.file_class.addfileType:
            if tmp_type.file_type == "screenshot":
                return tmp_type
        return DoleOrm.fileType(file_type="screenshot")

    def _seekFileClass_(self):
        for tmp_class in self.code.shot.addfileClass:
            if tmp_class.file_class == self.doodle_set.department:
                return tmp_class
        return DoleOrm.fileClass(file_class=self.doodle_set.department)


def doodleFileFactory(core, suffix):
    cls = None
    if isinstance(core, DoodleServer.DoodleCore.PrjShot):
        if suffix in [".mb", ".ma"]:
            cls = shotMayaFile
        elif suffix in [".mp4"]:
            cls = shotFBFile
        elif suffix in ["FB"]:
            cls = shotFBFile
        elif suffix in ["Screenshot"]:
            cls = shotScreenshot
    elif isinstance(core, DoodleServer.DoodleCore.PrjAss):
        if suffix in [".uproject"]:
            cls = assUePrj
        elif suffix in [".mb", ".ma"]:
            cls = assMayaFile
        elif suffix in ['.png', '.tga', '.jpg']:
            cls = assMapping
        elif suffix in ["FB"]:
            cls = assFBFile
        elif suffix in ["Screenshot"]:
            cls = assScreenshot
    else:
        cls = None
    return cls


if __name__ == '__main__':
    pass
