from unittest import TestCase
import pytest
from PyQt5 import QtTest
import unittest
import script.ProjectBrowserGUI
import script.doodle_setting
import script.MySqlComm
# class TestClass():
def test_getsever():
    doodleset = script.doodle_setting.Doodlesetting()

    print(doodleset.getsever())

if __name__ == '__main__':
    pytest.main(["-s"])