import json
import pathlib

import script.doodle_setting


class SeverSetting():
    setting = {}

    def getsever(self) -> dict:
        """返回服务器上的目录设置"""
        # 预备读取本地部门类型 以及每集类型
        setlocale = script.doodle_setting.Doodlesetting()

        file = pathlib.Path('W:\\data\\ue_prj\\synFile.json')
        settingtmp = file.read_text(encoding='utf-8')
        settingtmp = json.loads(settingtmp, encoding='utf-8')
        synpath: dict
        tmp = []
        for synpath in settingtmp['Synchronization']:
            for key, value in synpath.items():
                if key == 'Left':
                    synpath[key] = str(pathlib.Path(setlocale.setting['syn']).joinpath(value))
                else:
                    synpath[key] = str(pathlib.Path(setlocale.setting['synSever']).joinpath(value))
            tmp.append(synpath)
        settingtmp['Synchronization'] = tmp
        self.setting = settingtmp
        # 返回特定部门的同步路径设置
        return self.setting


print(SeverSetting().getsever())
