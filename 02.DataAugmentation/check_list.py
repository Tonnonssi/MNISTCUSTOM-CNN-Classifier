import pickle
import os

def clear(url):
    open(url, "w").close()

def classify_rightorwrong(fname:str):
    right = True
    if 'incorrect' in fname:
        right = False
    return right

def dect_misclassified(f: list, right:bool):
    i = 0
    file = f
    print(f'전체 자료 개수 : {len(f)}')
    if right == True:
        for data in f:
            if data[0] != data[1]:
                i += 1
                file.remove(data)

    else:
        for data in f:
            if data[0] == data[1]:
                i += 1
                file.remove(data)
    print(f'잘못 들어간 자료 : {i}')
    return file

def save(url: str, new_lst: list):
    with open(f'{url}', 'wb') as file:
        pickle.dump(new_lst, file)
        print('Saved properly.')

def open_url(url: str) -> list:
    with open(url, 'rb') as f:
        while True:
            try:
                data = pickle.load(f)
            except EOFError:
                break
    return data

def check_list(urls:list):
    for fname in urls:
        print(f'-----{fname}-----')
        right = classify_rightorwrong(fname)
        data = open_url('/Users/ijimin/Desktop/지민/pycharm/pyqt test/data_file/collected_data/'+fname)
        new_data = dect_misclassified(data,right)
        save('/Users/ijimin/Desktop/지민/pycharm/pyqt test/data_file/collected_data/'+fname, new_data)


def make_url_lst(pre_url:str) -> list:
    file_lst = os.listdir(pre_url)
    file_lst.remove('.DS_Store')
    return file_lst