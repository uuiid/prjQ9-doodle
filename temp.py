import pathlib
import json
import subprocess
import time
import script.MySqlComm

# import script.doodlePlayer
# if __name__ == '__main__':
#     in_filename = pathlib.Path(r'D:\EP01_4.3.mp4')
#     file = pathlib.Path(r"D:\test\EP01_.png")
#     test = script.doodlePlayer.videoConvert(in_filename, file)
#     lll_std = test.videoToImage()
#     print(lll_std)
# path = pathlib.Path(r"D:\image")
# image = [str(i) for i in path.iterdir()]
# image = "D:/image/ep010_sc0001_VFX_test_zhang-yu-bin.0159.png"
# djv = subprocess.Popen(['tools/bin/ffplay.exe',
#                         "-i","-",
#                         ],stdin=subprocess.PIPE,bufsize=10**8,universal_newlines=True)
# ssss= " ".join(image)
# djv.stdin.write(ssss)
# for image in path.iterdir():
#     data = image.read_bytes()
#     print(data)
#     djv.communicate(data)
#     time.sleep(0.04)
# image = pathlib.Path(image)

# <editor-fold desc="表格">
it = []
for dep in ["Light", "VFX"]:
    synPath = pathlib.Path(f"W:\\configuration\\{dep}_synFile.json")
    data = synPath.read_text(encoding='utf-8')
    data_d: dict = json.loads(data, encoding='utf-8')
    for key, value in data_d.items():
        for vs in value:
            for ls, lsvalue in vs.items():
                # print(lsvalue)
                temp = lsvalue.replace("\\","/")
                t = f"('synpath','{dep}','{key[2:5]}','{ls}','{temp}')"
                it.append(t)
                # sql_com = f"INSERT INTO `configure`(name, value, value2, value3, value4) VALUE {t}"
                # script.MySqlComm.inserteCommMysql("dubuxiaoyao", "", "", sql_command=sql_com)
                # print(sql_com)
# print(it)
sql_com = f"INSERT INTO `configure` (name, value, value2, value3, value4) VALUES {','.join(it)}"
# print(sql_com)
script.MySqlComm.inserteCommMysql("dubuxiaoyao", "", "", sql_command=sql_com)
# </editor-fold>
