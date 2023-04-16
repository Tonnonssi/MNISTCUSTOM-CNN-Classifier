import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import random
import pickle

import torch
import numpy as np
from net import *
from cut import *

ca = CuttingAugmentation()

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        #그리기 세팅
        self.image = QImage(QSize(400,400), QImage.Format_RGB32)
        self.image.fill(Qt.white)
        self.drawing = False
        self.brush_size = 20
        self.brush_color = Qt.black
        self.last_point = QPoint()

        #모델 자동으로 불러오기
        self.loaded_model = None
        self.path_of_model = '/Users/ijimin/내 드라이브/MNISTandCustom/trained_model/state/with_bn_model_63.5%.pth'

        # 저장 세팅
        self.num = random.randrange(0,10) #이부분은 차후 수정
        self.predicted_num = 0
        self.input_srr = np.zeros((28,28))
        self.new_data = []
        self.new_data_path = '/Users/ijimin/Desktop/지민/pycharm/pyqt test/new_custom_data.txt'
        self.improved = True

        self.initUI()

    def initUI(self):
        # 써야하는 숫자를 지정
        self.statusbar = self.statusBar()
        self.presented_value = QLabel(f'{self.num} 써주세요', self)
        self.presented_value.move(155, 0)

        # Right, Wrong, Save 버튼이 나타나는 부분
        self.formatbar = QToolBar(self)
        self.addToolBar(Qt.BottomToolBarArea, self.formatbar)

        right_button = QToolButton(self)
        right_button.setText('Right')
        right_button.clicked.connect(self.run_if_right_pushed)

        wrong_button = QToolButton(self)
        wrong_button.setText('Wrong')
        wrong_button.clicked.connect(self.run_if_wrong_pushed)

        save_button = QToolButton(self)
        save_button.setText('Save')
        save_button.clicked.connect(self.run_if_save_pushed)

        self.formatbar.addWidget(right_button)
        self.formatbar.addWidget(wrong_button)
        self.formatbar.addWidget(save_button)

        # 모델을 자동으로 로드
        if self.path_of_model:
            self.loaded_model = torch.load(self.path_of_model)
            self.statusbar.showMessage('모델이 로드되었습니다.')

        #제목 및 불러오기
        self.setWindowTitle('MNIST 분류기')
        self.setGeometry(300,300,400,400)
        self.show()

    def present_num(self):
        self.num = random.randrange(0,10)
        self.presented_value.setText(f'{self.num} 써주세요')

    def save(self, lst):
        correct_value = int(self.num)
        predicted_value = int(self.predicted_num)
        input_arr = self.input_arr
        lst.append([correct_value, predicted_value, input_arr])

    def clear(self):
        self.image.fill(Qt.white)
        self.update()
        self.statusbar.clearMessage()

    def run_if_empty(self):
        if np.any(self.input_arr.flatten()>0.) == False:
            self.statusbar.showMessage('숫자를 쓴 후 눌러주세요.')

    def run_if_right_pushed(self):
        self.run_if_empty()
        self.save(self.new_data)
        self.clear()
        self.present_num()

    def run_if_wrong_pushed(self):
        self.run_if_empty()
        self.save(self.new_data)
        self.clear()
        self.present_num()

    def run_if_save_pushed(self):
        self.exist_lst = self.load_f(self.new_data_path)

        with open(self.new_data_path,'wb') as f:
            process_lst = self.exist_lst + self.new_data
            pickle.dump(process_lst, f)
            f.close()

    def load_f(self):
        exist_lst = []
        with open(self.new_data_path,'rb') as f:
            while True:
                try:
                    exist_lst = pickle.load(f)
                except EOFError:
                    break
        return exist_lst

    def paintEvent(self, e):
        canvas = QPainter(self)
        canvas.drawImage(self.rect(), self.image, self.image.rect())

    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            self.drawing = True
            self.last_point = e.pos()

    def mouseMoveEvent(self, e):
        if (e.buttons() & Qt.LeftButton) & self.drawing:
            painter = QPainter(self.image)
            painter.setPen(QPen(self.brush_color, self.brush_size, Qt.SolidLine, Qt.RoundCap))
            painter.drawLine(self.last_point, e.pos())
            self.last_point = e.pos()
            self.update()

    def mouseReleaseEvent(self, e):
        if e.button() == Qt.LeftButton:
            # self.drawing = False
            self.input_arr = np.zeros((28, 28))
            for i in range(28):
                for j in range(28):
                    self.input_arr[j, i] = 1 - self.image.scaled(28, 28).pixelColor(i, j).getRgb()[0] / 255.0

            if self.improved:
                self.input_arr = ca.progress(self.input_arr,self.num)
            self.input_arr = self.input_arr.reshape(-1,28,28)
            tensor = torch.from_numpy(self.input_arr)
            x = tensor.unsqueeze(dim=0)
            x = x.to(torch.uint8)

            if self.loaded_model:
                model.load_state_dict(self.loaded_model)
                model.eval()

                with torch.no_grad():
                    pred = model(x)
                    ans = torch.argmax(pred).item()
                    self.predicted_num = classes[ans]
                    self.statusbar.showMessage("추정 값은" + self.predicted_num + "입니다.")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    ex.show()
    sys.exit(app.exec_())