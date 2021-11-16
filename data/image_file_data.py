from data.object_data import ObjectData


class ImageFileData:
    def __init__(self, image_width=0, image_height=0, image_channel=0, file_name="", path=""):
        self.image_width = image_width
        self.image_height = image_height
        self.image_channel = image_channel
        self.file_name = file_name
        self.path = path
        self.object_list = []

    def add_object_data_from_xml(self, name, x_min, y_min, x_max, y_max):
        new_object_data = ObjectData(image_width=self.image_width,
                                     image_height=self.image_height,
                                     name=name)

        new_object_data.make_bound_box_data_from_xml(x_min=x_min, y_min=y_min, x_max=x_max, y_max=y_max)

        self.object_list.append(new_object_data)

    def add_object_data_from_txt(self, name, center_x_ratio, center_y_ratio, width_ratio, height_ratio):
        new_object_data = ObjectData(image_width=self.image_width,
                                     image_height=self.image_height,
                                     name=name)

        new_object_data.make_bound_box_data_from_txt(center_x_ratio=center_x_ratio,
                                                     center_y_ratio=center_y_ratio,
                                                     width_ratio=width_ratio,
                                                     height_ratio=height_ratio)

        self.object_list.append(new_object_data)
