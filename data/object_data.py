from data.bound_box_data import BoundBoxData


class ObjectData:
    def __init__(self, image_width, image_height, name):
        self.image_width = image_width
        self.image_height = image_height
        self.name = name
        self.bound_box_data = None

    def make_bound_box_data_from_xml(self, x_min, y_min, x_max, y_max):
        self.bound_box_data = BoundBoxData()
        self.bound_box_data.image_width = self.image_width
        self.bound_box_data.image_height = self.image_height
        self.bound_box_data.x_min = x_min
        self.bound_box_data.y_min = y_min
        self.bound_box_data.x_max = x_max
        self.bound_box_data.y_max = y_max

        self.bound_box_data.set_image_ratio()

    def make_bound_box_data_from_txt(self, center_x_ratio, center_y_ratio, width_ratio, height_ratio):
        self.bound_box_data = BoundBoxData()
        self.bound_box_data.image_width = self.image_width
        self.bound_box_data.image_height = self.image_height
        self.bound_box_data.center_x_ratio = center_x_ratio
        self.bound_box_data.center_y_ratio = center_y_ratio
        self.bound_box_data.width_ratio = width_ratio
        self.bound_box_data.height_ratio = height_ratio

        self.bound_box_data.set_image_real_size()
