import matplotlib.pyplot as plt
from PIL import Image, ImageDraw
from xml.etree.ElementTree import parse
import shutil
import os
from data.image_file_data import ImageFileData


def load_xml(xml_file_path):
    file_data = ImageFileData()
    tree_xml = parse(xml_file_path)
    root_xml = tree_xml.getroot()

    file_data.file_name = root_xml.findtext('filename')
    file_data.path = root_xml.findtext('path')

    size_xml = root_xml.find("size")

    file_data.image_width = int(size_xml.findtext('width'))
    file_data.image_height = int(size_xml.findtext('height'))
    file_data.image_channel = int(size_xml.findtext('depth'))

    objects_xml = root_xml.findall('object')
    for obj_xml in objects_xml:
        bndbox_obj_xml = obj_xml.find('bndbox')
        file_data.add_object_data_from_xml(
            name=obj_xml.findtext('name'),
            x_min=int(bndbox_obj_xml.findtext('xmin')),
            y_min=int(bndbox_obj_xml.findtext('ymin')),
            x_max=int(bndbox_obj_xml.findtext('xmax')),
            y_max=int(bndbox_obj_xml.findtext('ymax')))

    return file_data


def convert_image_file_data_to_yolov5_txt(file_data, label_text_file_path):
    with open(label_text_file_path, 'w') as file:
        for object_data in file_data.object_list:
            yolov5_format_string = "{} {} {} {} {}\n".format(
                0,
                object_data.bound_box_data.center_x_ratio,
                object_data.bound_box_data.center_y_ratio,
                object_data.bound_box_data.width_ratio,
                object_data.bound_box_data.height_ratio)

            file.write(yolov5_format_string)


def make_dataset_files(file_data_list,
                       images_dataset_path, labels_dataset_path,
                       duplicate_data=False, log_interval=100):
    file_data_count = len(file_data_list)

    for index, file_data in enumerate(file_data_list):
        shutil.copy(file_data.path, os.path.join(images_dataset_path, file_data.file_name))

        if duplicate_data:
            duplicate_image_file_name = "{}_0{}".format(
                os.path.splitext(file_data.file_name)[0],
                os.path.splitext(file_data.file_name)[1])
            shutil.copy(file_data.path, os.path.join(images_dataset_path, duplicate_image_file_name))

        label_text_file_name = os.path.splitext(file_data.file_name)[0] + ".txt"
        convert_image_file_data_to_yolov5_txt(
            file_data=file_data,
            label_text_file_path=os.path.join(labels_dataset_path, label_text_file_name))

        if duplicate_data:
            duplicate_label_file_name = "{}_0.txt".format(os.path.splitext(file_data.file_name)[0])
            shutil.copy(os.path.join(labels_dataset_path, label_text_file_name),
                        os.path.join(labels_dataset_path, duplicate_label_file_name))

        if (index % log_interval == 0 or (index + 1) == file_data_count) and index != 0:
            print("MAKE DATASET : [{}/{}]({:.1f}%)".format(
                index, file_data_count, ((index + 1) / file_data_count) * 100.0))


def display_images(image_list, label_list, num_rows, num_cols, display_scale=3.0):
    plt.figure(figsize=(num_cols * display_scale, num_rows * display_scale))
    for index, (image, label) in enumerate(zip(image_list, label_list)):
        plt.subplot(num_rows, num_cols, index + 1)

        plt.grid(False)
        plt.xticks([])
        plt.yticks([])
        plt.imshow(image)

    plt.tight_layout()
    plt.show()


def display_images_and_bbox(image_file_data_list, num_rows, num_cols, display_scale=5.0):
    plt.figure(figsize=(num_cols * display_scale, num_rows * display_scale))
    sample_count = num_rows * num_cols
    for index, image_file_data in enumerate(image_file_data_list):
        if index >= sample_count:
            break

        plt.subplot(num_rows, num_cols, index + 1)

        plt.grid(False)
        plt.xticks([])
        plt.yticks([])

        image = Image.open(image_file_data.path)
        draw = ImageDraw.Draw(image)

        for object_data in image_file_data.object_list:
            draw.rectangle([(object_data.bound_box_data.x_min, object_data.bound_box_data.y_min),
                            (object_data.bound_box_data.x_max, object_data.bound_box_data.y_max)],
                           outline='red',
                           width=5)

        plt.imshow(image)
        plt.xlabel("File: {} | Label: {}".format(image_file_data.file_name, image_file_data.object_list[0].name))

    plt.tight_layout()
    plt.show()
