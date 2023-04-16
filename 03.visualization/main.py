import pickle
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy.special import softmax
import time
from classify import *
from classify_2dlist_to_df import *

#데이터 꺼내오기
with open('/Users/ijimin/Desktop/지민/pycharm/pyqt test/data_file/saved_right_ca.txt','rb') as f:
    improved_data_right = pickle.load(f)
    f.close()

with open('/Users/ijimin/Desktop/지민/pycharm/pyqt test/data_file/saved_wrong_ca.txt','rb') as f:
    improved_data_wrong = pickle.load(f)
    f.close()

with open('/Users/ijimin/Desktop/지민/pycharm/pyqt test/data_file/save_right.txt','rb') as f:
    data_right = pickle.load(f)
    f.close()

with open('/Users/ijimin/Desktop/지민/pycharm/pyqt test/data_file/save_wrong.txt','rb') as f:
    data_wrong = pickle.load(f)
    f.close()
#데이터 개수
print(f'''
improved_data_right : {len(improved_data_right)}
improved_data_wrong : {len(improved_data_wrong)}
data_right : {len(data_right)}
data_wrong : {len(data_wrong)}
''')

classify = Classifer()

classify.softmaxx = False
improved = True
drawing = False

if improved == True:
    classify.process(improved_data_wrong,improved_data_right)
else:
    classify.process(data_wrong,data_right)

df = classify.df

if drawing == True:
    if classify.softmaxx == True:
        sns.heatmap(df)
    else:
        sns.heatmap(df,annot=True, fmt='d')
    plt.title(f'x=label, y=predicted')
    plt.show()

def possibility(num):
    ans = classify.full_data[num][num]
    total = 0
    for i in range(10):
        total += classify.full_data[num][i]
    return f'{ans / total:.4f}', total

for i in range(10):
    poss, total = possibility(i)
    print(f'{i} : {poss}')

def nd(p,t):
    q = 1 - p
    z = abs( (p - 1) / (p*q/t)**0.5)
    return z

# poss, total = possibility(1)
# nd(float(poss), total)

print('1% 유의확률에서 p = 1')
for i in range(1,10):
    poss, total = possibility(i)
    if nd(float(poss), total) < 2.58:
        print(f'z{i} : {nd(float(poss), total):.4f}')

print('5% 유의확률에서 p = 1')
for i in range(1,10):
    poss, total = possibility(i)
    if nd(float(poss), total) < 1.96:
        print(f'z{i} : {nd(float(poss), total):.4f}')

print(classify.df)
'''
아타라시 ^___^
'''

with open('/Users/ijimin/Desktop/지민/pycharm/pyqt test/data_file/saved_right_ca.txt','rb') as f:
    improved_right_data = pickle.load(f)
    f.close()

with open('/Users/ijimin/Desktop/지민/pycharm/pyqt test/data_file/saved_wrong_ca.txt','rb') as f:
    improved_wrong_data = pickle.load(f)
    f.close()

with open('/Users/ijimin/Desktop/지민/pycharm/pyqt test/data_file/save_right.txt','rb') as f:
    unimproved_right_data = pickle.load(f)
    f.close()

with open('/Users/ijimin/Desktop/지민/pycharm/pyqt test/data_file/save_wrong.txt','rb') as f:
    unimproved_wrong_data = pickle.load(f)
    f.close()

new_classifier = classify_2dlist_to_df(softmax=False)
improved_df = new_classifier.process(improved_wrong_data+improved_right_data)

sns.heatmap(improved_df,annot=True, fmt='d')
plt.title(f'x=label, y=predicted')
plt.show()