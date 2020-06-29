import pytest

import DoodleServer.DoodleSet as DoleSet


@pytest.fixture
def setup_modle():
    test = DoleSet.Doodlesetting()
    return test


def test_getsever(setup_modle):
    print(setup_modle.getsever())


def test_FTP_Register(setup_modle):
    setup_modle.user = "测试"
    print(setup_modle.FTP_Register())
