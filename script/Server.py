import json
import logging
import pathlib
import pickle
import threading
import traceback
from multiprocessing import connection as Conn

import DoodleServer.DoodleBaseClass
import DoodleServer.DoodleCore
import DoodleServer.DoodleDictToObject
import DoodleServer.DoodleZNCHConvert
import script.DoodleCoreApp


# from DoodleServer.DoodleOrm import *


# class DoodleServer(threading.Thread):
#     server = None
#     connect: zmq.Context
#     socket: zmq.Socket
#
#     def __init__(self, doodle_set):
#         super().__init__()
#         self.doodle_set = doodle_set
#         """=============="""
#         # self.shot = script.DooDlePrjCode.PrjShot(self.doodle_set.projectname,
#         #                                          self.doodle_set.project,
#         #                                          self.doodle_set.shotRoot)
#         # self.ass = script.DooDlePrjCode.PrjAss(self.doodle_set.projectname,
#         #                                        self.doodle_set.project,
#         #                                        self.doodle_set.assetsRoot)
#
#     def run(self):
#         self.connect = zmq.Context()
#         self.socket = self.connect.socket(zmq.STREAM)
#         self.socket.bind("tcp://127.0.0.1:23369")
#
#         # self.server = Conn.Listener(("127.0.0.1", 23369), authkey=b"doodle")
#         while True:
#             try:
#                 self.recv_data = self.socket.recv_pyobj()
#                 if self.recv_data == b'close':
#                     self.socket.send_pyobj(b"close")
#                     self.socket.close()
#                     break
#                 self.analysis()
#             except EOFError:
#                 logging.error(traceback.print_exc())
#                 self.socket.send_pyobj("+++出错了++++")
#                 break
#             finally:
#                 logging.info("完成了一次转发")
#
#     def analysis(self):
#         logging.info("开始分析传入数据")
#         print(self.recv_data)
#         # try:
#         #     data = DoleDict.convertTool().convert(self.recv_data)
#         #     getattr(self, data.url)(data)
#         # except EOFError:
#         #     logging.error(traceback.print_exc())
#
#     def getDoodleSet(self, data):
#         my_set = {"user": Convert.isChinese(self.doodle_set.user).easyToEn(),
#                   "department": self.doodle_set.department,
#                   "projectname": self.doodle_set.projectname, "cache_path": self.doodle_set.cache_path.as_posix()}
#         self.socket.send_pyobj(my_set, protocol=2)


class DoodleServer__(threading.Thread, script.DoodleCoreApp.core):
    server = None
    client: Conn.Connection

    def __init__(self):
        super().__init__()

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
                data = DoodleServer.DoodleDictToObject.convertTool().convert(data)
                getattr(self, data.url)(data)
            except EOFError:
                logging.error(traceback.print_exc())
                self.client.close()
                break

    def send_To(self, data):
        self.client.send_bytes(pickle.dumps(data, protocol=2))

    def getDoodleSet(self, data):
        my_set = {"user": self.doodle_set.en_user,
                  "department": self.doodle_set.department,
                  "projectname": self.doodle_set.projectname,
                  "cache_path": self.doodle_set.cache_path.as_posix()}
        self.send_To(my_set)

    def getPath(self, data):
        if data.core == "shot":
            self.doodle_app.codeToShot()
        else:
            self.doodle_app.codeToAss()
        self._setBaseCoreAttr(data, self.core)
        path: pathlib.Path = self.core.commPath()
        self.send_To(path.as_posix())

    def subInfo(self, data):
        core = getattr(self, data.core)
        self._setBaseCoreAttr(data.info, core)
        assert isinstance(core, DoodleServer.DoodleCore.PrjShot)
        # 创建maya布料上传函数
        file = DoodleServer.DoodleBaseClass.shotMayaClothExportFile(core, self.doodle_set)
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
        if isinstance(core, DoodleServer.DoodleCore.PrjAss):
            try:
                pass
            except KeyError:
                pass
        elif isinstance(core, DoodleServer.DoodleCore.PrjShot):
            try:
                core.episodes = DoodleServer.DoodleOrm.Episodes(episodes=data.episodes)
                core.shot = DoodleServer.DoodleOrm.Shot(shot_=data.shot, shotab=data.shotab)
                core.file_class = DoodleServer.DoodleOrm.fileClass(file_class=self.doodle_set.department)
                core.file_type = DoodleServer.DoodleOrm.fileType(file_type=data.Type)
            except KeyError:
                logging.error("传入字典无法解析 %s", traceback.print_exc())


if __name__ == '__main__':
    t = DoodleServer__()
    t.start()
