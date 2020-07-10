# -*- coding: UTF-8 -*-
import pathlib
import re
import socket
import sys
import logging
import potplayer
import pyperclip
import typing

from PySide2 import QtCore
from PySide2 import QtGui
from PySide2 import QtWidgets

import qdarkstyle
import UiFile.ProjectBrowser

import script.DoodleSetGui
import script.DoodleCore
import DoodleServer
import script.DoodlePrjUI.DoodleListWidget
import script.DoodlePrjUI.DoodleTableWidget
import script.DoodlePrjUI.DoodleButten

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


class ProjectBrowserGUI(QtWidgets.QMainWindow, UiFile.ProjectBrowser.Ui_MainWindow,script.DoodleCore.core):
    """
    这个类用来实现项目管理的属性和UI操作,其中shot和ass是两个数据库链接器,  用来在ui和数据库中添加一个中间层
    """
    #
    # @property
    # def core(self) -> DoodleServer.Core.PrjCore:
    #     """
    #     获得核心解析器
    #     :return:
    #     :rtype:
    #     """
    #     return QtCore.QCoreApplication.instance().code
    #
    # @property
    # def doodle_set(self) -> DoodleServer.Set.Doodlesetting:
    #     """
    #     获得核心设置
    #     :return:
    #     :rtype:
    #     """
    #     return QtCore.QCoreApplication.instance().doodle_set

    def __init__(self, parent=None):
        super(ProjectBrowserGUI, self).__init__(parent)

        # 加载颜色类
        self._color = _prjColor
        # 最近打开的文件夹
        self.recentlyOpenedFolder = ""
        # 设置UI
        self.setupUi(self)

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
        # 在文件中添加点击事件
        self.listfile.cellClicked.connect(lambda row, column: self.shotFileClicked(row))
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
        # 在listassfile中获得资产信息
        self.listAssFile.cellClicked.connect(lambda row, colume: self.assFileClicked(row))

        # 双击打开文件
        self.listfile.doubleClicked.connect(self.openShotFile)
        # 添加刷新函数
        self.refresh.triggered.connect(self.setepisodex)
        # 关闭ue链接函数
        self.close_socket.triggered.connect(self.closesocket)
        # 合成拍屏
        self.actioncom_video.triggered.connect(self.comEpsVideo)
        # 转换布料
        self.actionclothToFbx.triggered.connect(self.convertCloth)

        # <editor-fold desc="添加上下文菜单">
        # 添加集数上下文菜单
        self.listepisodes.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.listepisodes.customContextMenuRequested.connect(
            lambda pos: self.addRightClickMenu(self.listepisodes.mapToGlobal(pos), 'episodes'))
        # 添加镜头上下文菜单
        self.listshot.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.listshot.customContextMenuRequested.connect(
            lambda pos: self.addRightClickMenu(self.listshot.mapToGlobal(pos), "shot"))
        # 部门菜单
        self.listdepartment.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.listdepartment.customContextMenuRequested.connect(
            lambda pos: self.addRightClickMenu(self.listdepartment.mapToGlobal(pos), "department"))
        # 部门类型菜单
        self.listdepType.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.listdepType.customContextMenuRequested.connect(
            lambda pos: self.addRightClickMenu(self.listdepType.mapToGlobal(pos), "depType"))

        # 镜头文件菜单
        self.listfile.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.listfile.customContextMenuRequested.connect(
            lambda pos: self.addRightClickMenu(self.listfile.mapToGlobal(pos), "shotFile"))

        # 资产种类菜单
        self.listAss.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.listAss.customContextMenuRequested.connect(
            lambda pos: self.addRightClickMenu(self.listAss.mapToGlobal(pos), "assFolder"))
        # 资产类型菜单
        self.listAssType.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.listAssType.customContextMenuRequested.connect(
            lambda pos: self.addRightClickMenu(self.listAssType.mapToGlobal(pos), "assType"))
        # 资产文件菜单
        self.listAssFile.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.listAssFile.customContextMenuRequested.connect(
            lambda pos: self.addRightClickMenu(self.listAssFile.mapToGlobal(pos), "assFile"))
        # </editor-fold>

        self.pot_player = potplayer.PlayList()

    def tabWigetClick(self, index: int):
        """
        选项卡切换事件
        """
        if index == 0:
            logging.info("点击资产")
            QtCore.QCoreApplication.instance().codeToAss()
            self.setepisodex()
        elif index == 1:
            QtCore.QCoreApplication.instance().codeToShot()
            logging.info("点击镜头")
            self.assClassSortClicked("character")

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

    def listDepartmenClicked(self, item):
        """
        部门点击事件
        """
        self.clearTableFile(self.listfile)
        self.listdepType.clear()
        self.shot_thumbnail.clear()

        self.listdepType.addItems(self.core.queryFileType())
        # 设置颜色
        # state = self.shot.getFileState("DepType")
        # for s in state:
        #     self._setQlistItemColor(self.listdepType, s.Type, s.filestate)

    def listDepTypeClicked(self, item):
        """
        部门类型点击事件
        """
        self.shot.Type = item.text()

        # 清空上一次文件显示和版本记录和文件路径
        self.clearTableFile(self.listfile)
        self._setWidegtItem(self.core.queryFile(), self.listfile)

    def shotFileClicked(self, shot_row):
        """
        镜头文件点击事件
        """
        # shot_row = row
        # shot_row = self.listfile.currentRow()
        self.shot.version = int(self.listfile.item(shot_row, 0).text()[1:])
        self.shot.infor = self.listfile.item(shot_row, 1).text()
        self.shot.fileSuffixes = self.listfile.item(shot_row, 3).text()
        self.shot.query_id = int(self.listfile.item(shot_row, 4).text())


    # </editor-fold>

    # <editor-fold desc="更新ass的各种操作">
    def assClassSortClicked(self, ass_name: str):
        """
        按钮点击事件, 更新资产种类
        """
        self.ass.sort = ass_name
        logging.info('将资产类型设置为 %s', ass_name)

        self.listAss.clear()
        self.listAssType.clear()
        self.clearTableFile(self.listAssFile)

        self.ass_thumbnail.clear()

        # 通过mySql命令获得数据
        self.listAss.addItems(self.ass.getAssClass())
        # 设置颜色
        state = self.ass.getFileState("Class")
        for s in state:
            self._setQlistItemColor(self.listAss, s.name, s.filestate)

        for name, loa in self.ass.convertMy.name.items():
            try:
                item = self.listAss.findItems(name, QtCore.Qt.MatchExactly)[0]
            except IndexError:
                logging.error("找不到中文项目")
            else:
                item.setText(loa)

    def assClassClicked(self, item):
        """
        资产种类点击事件, 资产类型的更新
        """

        self.ass.name = self.ass.convertMy.toEn(item.text())  # self.listAssType.selectedItems()[0].text()

        self.listAssType.clear()
        logging.info('清除资产类型中的项数')
        self.clearTableFile(self.listAssFile)
        logging.info('清除资产文件中的项数')

        self.ass_thumbnail.clear()
        self.listAssType.addItems(self.ass.getAssType())
        # 设置颜色
        state = self.ass.getFileState("Type")
        for s in state:
            self._setQlistItemColor(self.listAssType, s.type, s.filestate)

    def assClassTypeClicked(self, item):
        """资产类别点击事件, 更新资产文件列表"""
        self.ass.Type = item.text()
        self.setThumbnail("ass", self.ass_thumbnail)
        # 清空上一次文件显示和版本记录和文件路径
        self.clearTableFile(self.listAssFile)
        self._setWidegtItem(self.ass.getFileInfo(), self.listAssFile)

    def assFileClicked(self, ass_row):
        # ass_row = self.listAssFile.currentRow()
        self.ass.version = int(self.listAssFile.item(ass_row, 0).text()[1:])
        self.ass.infor = self.listAssFile.item(ass_row, 1).text()
        self.ass.fileSuffixes = self.listAssFile.item(ass_row, 3).text()
        self.ass.query_id = int(self.listAssFile.item(ass_row, 4).text())

    # </editor-fold>
    # def assUploadMapHandle(self, soure_file: pathlib.Path, target: pathlib.Path, version: int):
    #     """
    #     上传贴图文件
    #     :param version:
    #     :param target:
    #     :param soure_file: pathlib.Path
    #     :return: Bool
    #     """
    #     pass
    #
    # def download(self, core: script.DooDlePrjCode.PrjCode):
    #     path = QtWidgets.QFileDialog.getExistingDirectory(self,
    #                                                       "选择同步目录",
    #                                                       self.recentlyOpenedFolder,
    #                                                       QtWidgets.QFileDialog.ShowDirsOnly)
    #     pathprj = pathlib.Path(path)
    #     # is_enpty = True
    #     # for p in pathprj.iterdir():
    #     #     is_enpty = False
    #     #     break
    #     # if not is_enpty:
    #     #     QtWidgets.QMessageBox.warning(self, "警告", "请选择空目录",
    #     #                                   QtWidgets.QMessageBox.Yes)
    #     #     return None
    #     if isinstance(core, script.DooDlePrjCode.PrjAss):
    #         cls_file = doodleFileFactory(self.ass, ".uproject")
    #         if cls_file:
    #             cls_file = cls_file(core, self.setlocale)
    #             cls_file.down()
    #
    #         QtWidgets.QMessageBox.critical(self, "复制中", "请等待.....")
    #         logging.info(path)
    #
    #
    # def andTranslate(self):
    #     text = self.listAss.selectedItems()[0].text()
    #     self.ass.convertMy.getnameTochinese()
    #     try:
    #         self.ass.convertMy.local_name[text]
    #     except KeyError:
    #         self.ass.convertMy.addLocalName(self.ass.convertMy.toEn(text), text)
    #     else:
    #         logging.info("库中已经储存此键值,无需上传中文名称")
    #
    # # </editor-fold>
    #
    # # <editor-fold desc="各种对于文件的操作">
    #
    # def exportMaya(self):
    #     """
    #     导出maya相机和动画FBX
    #     """
    #     file_data = self.shot.queryFileName(self.shot.query_id)
    #
    #     logging.info(file_data)
    #     if file_data:
    #         QtWidgets.QMessageBox.warning(self, "警告", "不要关闭弹出窗口",
    #                                       QtWidgets.QMessageBox.Yes)
    #
    #         export = shotMayaExportFile(self.shot, self.setlocale)
    #         export.infor = "这是maya导出文件"
    #         export.subDataToBD(file_data)
    #
    #         self.listDepTypeClicked(self.listdepType.selectedItems()[0])
    #
    # def Screenshot(self, my_type: str, thumbnail: QtWidgets.QLabel):
    #     """
    #     截图保存动作
    #     """
    #     # 获得核心
    #     core: script.DooDlePrjCode.PrjCode = getattr(self, my_type)
    #     # 判断类型
    #     cls_sshot = doodleFileFactory(core, "Screenshot")(core, self.setlocale)
    #     cls_sshot.infor = "这是截图"
    #     # 上传截屏
    #     with cls_sshot.upload() as cache:
    #         screen_shot = script.DoodlePlayer.doodleScreenshot(path=cache.as_posix())
    #         self.hide()
    #         screen_shot.exec_()
    #         self.show()
    #     self.setThumbnail(my_type, thumbnail)
    #
    # def setThumbnail(self, type_: str, thumbnail: QtWidgets.QLabel):
    #     """
    #     设置截图显示
    #     """
    #     core = getattr(self, type_)
    #     # 获得截图类
    #     cls_sshot = doodleFileFactory(core, "Screenshot")(core, self.setlocale)
    #     # 下载文件
    #     path = cls_sshot.down()
    #
    #     pixmap = QtGui.QPixmap(str(path))
    #     pixmap = pixmap.scaled(thumbnail.geometry().size(), QtCore.Qt.KeepAspectRatio)
    #     thumbnail.setPixmap(pixmap)
    #
    # def uploadFlipBook(self, code: script.DooDlePrjCode.PrjCode):
    #     """
    #     上传拍屏 多线程
    #     :return: None
    #     """
    #     file, file_type = QtWidgets.QFileDialog.getOpenFileName(self,
    #                                                             "选择上传文件",
    #                                                             self.recentlyOpenedFolder,
    #                                                             "files (*.mp4 *.avi *.mov *.exr "
    #                                                             "*.png *.tga *.jpg)")
    #
    #     self.recentlyOpenedFolder = file
    #     # 获得拍屏类
    #     cla_FB = assFBFile(code, self.setlocale)
    #     cla_FB.infor = "这是拍屏"
    #     cla_FB.upload(file)
    #     self.listDepartmenClicked(self.listdepartment.selectedItems()[0])
    #
    # def playerButtenClicked(self, one_or_mut: str, department="Anm"):
    #     """
    #     打开拍屏
    #     """
    #     tmp_path = os.path.join(tempfile.gettempdir(), "potplayer_temp.dpl")
    #     self.pot_player = potplayer.PlayList()
    #     if one_or_mut == "one":
    #         path = pathlib.Path("")
    #         if self.listAssType.selectedItems():
    #             code = self.ass
    #         else:
    #             code = self.shot
    #         player = doodleFileFactory(code, "FB")(code, self.setlocale)
    #
    #         path = player.downPlayer(code.Type)
    #
    #         while player.syn.is_alive():
    #             pass
    #
    #         if path:
    #             self.pot_player.add(path.as_posix())
    #     else:
    #         player = shotMayaFBFile(self.shot, self.setlocale)
    #         video = player.getEpisodesFlipBook()
    #
    #         while player.syn.is_alive():
    #             pass
    #
    #         if video:
    #             self.pot_player.add(video)
    #         else:
    #             reply = QtWidgets.QMessageBox.warning(self, "警告:", "没有找到转换视频，是否执行自动转换",
    #                                                   QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
    #             if reply == QtWidgets.QMessageBox.Yes:
    #                 # 合成视频
    #                 video = player.makeEpisodesFlipBook()
    #
    #                 self.pot_player.dump(video.as_posix())
    #             else:
    #                 return None
    #
    #     self.pot_player.dump(tmp_path)
    #     try:
    #         potplayer.run(tmp_path)
    #     except:
    #         QtWidgets.QMessageBox.warning(self, "警告:", "警告:请关闭360后重新打开本软件,或者检查安装potplayer",
    #                                       QtWidgets.QMessageBox.Yes)
    #
    # def comEpsVideo(self):
    #     player = shotMayaFBFile(self.shot, self.setlocale)
    #     video = player.makeEpisodesFlipBook()
    #     return video
    #
    # def subInfo(self, code: script.DooDlePrjCode.PrjCode):
    #     """
    #     修改评论
    #     """
    #     info, is_input = QtWidgets.QInputDialog.getText(self, "输入信息", "", QtWidgets.QLineEdit.Normal)
    #     if is_input:
    #         if not re.findall(r"\|", info):
    #             code.infor += "|" + info
    #             code.undataInformation(code.query_id)
    #
    # def markFileStart(self, code: script.DooDlePrjCode.PrjCode):
    #     """
    #     标记文件状态
    #     """
    #     items = self.setlocale.filestate
    #     ass_type, is_type = QtWidgets.QInputDialog.getItem(self, "标记文件状态", "要先选中文件", items, 0, False)
    #     info, is_input = QtWidgets.QInputDialog.getText(self, "输入信息", "", QtWidgets.QLineEdit.Normal)
    #     if is_type and is_input:
    #         code.filestate = ass_type
    #         code.infor = f"| {self.setlocale.user}:  {info}"
    #         code.undataInformation(code.query_id)
    #     logging.info("%s , %s", ass_type, info)

    # def importUe(self):
    #     address = ("127.0.0.1", 23335)
    #     so = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #     try:
    #         so.connect(address)
    #         maya_export = shotMayaExportFile(self.shot, self.setlocale)
    #         content = maya_export.down(self.shot.query_id)
    #
    #         data = {"eps": self.shot.episodes, "shot": self.shot.shot, "content": json.loads(content)}
    #
    #         so.send(json.dumps(data, ensure_ascii=False, indent=4, separators=(',', ':')).encode("utf-8"))
    #         so.close()
    #     except ConnectionRefusedError:
    #         logging.info("导入ue失败")
    #     else:
    #         logging.info("成功导入ue")

    # @staticmethod
    # def closesocket():
    #     address = ("127.0.0.1", 23335)
    #     so = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #     try:
    #         so.connect(address)
    #         data = "close"
    #         so.send(data.encode("utf-8"))
    #         so.close()
    #     except ConnectionRefusedError:
    #         logging.info("关闭链接失败")
    #     else:
    #         logging.info("成功关闭链接")
    #
    # def convertCloth(self):
    #     shotMayaClothExportFile(self.shot, self.setlocale).down(self.shot.query_id)
    # </editor-fold>


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet())
    w = ProjectBrowserGUI()
    w.setWindowTitle("Remer")
    w.show()

    sys.exit(app.exec_())
