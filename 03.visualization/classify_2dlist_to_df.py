import pandas as pd
from scipy.special import softmax
import numpy as np

class classify_2dlist_to_df:
    def __init__(self, softmax):
        self.softmax = softmax

    def classify_2dlist(self, lst_2d):
        # self.input_data = lst_2d
        total_counts = []

        for _ in range(10): #횟수 박스
            total_counts.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

        for inner_list in lst_2d:
            correct_label = inner_list[0]
            predict_value = inner_list[1]
            total_counts[correct_label][predict_value] += 1
        return total_counts

    def softmax_TF(self,total_counts):
        softmaxed_counts = []
        for inner_list in total_counts:
             softmaxed_counts.append(softmax(np.array(inner_list)))
        return softmaxed_counts

    def transfer_counts_to_df(self, total_counts):
        if self.softmax == True:
            total_counts = self.softmaxed_TF(total_counts)

        self.dict = {}

        for i in range(10):
            self.dict[i] = total_counts[i]
        self.df = pd.DataFrame(self.dict)
        return self.df

    def process(self, lst_2d):
        total_counts = self.classify_2dlist(lst_2d)
        df = self.transfer_counts_to_df(total_counts)
        return df

