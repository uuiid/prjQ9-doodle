from PySide2 import QtCore, QtGui, QtWidgets
import DoodleServer
import typing

class core:

    @property
    def core(self) -> typing.Union[DoodleServer.Core.PrjShot,DoodleServer.Core.PrjAss]:
        """
        获得核心解析器
        :return:
        :rtype:
        """
        return QtCore.QCoreApplication.instance().core

    @property
    def doodle_set(self) -> DoodleServer.Set.Doodlesetting:
        """
        获得核心设置
        :return:
        :rtype:
        """
        return QtCore.QCoreApplication.instance().doodle_set

    @property
    def doodle_app(self):
        return QtCore.QCoreApplication.instance()



