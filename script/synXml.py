# -*- coding: UTF-8 -*-
# try:
#     import xml.etree.cElementTree as ET
# except:
#     import xml.etree.ElementTree as ET
import xml.etree.cElementTree as Et
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


def weiteXml(doc: pathlib.Path, synFile: list,**syn_parameter) -> pathlib.Path:
    '''传入对象是一个写入文件的路径和一个同步列表,
    key : fileName Include Exclude Variant VersioningFolder
    Variant(TwoWay,Update)
    这个列表由一个key是Left和Right的字典构成'''
    template_path = pathlib.Path("tools\\template\\temp.ffs_batch")
    tree = Et.parse(str(template_path))
    # 加入同步目录
    for syn in synFile:
        pair = Et.SubElement(tree.findall('./FolderPairs')[0], 'Pair')
        LElement = Et.SubElement(pair, "Left")
        LElement.text = syn['Left']
        RElement = Et.SubElement(pair, "Right")
        RElement.text = syn['Right']

    # 查看是否具有过滤器,如果有就删除原来过滤器后添加传入过滤器
    if 'Include' in syn_parameter.keys():
        includes = syn_parameter['Include']
        include_my = tree.findall('./Filter/Include')[0]
        include_my.remove(include_my.findall('./Item')[0])
        for include_i in includes:
            includepath = Et.SubElement(include_my, 'Item')
            includepath.text = include_i
    if 'Exclude' in syn_parameter.keys():
        exclude = syn_parameter['Exclude']
        exclude_my = tree.findall('./Filter/Exclude')[0]
        for exclude_i in exclude:
            exclude_path = Et.SubElement(exclude_my, 'Item')
            exclude_path.text = exclude_i
    # 设置同步方式
    if 'Variant' in syn_parameter.keys():
        variant = syn_parameter['Variant']
        variant_my = tree.findall('./Synchronize/Variant')[0]
        variant_my.text = variant
    # 设置同步时备份目录
    if 'VersioningFolder' in syn_parameter.keys():
        versioningFolder = syn_parameter['VersioningFolder']
        VersioningFolder_my = tree.findall('./Synchronize/VersioningFolder')[0]
        VersioningFolder_my.text = versioningFolder
    # 将xml文档格式化
    root = tree.getroot()
    indent(root)
    # 获取写入文件路径和文件命
    writePath = doc.joinpath('{}.ffs_batch'.format(syn_parameter['fileName']))
    # 写入文件
    tree.write(writePath, encoding='utf-8', xml_declaration=True)
    return writePath
