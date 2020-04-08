import json
import pathlib

import script.doodle_setting


class SeverSetting:
    _setting = {}

    def __init__(self):
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
        """返回服务器上的目录设置"""
        # 读取本地部门类型 以及每集类型
        self.setlocale = script.doodle_setting.Doodlesetting()
        # 获得设置的文件路径
        file = pathlib.Path(self.setlocale.setting['project']).joinpath('configuration', '{}_synFile.json'.format(
            self.setlocale.setting['department']))
        # 读取文件
        settingtmp = file.read_text(encoding='utf-8')
        settingtmp = json.loads(settingtmp, encoding='utf-8')
        synpath: dict
        tmp = []
        for synpath in settingtmp['ep{:0>3d}Syn'.format(self.setlocale.setting['synEp'])]:
            for key, value in synpath.items():
                if key == 'Left':
                    synpath[key] = str(pathlib.Path(self.setlocale.setting['syn']).joinpath(value))
                else:
                    synpath[key] = str(pathlib.Path(self.setlocale.setting['synSever']).joinpath(value))
            tmp.append(synpath)
        settingtmp['ep{:0>3d}Syn'.format(self.setlocale.setting['synEp'])] = tmp
        self.setting = settingtmp
        # 返回特定部门的同步路径设置
        return self.setting

    def getseverPrjBrowser(self) -> dict:
        '''返回服务器上的project设置'''
        prjSetFile = pathlib.Path(self.setlocale.setting['project']).joinpath('configuration',
                                                                              'Doodle_Prj_Browser.json')

        prjset = prjSetFile.read_text(encoding='utf-8')
        prjset = json.loads(prjset, encoding='utf-8')
        return prjset


if __name__ == '__main__':
    test = SeverSetting().setting
    print(SeverSetting().getseverPrjBrowser())
    print(test)
