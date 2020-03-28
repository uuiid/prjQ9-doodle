#coding=utf-8
import os
import xml.etree.ElementTree as ET

filepath = "C:/Users/teXiao/Documents/template.ffs_batch"

tree = ET.parse(filepath)
root = tree.getroot()
for neighbor in root.iter('Item'):
    print(neighbor.tag, neighbor.attrib, neighbor.text)
# for neighbor in root.itertext():
#     print(neighbor)
# for country in root.findall('country'):
#     rank = country.find('Variant').text
#     print(rank)
# for child in root:
#     print(child.tag,child.attrib)