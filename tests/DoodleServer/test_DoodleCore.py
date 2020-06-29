import pytest
import pickle
import zmq

import DoodleServer.DoodleCore as Server
import DoodleServer.DoodleSet as DoleSet
import DoodleServer.DoodleOrm as DoleOrm


@pytest.fixture
def setup_modle():
    pass
    test = Server.DoodleServer(DoleSet.Doodlesetting())
    test.start()
    # test.setDaemon(True)
    return test


@pytest.fixture
def prjCode_setup():
    test = Server.PrjCore("dubuxiaoyao", "Shots", "/w")
    return test


@pytest.fixture
def prjshot_setup():
    test = Server.PrjShot("dubuxiaoyao", "Shots", "/w")
    return test


@pytest.fixture
def prjAss_setup():
    test = Server.PrjAss("dubuxiaoyao", "Shots", "/w")
    return test


def test_get_doodle_set():
    connect = zmq.Context()
    socket = connect.socket(zmq.REQ)
    socket.connect("tcp://127.0.0.1:23369")
    my_test = {"url": "getDoodleSet"}
    socket.send_pyobj(my_test)
    print(socket.recv_pyobj())
    # socket.close()
    # socket.send_pyobj(b"close")
    # print(socket.recv_pyobj())


def test_get_eps_root(prjCode_setup):
    print(prjCode_setup.getEpsRoot())


def test_query_eps(prjshot_setup):
    print(prjshot_setup.queryEps())


def test_query_shot(prjshot_setup):
    prjshot_setup.episodes = 30
    print(prjshot_setup.queryShot())


def test_query_file_class(prjshot_setup):
    prjshot_setup.episodes = 30
    prjshot_setup.shot = 8
    prjshot_setup.shotab = ""
    print(prjshot_setup.queryFileClass())


def test_query_file_type(prjshot_setup):
    prjshot_setup.episodes = 30
    prjshot_setup.shot = 8
    prjshot_setup.shotab = ""
    prjshot_setup.file_class = 'VFX'
    print(prjshot_setup.queryFileType())


def test_query_file(prjshot_setup):
    prjshot_setup.episodes = 30
    prjshot_setup.shot = 8
    prjshot_setup.shotab = ""
    prjshot_setup.file_class = 'VFX'
    prjshot_setup.file_type = "FB_VFX"
    file = prjshot_setup.queryFile(DoleOrm.shotFlipBook)
    print(file[0].filepath)


def test_query_max_version(prjshot_setup):
    prjshot_setup.episodes = 30
    prjshot_setup.shot = 8
    prjshot_setup.shotab = ""
    prjshot_setup.file_class = 'VFX'
    prjshot_setup.file_type = "FB_VFX"
    print(prjshot_setup.queryMaxVersion(DoleOrm.shotFlipBook))


def test_comm_path(prjshot_setup):
    prjshot_setup.episodes = 30
    prjshot_setup.shot = 8
    prjshot_setup.shotab = ""
    prjshot_setup.file_class = 'VFX'
    prjshot_setup.file_type = "FB_VFX"
    print(prjshot_setup.commPath())


def test_comm_name(prjshot_setup):
    prjshot_setup.episodes = 30
    prjshot_setup.shot = 8
    prjshot_setup.shotab = ""
    prjshot_setup.file_class = 'VFX'
    prjshot_setup.file_type = "FB_VFX"
    print(prjshot_setup.commName(10, "ers"))


def test_query_ass_class(prjAss_setup):
    prjAss_setup.file_class = "character"
    print(prjAss_setup.queryAssname())


def test_query_ass_type(prjAss_setup):
    prjAss_setup.file_class = "character"
    prjAss_setup.ass_name = "XueMang"
    print(prjAss_setup.queryAssType())


def test_Ass_query_file(prjAss_setup):
    prjAss_setup.file_class = "character"
    prjAss_setup.ass_name = "XueMang"
    prjAss_setup.file_type = "rig"
    print(prjAss_setup.queryFile(DoleOrm.assMayaRigModel)[0].filepath)


def test_query_Ass_max_version(prjAss_setup):
    prjAss_setup.file_class = "character"
    prjAss_setup.ass_name = "XueMang"
    prjAss_setup.file_type = "rig"
    print(prjAss_setup.queryMaxVersion(DoleOrm.assMayaRigModel))
