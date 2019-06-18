# ..................................................................
# This python file converts xml files to csv files
# ..................................................................
import os
import glob
import argparse
import pandas as pd
import xml.etree.cElementTree as ET

parser = argparse.ArgumentParser()
parser.add_argument('--xml_dir', help='name of the dir where xml files are present')
parser.add_argument('--output_dir', help='output dir where csv file will be placed')
parser.add_argument('--filename', help='name of the file')
parser = parser.parse_args()

CWD = os.getcwd()
XML_DIR = parser.xml_dir
OUTPUT_DIR = parser.output_dir
FILENAME = parser.filename
COLUMNS = ['filename', 'width', 'height', 'class', 'xmin', 'ymin', 'xmax', 'ymax']

xml_val = []

for xml in glob.glob(os.path.join(CWD, XML_DIR, '*.xml')):
    tree = ET.parse(xml)
    root = tree.getroot()

    for child in root.findall('object'):
        value = (root.find('filename').text,
                 int(root.find('size')[0].text),
                 int(root.find('size')[1].text),
                 child[0].text,
                 int(child[4][0].text),
                 int(child[4][1].text),
                 int(child[4][2].text),
                 int(child[4][3].text))
        xml_val.append(value)

df = pd.DataFrame(data=xml_val, columns=COLUMNS)
df.to_csv(os.path.join(CWD, OUTPUT_DIR, FILENAME), index=None)

print(FILENAME, 'created successfully')
