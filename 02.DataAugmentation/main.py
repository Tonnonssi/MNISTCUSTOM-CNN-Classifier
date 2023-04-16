import pickle
import numpy as np
import matplotlib.pyplot as plt
import os
import re

from txpand_augmentation import *
from angleaugmentation import *
from cutting_augmentation import *
from check_list import *
from utils import *

#중복된 데이터가 있는지 확인하는 코드
dir_path_4_collected = '/Users/ijimin/Desktop/지민/pycharm/pyqt test/data_file/collected_data/'

collected_fname = make_url_lst(dir_path_4_collected)
check_list(collected_fname)

#class에서 가져오기
aa = AngleAugmentation()
ca = CuttingAugmentation()
ta = TxpandAugmentation()

augmentation_urls_path = '/Users/ijimin/Desktop/지민/pycharm/pyqt test/data_file/augmentation/'

for fname in collected_fname:
    print('-----------------------------')
    print(f'증강할 데이터 : {fname}')
    improved, correct = find_url_by_fname(fname)
    url = improved_or_correct_url(improved, correct)
    augmentation_urls_lst = make_url_lst(augmentation_urls_path+url)

    for name in augmentation_urls_lst:
        if 'expand' in name:
            ca.expand_image(dir_path_4_collected+fname,augmentation_urls_path+url+name)
        elif 'turn' in name:
            aa.turn_angles(dir_path_4_collected+fname,augmentation_urls_path+url+name)
        else:
            ta.txpand_image(dir_path_4_collected + fname, augmentation_urls_path + url + name)
        # clear(augmentation_urls_path+url+name)