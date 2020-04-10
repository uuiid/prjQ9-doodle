import json
import pathlib
import threading

import script.doodleLog
import script.doodle_setting


class SeverSetting:
    _setting = {}
    _instance_lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not hasattr(SeverSetting, '_instance'):
            with SeverSetting._instance_lock:
                if not hasattr(SeverSetting, '_instance'):
                    SeverSetting._instance = object.__new__(cls)
        return SeverSetting._instance

    def __init__(self):
        self.ta_log_Sever = script.doodleLog.get_logger(__name__)
        self.setlocale = script.doodle_setting.Doodlesetting()
        self.setting = self.getsever()
        pass

    @property
    def setting(self):
        return SeverSetting._setting

    @setting.setter
    def setting(self, tmp: dict):
        SeverSetting._setting = tmp;

    def getsever(self) -> dict:
        """返回服务器上的 同步目录设置"""
        # 读取本地部门类型 以及每集类型
        # self.setlocale = script.doodle_setting.Doodlesetting()
        # 获得设置的文件路径
        file = pathlib.Path(self.setlocale.project).joinpath('configuration', '{}_synFile.json'.format(
            self.setlocale.department))
        self.ta_log_Sever.info('服务器文件路径 %s', file)
        # 读取文件
        settingtmp = file.read_text(encoding='utf-8')
        settingtmp = json.loads(settingtmp, encoding='utf-8')
        synpath: dict
        tmp = []
        # 将服务器上的同步路径和本地链接
        try:
            for synpath in settingtmp['ep{:0>3d}Syn'.format(self.setlocale.synEp)]:
                for key, value in synpath.items():
                    if key == 'Left':
                        synpath[key] = str(pathlib.Path(self.setlocale.syn).joinpath(value))
                    else:
                        synpath[key] = str(pathlib.Path(self.setlocale.synSever).joinpath(value))
                tmp.append(synpath)
        except KeyError as err:
            self.ta_log_Sever.error('服务器文件转为字典时出错 %s', err)
            return None
        except:
            self.ta_log_Sever.error('服务器文件不知道为什么出错 %s')
            return None

        settingtmp['ep{:0>3d}Syn'.format(self.setlocale.synEp)] = tmp
        self.setting = settingtmp
        # 返回特定部门的同步路径设置
        return self.setting

    def getseverPrjBrowser(self) -> dict:
        '''返回服务器上的project设置'''
        prjSetFile = pathlib.Path(self.setlocale.project).joinpath('configuration',
                                                                   'Doodle_Prj_Browser.json')
        self.ta_log_Sever.info('服务器上的项目设置 %s', prjSetFile)
        prjset = prjSetFile.read_text(encoding='utf-8')
        prjset = json.loads(prjset, encoding='utf-8')
        self.ta_log_Sever.info('服务器上的项目设置(json) %s', prjset)
        return prjset


if __name__ == '__main__':
    test = SeverSetting().setting
    print(SeverSetting().getseverPrjBrowser())
    print(test)
