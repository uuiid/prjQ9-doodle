import logging
import pathlib
import pickle
import threading
import traceback
from multiprocessing import connection as Conn

import script.DooDlePrjCode
import script.convert
import script.DoodleDictToObject as DleDict


class DoodleServer(threading.Thread):
    server = None
    client: Conn.Connection

    def __init__(self, doodle_set):
        super().__init__()
        self.doodle_set = doodle_set
        """=============="""
        self.shot = script.DooDlePrjCode.PrjShot(self.doodle_set.projectname,
                                                 self.doodle_set.project,
                                                 self.doodle_set.shotRoot)
        self.ass = script.DooDlePrjCode.PrjAss(self.doodle_set.projectname,
                                               self.doodle_set.project,
                                               self.doodle_set.assetsRoot)

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
                    self.client.close()
                    logging.info("客户端连接主动断开")
                    break
                data = pickle.loads(recv_bytes)
                data = DleDict.convertTool().convert(data)
                getattr(self, data.url)(data)
            except EOFError:
                logging.error(traceback.print_exc())
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
        if isinstance(core, script.DooDlePrjCode.PrjAss):
            try:
                pass
            except KeyError:
                pass
        elif isinstance(core, script.DooDlePrjCode.PrjShot):
            try:
                core.episodes = data.episodes
                core.shot = data.shot
                core.shotab = data.shotab
                core.department = self.doodle_set.department
                core.Type = data.Type
            except KeyError:
                logging.error("传入字典无法解析 %s", traceback.print_exc())
        path: pathlib.Path = core.getFilePath(data.folder_type)
        self.send_To(path.as_posix())

    def subInfo(self,data):
        pass
