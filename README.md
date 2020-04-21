# prjQ9-doodle
pip freeze > requirements.txt
pip install -r requirements.txt

pyinstaller doodle.spec

             ('script','script'),
a = Analysis(['doodle_tray.py'],
             pathex=['D:\\ueFile'],
             binaries=[],

             datas=[('datas\\icon.png','datas'),
             ('UiFile','UiFile'),
             ('tools','tools'),
             ('script','script'),
             ('config','config')],