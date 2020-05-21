import pytest
import script.ProjectBrowserGUI
import script.DooDlePrjCode
import script.MySqlComm


@pytest.fixture
def setup_modle():
    test = script.DooDlePrjCode.PrjShot
    prj_shot = script.DooDlePrjCode.PrjShot('dubuxiaoyao', 'W:\\', "03_Workflow/Shots")
    return prj_shot


# class TestClass():
def test_getepsodes(setup_modle):
    print(setup_modle.getEpsodes())


def test_getShot(setup_modle):
    setup_modle.episodes = 1
    print(setup_modle.getShot())


def test_getDepartment(setup_modle):
    setup_modle.episodes = 1
    setup_modle.shot = 10
    setup_modle.shotab = ''
    print(setup_modle.getDepartment())


def test_getDepType(setup_modle):
    setup_modle.episodes = 1
    setup_modle.shot = 10
    setup_modle.shotab = ''
    setup_modle.department = "anm"
    print(setup_modle.getDepType())


def test_getFile(setup_modle):
    setup_modle.episodes = 1
    setup_modle.shot = 10
    setup_modle.shotab = ''
    setup_modle.department = "anm"
    setup_modle.Type = "Animation"
    print(setup_modle.getFile())


def test_queryFlipBookShotTotal(setup_modle):
    setup_modle.episodes = 19
    setup_modle.shot = 10
    setup_modle.shotab = ''
    setup_modle.department = "anm"
    setup_modle.Type = "Animation"
    script.DooDlePrjCode._shot.__table__.name = "ep019"
    total = setup_modle.querFlipBookShotTotal()
    for i in total:
        print(i)


if __name__ == '__main__':
    pytest.main(["-s"])
