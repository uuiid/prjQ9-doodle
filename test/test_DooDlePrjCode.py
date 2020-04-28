import pytest
import script.ProjectBrowserGUI
import script.DooDlePrjCode
import script.MySqlComm


@pytest.fixture
def setup_modle():
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
if __name__ == '__main__':
    pytest.main(["-s"])
