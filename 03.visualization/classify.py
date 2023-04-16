import pandas as pd
import numpy as np
from scipy.special import softmax

class Classifer:
    def __init__(self):
        self.lst_0 = []
        self.lst_1 = []
        self.lst_2 = []
        self.lst_3 = []
        self.lst_4 = []
        self.lst_5 = []
        self.lst_6 = []
        self.lst_7 = []
        self.lst_8 = []
        self.lst_9 = []

        self.softmaxx = True

    def find_correct_num(self, data: list, num: int):
        num_lst = []
        for i in data:
            if i[0] == num:
                num_lst.append(i)
        return num_lst

    def make_complete_lst(self,wrong_data:list,right_data:list,num:int):
        return self.find_correct_num(right_data,num) + self.find_correct_num(wrong_data, num)

    def classify_predicted(self, data: list):
        zero = one = two = three = four = five = six = seven = eight = nine = 0
        for i in data:
            correct, predicted, arr = i
            if predicted == 0:
                zero += 1
            elif predicted == 1:
                one += 1
            elif predicted == 2:
                two += 1
            elif predicted == 3:
                three += 1
            elif predicted == 4:
                four += 1
            elif predicted == 5:
                five += 1
            elif predicted == 6:
                six += 1
            elif predicted == 7:
                seven += 1
            elif predicted == 8:
                eight += 1
            elif predicted == 9:
                nine += 1

        return [zero, one, two, three, four, five, six, seven, eight, nine]

    def process(self, wrong_data:list, right_data: list):

        self.lst_0 = self.make_complete_lst(wrong_data, right_data, 0)
        self.lst_1 = self.make_complete_lst(wrong_data, right_data, 1)
        self.lst_2 = self.make_complete_lst(wrong_data, right_data, 2)
        self.lst_3 = self.make_complete_lst(wrong_data, right_data, 3)
        self.lst_4 = self.make_complete_lst(wrong_data, right_data, 4)
        self.lst_5 = self.make_complete_lst(wrong_data, right_data, 5)
        self.lst_6 = self.make_complete_lst(wrong_data, right_data, 6)
        self.lst_7 = self.make_complete_lst(wrong_data, right_data, 7)
        self.lst_8 = self.make_complete_lst(wrong_data, right_data, 8)
        self.lst_9 = self.make_complete_lst(wrong_data, right_data, 9)

        self.full_data = []

        self.full_data.append(self.classify_predicted(self.lst_0))
        self.full_data.append(self.classify_predicted(self.lst_1))
        self.full_data.append(self.classify_predicted(self.lst_2))
        self.full_data.append(self.classify_predicted(self.lst_3))
        self.full_data.append(self.classify_predicted(self.lst_4))
        self.full_data.append(self.classify_predicted(self.lst_5))
        self.full_data.append(self.classify_predicted(self.lst_6))
        self.full_data.append(self.classify_predicted(self.lst_7))
        self.full_data.append(self.classify_predicted(self.lst_8))
        self.full_data.append(self.classify_predicted(self.lst_9))

        if self.softmaxx == True:
            self.dict_for_df = {'0':list(softmax(np.array(self.classify_predicted(self.lst_0)))),
                                '1':list(softmax(np.array(self.classify_predicted(self.lst_1)))),
                                '2':list(softmax(np.array(self.classify_predicted(self.lst_2)))),
                                '3':list(softmax(np.array(self.classify_predicted(self.lst_3)))),
                                '4':list(softmax(np.array(self.classify_predicted(self.lst_4)))),
                                '5':list(softmax(np.array(self.classify_predicted(self.lst_5)))),
                                '6':list(softmax(np.array(self.classify_predicted(self.lst_6)))),
                                '7':list(softmax(np.array(self.classify_predicted(self.lst_7)))),
                                '8':list(softmax(np.array(self.classify_predicted(self.lst_8)))),
                                '9':list(softmax(np.array(self.classify_predicted(self.lst_9))))}
        else:
            self.dict_for_df = {'0':self.classify_predicted(self.lst_0),
                                '1':self.classify_predicted(self.lst_1),
                                '2':self.classify_predicted(self.lst_2),
                                '3':self.classify_predicted(self.lst_3),
                                '4':self.classify_predicted(self.lst_4),
                                '5':self.classify_predicted(self.lst_5),
                                '6':self.classify_predicted(self.lst_6),
                                '7':self.classify_predicted(self.lst_7),
                                '8':self.classify_predicted(self.lst_8),
                                '9':self.classify_predicted(self.lst_9)}

        self.df = pd.DataFrame(self.dict_for_df)

