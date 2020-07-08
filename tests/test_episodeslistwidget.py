import pytest
# import tests
import pytestqt.plugin
from PyQt5 import QtGui, QtCore, QtWidgets, QtTest

class TestEpisodesListWidget:
    @pytest.fixture()
    def viewer(self):
        print("setup GUI")

    def test_add_episodes_folder(self):
        assert False

    def test_add_items(self):
        assert False