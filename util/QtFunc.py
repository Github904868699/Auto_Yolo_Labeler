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
    """计算图像在界面中的显示尺寸并返回缩放比例。

    该函数仅根据原始图像尺寸计算目标显示尺寸，
    不会对磁盘上的原图进行任何修改。

    Returns:
        tuple: (target_width, target_height, scale_ratio)
    """

    with Image.open(image_path) as original_image:
        width, height = original_image.size

    if width == 0 or height == 0:
        return 0, 0, 1.0

    max_width = 1300
    max_height = 850

    width_ratio = max_width / width
    height_ratio = max_height / height
    scale_ratio = min(width_ratio, height_ratio)

    target_width = max(1, int(round(width * scale_ratio)))
    target_height = max(1, int(round(height * scale_ratio)))

    return target_width, target_height, scale_ratio


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


