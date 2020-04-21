import pathlib
import subprocess
import sqlite3
import filecmp
import os


class fileSyn(object):
    @property
    def left(self) -> pathlib.Path:
        if not hasattr(self, '_left'):
            self._left = ''
        return self._left

    @left.setter
    def left(self, left):
        self._left = left

    @property
    def right(self) -> pathlib.Path:
        if not hasattr(self, '_right'):
            self._right = ''
        return self._right

    @right.setter
    def right(self, right):
        self._right = right

    @property
    def file_db(self) -> pathlib.Path:
        if not hasattr(self, '_file_db'):
            self._file_db = ''
        return self._file_db

    @property
    def ignore(self):
        if not hasattr(self, '_ignore'):
            self._ignore = ''
        return self._ignore

    @ignore.setter
    def ignore(self, ignore):
        self._ignore = ignore

    @property
    def include(self):
        if not hasattr(self, '_include'):
            self._include = ['.']
        return self._include

    @include.setter
    def include(self, include):
        self._include = include

    @file_db.setter
    def file_db(self, file_db):
        self._file_db = file_db

    def __init__(self, left: pathlib.Path, right: pathlib.Path, ignore=''):
        self._left = left
        self._right = right
        self._file_db = left.joinpath("Sql_syn_file.db")
        if self.file_db.is_file():
            pass
        else:
            pass

    def fileComp(self):
        file_match_list = []
        file_left_list = []
        file_right_list = []
        # for _, _, lift_file in os.walk():
        #     lift_file = pathlib.Path(lift_file)
        #     if not lift_file.is_dir():
        #         right_path_file = self.right.joinpath(lift_file.relative_to(self.left))
        #         if filecmp.cmp(lift_file, right_path_file.right, True):
        #             print(lift_file)
        #             print(right_path_file)
        #             file_match_list.append(lift_file)
        #         else:
        #             file_left_list.append(lift_file)
        #
        # for right_file in self.right.glob('**'):
        #     if not right_file.is_dir():
        #         if filecmp.cmp(self):
        #             pass
        # test = filecmp.cmpfiles(self.left, self.right,['**'], shallow=True)
        # print(test)
        # match= filecmp.dircmp(self.left, self.right)
        # print(file_match_list)
        # print(file_left_list)
        # print(errors)


if __name__ == '__main__':
    left = pathlib.Path("D:\\Source\\UnrealEngine\\Engine\\Binaries")
    right = pathlib.Path("W:\\data\\Source\\UnrealEngine\\Engine\\Binaries")

    test = fileSyn(left, right)
    test.fileComp()
