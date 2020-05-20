import pytest
import pathlib
import script.synchronizeFiles


def test_robocopy():
    soure = pathlib.Path(r"D:\ue_project\YanJiaHouShan_ZX")
    trange = pathlib.Path(r"D:\ue_project_backup\YanJiaHouShan_ZX")
    test = script.synchronizeFiles.robocopy(soure, trange, ("/E", "/L"))
    for i in test:
        print(i)
