import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.nn.modules.pooling import MaxPool2d

class Net(nn.Module):
    def __init__(self):
        super().__init__()

        self.conv1 = nn.Conv2d(1,10,5)
        self.conv2 = nn.Conv2d(10,20,5)

        self.pool = MaxPool2d(2,2)

        self.fc1 = nn.Linear(20*4*4, 100)
        self.fc2 = nn.Linear(100,10)
        #batch normalization
        self.bn1 = nn.BatchNorm2d(10)
        self.bn2 = nn.BatchNorm2d(20)

    def forward(self,x):
        x = x.to(torch.uint8)
        x = self.pool(F.relu(self.bn1(self.conv1(x))))
        print('debug')
        x = self.pool(F.relu(self.bn2(self.conv2(x))))
        print('debug')
        x = x.view(x.size(0), -1) # flat 꼭 해요오오
        print('debug')
        x = F.relu(self.fc1(x))
        print('debug')
        x = F.relu(self.fc2(x))
        print('debug')
        return x

model = Net()

classes = [0,1,2,3,4,5,6,7,8,9]