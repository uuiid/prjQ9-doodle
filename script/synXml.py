# -*- coding: UTF-8 -*-
import subprocess
import xml.etree.cElementTree as Et
import pathlib
import shutil


def indent(elem, level=0):
    i = "\n" + level * "\t"
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "\t"
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level + 1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i


class FreeFileSync(object):

    def __init__(self,
                 program: str,
                 user: str,
                 ip_,
                 password: str,
                 doc=pathlib.Path(""),
                 syn_file=(),
                 file_name="",
                 include=(),
                 exclude=(),
                 variant="",
                 versioning_folder=""):
        """
        Args:
            program: 程序所在位置
            user: 用户名称暂时用来定位项目
            ip_: ftp服务器所在ip
            password: ftp密码
            doc: 用户文档所在用户文档所在位置，也是写入配置位置
            syn_file: 同步文件夹对
                [{Left:path,Right:path},{Left:path,Right:path}]
            file_name: 配置文件名称
            include: 包含过滤器
            exclude: 排除过滤器
            variant: 同步方式
            versioning_folder: 备份位置
        """
        self.program = program
        self.tree = Et.parse(pathlib.Path("tools\\template\\temp.ffs_batch").as_posix())

        self.pair = Et.SubElement(self.tree.findall('./FolderPairs')[0], 'Pair')
        self.user = user
        self.ip_ = ip_
        self.password = password
        self.doc_: pathlib.Path = doc
        self.file_name = file_name

        self.config_path = pathlib.Path("")

        # 加入同步目录
        self.addSynFile(syn_file)

        # 查看是否具有过滤器,如果有就删除原来过滤器后添加传入过滤器
        if include:
            self.addInclude(include)
        if exclude:
            self.addExclude(exclude)
        # 设置同步方式
        if variant:
            self.setVariant(variant)
        # 设置同步时备份目录
        if versioning_folder:
            self.setVersioningFolder(versioning_folder,3)
        # 将xml文档格式化
        # 复制出全局设置
        self.__copyGlob()

    def run(self):
        self.write()
        subprocess.Popen([self.program, self.config_path.as_posix(), self.golb_setting.as_posix()])

    def write(self):
        self.__indentTree()
        # 获取写入文件路径和文件命
        self.config_path = self.doc_.joinpath('{}.ffs_batch'.format(self.file_name))
        # 写入文件
        self.tree.write(self.config_path.as_posix(), encoding='utf-8', xml_declaration=True)

    def addSynFile(self, syn_file: list):
        for syn in syn_file:
            l_element = Et.SubElement(self.pair, "Left")
            l_element.text = syn['Left']
            r_element = Et.SubElement(self.pair, "Right")
            r_element.text = "ftp://{user}@{ip_}:21{path}|pass64={password}".format(user=self.user,
                                                                                    ip_=self.ip_,
                                                                                    path=self.testpath(syn['Right']),
                                                                                    password=self.password)

    def addInclude(self, include: list):
        include_my = self.tree.findall('./Filter/Include')[0]
        for include_i in include:
            includepath = Et.SubElement(include_my, 'Item')
            includepath.text = include_i

    def addExclude(self, exclude: list):
        exclude_my = self.tree.findall('./Filter/Exclude')[0]
        for exclude_i in exclude:
            exclude_path = Et.SubElement(exclude_my, 'Item')
            exclude_path.text = exclude_i

    def setVariant(self, variant):
        variant_my = self.tree.findall('./Synchronize/Variant')[0]
        variant_my.text = variant

    def setVersioningFolder(self, versioning_folder, max_age=-1):
        versioning_folder_my = self.tree.findall('./Synchronize/VersioningFolder')[0]
        versioning_folder_my.text = versioning_folder
        if max_age > 0:
            versioning_folder_my.set("MaxAge", max_age.__str__())

    def __indentTree(self):
        root = self.tree.getroot()
        indent(root)

    def __copyGlob(self):
        self.golb_setting = self.doc_.joinpath("golb_setting")
        shutil.copy2("tools\\template\\_GlobalSettings.xml", self.golb_setting.as_posix())

    @staticmethod
    def testpath(path: str):
        path = pathlib.Path(path)
        if path.drive:
            return path.as_posix()[2:]
        else:
            return path.as_posix()
