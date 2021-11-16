import numpy as np


class BoundBoxData:
    def __init__(self):
        self.image_width = 0
        self.image_height = 0
        self.x_min = 0
        self.y_min = 0
        self.x_max = 0
        self.y_max = 0
        self.center_x_ratio = 0.0
        self.center_y_ratio = 0.0
        self.width_ratio = 0.0
        self.height_ratio = 0.0

    def get_image_ratio(self, image_width, image_height, x_min, y_min, x_max, y_max):
        center_x = x_max - np.round((x_max - x_min) / 2)
        center_y = y_max - np.round((y_max - y_min) / 2)
        object_center_x_ratio = center_x / image_width
        object_center_y_ratio = center_y / image_height
        object_width_ratio = (x_max - x_min) / image_width
        object_height_ratio = (y_max - y_min) / image_height

        return (object_center_x_ratio, object_center_y_ratio), (object_width_ratio, object_height_ratio)

    def get_image_real_size(self, image_width, image_height,
                             object_center_x_ratio, object_center_y_ratio,
                             object_width_ratio, object_height_ratio):

        object_width = image_width * object_width_ratio
        object_height = image_height * object_height_ratio
        object_center_x = image_width * object_center_x_ratio
        object_center_y = image_height * object_center_y_ratio

        x_min = np.round(object_center_x - (object_width / 2))
        x_max = np.round(object_center_x + (object_width / 2))

        y_min = np.round(object_center_y - (object_height / 2))
        y_max = np.round(object_center_y + (object_height / 2))

        return (x_min, y_min), (x_max, y_max)

    def set_image_ratio(self):
        if self.image_width != 0 and self.image_height != 0 and self.x_max != 0 and self.y_max != 0:
            (self.center_x_ratio, self.center_y_ratio), (self.width_ratio, self.height_ratio) = \
                self.get_image_ratio(image_width=self.image_width,
                                     image_height=self.image_height,
                                     x_min=self.x_min, y_min=self.y_min,
                                     x_max=self.x_max, y_max=self.y_max)

    def set_image_real_size(self):
        (self.x_min, self.y_min), (self.x_max, self.y_max) = self.get_image_real_size(
            image_width=self.image_width, image_height=self.image_height,
            object_center_x_ratio=self.center_x_ratio, object_center_y_ratio=self.center_y_ratio,
            object_width_ratio=self.width_ratio, object_height_ratio=self.height_ratio)
