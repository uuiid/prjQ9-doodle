import logging
import pathlib
import os
import shutil
import subprocess
import sys
import numpy
import filecmp
import script.synXml
import tempfile
import multiprocessing
import script.doodle_setting


class synFile(object):
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
    def minclude(self):
        if not hasattr(self, '_include'):
            self._include = ['.']
        return self._include

    @minclude.setter
    def minclude(self, minclude):
        self._include = minclude

    @file_db.setter
    def file_db(self, file_db):
        self._file_db = file_db

    def __init__(self, left: pathlib.Path, right: pathlib.Path, ignore=''):
        self.doodleSet = script.doodle_setting.Doodlesetting()
        self._left = left
        self._right = right
        # self._file_db = left.joinpath("Sql_syn_file.db")
        # if self.file_db.is_file():
        #     pass
        # else:
        #     pass

    def getFilePath(self):
        for l_root, dirs, names in os.walk(str(self.left)):
            for name in names:
                r_root = l_root.replace(str(self.left), str(self.right))
                print(f"""{l_root}\\{name}""")
                print(f"""{r_root}\\{name}""")

    def copyAndBakeup(self, is_dir: bool):
        backup = self.right.joinpath("backup")
        tem = pathlib.Path(tempfile.gettempdir())
        synlist = [{"Left": str(self.left), "Right": str(self.right)}]
        if is_dir:
            # pool = multiprocessing.Pool(processes=4)
            for root, dors, files in os.walk(str(self.left)):
                for file in files:
                    left_file = os.path.join(root, file)
                    right_file = left_file.replace(str(self.left), str(self.right))
                    shutil.copy2(left_file, right_file)
                    logging.info( "%s-------%s",left_file,right_file)
                    # pool.apply(_copyfile, (left_file, right_file))
            # pool.close()
            # pool.join()
            # synfile = script.synXml.weiteXml(tem,synlist,Exclude=["backup"],VersioningFolder=[str(backup)])
        else:
            if not backup.is_dir():
                backup.mkdir()
            # synfile = script.synXml.weiteXml(tem, synlist, Exclude=["backup"], VersioningFolder=[str(backup)])
        # program = self.doodleSet.FreeFileSync
        # subprocess.run('{} "{}"'.format(program, synfile), shell=True)


def _copyfile(left: str, right: str):
    """
    复制文件的多线程函数
    :param left: str
    :param right: str
    :return:
    """
    print(left + '--------' + right)
    shutil.copy2(left, right)


if __name__ == '__main__':
    left = pathlib.Path("D:\\image")
    right = pathlib.Path("F:\\image")

    test = synFile(left, right, version=0)
    test.copyAndBakeup(True)
    # path = getFilePath(str(left.stem),str(left.parent),[])
    # for i in os.walk(str(left)):
    #     print(i)
