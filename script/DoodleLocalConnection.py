import logging
import pathlib
import pickle
import threading
import traceback
import json
from multiprocessing import connection as Conn

import DoodleServer.DoodleDictToObject as DleDict
import DoodleServer.DoodleBaseClass as DleFile
import DoodleServer as Doodle


class DoodleServer(threading.Thread):
    server = None
    client: Conn.Connection

    def __init__(self, doodle_set):
        super().__init__()
        self.doodle_set = doodle_set
        """=============="""
        self.shot = Doodle.DoodleCore.PrjShot(self.doodle_set)
        self.ass = Doodle.DoodleCore.PrjAss(self.doodle_set)

    def run(self):
        self.server = Conn.Listener(("127.0.0.1", 23369), authkey=b"doodle")
        while True:
            try:
                self.client = self.server.accept()
                self.analysis()
            except Exception:
                logging.error(traceback.print_exc())

    def analysis(self):
        while True:
            try:
                recv_bytes = self.client.recv_bytes()
                if recv_bytes == b"close":
                    logging.info("客户端连接主动断开")
                    break
                data = pickle.loads(recv_bytes)
                data = DleDict.convertTool().convert(data)
                getattr(self, data.url)(data)
            except EOFError:
                logging.error(traceback.print_exc())
                self.client.close()
                break

    def send_To(self, data):
        self.client.send_bytes(pickle.dumps(data, protocol=2))

    def getDoodleSet(self, data):
        my_set = {"user": script.convert.isChinese(self.doodle_set.user).easyToEn(),
                  "department": self.doodle_set.department,
                  "projectname": self.doodle_set.projectname, "cache_path": self.doodle_set.cache_path.as_posix()}
        self.send_To(my_set)

    def getPath(self, data):
        core = getattr(self, data.core)
        self._setBaseCoreAttr(data, core)
        path: pathlib.Path = core.getFilePath(data.folder_type)
        self.send_To(path.as_posix())

    def subInfo(self, data):
        core = getattr(self, data.core)
        self._setBaseCoreAttr(data.info, core)
        assert isinstance(core, Doodle.DoodleCore.PrjShot)
        # 创建maya布料上传函数
        file = DleFile.shotMayaClothExportFile(core, self.doodle_set)
        # 转换需要上传路径
        data.info.filepath = [pathlib.Path(_path) for _path in data.info.filepath[:]]
        # 写出决策文件
        cloth_export = pathlib.Path(data.info.filepath[0]).parent.joinpath("Doodle_Cloth_export.json")
        cloth_export.write_text(json.dumps([dem.__dict__ for dem in data._data_],
                                           ensure_ascii=False, indent=4, separators=(',', ':')))
        # 将决策文件同时上传
        data.info.filepath.append(cloth_export)
        file.upload(data.info.filepath)

    def _setBaseCoreAttr(self, data, core):
        if isinstance(core, Doodle.DoodleCore.PrjAss):
            try:
                pass
            except KeyError:
                pass
        elif isinstance(core, Doodle.DoodleCore.PrjShot):
            try:
                core.episodes = data.episodes
                core.shot = data.shot
                core.shotab = data.shotab
                core.department = self.doodle_set.department
                core.Type = data.Type
            except KeyError:
                logging.error("传入字典无法解析 %s", traceback.print_exc())
