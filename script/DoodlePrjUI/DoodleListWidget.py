import sys

import typing
from PySide2 import QtCore, QtGui, QtWidgets

import DoodleServer


class EpisodesListWidgetItem(QtWidgets.QListWidgetItem):
    _eps_data_: DoodleServer.DoodleOrm.Episodes

    @property
    def eps_data(self):
        if not hasattr(self, '_eps_data_'):
            self._eps_data_ = DoodleServer.DoodleOrm.Episodes()
        return self._eps_data_

    @eps_data.setter
    def eps_data(self, eps_data):
        self._eps_data_ = eps_data
        self.setText('ep{:0>3d}'.format(self._eps_data_.episodes))


class EpisodesListWidget(QtWidgets.QListWidget):
    player = QtCore.Signal(EpisodesListWidgetItem, str)

    select_item: EpisodesListWidgetItem

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.select_item = None
        # self.setupUi(self)

    def contextMenuEvent(self, arg__1: QtGui.QContextMenuEvent):
        # print(arg__1)
        menu = QtWidgets.QMenu(self)
        add_episodes_folder = menu.addAction('添加')
        add_episodes_folder.triggered.connect(self.addEpisodesFolder)
        add_player = menu.addMenu("播放整集拍屏")
        anm_player = add_player.addAction("播放Anm拍屏")
        vfx_player = add_player.addAction("播放vfx拍屏")
        light_player = add_player.addAction("播放light拍屏")
        anm_player.triggered.connect(lambda: self.player.emit(self.currentItem(), "Anm"))
        vfx_player.triggered.connect(lambda: self.player.emit(self.currentItem(), "VFX"))
        light_player.triggered.connect(lambda: self.player.emit(self.currentItem(), "Light"))
        menu.move(QtGui.QCursor().pos())
        return menu.show()

    def itemClicked(self, *args, **kwargs):
        print("ok")

    @QtCore.Slot()
    def addEpisodesFolder(self):
        episode, is_ok = QtWidgets.QInputDialog.getInt(self, '输入集数', "ep", 1, 1, 999, 1)
        if is_ok:
            item = EpisodesListWidgetItem()
            item.eps_data = DoodleServer.DoodleOrm.Episodes(episodes=episode)
            self.addItem(item)

    def addItems(self, labels: typing.List[DoodleServer.DoodleOrm.Episodes], p_str=None):
        for i in labels:
            item = EpisodesListWidgetItem()
            item.eps_data = i
            self.addItem(item)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = EpisodesListWidget()
    w.addItems(DoodleServer.Core.PrjShot(DoodleServer.DoodleSet.Doodlesetting()).queryEps())
    w.setWindowTitle("Remer")
    w.show()

    sys.exit(app.exec_())
