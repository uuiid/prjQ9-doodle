本地设置:
user 制作人
department 部门选项
    Light
    VFX
    modle
    rig
    Aim
syn D:\\ue_prj
synSever W:\\data\\ue_prj
synEp: 1  同步集数
FreeFileSync C:\\PROGRA~1\\FREEFI~1\\FreeFileSync.exe

build_ext --inplace
setup(name="test", ext_modules=cythonize('temp/test.pyx', annotate=True),)
python setup.py build
"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" anzhuang.iss



