import pathlib
import json
import subprocess
import time
import script.MySqlComm
import tools.ue_path
# <editor-fold desc="表格">
# it = []
# for dep in ["Light", "VFX"]:
#     synPath = pathlib.Path(f"W:\\configuration\\{dep}_synFile.json")
#     data = synPath.read_text(encoding='utf-8')
#     data_d: dict = json.loads(data, encoding='utf-8')
#     for key, value in data_d.items():
#         for vs in value:
#             for ls, lsvalue in vs.items():
#                 # print(lsvalue)
#                 temp = lsvalue.replace("\\","/")
#                 t = f"('synpath','{dep}','{key[2:5]}','{ls}','{temp}')"
#                 it.append(t)
#                 # sql_com = f"INSERT INTO `configure`(name, value, value2, value3, value4) VALUE {t}"
#                 # script.MySqlComm.inserteCommMysql("dubuxiaoyao", "", "", sql_command=sql_com)
#                 # print(sql_com)
synfile = ['BiTaoGe_UE4',"SanChaLu_LWZ"]
LR = ["Left", "Right"]
ep = 15
it = []
for dep in ["Light", "VFX"]:
    for key in synfile:
        for ls in LR:
            t = f"('synpath','{dep}','{ep:0>3d}','{ls}','Ep_{ep:0>2d}/{key}/Content/shot')"
            path = tools.ue_path.createPath(f"W:/data/ue_prjEp_{ep:0>2d}/{key}/Content",eps=ep,secene=120)
            path.create()
            it.append(t)

# print(it)
sql_com = f"INSERT INTO `configure` (name, value, value2, value3, value4) VALUES {','.join(it)}"

script.MySqlComm.inserteCommMysql("dubuxiaoyao", "", "", sql_command=sql_com)
# </editor-fold>
