import argparse
from utils.common import *

CLASS_NAMES = ['License-plate']

NUM_ROWS = 5
NUM_COLS = 4
SAMPLE_COUNT = NUM_ROWS * NUM_COLS

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Display images and labels.")
    parser.add_argument("--image-path", help="Dataset images path", type=str,
                        required=False, default='./dataset/train/images', metavar='./dataset/train/images')
    parser.add_argument("--label-path", help="Dataset labels path", type=str,
                        required=False, default='./dataset/train/labels', metavar='./dataset/train/labels')

    args = parser.parse_args()

    image_path = args.image_path
    label_path = args.label_path

    image_file_name_list = os.listdir(image_path)
    print("Image file count: ", len(image_file_name_list))

    label_file_name_list = os.listdir(label_path)
    print("Label file count: ", len(label_file_name_list))

    file_data_list = []

    # 모든 이미지 resize 후 저장하기
    for image_file_name, label_file_name in zip(image_file_name_list, label_file_name_list):
        image_file_path = os.path.join(image_path, image_file_name)
        label_file_path = os.path.join(label_path, label_file_name)

        image_file_name_no_ext = os.path.splitext(image_file_name)[0]
        label_file_name_no_ext = os.path.splitext(label_file_name)[0]

        if image_file_name_no_ext != label_file_name_no_ext:
            print("{} is not label of {}".format(label_file_name, image_file_name))
        else:
            image = Image.open(image_file_path)
            file_data = ImageFileData(
                image_width=image.width, image_height=image.height, image_channel=3,
                file_name=image_file_name, path=image_file_path)

            with open(label_file_path, 'r') as label_file:
                read_data_list = label_file.readlines()
                for read_data in read_data_list:
                    split_data = read_data.split(' ')
                    file_data.add_object_data_from_txt(name=CLASS_NAMES[int(split_data[0])],
                                                       center_x_ratio=float(split_data[1]),
                                                       center_y_ratio=float(split_data[2]),
                                                       width_ratio=float(split_data[3]),
                                                       height_ratio=float(split_data[4]))
            file_data_list.append(file_data)

    show_count = int(len(file_data_list) / SAMPLE_COUNT)

    for show_index in range(show_count):
        current_index = show_index * SAMPLE_COUNT
        sample_file_data_list = file_data_list[current_index:current_index+SAMPLE_COUNT]
        display_images_and_bbox(image_file_data_list=sample_file_data_list, num_rows=NUM_ROWS, num_cols=NUM_COLS)

print("display image done.")
