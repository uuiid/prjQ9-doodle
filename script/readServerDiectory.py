import json
import pathlib

import script.doodle_setting


class SeverSetting:
    _setting = {}

    def __init__(self):
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
        # 预备读取本地部门类型 以及每集类型
        setlocale = script.doodle_setting.Doodlesetting()

        file = pathlib.Path(setlocale.setting['project']).joinpath('configuration', '{}_synFile.json'.format(
            setlocale.setting['department']))
        settingtmp = file.read_text(encoding='utf-8')
        settingtmp = json.loads(settingtmp, encoding='utf-8')
        synpath: dict
        tmp = []
        for synpath in settingtmp['ep{:0>3d}Syn'.format(setlocale.setting['synEp'])]:
            for key, value in synpath.items():
                if key == 'Left':
                    synpath[key] = str(pathlib.Path(setlocale.setting['syn']).joinpath(value))
                else:
                    synpath[key] = str(pathlib.Path(setlocale.setting['synSever']).joinpath(value))
            tmp.append(synpath)
        settingtmp['ep{:0>3d}Syn'.format(setlocale.setting['synEp'])] = tmp
        self.setting = settingtmp
        # 返回特定部门的同步路径设置
        return self.setting


if __name__ == '__main__':
    test = SeverSetting().setting
    print(test)
