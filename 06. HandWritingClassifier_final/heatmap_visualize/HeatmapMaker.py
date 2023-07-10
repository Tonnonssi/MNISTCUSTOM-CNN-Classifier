import matplotlib.pyplot as plt
import numpy as np
import pickle

class HeatmapMaker:
    def __init__(self, floc, softmax=True):
        self.floc = floc
        self.softmax = softmax

    def printing(self):
        lst_data = self.open_pickle(self.floc)
        np_heatmap = self.make_np_heatmap(lst_data)
        self.make_heatmap(np_heatmap)

    def open_pickle(self, floc:str):
        with open (floc, 'rb') as f:
            while True:
                try:
                    lst = pickle.load(f)
                except EOFError:
                    break
        return lst

    def make_np_heatmap(self, lst):
        arr = np.zeros((10,10))
        for l in lst:
            label, pred, img = l
            arr[label, pred] += 1
        return arr[::-1] # 좌측하단에서 0부터 시작하게 만들기 위해서

    def make_heatmap(self, arr):
        if self.softmax: # softmax를 적용한다.
            for i in range(10):
                arr[i] /= sum(arr[i])
            arr = np.round(arr, decimals=2)
        # 시각화
        plt.imshow(arr, cmap='plasma')
        reversed_cols = np.flip(range(10))
        plt.xticks(range(10))
        plt.yticks(range(10), reversed_cols)

        plt.xlabel('pred')
        plt.ylabel('index')
        plt.title('heatmap')

        for i in range(10):
            for j in range(10):
                value = arr[i, j]
                if value > np.max(arr) / 2:
                    plt.text(j, i, str(value), ha='center', va='center', color='black')
                else:
                    plt.text(j, i, str(value), ha='center', va='center', color='white')
        plt.show()
