import os
import argparse
import numpy as np
from PIL import Image

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Resize images.")
    parser.add_argument("--resize-width", help="Resize image width", type=int,
                        required=False, default=836, metavar="416 or 608 or 836")
    parser.add_argument("--resize-height", help="Resize image height", type=int,
                        required=False, default=836, metavar="416 or 608 or 836")
    parser.add_argument("--source-path", help="Source images path", type=str,
                        required=False, default='./original_images', metavar='./original_images')
    parser.add_argument("--resize-path", help="Resize images path", type=str,
                        required=False, default='./resize_images', metavar='./resize_images')

    args = parser.parse_args()

    resize_width = args.resize_width
    resize_height = args.resize_height
    source_path = args.source_path
    resize_path = args.resize_path

    # 저장할 경로 없으면 생성
    if not os.path.exists(resize_path):
        os.mkdir(resize_path)

    # 원본 이미지 경로의 모든 이미지 list 지정
    file_name_list = os.listdir(source_path)
    image_files_count = len(file_name_list)
    print("Image files count: ", image_files_count)
    LOG_INTERVAL = np.round(image_files_count * 0.2)

    # 모든 이미지 resize 후 저장하기
    for index, file_name in enumerate(file_name_list):
        # 이미지 열기
        source_image = Image.open(os.path.join(source_path, file_name))

        # 이미지 resize
        resize_image = source_image.resize((resize_width, resize_height))

        # 이미지 JPG`로 저장
        resize_image = resize_image.convert('RGB')
        resize_image.save(os.path.join(resize_path, file_name))

        if (index % LOG_INTERVAL == 0 or (index + 1) == image_files_count) and index != 0:
            print("RESIZE IMAGES: [{}/{}]({:.1f}%)".format(
                index, image_files_count, ((index + 1) / image_files_count) * 100.0))

    print("Resize image done.")
