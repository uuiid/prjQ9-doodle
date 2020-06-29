import abc
import contextlib
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

import ftputil
import typing
import script.DooDlePrjCode
import script.doodle_setting
import script.doodlePlayer
import uuid

from DoodleServer import DoodleSynXml as Syn
import script.convert


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

    def __init__(self, local_path: pathlib.Path = "", server_path: pathlib.Path = "", file_name: str = ""):
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
            self._path = ''
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

    def run(self):
        self.my_run()

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
        else:
            self.my_run = None

    def clear(self):
        self._file_.clear()


class _fileclass(object):
    code: script.DooDlePrjCode.PrjCode
    doodle_set: script.doodle_setting.Doodlesetting
    _soure_file = ""
    user = ""
    version_max = 0
    file_name = ""
    trange_path: pathlib.Path
    infor = ""

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

    def down(self, query_id: int, down_path: pathlib.Path = ""):
        # 查询数据库获得文件路径
        path = self.code.convertPathToIp(self.code.queryFileName(query_id))
        # 获得下载路径或者输入路径
        if down_path:
            down_path = down_path.as_posix()
        else:
            down_path = self.pathAndCache(path.parent).as_posix()
        # 添加文件下载路径
        file_tmp = DoodlefilePath(down_path, path.parent, path.name)

        self.ftp.addFile(file_tmp)
        self.ftp.setRun("down")
        # 开始线程
        self.ftp.run()

    @staticmethod
    def copyToCache(soure: pathlib.Path, trange: pathlib.Path):
        trange.parent.mkdir(parents=True, exist_ok=True)
        try:
            shutil.copy2(soure.as_posix(), trange.as_posix())
        except shutil.SameFileError:
            logging.info("目标已经在临时目录中")
        return trange

    def pathAndCache(self, trange: pathlib.Path):
        path = trange.as_posix()
        if path[:1] == "/":
            path = path[1:]
        else:
            path = path
        return self.doodle_set.cache_path.joinpath(path)

    def upload(self, soure_file):
        self.soure_file = soure_file
        # 获得目标路径
        trange_path = self.code.getFilePath()
        # 获得缓存路径
        cache_path = self.pathAndCache(trange_path)
        # 获得版本
        self.version_max = self.code.getMaxVersion() + 1
        # 获得文件名称
        self.file_name = self.code.getFileName(version=self.version_max, user_=self.user__easy_to_en,
                                               suffix=self.soure_file.suffix)

        # 复制文件到缓存路径
        self.copyToCache(self.soure_file, cache_path.joinpath(self.file_name))

        # 添加上传路径
        self.ftp.addFile(DoodlefilePath(cache_path, trange_path, self.file_name))

        # 添加服务器路径
        self.trange_path = trange_path.joinpath(self.file_name)
        # 提交文件到数据库
        self.subInfo()
        self.code.submitInfo()
        # 开始提交线程
        self.ftp.setRun("upload")
        self.ftp.run()

    def subInfo(self):
        self.code.file = self.file_name
        self.code.fileSuffixes = self.trange_path.suffix
        self.code.user = self.doodle_set.user
        self.code.version = self.version_max
        self.code.filepath = self.trange_path.as_posix()
        self.code.infor = self.infor


class _ShotFile(_fileclass):

    def __init__(self, code_shot: script.DooDlePrjCode.PrjShot, doodle_set: script.doodle_setting.Doodlesetting):
        """
        使用doodle初始化
        Args:
            code_shot: DooDlePrjCode._shot
        """
        self.code = code_shot
        self.doodle_set = doodle_set
        self.user = doodle_set.user
        self._creteThread()
        self._creteFtpServer()
        self.user__easy_to_en = script.convert.isChinese(self.doodle_set.user).easyToEn()


class _AssFile(_fileclass):
    def __init__(self, code_shot: script.DooDlePrjCode.PrjAss, doodle_set: script.doodle_setting.Doodlesetting):
        """
        使用doodle初始化
        Args:
            code_shot: DooDlePrjCode._shot
        """
        self.code = code_shot
        self.doodle_set = doodle_set
        self._creteThread()
        self._creteFtpServer()
        self.user__easy_to_en = script.convert.isChinese(self.doodle_set.user).easyToEn()

    def appoint(self, soure_file):
        self.soure_file = soure_file
        # 获得版本
        self.version_max = self.code.getMaxVersion() + 1
        # 获得文件名称
        self.file_name = self.soure_file.stem
        # 添加服务器路径
        self.trange_path = self.code.convertPathToIp(soure_file)
        # 开始提交
        self.subInfo()
        # 提交文件到数据库
        self.code.submitInfo()


class _Screenshot(_fileclass):

    @contextlib.contextmanager
    def upload(self, soure_file="") -> pathlib.Path:
        self.trange_path = self.code.getScreenshot()
        # 截图直接保存到缓存路径当中
        cache_path = self.pathAndCache(self.trange_path)
        # 版本固定为0
        self.version_max = self.code.getMaxVersion() + 1
        # 文件名称固定为
        self.file_name = cache_path.name
        if not cache_path.parent.is_dir():
            cache_path.parent.mkdir(parents=True, exist_ok=True)
        try:
            yield cache_path
        except BaseException:
            logging.info("保存截图失败")
        else:
            if cache_path.is_file():
                # 添加上传文件路径
                self.ftp.addFile(DoodlefilePath(cache_path.parent, self.trange_path.parent, self.file_name))
                # 更新核心信息后提交
                self.subInfo()
                self.code.submitInfo()
                # 进行文件复制
                self.ftp.setRun("upload")
                self.ftp.run()

    def down(self, query_id: int = 0, down_path: pathlib.Path = ""):
        # 查询数据库获得文件路径
        path = self.code.convertPathToIp(self.code.getScreenshotPath())
        if path == pathlib.Path(""):
            return None
        # 获得下载路径
        down_path_ = self.pathAndCache(self.code.getScreenshot())
        if down_path_ == pathlib.Path(""):
            return pathlib.Path("datas/icon.png")
        else:
            down_path = down_path_.parent.as_posix()
        # 添加文件下载路径
        self.ftp.addFile(DoodlefilePath(down_path, path.parent, path.name))

        self.ftp.setRun("down")
        # 开始线程
        self.ftp.run()

        return down_path_


class _FlipBook(_fileclass):
    def __init__(self, code_shot: script.DooDlePrjCode.PrjCode, doodle_set: script.doodle_setting.Doodlesetting):
        """
        使用doodle初始化
        Args:
            code_shot: DooDlePrjCode._shot
        """
        self.code = code_shot
        self.doodle_set = doodle_set
        self._creteThread()
        self._creteFtpServer()
        self.user__easy_to_en = script.convert.isChinese(self.doodle_set.user).easyToEn()

    def upload(self, soure_file):
        self.soure_file = soure_file

        # 获得目标路径
        trange_path = self.code.getFilePath("FlipBook")
        # 获得缓存路径
        cache_path = self.pathAndCache(trange_path)
        # 获得版本
        self.version_max = self.code.getMaxVersion() + 1

        if re.match("^FB_.*", self.code.Type):
            prefix_ = ''
        else:
            prefix_ = "FB_"
            self.code.Type = f"FB_{self.code.Type}"

        # 获得文件名称
        self.file_name = self.code.getFileName(version=self.version_max, user_=self.user__easy_to_en,
                                               suffix=".mp4", prefix=prefix_)

        # 获得缓存目标
        # 为转换视频做准备
        self.caahe_path = cache_path
        self.converMP4(self.soure_file)
        # 添加上传信息
        self.ftp.addFile(DoodlefilePath(cache_path, trange_path, self.file_name))

        # 开始提交线程
        self.trange_path = trange_path.joinpath(self.file_name)
        self.subInfo()
        self.code.submitInfo()
        self.ftp.setRun("upload")
        self.ftp.run()

    def converMP4(self, file):
        if file:
            file = pathlib.Path(file)
            if file.suffix in ['.mov', '.avi', ".mp4"]:
                path = self.caahe_path.joinpath(self.file_name)
                if path.is_file():
                    os.remove(str(path))
                script.doodlePlayer.videoToMp4(video=file, mp4_path=path, watermark=f"{self.file_name}")
            elif file.suffix in [".exr", ".png", ".tga", "jpg"]:
                try:
                    path = self.caahe_path.joinpath(self.file_name)
                    if path.is_file():
                        os.remove(str(path))
                    script.doodlePlayer.imageToMp4(video_path=path, image_path=file, watermark=f"{self.file_name}")
                except:
                    pass

    def downPlayer(self, query_type):
        my_ass_type = "FB_" + re.split("FB_", self.code.Type)[-1]
        fb_id = self.code.queryFlipBook(my_ass_type)
        # 获得目标路径
        trange_path = self.code.getFilePath("FlipBook")
        # 获得缓存路径
        cache_path = self.pathAndCache(trange_path)
        self.down(fb_id, cache_path)
        return cache_path


# <editor-fold desc="Description">
class assUePrj(_AssFile):

    def down(self, query_id: int, down_path: pathlib.Path = ""):
        # 查询数据库获得文件路径
        path = self.code.convertPathToIp(self.code.queryFileName(query_id))
        # 获得下载路径或者输入路径
        if down_path:
            down_path = down_path.as_posix()
        else:
            down_path = self.pathAndCache(path.parent).as_posix()
        # 添加文件下载路径
        self.syn.addSynFile([{"Left": down_path,
                              "Right": path.parent.as_posix()}])
        # 添加下载名称
        self.syn.addInclude([path.name, "Content\\*"])
        # 设置下载属性
        self.syn.setSynchronize("dow")

        # 开始线程
        self.syn.start()

    def upload(self, soure_file):
        self.soure_file = soure_file
        # 获得目标路径
        self.trange_path = self.code.getFilePath()
        # 获得缓存路径
        cache_path = self.pathAndCache(self.trange_path)
        # 获得版本
        self.version_max = self.code.getMaxVersion() + 1
        # 获得文件名称
        self.file_name = self.code.getFileName(version=self.version_max, user_=self.user__easy_to_en,
                                               suffix=self.soure_file.suffix)

        # 复制文件到缓存路径
        self.copyToCache(self.soure_file, cache_path.joinpath(self.file_name))
        # 添加上传路径
        self.syn.addSynFile([{"Left": cache_path.as_posix(), "Right": self.trange_path.as_posix()}])
        self.syn.addSynFile([{"Left": self.soure_file.parent.as_posix(), "Right": self.trange_path.as_posix()}])

        # 添加上传文件名称
        self.syn.addInclude([self.file_name, "Content\\*"])

        # 将目标路径进行组合后提交数据库
        self.trange_path = self.trange_path.joinpath(self.file_name)
        self.subInfo()
        # 提交文件到数据库
        self.code.submitInfo()
        # 开始提交线程
        self.syn.start()

    def subInfo(self):
        self.code.file = self.file_name
        self.code.fileSuffixes = self.soure_file.suffix
        self.code.user = self.doodle_set.user
        self.code.version = self.version_max
        self.code.filepath = self.trange_path.as_posix()
        self.code.infor = self.infor


class assMapping(_AssFile):
    pass


class assScreenshot(_Screenshot):
    def __init__(self, code_shot: script.DooDlePrjCode.PrjAss, doodle_set: script.doodle_setting.Doodlesetting):
        """
        使用doodle初始化
        Args:
            code_shot: DooDlePrjCode._shot
        """
        self.code = code_shot
        self.doodle_set = doodle_set
        self._creteThread()
        self._creteFtpServer()


class assFBFile(_FlipBook):
    pass


class assMayaFile(_AssFile):
    pass


class shotMayaFile(_ShotFile):
    pass


class shotMayaFBFile(_FlipBook):
    code: script.DooDlePrjCode.PrjShot

    def __init__(self, code_shot: script.DooDlePrjCode.PrjShot, doodle_set: script.doodle_setting.Doodlesetting):
        """
        使用doodle初始化
        Args:
            code_shot: DooDlePrjCode._shot
        """
        self.code = code_shot
        self.doodle_set = doodle_set
        self.user = doodle_set.user
        self._creteThread()
        self._creteFtpServer()
        self.re_test = re.compile("\\d+")

    def downFlipBook(self, query_path: pathlib.Path):
        """
        下载flipbook
        Args:
            query_path: 查询路径(带文件名称)

        Returns:

        """
        # 查询数据库获得文件路径
        path = self.code.convertPathToIp(query_path)
        # 获得下载路径
        down_path = self.pathAndCache(path.parent).as_posix()
        # 添加文件下载路径
        self.ftp.addFile(DoodlefilePath(down_path, path.parent, path.name))
        # 设置下载属性
        self.ftp.setRun()

        # 开始线程
        self.ftp.run()

    def getEpisodesFlipBook(self) -> pathlib.Path:
        """
        获得整集的拍屏
        Returns:

        """
        # 获得服务器路径
        ftp_path = self.code.getFlipBookEpsisodesPath()
        # 获得缓存路径
        cache_path = self.pathAndCache(ftp_path)
        # 查询拍屏路径
        flipbook_path = self.code.queryEpisodesFlipBook()

        self.ftp.clear()
        self.ftp.addFile(DoodlefilePath(cache_path.parent, flipbook_path.parent, cache_path.name))
        self.ftp.setRun()
        self.ftp.run()

        if cache_path.is_file():
            return cache_path
        else:
            pass

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

    def makeEpisodesFlipBook(self) -> pathlib.Path:
        shots_ = [(int(s[2:-1]), s[-1:]) if s[6:] else (int(s[2:]), "") for s in self.code.getShot()[:]]
        path = [self.code.convertPathToIp(self.code.queryFlipBookShot(*pp)) for pp in shots_]

        # 获得服务器路径
        ftp_path = self.code.getFlipBookEpsisodesPath()
        # 获得缓存路径
        cache_file = self.pathAndCache(ftp_path)
        path_ = []
        for fb_path in path:
            if not fb_path:
                continue
            path_.append(self.pathAndCache(ftp_path.parent).joinpath(fb_path.name))
            self.ftp.addFile(DoodlefilePath(self.pathAndCache(ftp_path.parent), fb_path.parent, fb_path.name))
        self.ftp.setRun("down")
        self.ftp.run()

        cache_file.parent.mkdir(parents=True, exist_ok=True)
        if cache_file.is_file():
            os.remove(cache_file.as_posix())
        script.doodlePlayer.comMp4(video_path=cache_file, paths=path_)

        self.subAndUploadFlipBook(cache_file, ftp_path)

        return cache_file

    def subAndUploadFlipBook(self, cache_file: pathlib.Path, trange_file: pathlib.Path):
        self.ftp.clear()
        self.ftp.addFile(DoodlefilePath(cache_file.parent, trange_file.parent, cache_file.name))
        self.ftp.setRun("upload")
        self.ftp.run()
        self.code.filepath = trange_file.as_posix()
        self.code.version = 0
        self.code.subEpisodesFlipBook()


# </editor-fold>


class shotMayaExportFile(_ShotFile):

    def down(self, query_id: int, down_path: pathlib.Path = ""):
        """
        需要下载
        Args:
            query_id:
            down_path:

        Returns:

        """
        path = self.code.queryFileName(query_id)
        path = self.code.convertPathToIp(path)
        cache = self.pathAndCache(path)
        self.ftp.addFile(DoodlefilePath(cache.parent, path.parent, cache.name))

        self.ftp.setRun("down")
        self.ftp.run()

        down_name: list = []
        if cache.is_file():
            json_text = cache.read_text(encoding="utf-8")
            filedow: dict = json.loads(json_text)
            for key, value in filedow.items():
                value: typing.List[str]
                split_name = value[0].split("/")[0]
                down_name.append(split_name)
                filedow[key] = cache.parent.joinpath(split_name)

        self.ftp.addFile(DoodlefilePath(cache.parent, path.parent, down_name))

        self.ftp.setRun("down")
        self.ftp.run()
        pass

    def MY_upload(self, soure_file: pathlib.Path, trange_path: pathlib.Path, cache_path: pathlib.Path):
        # trange_path = self.code.getFilePath()
        # # 获得缓存路径
        # cache_path = self.pathAndCache(trange_path)

        self.ftp.addFile(DoodlefilePath(cache_path, trange_path, self.file_name))
        if soure_file.is_file():
            maya_export_info: dict = json.loads(soure_file.read_text(encoding="utf-8"))
            # 添加上传文件名称
            for key, value in maya_export_info.items():
                path_value__name = pathlib.Path(value[0]).name
                self.ftp.addFile(DoodlefilePath(cache_path, trange_path, path_value__name))
                maya_export_info[key] = [trange_path.joinpath(path_value__name).as_posix(), value[1]]
            # 将json重新写入
            soure_file.write_text(json.dumps(maya_export_info, ensure_ascii=False, indent=4, separators=(',', ':')))
            # 开始提交线程
            self.ftp.setRun("upload")
            self.ftp.run()

    def exportRun(self, soure_file: pathlib.Path):
        self.soure_file = soure_file
        # 获得目标路径
        trange_path = self.code.getFilePath()
        # 获得缓存路径
        cache_path = self.pathAndCache(trange_path)
        # 获得版本
        self.version_max = self.code.getMaxVersion()
        # 获得文件名称
        self.file_name = "doodle_Export.json"
        # 更新目标路径,进行提交
        self.trange_path = trange_path.joinpath(self.file_name)
        # 更新核心信息
        self.subInfo()
        # 提交文件到数据库
        self.code.submitInfo()
        export(soure_file, self.code.version, cache_path, self).start()

    def subInfo(self):
        super().subInfo()
        self.code.Type = "export"


class shotMayaClothExportFile(_ShotFile):

    def upload(self, soure_file: typing.List[pathlib.Path]):
        self.soure_file = soure_file[-1]
        self.file_name = soure_file[-1].name
        trange_path = self.code.getFilePath("export_clothToFbx")
        # 获得版本
        self.version_max = self.code.getMaxVersion() + 1
        # 添加多个文件路径
        for path in soure_file:
            self.ftp.addFile(DoodlefilePath(path.parent, trange_path, path.name))

        # 添加服务器路径
        self.trange_path = trange_path.joinpath(self.file_name)
        # 提交文件到数据库
        self.subInfo()
        self.code.submitInfo()
        # 开始提交线程
        self.ftp.setRun("upload")
        self.ftp.run()

    def down(self, query_id: int, down_path: pathlib.Path = ""):
        # 获得服务器路径
        path = self.code.convertPathToIp(self.code.queryFileName(query_id))
        # 添加下载路径
        down_path = self.pathAndCache(path.parent)
        # 添加文件
        file_tmp = DoodlefilePath(down_path.as_posix(), path.parent, path.name)

        self.ftp.addFile(file_tmp)
        self.ftp.setRun("down")
        # 开始线程
        self.ftp.run()

        # 开始其他文件的下载和读取
        self.ftp.clear()
        data = down_path.joinpath(path.name).read_text(encoding="utf-8")
        data = json.loads(data)
        for d_ in data:
            Ifbx_path = pathlib.Path(d_["Ifbx_filepath"])
            Iabc_path = pathlib.Path(d_["Iabc_filepath"])
            self.ftp.addFile(DoodlefilePath(down_path.as_posix(), path.parent, Ifbx_path.name))
            self.ftp.addFile(DoodlefilePath(down_path.as_posix(), path.parent, Iabc_path.name))
        self.ftp.setRun("down")
        # 开始线程
        self.ftp.run()

        for d_ in data:
            self.convertCloth(d_["Command"])
        try:
            os.startfile(str(down_path))
        except:
            logging.info("无法打开文件位置")

    @staticmethod
    def convertCloth(comm: list):
        comm[0] = "tools\\dem_bones\\" + comm[0]
        subprocess.Popen(comm[:1] + list(map(lambda x, y: "=".join([str(x), str(y)]), comm[1::2], comm[2::2])),
                         start_new_session=True)
        # p = subprocess.Popen(comm[:1] + list(map(lambda x,y:"=".join([str(x),str(y)]), comm[1::2],comm[2::2])),
        #                      stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        # while True:
        #     i = p.stdout.readline()
        #     if i:
        #         logging.info(i)
        #     elif p.poll() is not None:
        #         break


class shotScreenshot(_Screenshot):
    def __init__(self, code_shot: script.DooDlePrjCode.PrjShot, doodle_set: script.doodle_setting.Doodlesetting):
        """
        使用doodle初始化
        Args:
            code_shot: DooDlePrjCode._shot
        """
        self.code = code_shot
        self.doodle_set = doodle_set
        self.user = doodle_set.user
        self._creteThread()
        self._creteFtpServer()


def doodleFileFactory(core, suffix):
    cls = None
    if isinstance(core, script.DooDlePrjCode.PrjShot):
        if suffix in [".mb", ".ma"]:
            cls = shotMayaFile
        elif suffix in [".mp4"]:
            cls = shotMayaFBFile
        elif suffix in ["FB"]:
            cls = shotMayaFBFile
        elif suffix in ["Screenshot"]:
            cls = shotScreenshot
    elif isinstance(core, script.DooDlePrjCode.PrjAss):
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
