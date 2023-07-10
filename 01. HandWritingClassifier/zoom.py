import numpy as np
import PIL.Image as Image

class ZoomAugmentor:
    def __init__(self, data):
        self.np_img = data # (28*28)
        self.pil_img = Image.fromarray(self.np_img)

    def run(self):
        area_box = self.find_area_box(self.np_img)
        padded_box = self.padding(area_box=area_box)

        self.cropped_img = self.pil_img.crop(box=padded_box)
        self.zoomed_img = self.zoom_cropped_img(self.cropped_img)
        self.np_zoomed_img = np.array(self.zoomed_img)

        self.final_img = self.pad_to_28x28(self.np_zoomed_img)
        self.final_img = np.expand_dims(self.final_img, axis=2)  # (28, 28) -> (28,28,1)


    def find_area_box(self, img):
        self.location = np.where(img != 0)
        self.upper, self.lower = min(self.location[0]), max(self.location[0])
        self.left, self.right = min(self.location[1]), max(self.location[1])
        return (self.left, self.upper, self.right, self.lower)  # left, upper, right, lower

    def padding(self, area_box):
        left, upper, right, lower = area_box
        if left > 1:
            left -= 2
        if right < 26:
            right += 2
        if lower < 26:
            lower += 2
        if upper > 1:
            upper -= 2
        return (left, upper, right, lower)

    def zoom_cropped_img(self, img):
        self.width, self.height = (self.right - self.left + 1), (self.lower - self.upper + 1)

        if self.width > self.height:
            width_ratio = 28 / self.width

            zoomed_img = img.resize((round(width_ratio * self.width),
                                     round(width_ratio * self.height)),
                                    resample=Image.LANCZOS)
        else:
            height_ratio = 28 / self.height
            zoomed_img = img.resize((round(height_ratio * self.width),
                                     round(height_ratio * self.height)),
                                    resample=Image.LANCZOS)  # BICUBIC
        return zoomed_img

    def pad_to_28x28(self, img):
        w, h = img.shape
        if (28 - w) % 2 == 0:
            left = right = int((28 - w) / 2)
        else:
            right = int((28 - w) // 2)
            left = int((28 - w) // 2 + 1)

        if (28 - h) % 2 == 0:
            upper = lower = int((28 - h) / 2)
        else:
            upper = int((28 - h) // 2)
            lower = int((28 - h) // 2 + 1)

        final_img = np.pad(img, ((left, right), (upper, lower)), 'constant', constant_values=0)

        return final_img
