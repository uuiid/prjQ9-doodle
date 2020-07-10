from unittest import TestCase
import pytest
from PySide2 import QtTest
import unittest
import script.DoodleBrowserGUI
import script.DoodleSetGui
import script.MySqlComm
# class TestClass():
def test_getsever():
    doodleset = script.DoodleSetGui.Doodlesetting()

    print(doodleset.getsever())

if __name__ == '__main__':
    pytest.main(["-s"])