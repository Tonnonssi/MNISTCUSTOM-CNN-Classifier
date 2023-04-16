import numpy as np
from PIL import Image

class CuttingAugmentation:
    def __init__(self):
        self.height_min = 0
        self.width_min = 0
        self.height_max = 0
        self.width_max = 0

    def search_int_area(self,img):
        '''
        높낮이, 너비의 최솟값/최댓값을 찾는 것
        :param img: np.array
        '''
        img = img.reshape(28,28)
        location = np.where(img != 0)
        location_list = []

        for arr in list(location):
            lst = arr.tolist()
            lst.sort()
            location_list.append(lst)

        self.height_min = location_list[0][0]
        self.height_max = location_list[0][-1]
        self.width_min = location_list[1][0]
        self.width_max = location_list[1][-1]

    def reduce_error(self):
        '''
        위 아래로 꽉 찬 사진보단 좀 여유가 있어야 해서
        '''
        if self.height_min > 0:
            self.height_min -= 1
        if self.width_min > 0:
            self.width_min -= 1
        self.height_max += 1
        self.width_max += 1

    def expand_img(self, img, num):
        height_len = self.height_max - self.height_min
        width_len = self.width_max - self.width_min

        img = (img * 255).astype(np.uint8)  # 이유 정리해보기
        img = Image.fromarray(img)

        img_trim = img.crop((self.width_min, self.height_min, self.width_max, self.height_max))

        #1 예외처리
        if num == 1:
            if height_len > 20:
                pass
            hs_ratio = 20 // height_len
            resized_hs = img_trim.resize((hs_ratio * height_len, hs_ratio * width_len))
            return resized_hs

        if height_len > width_len:
            hs_ratio = 28 // height_len
            resized_hs = img_trim.resize((hs_ratio * height_len, hs_ratio * width_len))
            return resized_hs

        else:
            ws_ratio = 28 // width_len
            resized_ws = img_trim.resize((ws_ratio * height_len, ws_ratio * width_len))
            return resized_ws

    def return_to_28(self, img):
        img_arr = np.array(img)
        h, w = img_arr.shape  # 이거 잘 봐두기
        if (28 - w) % 2 == 0:
            left = right = int((28 - w) / 2)
        else:
            right = int((28 - w) // 2)
            left = int((28 - w) // 2 + 1)

        if (28 - h) % 2 == 0:
            top = bottom = int((28 - h) / 2)
        else:
            top = int((28 - h) // 2)
            bottom = int((28 - h) // 2 + 1)

        # print(top, bottom,left, right)
        padded_np_img = np.pad(img_arr, ((top, bottom), (left, right)),
                               'constant', constant_values=0)
        return padded_np_img

    def progress(self, np_img, num) -> list:
        self.search_int_area(np_img)
        self.reduce_error()
        img = self.expand_img(np_img, num)
        img = self.return_to_28(img)
        return img
