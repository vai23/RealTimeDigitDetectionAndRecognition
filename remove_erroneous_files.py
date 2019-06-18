# ..................................................................
# This python file removes erroneous xml file
# ..................................................................
import os
import glob
import argparse
import xml.etree.cElementTree as ET

parser = argparse.ArgumentParser()
parser.add_argument('--xml_dir', help='dir where xml of all images are stored')

parser = parser.parse_args()

CWD = os.getcwd()
XML_DIR = parser.xml_dir

for xml in glob.glob(os.path.join(CWD, XML_DIR, '*.xml')):
    tree = ET.parse(xml)
    root = tree.getroot()

    error = False

    width = int(root.find('size')[0].text)
    height = int(root.find('size')[1].text)

    for child in root.findall('object'):
        xmin = int(child[4][0].text)
        ymin = int(child[4][1].text)
        xmax = int(child[4][2].text)
        ymax = int(child[4][3].text)

        if not (0 <= xmin <= width and 0 <= xmax <= width and
                0 <= ymin <= height and 0 <= ymax <= height):
            error = True
            break
    if error:
        os.remove(root.find('path').text)
        os.remove(xml)

        # print(xml + ' removed')
        # print(root.find('path').text + ' removed')
print('DONE')
