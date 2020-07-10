import sys
import time

import pytest
# import tests
import pytestqt
import DoodleServer
import script.DoodlePrjUI.DoodleListWidget
from PySide2 import QtGui, QtCore, QtWidgets


class TestEpisodesListWidget:
    @pytest.fixture()
    def viewer(self, qtbot):
        window = script.DoodlePrjUI.DoodleListWidget.EpisodesListWidget()
        qtbot.add_widget(window)
        window.show()
        return window

    def test_add_episodes_folder(self, qtbot, viewer):
        assert viewer.isVisible()
        viewer.addItems(DoodleServer.Core.PrjShot(DoodleServer.DoodleSet.Doodlesetting()).queryEps())
        viewer.show()

        qtbot.stop()
        print([viewer.item(i).eps_data.episodes for i in range(10)])


class TestShotListWidget:
    @pytest.fixture()
    def viewer(self, qtbot):
        window = script.DoodlePrjUI.DoodleListWidget.ShotListWidget()
        qtbot.add_widget(window)
        window.show()
        return window

    def test_add_folder(self, qtbot, viewer):
        assert viewer.isVisible()
        core = DoodleServer.Core.PrjShot(DoodleServer.DoodleSet.Doodlesetting())
        core.episodes = core.queryEps()[24]
        viewer.addItems(core.queryShot())
        print([viewer.item(i).shot.shot_ for i in range(10)])
        qtbot.stopForInteraction()
        qtbot.mouseClick(viewer, QtCore.Qt.RightButton)


class TestShotFileClassListWidget:
    @pytest.fixture()
    def viewer(self, qtbot):
        window = script.DoodlePrjUI.DoodleListWidget.ShotFileClassListWidget()
        window.doodle_stting = DoodleServer.DoodleSet.Doodlesetting()
        qtbot.add_widget(window)
        window.show()
        return window

    def test_add_fodle(self, qtbot, viewer):
        assert viewer.isVisible()
        core = DoodleServer.Core.PrjShot(DoodleServer.DoodleSet.Doodlesetting())
        core.episodes = core.queryEps()[24]
        core.shot = core.queryShot()[0]
        viewer.addItems(core.queryFileClass())
        qtbot.stopForInteraction()


class TestShotFileTypeListWidget:
    @pytest.fixture()
    def viewer(self, qtbot):
        window = script.DoodlePrjUI.DoodleListWidget.ShotFileTypeListWidget()
        window.doodle_stting = DoodleServer.DoodleSet.Doodlesetting()
        qtbot.add_widget(window)
        window.show()
        return window

    def test_add_fodle(self, qtbot, viewer):
        assert viewer.isVisible()
        core = DoodleServer.Core.PrjShot(DoodleServer.DoodleSet.Doodlesetting())
        core.episodes = core.queryEps()[24]
        core.shot = core.queryShot()[0]
        core.file_class = core.queryFileClass()[0]
        viewer.addItems(core.queryFileType())
        qtbot.stopForInteraction()

class TestshotTableWidget:
    @pytest.fixture()
    def viewer(self, qtbot):
        window = script.DoodlePrjUI.DoodleListWidget.shotTableWidget()
        window.doodle_stting = DoodleServer.DoodleSet.Doodlesetting()
        qtbot.add_widget(window)

        window.setColumnCount(5)
        window.setRowCount(0)

        item = QtWidgets.QTableWidgetItem()
        window.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        window.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        window.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        window.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        window.setHorizontalHeaderItem(4, item)

        window.horizontalHeaderItem(0).setText(QtWidgets.QApplication.translate("MainWindow", "版本", None, -1))
        window.horizontalHeaderItem(1).setText(QtWidgets.QApplication.translate("MainWindow", "概述", None, -1))
        window.horizontalHeaderItem(2).setText(QtWidgets.QApplication.translate("MainWindow", "制作人", None, -1))
        window.horizontalHeaderItem(3).setText(QtWidgets.QApplication.translate("MainWindow", "格式", None, -1))
        window.horizontalHeaderItem(4).setText(QtWidgets.QApplication.translate("MainWindow", "ID", None, -1))

        window.show()
        return window

    def test_add_fofle(self,qtbot,viewer):
        assert viewer.isVisible()
        core = DoodleServer.Core.PrjShot(DoodleServer.DoodleSet.Doodlesetting())
        core.episodes = core.queryEps()[24]
        core.shot = core.queryShot()[0]
        core.file_class = core.queryFileClass()[0]
        core.file_type = core.queryFileType()[1]
        viewer.addTableItems(core.queryFile())
        # viewer.set
        qtbot.stopForInteraction()