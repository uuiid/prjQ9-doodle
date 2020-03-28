# -*- coding: UTF-8 -*-
# try:
#     import xml.etree.cElementTree as ET
# except:
#     import xml.etree.ElementTree as ET
import xml.etree.ElementTree as ET
import pathlib


def weiteXml(doc: pathlib.Path, synFile: list) -> pathlib.Path:
    '''传入对象时一个写入文件的路径和一个列表,

    这个列表由一个key是Left和Right的字典构成'''
    tree = ET.parse("tools\\template\\temp.ffs_batch")

    for syn in synFile:
        LElement = ET.SubElement(tree.findall('./FolderPairs/Pair')[0], "Left")
        LElement.text = syn['Left']
        RElement = ET.SubElement(tree.findall('./FolderPairs/Pair')[0], "Right")
        RElement.text = syn['Right']

    writePath = doc.joinpath('test.ffs_batch')
    tree.write(writePath, encoding='utf-8', xml_declaration=True)
    return writePath


print(weiteXml(doc, synFile))
