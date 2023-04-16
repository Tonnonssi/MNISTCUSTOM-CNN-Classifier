import pickle
import numpy as np
from skimage.transform import rotate

class AngleAugmentation:
    def open_url(self,url1,url2):
        '''
        :param url1: 증강할 대상 데이터
        :param url2: 증강된 데이터가 저장될 장소
        '''
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
            np_img = data[2]
            img = (np_img * 255).astype(np.uint8)

            for ang in range(5, 41, 5):
                i = self.rotate_image(img,ang)
                self.rotated_imgs.append([correct_value, predicted_value,i])
                j = self.rotate_image(img,-ang)
                self.rotated_imgs.append([correct_value, predicted_value,j])

        return self.rotated_imgs

    def turn_angles(self, url1, url2):
        self.open_url(url1, url2)
        avoid_overlaped_data = self.avoid_preaugmented()
        rotated_imgs = self.process(avoid_overlaped_data)
        self.save_by_pickle(rotated_imgs)

        if len(avoid_overlaped_data) == 0:
            print('angle_augmentation : 추가된 데이터가 없어 수정된 사항이 없습니다.')
        else:
            print(f'angle_augmentation : {len(rotated_imgs)}개로 증강되었습니다.')
        return len(rotated_imgs)
