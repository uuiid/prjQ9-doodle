# -*- coding: UTF-8 -*-
import logging
import sys

import potplayer
import qdarkstyle
from PySide2 import QtCore
from PySide2 import QtGui
from PySide2 import QtWidgets

import UiFile.ProjectBrowser
import script.DoodleCoreApp
import script.DoodlePrjUI.DoodleButten
import DoodleServer.DoodleBaseClass


class _prjColor(object):
    @staticmethod
    def listItemStateError():
        bush = QtGui.QBrush()
        bush.setColor(QtCore.Qt.red)
        return bush

    @staticmethod
    def listItemStateAmend():
        bush = QtGui.QBrush()
        bush.setColor(QtCore.Qt.darkYellow)
        return bush

    @staticmethod
    def listItemStateComplete():
        bush = QtGui.QBrush()
        bush.setColor(QtCore.Qt.darkGreen)
        return bush

    def __getattr__(self, item):
        bush = QtGui.QBrush()
        bush.setColor(QtCore.Qt.black)
        return bush


class ProjectBrowserGUI(QtWidgets.QMainWindow, UiFile.ProjectBrowser.Ui_MainWindow, script.DoodleCoreApp.core):
    """
    这个类用来实现项目管理的属性和UI操作,其中shot和ass是两个数据库链接器,  用来在ui和数据库中添加一个中间层
    """

    def __init__(self, parent=None):
        super(ProjectBrowserGUI, self).__init__(parent)

        # 加载颜色类
        self._color = _prjColor
        # 最近打开的文件夹
        self.recentlyOpenedFolder = ""
        # 设置UI
        self.setupUi(self)
        self.doodle_app.codeToShot()
        # self.setToolTip("Remer")
        # 设置最后的文件编辑器的一些标准动作
        # 设置每行选择
        self.listfile.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.listAssFile.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        # 设置单选
        self.listfile.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        # 设置注释最大(资产和镜头都是)
        self.listfile.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        self.listAssFile.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        # 设置不可编辑
        self.listfile.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.listAssFile.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

        # 设置tabWigget点击清除事件
        self.tabWidget.currentChanged.connect(lambda index: self.tabWigetClick(index))
        self.setAcceptDrops(True)
        # 首先扫描根目录获得集数
        self.setepisodex()
        # 并链接函数处理下一级
        self.listepisodes.itemClicked.connect(lambda item: self.listEpisodesClicked(item))
        # 在shot文件列表中添加点击事件更改下一级部门列表
        self.listshot.itemClicked.connect(lambda item: self.listshotClicked(item))
        # 在department中添加下一级的更新事件
        self.listdepartment.itemClicked.connect(lambda item: self.listDepartmenClicked(item))
        # 在depType中添加点击跟新文件事件
        self.listdepType.itemClicked.connect(lambda item: self.listDepTypeClicked(item))
        # </editor-fold>

        # 设置ass类型
        self.scane.clicked.connect(lambda: self.assClassSortClicked('scane'))
        self.props.clicked.connect(lambda: self.assClassSortClicked('props'))
        self.character.clicked.connect(lambda: self.assClassSortClicked('character'))
        self.effects.clicked.connect(lambda: self.assClassSortClicked('effects'))

        # 在listAss中添加点击事件生成Ass资产列表
        self.listAss.itemClicked.connect(lambda item: self.assClassClicked(item))
        # 在listType中添加点击事件生成file列表
        self.listAssType.itemClicked.connect(lambda item: self.assClassTypeClicked(item))

        # 双击打开文件
        # self.listfile.doubleClicked.connect(self.openShotFile)
        # 添加刷新函数
        self.refresh.triggered.connect(self.setepisodex)
        # # 关闭ue链接函数
        # self.close_socket.triggered.connect(self.closesocket)
        # # 合成拍屏
        self.actioncom_video.triggered.connect(self.comEpsVideo)
        # # 转换布料
        # self.actionclothToFbx.triggered.connect(self.convertCloth)

        self.pot_player = potplayer.PlayList()

    def tabWigetClick(self, index: int):
        """
        选项卡切换事件
        """
        if index == 0:
            logging.info("点击资产")
            self.doodle_app.codeToAss()
            self.character.file_clas, self.effects.file_clas, self.props.file_clas, self.scane.file_clas = self.core.queryAssClass()[
                                                                                                           :4]
            # self.assClassSortClicked("character")
        elif index == 1:
            self.doodle_app.codeToShot()
            logging.info("点击镜头")
            self.setepisodex()

    # </editor-fold>
    # @staticmethod
    # def _setQlistItemColor(list_: QtWidgets.QListWidget, finds, state_type):
    #     """设置小部件颜色, 用来显示有问题的"""
    #     item = list_.findItems(finds, QtCore.Qt.MatchExactly)
    #     try:
    #         item = item[0]
    #     except IndexError as err:
    #         logging.error("没有找到这个小部件 %s", err)
    #     else:
    #         item.setBackground(getattr(_prjColor, f"listItemState{state_type}")())
    # item.setBackground(QtGui.QBrush(QtCore.Qt.red))

    # <editor-fold desc="镜头更新事件">

    def setepisodex(self):
        """
        更新集数
        """
        self.listepisodes.clear()
        self.listshot.clear()
        self.listdepartment.clear()
        self.listdepType.clear()
        self.listfile.doodleClear()

        self.shot_thumbnail.clear()

        logging.info('更新集数列表')
        self.listepisodes.doodleUpdata()

    def listEpisodesClicked(self, item):
        """
        集数点击事件
        """
        # 设置属性
        self.listdepartment.clear()
        self.listdepType.clear()
        self.listfile.doodleClear()

        self.listshot.clear()
        self.shot_thumbnail.clear()

        logging.info('更新shot列表')

        self.listshot.doodleUpdata()

    def listshotClicked(self, item):
        """
        镜头点击事件
        """
        self.listdepartment.clear()
        self.listdepType.clear()
        self.listfile.doodleClear()
        self.shot_thumbnail.clear()

        logging.info('更新Department列表')

        self.listdepartment.doodleUpdata()
        self.shot_thumbnail.doodleUpdata()

    def listDepartmenClicked(self, item):
        """
        部门点击事件
        """
        self.listfile.doodleClear()
        self.listdepType.clear()
        self.shot_thumbnail.clear()

        self.listdepType.doodleUpdata()
        self.shot_thumbnail.doodleUpdata()

    def listDepTypeClicked(self, item):
        """
        部门类型点击事件
        """
        # 清空上一次文件显示和版本记录和文件路径
        self.listfile.doodleClear()
        self.listfile.doodleUpdata()
        self.shot_thumbnail.doodleUpdata()

    # </editor-fold>

    # <editor-fold desc="更新ass的各种操作">
    def assClassSortClicked(self, ass_name: str):
        """
        按钮点击事件, 更新资产种类
        """
        # self.core.file_class
        self.listAss.clear()
        self.listAssType.clear()
        self.listAssFile.doodleClear()

        self.ass_thumbnail.clear()

        self.listAss.doodleUpdata()

    def assClassClicked(self, item):
        """
        资产种类点击事件, 资产类型的更新
        """

        self.listAssType.clear()
        self.listAssFile.doodleClear()
        logging.info('清除资产类型,文件中的项数')

        self.ass_thumbnail.clear()
        self.listAssType.doodleUpdata()
        self.ass_thumbnail.doodleUpdata()

    def assClassTypeClicked(self, item):
        """资产类别点击事件, 更新资产文件列表"""
        # 清空上一次文件显示和版本记录和文件路径
        self.listAssFile.doodleClear()
        self.listAssFile.doodleUpdata()
        self.ass_thumbnail.doodleUpdata()

    @QtCore.Slot()
    def comEpsVideo(self):
        return DoodleServer.DoodleBaseClass.shotFbEpisodesFile(self.core, self.doodle_set).makeEpisodesFlipBook()

    def closeEvent(self, event):
        self.doodle_app.codeToShot()
        self.doodle_set.my_sql.sessionclass().close()
        print("关闭")


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet())
    w = ProjectBrowserGUI()
    w.setWindowTitle("Remer")
    w.show()

    sys.exit(app.exec_())
