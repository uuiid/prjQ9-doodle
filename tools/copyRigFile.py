import pathlib
from typing import List, Any

soure = pathlib.Path(r'W:\03_Workflow\Assets\DuBuXiaoYao\BangDing')
ten_MoXing = pathlib.Path(r'W:\03_Workflow\Assets\DuBuXiaoYao\MoXing')

item = []
for path in ten_MoXing.iterdir():
    for pat in path.iterdir():
        if pat.match('*ep_*'):
            for children_path in pat.iterdir():
                item.append(children_path.stem)
        else:
            item.append(path.stem)
            
RigFile: List[str] = []
for it in item:
    Folder = soure.glob('*\\{}'.format(it))
    Folder = list(Folder)
    if Folder:
        Folder = Folder[0]
        RigFile.append(list(Folder.glob('**\\*.m*')))
