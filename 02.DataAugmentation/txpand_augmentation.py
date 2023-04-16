import pickle
import numpy as np
from skimage.transform import rotate
from PIL import Image

class TxpandAugmentation:
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

    def expand_img(self,img):
        height_len = self.height_max - self.height_min
        width_len = self.width_max - self.width_min
        #print(img)
        img = (img *255).astype(np.uint8) #ㅇㅣ유 정리해보기
        img = Image.fromarray(img)
        #img.show()
        img_trim = img.crop((self.width_min,self.height_min,self.width_max,self.height_max))
        #img_trim.show()
        if height_len > width_len:
            hs_ratio = 28 // height_len
            resized_hs = img_trim.resize((hs_ratio*height_len, hs_ratio*width_len))
            return resized_hs

        else:
            ws_ratio = 28 // width_len
            resized_ws = img_trim.resize((ws_ratio*height_len,ws_ratio*width_len))
            return resized_ws

    def return_to_28(self,img):

        img_arr = np.array(img)
        h, w = img_arr.shape #이거 잘 봐두기
        if (28-w) % 2 == 0:
            left = right = int((28-w) / 2)
        else:
            right = int((28 - w) // 2)
            left = int((28 - w) // 2 + 1)

        if (28-h) % 2 == 0:
            top = bottom = int((28-h) / 2)
        else:
            top = int((28-h) // 2)
            bottom = int((28-h) // 2 + 1)

        #print(top, bottom,left, right)
        padded_np_img = np.pad(img_arr, ((top, bottom), (left, right)),
                               'constant', constant_values=0)
        return padded_np_img

    def process(self, new_data) -> list:
        for data in new_data:
            correct_value = data[0]
            predicted_value = data[1]
            np_img = data[2].reshape(28,28)

            self.search_int_area(np_img)
            self.reduce_error()
            i = self.expand_img(np_img)
            i = self.return_to_28(i)
            self.cut_imgs.append([correct_value, predicted_value,i])

        return self.cut_imgs

    def open_url(self,url1,url2):
        '''
        :param url1: 증강할 대상 데이터
        :param url2: 증강된 데이터가 저장될 장소
        '''
        self.height_min = 0
        self.width_min = 0
        self.height_max = 0
        self.width_max = 0
        self.cut_imgs = []
        self.rotated_imgs = []
        self.new_appended = True
        self.exist_lst = []
        self.save_url = url2

        with open(f'{url1}', 'rb') as f:
            while True:
                try:
                    self.wrong_data = pickle.load(f)
                except EOFError:
                    break
            f.close()

        with open(f'{url2}', 'rb') as f:
            while True:
                try:
                    self.exist_lst = pickle.load(f)
                except EOFError:
                    break
            f.close()

        self.exist_len = int(len(self.exist_lst) / 16)

    def rotate_image(self, img, angle):
        img = img.reshape(28, 28)
        return rotate(img, angle)

    def save_by_pickle(self, appended_lst):
        with open(f'{self.save_url}', 'wb') as file:
            new_lst = self.exist_lst + appended_lst
            pickle.dump(new_lst, file)
            file.close()
        # print('Saved properly.')

    def avoid_preaugmented(self):
        return self.wrong_data[self.exist_len:]

    def process(self, new_data) -> list:
        for data in new_data:
            correct_value = data[0]
            predicted_value = data[1]
            np_img = data[2].reshape(28, 28)
            img = (np_img * 255).astype(np.uint8)

            for ang in range(5, 41, 5):
                i = self.rotate_image(img,ang)
                self.search_int_area(i)
                self.reduce_error()
                i = self.expand_img(i)
                i = self.return_to_28(i)
                self.rotated_imgs.append([correct_value, predicted_value,i])

                j = self.rotate_image(img,-ang)
                self.search_int_area(j)
                self.reduce_error()
                j = self.expand_img(j)
                j = self.return_to_28(j)
                self.rotated_imgs.append([correct_value, predicted_value,j])

        return self.rotated_imgs


    def txpand_image(self, url1, url2):
        self.open_url(url1, url2)
        avoid_overlaped_data = self.avoid_preaugmented()
        rotated_imgs = self.process(avoid_overlaped_data)
        self.save_by_pickle(rotated_imgs)
        if len(avoid_overlaped_data) == 0:
            print('txpand_augmentation : 추가된 데이터가 없어 수정된 사항이 없습니다.')
        else:
            print(f'txpand_augmentation : {len(rotated_imgs)}개로 증강되었습니다.')
        return len(rotated_imgs)