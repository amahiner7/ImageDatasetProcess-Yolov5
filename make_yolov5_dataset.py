import numpy as np
import argparse
import random
from utils.common import *

DATASET_PATH = "./dataset"
TRAIN_DATASET_PATH = os.path.join(DATASET_PATH, "train")
VALID_DATASET_PATH = os.path.join(DATASET_PATH, "valid")
IMAGES_TRAIN_DATASET_PATH = os.path.join(TRAIN_DATASET_PATH, "images")
LABELS_TRAIN_DATASET_PATH = os.path.join(TRAIN_DATASET_PATH, "labels")
IMAGES_VALID_DATASET_PATH = os.path.join(VALID_DATASET_PATH, "images")
LABELS_VALID_DATASET_PATH = os.path.join(VALID_DATASET_PATH, "labels")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Make yolov5 dataset.")
    parser.add_argument("--source-path", help="Source images and label path", type=str,
                        required=False, default='./source_images', metavar='./source_images')
    parser.add_argument("--train-ratio", help="Train/Validation ratio", type=float,
                        required=False, default=0.8, metavar="recommend 0.7 or 0.8")

    args = parser.parse_args()
    source_path = args.source_path
    train_ratio = args.train_ratio

    if not os.path.exists(DATASET_PATH):
        os.mkdir(DATASET_PATH)

    if not os.path.exists(TRAIN_DATASET_PATH):
        os.mkdir(TRAIN_DATASET_PATH)

    if not os.path.exists(VALID_DATASET_PATH):
        os.mkdir(VALID_DATASET_PATH)

    if not os.path.exists(IMAGES_TRAIN_DATASET_PATH):
        os.mkdir(IMAGES_TRAIN_DATASET_PATH)

    if not os.path.exists(LABELS_TRAIN_DATASET_PATH):
        os.mkdir(LABELS_TRAIN_DATASET_PATH)

    if not os.path.exists(IMAGES_VALID_DATASET_PATH):
        os.mkdir(IMAGES_VALID_DATASET_PATH)

    if not os.path.exists(LABELS_VALID_DATASET_PATH):
        os.mkdir(LABELS_VALID_DATASET_PATH)

    source_file_name_list = os.listdir(source_path)
    image_file_name_list = []
    label_file_name_list = []

    for file_name in source_file_name_list:
        file_ext = os.path.splitext(file_name)[1]
        if file_ext == ".jpg" or file_ext == ".png":
            image_file_name_list.append(file_name)
        elif file_ext == ".xml":
            label_file_name_list.append(file_name)

    file_data_list = []

    for file_name in source_file_name_list:
        file_ext = os.path.splitext(file_name)[1]
        if file_ext == ".xml":
            label_file_path = os.path.join(source_path, file_name)

            file_data = load_xml(xml_file_path=label_file_path)
            file_data.path = os.path.join(source_path, file_data.file_name)

            file_data_list.append(file_data)

    random.shuffle(file_data_list)

    train_data_length = int(len(file_data_list) * train_ratio)
    train_data_list = file_data_list[:train_data_length]  # Train: 80%
    valid_data_list = file_data_list[train_data_length:]  # Validation: 20%

    print("Train data count: ", len(train_data_list))
    print("Validation data count: ", len(valid_data_list))

    print("====================== Make train dataset ======================")
    make_dataset_files(file_data_list=train_data_list,
                       images_dataset_path=IMAGES_TRAIN_DATASET_PATH,
                       labels_dataset_path=LABELS_TRAIN_DATASET_PATH,
                       duplicate_data=True,
                       log_interval=np.round(len(train_data_list) * 0.2))

    print("\n=================== Make validation dataset ===================")
    make_dataset_files(file_data_list=valid_data_list,
                       images_dataset_path=IMAGES_VALID_DATASET_PATH,
                       labels_dataset_path=LABELS_VALID_DATASET_PATH,
                       duplicate_data=True,
                       log_interval=np.round(len(valid_data_list) * 0.2))

    print("Make yolov5 dataset done.")
