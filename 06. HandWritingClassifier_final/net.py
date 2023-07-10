import torch.nn as nn
import torch.nn.functional as F
from torch.nn.modules.pooling import MaxPool2d

class Net3x3(nn.Module):
    def __init__(self, bn=False):
        super().__init__()
        self.bn = bn

        self.conv1 = nn.Conv2d(1,10,3)
        self.conv2 = nn.Conv2d(10,20,3)

        self.pool = MaxPool2d(2,2)

        self.fc1 = nn.Linear(20*5*5, 100)
        self.fc2 = nn.Linear(100,10)

        #batch normalization
        self.bn1 = nn.BatchNorm2d(10)
        self.bn2 = nn.BatchNorm2d(20)

    def forward(self,x):
        if self.bn == True:
            x = self.pool(F.relu(self.bn1(self.conv1(x))))
            x = self.pool(F.relu(self.bn2(self.conv2(x))))
        else:
            x = self.pool(F.relu(self.conv1(x)))
            x = self.pool(F.relu(self.conv2(x)))
        x = x.view(x.size(0), -1) #flat
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        return x

net = Net3x3()
