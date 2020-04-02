# -*- coding: UTF-8 -*-
# try:
#     import xml.etree.cElementTree as ET
# except:
#     import xml.etree.ElementTree as ET
import xml.etree.cElementTree as ET
import pathlib


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


def weiteXml(doc: pathlib.Path, synFile: list, Filter={}, fileName='ff') -> pathlib.Path:
    '''传入对象是一个写入文件的路径和一个同步列表,过滤器名称,文件名

    这个列表由一个key是Left和Right的字典构成'''
    tree = ET.parse("tools\\template\\temp.ffs_batch")
    # 加入同步目录
    for syn in synFile:
        pair = ET.SubElement(tree.findall('./FolderPairs')[0], 'Pair')
        LElement = ET.SubElement(pair, "Left")
        LElement.text = syn['Left']
        RElement = ET.SubElement(pair, "Right")
        RElement.text = syn['Right']
    # 查看是否具有过滤器,如果有就删除原来过滤器后添加传入过滤器
    try:
        includes = Filter['include']
    except:
        pass
    else:
        include_my = tree.findall('./Filter/Include')[0]
        include_my.remove(include_my.findall('./Item')[0])
        for include_i in includes:
            includepath = ET.SubElement(include_my, 'Item')
            includepath.text = include_i
    # 将xml文档格式化
    root = tree.getroot()
    indent(root)
    # 获取写入文件路径和文件命
    writePath = doc.joinpath('{}.ffs_batch'.format(fileName))
    # 写入文件
    tree.write(writePath, encoding='utf-8', xml_declaration=True)
    return writePath
