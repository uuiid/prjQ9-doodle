import pytest
import pathlib
import script.synchronizeFiles


def test_robocopy():
    soure = pathlib.Path(r"D:\ue_project\YanJiaHouShan_ZX")
    trange = pathlib.Path(r"D:\ue_project_backup\YanJiaHouShan_ZX")
    test = script.synchronizeFiles.robocopy(soure, trange, ("/E", "/L"))
    for i in test:
        print(i)


def test_ftpDownload():
    my_l = pathlib.Path("D:\\tmp\\test")
    my_r = pathlib.Path("/03_Workflow/Assets/Character/Ch003A/Ch003A_UE4")

    t = script.synchronizeFiles.ftpDownload(my_l,my_r,None,{})
    t.dow()

def test_ftpUpload():
    my_l = pathlib.Path("D:\\tmp\\test")
    my_r = pathlib.Path("/configuration")

    t = script.synchronizeFiles.ftpUpload(my_l,my_r,None,{})
    t.Upload()