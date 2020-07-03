import pytest
import pickle
import zmq

import DoodleServer.DoodleCore as Server
import DoodleServer.DoodleSet as DoleSet
import DoodleServer.DoodleOrm as DoleOrm


@pytest.fixture
def setup_server_modle():
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
    set = DoleSet.Doodlesetting()
    test = Server.PrjAss(set)
    return test


# def test_get_doodle_set(setup_server_modle):
#     connect = zmq.Context()
#     socket = connect.socket(zmq.REQ)
#     socket.connect("tcp://127.0.0.1:23369")
#     my_test = {"url": "getDoodleSet"}
#     socket.send_pyobj(my_test)
#     print(socket.recv_pyobj())

# socket.close()
# socket.send_pyobj(b"close")
# print(socket.recv_pyobj())


def test_query_eps(prjshot_setup):
    print(prjshot_setup.queryEps())


def test_query_shot(prjshot_setup):
    prjshot_setup.episodes = DoleOrm.Episodes(id=23, episodes=30)
    query_shot = prjshot_setup.queryShot()
    print(query_shot)
    print(prjshot_setup.queryShotList())


def test_query_file_class(prjshot_setup):
    prjshot_setup.episodes = DoleOrm.Episodes(id=23, episodes=30)
    prjshot_setup.shot = DoleOrm.Shot(id=602, shot_=8, shotab="")
    query_file_class = prjshot_setup.queryFileClass()
    print(query_file_class)


def test_query_file_type(prjshot_setup):
    prjshot_setup.episodes = DoleOrm.Episodes(id=23, episodes=30)
    prjshot_setup.shot = DoleOrm.Shot(id=602, shot_=8, shotab="")
    prjshot_setup.file_class = DoleOrm.fileClass(id=813, file_class="VFX")
    file_type = prjshot_setup.queryFileType()
    print(file_type)


def test_query_file(prjshot_setup):
    prjshot_setup.episodes = DoleOrm.Episodes(id=23, episodes=30)
    prjshot_setup.shot = DoleOrm.Shot(id=602, shot_=8, shotab="")
    prjshot_setup.file_class = DoleOrm.fileClass(id=813, file_class="VFX")
    prjshot_setup.file_type = DoleOrm.fileType(id=3687, file_type="FB_VFX")
    file = prjshot_setup.queryFile()
    print(file[0].filepath)


def test_query_max_version(prjshot_setup):
    prjshot_setup.episodes = DoleOrm.Episodes(id=23, episodes=30)
    prjshot_setup.shot = DoleOrm.Shot(id=602, shot_=8, shotab="")
    prjshot_setup.file_class = DoleOrm.fileClass(id=813, file_class="VFX")
    prjshot_setup.file_type = DoleOrm.fileType(id=3687, file_type="FB_VFX")
    print(prjshot_setup.queryMaxVersion())


def test_comm_path(prjshot_setup):
    prjshot_setup.episodes = DoleOrm.Episodes(id=23, episodes=30)
    prjshot_setup.shot = DoleOrm.Shot(id=602, shot_=8, shotab="")
    prjshot_setup.file_class = DoleOrm.fileClass(id=813, file_class="VFX")
    # prjshot_setup.file_type = DoleOrm.fileType(id=3687,file_type="FB_VFX")
    print(prjshot_setup.commPath())


def test_comm_name(prjshot_setup):
    prjshot_setup.episodes = DoleOrm.Episodes(id=23, episodes=30)
    prjshot_setup.shot = DoleOrm.Shot(id=602, shot_=8, shotab="")
    prjshot_setup.file_class = DoleOrm.fileClass(id=813, file_class="VFX")
    prjshot_setup.file_type = DoleOrm.fileType(id=3687, file_type="FB_VFX")
    print(prjshot_setup.commName(10, "ers"))


def test_query_ass_name(prjAss_setup):
    prjAss_setup.file_class = DoleOrm.fileClass(id=1, file_class="character")
    query_assname = prjAss_setup.queryAssname()
    print(query_assname)


def test_query_ass_type(prjAss_setup):
    prjAss_setup.file_class = DoleOrm.fileClass(id=1, file_class="character")
    prjAss_setup.ass_class = DoleOrm.assClass(id=1, file_name='10GeZhongJingXiuXianZhe')
    query_ass_type = prjAss_setup.queryAssType()
    print(query_ass_type)


def test_Ass_query_file(prjAss_setup):
    prjAss_setup.file_class = DoleOrm.fileClass(id=1, file_class="character")
    prjAss_setup.ass_class = DoleOrm.assClass(id=99, file_name='10GeZhongJingXiuXianZhe')
    prjAss_setup.file_type = DoleOrm.fileType(id=270, file_type='10GeZhongJingXiuXianZhe_UE4')
    print(prjAss_setup.queryFile()[0].filepath)


def test_query_Ass_max_version(prjAss_setup):
    prjAss_setup.file_class = DoleOrm.fileClass(id=1, file_class="character")
    prjAss_setup.ass_class = DoleOrm.assClass(id=99, file_name='10GeZhongJingXiuXianZhe')
    prjAss_setup.file_type = DoleOrm.fileType(id=270, file_type='10GeZhongJingXiuXianZhe_UE4')
    print(prjAss_setup.queryMaxVersion())


def test_Ass_comm_name(prjAss_setup):
    prjAss_setup.file_class = DoleOrm.fileClass(id=1, file_class="character")
    prjAss_setup.ass_class = DoleOrm.assClass(id=99, file_name='10GeZhongJingXiuXianZhe')
    # prjAss_setup.file_type = DoleOrm.fileType(id=270, file_type='10GeZhongJingXiuXianZhe_UE4')
    print(prjAss_setup.commName(1, "ad"))


def test_Ass_comm_path(prjAss_setup):
    prjAss_setup.file_class = DoleOrm.fileClass(id=1, file_class="character")
    prjAss_setup.ass_class = DoleOrm.assClass(id=99, file_name='10GeZhongJingXiuXianZhe')
    # prjAss_setup.file_type = DoleOrm.fileType(id=270, file_type='10GeZhongJingXiuXianZhe_UE4')
    print(prjAss_setup.commPath("ad"))