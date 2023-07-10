import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import numpy as np
import random
import torch
import pickle

from net import net
import zoom

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        # 정규화 유무
        self.improved = True
        # 그리기 관련 기본 세팅
        self.image = QImage(QSize(400,400), QImage.Format_RGB32)
        self.image.fill(Qt.white)
        self.drawing = False
        self.brush_size = 20
        self.brush_color = Qt.black
        self.last_point = QPoint()
        # 모델 불러오기 관련 기본 세팅
        self.loaded_model = None
        self.path_of_model = '/Users/ijimin/Desktop/Python Code/MNISTCUSTOM_CNN_Classifier/01. HandWritingClassifier/models/MNIST_CNNmodel_99%_state.pth'
        # 여러가지
        self.improved_dict = {True:'improved_custom_data.txt',
                              False:'unimproved_custom_data.txt'}
        self.improved_num = 0
        self.classes = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        # 저장 관련 기본 세팅
        self.num = random.randrange(0,10)
        self.predicted_num = 0
        self.input_arr = np.zeros((28,28))
        self.present_lst = []
        self.initUI()

    def initUI(self):
        '''
        1. self.statusbar : 써야하는 숫자를 지정
        2. self.formatbar : Next, Save 버튼이 나타나는 부분
        3. 모델을 자동으로 로드
        4. 이외 추가 기능들을 구현
        5. 제목 및 불러오기
        '''
        # 써야하는 숫자를 지정
        self.statusbar = self.statusBar()
        self.presented_value = QLabel(f'{self.num} 써주세요',self)
        self.presented_value.move(155,0)

        # Next, Save 버튼이 나타나는 부분
        self.formatbar = QToolBar(self)
        self.addToolBar(Qt.BottomToolBarArea, self.formatbar)

        next_button = QToolButton(self)
        next_button.setText('Next')
        next_button.clicked.connect(self.run_if_next_pushed)

        save_button = QToolButton(self)
        save_button.setText('Save')
        save_button.clicked.connect(self.run_if_save_pushed)

        self.formatbar.addWidget(next_button)
        self.formatbar.addWidget(save_button)

        #모델을 자동으로 로드
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

    def run_if_next_pushed(self):
        self.run_if_empty()
        self.save(self.present_lst)
        self.clear()
        self.present_num()

    def run_if_save_pushed(self):
        #by pickle
        self.exist_lst = self.load_f()

        fname = self.improved_dict[self.improved]
        with open('/Users/ijimin/Desktop/Python Code/MNISTCUSTOM_CNN_Classifier/01. HandWritingClassifier/datafile/'+fname, 'wb') as f:
            new_lst = self.exist_lst + self.present_lst
            pickle.dump(new_lst, f)
            f.close()

        self.statusbar.showMessage("저장되었습니다.")

    def load_f(self):
        fname = self.improved_dict[self.improved]

        pre_lst = []
        f = open(f'/Users/ijimin/Desktop/Python Code/MNISTCUSTOM_CNN_Classifier/01. HandWritingClassifier/datafile/'+fname,'rb')
        while True:
            try:
                pre_lst = pickle.load(f)
            except EOFError:
                break
        return pre_lst

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
            self.drawing = False
            self.input_arr = np.zeros((28, 28))
            for i in range(28):
                for j in range(28):
                    self.input_arr[j, i] = 1 - self.image.scaled(28, 28).pixelColor(i, j).getRgb()[0] / 255.0

            if self.improved == True:
                zooming = zoom.ZoomAugmentor(self.input_arr)
                zooming.run()
                self.input_arr = zooming.final_img

            self.input_arr = self.input_arr.reshape(-1, 28, 28)
            tensor = torch.from_numpy(self.input_arr).float()
            x = tensor.unsqueeze(dim=0)

            if self.loaded_model:
                net.load_state_dict(self.loaded_model)
                net.eval()

                with torch.no_grad():
                    pred = net(x)
                    ans = torch.argmax(pred).item()
                    self.predicted_num = self.classes[ans]
                    self.statusbar.showMessage("추정 값은" + str(self.predicted_num) + "입니다.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    ex.show()
    sys.exit(app.exec_())