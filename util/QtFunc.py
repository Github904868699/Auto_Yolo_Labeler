import os
from PIL import Image
import xml.etree.ElementTree as ET

from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox


def upWindowsh(hint):
    messBox = QMessageBox()
    messBox.setWindowTitle(u'提示')
    messBox.setText(hint)
    messBox.exec_()


def list_images_in_directory(directory):
    image_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                image_files.append(os.path.join(root, file))
    return image_files


# 修改照片大小
def Change_image_Size(image_path):
    # 打开原图像
    original_image = Image.open(image_path)
    # 获取照片大小
    width, height = original_image.size
    ratio = 1300 / width
    width = 1300
    height *= ratio
    reduced_image = original_image.resize((int(width), int(height)))
    if height > 850:
        ratio = 850 / height
        height = 850
        width *= ratio
        reduced_image = original_image.resize((int(width), int(height)))
    reduced_image.save((image_path))
    return image_path, int(width), int(height)


def list_label(label_path):
    with open(label_path, 'r') as file:
        content = file.read()
    root = ET.fromstring(content)

    objects = root.findall('object')

    list_labels = []
    list_box = []
    for obj in objects:
        name = obj.find('name').text
        xmin = int(obj.find('bndbox/xmin').text)
        ymin = int(obj.find('bndbox/ymin').text)
        xmax = int(obj.find('bndbox/xmax').text)
        ymax = int(obj.find('bndbox/ymax').text)

        if xmax <= xmin and xmax > 0:
            xmax = xmin + xmax
        if ymax <= ymin and ymax > 0:
            ymax = ymin + ymax

        box = [xmin, ymin, xmax, ymax]
        list_labels.append(name)
        list_box.append(box)
    return list_labels,list_box


def get_labels(label_path):
    with open(label_path, 'r') as file:
        content = file.read()
    root = ET.fromstring(content)

    get_list_label = []

    for obj in root.findall('object'):
        item = {
            'name': obj.find('name').text,
            'pose': obj.find('pose').text,
            'truncated': int(obj.find('truncated').text),
            'difficult': int(obj.find('difficult').text),
            'bndbox': [
                int(obj.find('bndbox/xmin').text),
                int(obj.find('bndbox/ymin').text),
                int(obj.find('bndbox/xmax').text),
                int(obj.find('bndbox/ymax').text)
            ]
        }
        x_min, y_min, x_max, y_max = item['bndbox']
        if x_max <= x_min and x_max > 0:
            x_max = x_min + x_max
        if y_max <= y_min and y_max > 0:
            y_max = y_min + y_max
        item['bndbox'] = [x_min, y_min, x_max, y_max]

        get_list_label.append(item)

    return get_list_label


