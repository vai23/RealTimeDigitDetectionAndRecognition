# ..................................................................
#   This python file extract information
#   from dataStruct.mat file contained in
#   SVHN dataset and save it in PASCAL VOC
#   XML format.
#
#   To run this file:
#
#   python3 mat_to_xml.py --image_dir='path to images' \
#       --mat_dir='dir path in which mat file is present' \
#       --mat_file_name='name of the mat file'
# ...................................................................
import os
import cv2
import argparse
import h5py as h5
import xml.etree.cElementTree as ET

parser = argparse.ArgumentParser()
parser.add_argument('--image_dir', help='name of directory where images are present')
parser.add_argument('--mat_dir', help='name of directory where mat file is present')
parser.add_argument('--mat_file_name', help='name of the mat file')
parser = parser.parse_args()

CWD = os.getcwd()
IMAGE_FOLDER = parser.image_dir
MAT_FOLDER = parser.mat_dir
MAT_FILE_NAME = parser.mat_file_name

f = h5.File(os.path.join(CWD, MAT_FOLDER, MAT_FILE_NAME))

for i in range(len(f['digitStruct']['name'])):
    annotation_ = ET.Element('annotation')
    folder_ = ET.SubElement(annotation_, 'folder')
    folder_.text = IMAGE_FOLDER

    name = f[f['digitStruct']['name'][i][0]][()].tobytes()[::2].decode()

    filename_ = ET.SubElement(annotation_, 'filename')
    filename_.text = name

    path_ = ET.SubElement(annotation_, 'path')
    path_.text = os.path.join(CWD, IMAGE_FOLDER, name)

    source_ = ET.SubElement(annotation_, 'source')
    database_ = ET.SubElement(source_, 'database')
    database_.text = 'Unknown'

    size_ = ET.SubElement(annotation_, 'size')
    width_ = ET.SubElement(size_, 'width')
    height_ = ET.SubElement(size_, 'height')
    depth_ = ET.SubElement(size_, 'depth')

    image = cv2.imread(os.path.join(CWD, IMAGE_FOLDER, name))

    (height_.text, width_.text, depth_.text) = map(str, image.shape)

    segmented_ = ET.SubElement(annotation_, 'segmented')
    segmented_.text = str(0)

    for j in range(len(f[f['digitStruct']['bbox'][i][0]]['label'][()])):
        label = f[f['digitStruct']['bbox'][i][0]]['label'][()][j][0]
        width = f[f['digitStruct']['bbox'][i][0]]['width'][()][j][0]
        height = f[f['digitStruct']['bbox'][i][0]]['height'][()][j][0]
        top = f[f['digitStruct']['bbox'][i][0]]['top'][()][j][0]
        left = f[f['digitStruct']['bbox'][i][0]]['left'][()][j][0]
        # f[f[f['digitStruct']['bbox'][i][0]]['left'][()][j][0]][()][0][0]

        if str(label.__class__) == "<class 'h5py.h5r.Reference'>":
            label = f[label][0][0]
            width = f[width][0][0]
            height = f[height][0][0]
            top = f[top][0][0]
            left = f[left][0][0]

        x1 = int(left)
        y1 = int(top)
        x2 = int(x1 + width)
        y2 = int(y1 + height)

        object_ = ET.SubElement(annotation_, 'object')
        name_ = ET.SubElement(object_, 'name')
        pose_ = ET.SubElement(object_, 'pose')
        truncated_ = ET.SubElement(object_, 'truncated')
        difficult_ = ET.SubElement(object_, 'difficult')
        bndbox_ = ET.SubElement(object_, 'bndbox')
        xmin_ = ET.SubElement(bndbox_, 'xmin')
        ymin_ = ET.SubElement(bndbox_, 'ymin')
        xmax_ = ET.SubElement(bndbox_, 'xmax')
        ymax_ = ET.SubElement(bndbox_, 'ymax')

        if label == 10:
            label = 0

        name_.text = str(int(label))
        pose_.text = 'Unspecified'
        truncated_.text = str(0)
        difficult_.text = str(0)
        xmin_.text = str(min(x1, x2))
        ymin_.text = str(min(y1, y2))
        xmax_.text = str(max(x1, x2))
        ymax_.text = str(max(y1, y2))

    tree = ET.ElementTree(annotation_)
    tree.write(os.path.join(CWD, IMAGE_FOLDER, str(i + 1) + '.xml'))
    # print('XML of ' + name + ' file created')

print('PASCAL VOC xml of ' + str(len(f['digitStruct']['name'])) + ' images created')
