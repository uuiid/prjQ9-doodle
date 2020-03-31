# -*- coding: UTF-8 -*-
# try:
#     import xml.etree.cElementTree as ET
# except:
#     import xml.etree.ElementTree as ET
import xml.etree.cElementTree as ET
import pathlib

def indent(elem, level=0):
    i = "\n" + level*"\t"
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "\t"
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i

def weiteXml(doc: pathlib.Path, synFile: list, fileName: str) -> pathlib.Path:
    '''传入对象时一个写入文件的路径和一个列表,文件名

    这个列表由一个key是Left和Right的字典构成'''
    tree = ET.parse("tools\\template\\temp.ffs_batch")

    for syn in synFile:
        pair = ET.SubElement(tree.findall('./FolderPairs')[0],'Pair')
        LElement = ET.SubElement(pair, "Left")
        LElement.text = syn['Left']
        RElement = ET.SubElement(pair, "Right")
        RElement.text = syn['Right']
    root = tree.getroot()
    indent(root)
    writePath = doc.joinpath('{}.ffs_batch'.format(fileName))
    tree.write(writePath, encoding='utf-8', xml_declaration=True)
    return writePath
