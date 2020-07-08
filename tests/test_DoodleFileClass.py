import pathlib
import shutil
import pytest
import typing
import DoodleServer.DoodleBaseClass
import DoodleServer.DoodleOrm as DoleOrm
import DoodleServer.DoodleCore
import DoodleServer.DoodleSet
import DoodleServer.DoodlePlayer


class TestAssUePrj(object):
    @pytest.fixture()
    def create_obj(self) -> typing.Tuple[DoodleServer.DoodleCore.PrjAss, DoodleServer.DoodleBaseClass.assUePrj]:
        doodleset = DoodleServer.DoodleSet.Doodlesetting()
        doodleset.projectname = "dubuxiaoyao"
        core = DoodleServer.DoodleCore.PrjAss(doodleset)

        ass_ue_prj = DoodleServer.DoodleBaseClass.assUePrj(core, doodleset)
        return core, ass_ue_prj

    def test_down(self, create_obj):
        core, ueprj = create_obj
        core.file_class = DoleOrm.fileClass(id=1, file_class="character")
        core.ass_class = DoleOrm.assClass(id=99, file_name='10GeZhongJingXiuXianZhe')
        core.file_type = DoleOrm.fileType(id=270, file_type='10GeZhongJingXiuXianZhe_UE4')
        core.query_id = 1
        path = ueprj.down()
        print(path.as_posix())

    def test_upload(self, create_obj):
        core, ueprj = create_obj
        core.file_class = core.queryAssClass()[0]
        # core.file_class = DoleOrm.fileClass(id=1, file_class="character")
        core.ass_class = core.file_class.addass_class[1]
        core.file_type = core.ass_class.addfileType[0]
        core.query_id = 1
        ueprj.upload(pathlib.Path(r"D:/Doodle_cache/03_Workflow/Assets/character/"
                                  r"10GeZhongJingXiuXianZhe/Scenefiles/10GeZhongJ"
                                  r"ingXiuXianZhe_UE4/CH_Projects.uproject"))

    def test_appoint(self, create_obj):
        core, ueprj = create_obj
        core.file_class = core.queryAssClass()[0]
        # core.file_class = DoleOrm.fileClass(id=1, file_class="character")
        core.ass_class = core.file_class.addass_class[1]
        core.file_type = core.ass_class.addfileType[0]
        core.query_id = 1
        ueprj.appoint(pathlib.Path(r"D:/Doodle_cache/03_Workflow/Assets/character/"
                                   r"10GeZhongJingXiuXianZhe/Scenefiles/10GeZhongJ"
                                   r"ingXiuXianZhe_UE4/CH_Projects.uproject"))


class TestAssScreenshot:

    @pytest.fixture()
    def create_obj(self) -> typing.Tuple[DoodleServer.DoodleCore.PrjAss, DoodleServer.DoodleBaseClass.assScreenshot]:
        doodleset = DoodleServer.DoodleSet.Doodlesetting()
        doodleset.projectname = "dubuxiaoyao"
        core = DoodleServer.DoodleCore.PrjAss(doodleset)

        ass_screenshot = DoodleServer.DoodleBaseClass.assScreenshot(core, doodleset)
        return core, ass_screenshot

    def test_upload(self, create_obj):
        core, ass_screenshot = create_obj
        core.file_class = core.queryAssClass()[0]
        # core.file_class = DoleOrm.fileClass(id=1, file_class="character")
        core.ass_class = core.file_class.addass_class[1]
        core.file_type = DoleOrm.fileType(file_type="test")
        with ass_screenshot.upload() as path:
            shutil.copy2(r"D:\test\test.jpg", path)

    def test_down(self, create_obj):
        core, ass_screenshot = create_obj
        core.file_class = core.queryAssClass()[0]
        # core.file_class = DoleOrm.fileClass(id=1, file_class="character")
        core.ass_class = core.file_class.addass_class[1]
        core.file_type = DoleOrm.fileType(file_type="test")
        print(ass_screenshot.down())


class TestAssFBFile:
    @pytest.fixture()
    def create_obj(self) -> typing.Tuple[DoodleServer.DoodleCore.PrjAss, DoodleServer.DoodleBaseClass.assFBFile]:
        doodleset = DoodleServer.DoodleSet.Doodlesetting()
        doodleset.projectname = "dubuxiaoyao"
        core = DoodleServer.DoodleCore.PrjAss(doodleset)

        ass_ass_fb_file = DoodleServer.DoodleBaseClass.assFBFile(core, doodleset)
        return core, ass_ass_fb_file

    def test_upload(self, create_obj):
        core, ass_ass_fb_file = create_obj
        core.file_class = core.queryAssClass()[0]
        core.ass_class = core.file_class.addass_class[1]
        ass_ass_fb_file.upload(pathlib.Path(r"D:\sc_064\BuJu.1078.png"))

    def test_down(self, create_obj):
        core, ass_ass_fb_file = create_obj
        core.file_class = core.queryAssClass()[0]
        core.ass_class = core.file_class.addass_class[1]
        core.query_id = 4
        print(ass_ass_fb_file.down())


class TestAssMayaFile:
    @pytest.fixture()
    def create_obj(self) -> typing.Tuple[DoodleServer.DoodleCore.PrjAss, DoodleServer.DoodleBaseClass.assMayaFile]:
        doodleset = DoodleServer.DoodleSet.Doodlesetting()
        doodleset.projectname = "dubuxiaoyao"
        core = DoodleServer.DoodleCore.PrjAss(doodleset)

        ass_maya_file = DoodleServer.DoodleBaseClass.assMayaFile(core, doodleset)
        return core, ass_maya_file

    def test_upload(self, create_obj):
        core, ass_maya_file = create_obj
        core.file_class = core.queryAssClass()[0]
        core.ass_class = core.file_class.addass_class[1]
        core.file_type = core.ass_class.addfileType[1]
        ass_maya_file.upload(pathlib.Path(r"D:\DBXY_004_035.mb"))
        print(core.file_type.file_type)

    def test_down(self, create_obj):
        core, ass_maya_file = create_obj
        core.file_class = core.queryAssClass()[0]
        core.ass_class = core.file_class.addass_class[1]
        core.file_type = core.ass_class.addfileType[1]
        core.query_id = 254
        # ass_maya_file.down()
        print(ass_maya_file.down())


# ==================================================================================================================
# shot类测试方法
class TestShotMayaFile:
    @pytest.fixture()
    def create_obj(self) -> typing.Tuple[DoodleServer.DoodleCore.PrjShot, DoodleServer.DoodleBaseClass.shotMayaFile]:
        doodleset = DoodleServer.DoodleSet.Doodlesetting()
        doodleset.projectname = "dubuxiaoyao"
        core = DoodleServer.DoodleCore.PrjShot(doodleset)

        shot_maya_file = DoodleServer.DoodleBaseClass.shotMayaFile(core, doodleset)
        return core, shot_maya_file

    def testUpload(self, create_obj):
        core, shot_maya_file = create_obj
        core.episodes = core.queryEps()[0]
        core.shot = core.episodes.addShot[0]
        core.file_class = core.shot.addfileClass[0]
        core.file_type = core.file_class.addfileType[0]
        shot_maya_file.upload(pathlib.Path(r"D:\DBXY_004_035.mb"))

    def testDown(self, create_obj):
        core, shot_maya_file = create_obj
        core.episodes = core.queryEps()[0]
        core.shot = core.episodes.addShot[0]
        core.file_class = core.shot.addfileClass[0]
        core.file_type = core.file_class.addfileType[0]
        core.query_id = 1270
        print(shot_maya_file.down())


class TestShotFBFile:
    @pytest.fixture()
    def create_obj(self) -> typing.Tuple[DoodleServer.DoodleCore.PrjShot, DoodleServer.DoodleBaseClass.shotFBFile]:
        doodleset = DoodleServer.DoodleSet.Doodlesetting()
        doodleset.projectname = "dubuxiaoyao"
        core = DoodleServer.DoodleCore.PrjShot(doodleset)

        shot_fb_file = DoodleServer.DoodleBaseClass.shotFBFile(core, doodleset)
        return core, shot_fb_file

    def test_upload(self, create_obj):
        core, shot_fb_file = create_obj
        core.episodes = core.queryEps()[0]
        core.shot = core.episodes.addShot[0]
        core.file_class = core.shot.addfileClass[0]
        core.file_type = core.file_class.addfileType[0]
        shot_fb_file.upload(pathlib.Path(r"D:\sc_064\BuJu.1078.png"))

    def test_down(self, create_obj):
        core, shot_fb_file = create_obj
        core.episodes = core.queryEps()[0]
        core.shot = core.episodes.addShot[0]
        core.file_class = core.shot.addfileClass[0]
        core.file_type = core.file_class.addfileType[0]
        core.query_id = 666
        print(shot_fb_file.down())


class TestShotFbEpsiodesFile:
    @pytest.fixture()
    def create_obj(self) -> typing.Tuple[DoodleServer.DoodleCore.PrjShot, DoodleServer.DoodleBaseClass.shotFbEpisodesFile]:
        doodleset = DoodleServer.DoodleSet.Doodlesetting()
        doodleset.projectname = "dubuxiaoyao"
        core = DoodleServer.DoodleCore.PrjShot(doodleset)

        shot_fb_eps_file = DoodleServer.DoodleBaseClass.shotFbEpisodesFile(core, doodleset)
        return core, shot_fb_eps_file

    def test_makeEpsFB(self, create_obj):
        core, shot_fb_eps_file = create_obj
        core.episodes = core.queryEps()[24]
        print(shot_fb_eps_file.makeEpisodesFlipBook())

    def test_down(self, create_obj):
        core, shot_fb_eps_file = create_obj
        core.episodes = core.queryEps()[24]
        print(shot_fb_eps_file.down())


class TestShotMayaExportFile:
    @pytest.fixture()
    def create_obj(self) -> typing.Tuple[DoodleServer.DoodleCore.PrjShot, DoodleServer.DoodleBaseClass.shotMayaExportFile]:
        doodleset = DoodleServer.DoodleSet.Doodlesetting()
        doodleset.projectname = "dubuxiaoyao"
        core = DoodleServer.DoodleCore.PrjShot(doodleset)

        shot_export_file = DoodleServer.DoodleBaseClass.shotMayaExportFile(core, doodleset)
        return core, shot_export_file

    def test_down(self, create_obj):
        core, shot_export_file = create_obj
        core.episodes = core.queryEps()[24]
        core.shot = core.episodes.addShot[26]
        core.file_class = core.shot.addfileClass[0]
        core.file_type = core.file_class.addfileType[2]
        core.query_file = core.file_type.addshotMayaAnmExport[0]
        print(shot_export_file.down())
        pass

    def test_export(self, create_obj):
        core, shot_export_file = create_obj
        core.episodes = core.queryEps()[24]
        core.shot = core.episodes.addShot[26]
        core.file_class = core.shot.addfileClass[0]
        core.file_type = core.file_class.addfileType[0]
        core.query_file = core.file_type.addshotMayaAnmScane[0]
        shot_export_file.export()


class TestshotMayaClothExportFile:
    @pytest.fixture()
    def create_obj(self) -> typing.Tuple[
        DoodleServer.DoodleCore.PrjShot, DoodleServer.DoodleBaseClass.shotMayaClothExportFile]:
        doodleset = DoodleServer.DoodleSet.Doodlesetting()
        doodleset.projectname = "dubuxiaoyao"
        core = DoodleServer.DoodleCore.PrjShot(doodleset)

        shot_export_file = DoodleServer.DoodleBaseClass.shotMayaClothExportFile(core, doodleset)
        return core, shot_export_file

    def test_dow(self, create_obj):
        core, shot_export_file = create_obj
        core.episodes = core.queryEps()[14]
        core.shot = DoleOrm.Shot(shot_=34, episodes=core.episodes)
        uplist = list(pathlib.Path(r"D:\Doodle_cache\03_Workflow\Shots\ep015\sc0034\export_clothToFbx\VFX\clothToFbx")
                      .iterdir())
        uplist.append(uplist.pop(0))
        shot_export_file.upload(uplist)

    def test_down(self, create_obj):
        core, shot_export_file = create_obj
        core.episodes = core.queryEps()[14]
        core.shot = core.episodes.addShot[0]
        core.file_class = core.shot.addfileClass[0]
        core.file_type = core.file_class.addfileType[0]
        core.query_file = core.file_type.addshotMayaAnmExport[0]
        shot_export_file.down()


class TestshotScreenshot:
    @pytest.fixture()
    def create_obj(self) -> typing.Tuple[
        DoodleServer.DoodleCore.PrjShot, DoodleServer.DoodleBaseClass.shotScreenshot]:
        doodleset = DoodleServer.DoodleSet.Doodlesetting()
        doodleset.projectname = "dubuxiaoyao"
        core = DoodleServer.DoodleCore.PrjShot(doodleset)

        shot_screenshot = DoodleServer.DoodleBaseClass.shotScreenshot(core, doodleset)
        return core, shot_screenshot

    def test_upload(self,create_obj):
        core, shot_screenshot = create_obj
        core.episodes = core.queryEps()[14]
        core.shot = core.episodes.addShot[0]
        with shot_screenshot.upload() as path:
            shutil.copy2(pathlib.Path(r"D:\test\test.jpg"),path)

    def test_down(self,create_obj):
        core, shot_screenshot = create_obj
        core.episodes = core.queryEps()[14]
        core.shot = core.episodes.addShot[0]
        core.file_class = core.shot.addfileClass[0]
        core.file_type = core.file_class.addfileType[1]
        core.query_file = core.file_type.addshotScreenshot[0]
        shot_screenshot.down()