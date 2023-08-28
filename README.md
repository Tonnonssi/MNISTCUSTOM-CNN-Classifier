# MNIST CUSTOM-CNN-Classifier

MNIST 데이터 셋을 이용하여 CNN 신경망 학습, 숫자 분류기 제작, 개인 데이터 셋 수집 후 재학습의 과정이 들어있다. CNN 신경망을 공부하는 도중 생기는 여러가지 문제점과 구현하고자 하는 기능들을 추가했다. 

## Code Structure

**`01. HandWritingClassifier`** : MNIST 데이터로 학습시킨 신경망을 기반으로 만든 숫자 분류기 

**`02. DataAugmentation`** : 개인 데이터 셋을 증강시키는 코드 (여러 문제가 있어, 04 버전에서 해결함.)

**`03. Visualization`** : 히트맵으로 경향성 확인

**`04. Augmentation`** : 02에 있었던 여러 문제들을 해결함 

**`05. trainercode.ipynb`** : 개인데이터셋, MNIST를 이용해 재학습하는 코드

**`01. HandWritingClassifier_final`** : 가장 성능이 좋은 신경망을 적용한 숫자 분류기+시각화 코드 포함

## Result
### 01. MNIST로 학습시킨 신경망
커스텀 데이터는 MNIST 데이터 셋과 달리, 숫자의 크기가 제각각이기 때문에 제대로된 예측이 되지 않았다. 이 문제를 1차적으로 해결하기 위해 숫자 영역을 인식해 확대하는 방식의 스케일링을 적용했다. 
![image](https://github.com/Tonnonssi/MNISTCUSTOM-CNN-Classifier/assets/126959470/30258b11-5649-418f-8591-88f2d952fa24)
![image](https://github.com/Tonnonssi/MNISTCUSTOM-CNN-Classifier/assets/126959470/b726eef1-e33a-4d0a-8b76-8daa548edbf3)

### 02. 확대 방식을 바꾼 숫자 분류기
회전, 확대와 같은 증강기법을 적용하는 과정에서 데이터 타입 변환에 따른 스택오버플로우 문제가 발생한다. 이 문제를 해결하자, 1을 잘 인식하지 못하던 기존의 문제가 해결되는 모습을 보였다. 

![image](https://github.com/Tonnonssi/MNISTCUSTOM-CNN-Classifier/assets/126959470/11f9bd62-5500-4fbf-8c2f-bd9fa6581a5e)
![image](https://github.com/Tonnonssi/MNISTCUSTOM-CNN-Classifier/assets/126959470/b45e830b-712a-4f0b-98c8-bfd450ab5bbe)


### 03. MNIST+Custom 데이터로 학습시킨 모델
불규칙한 사이즈의 데이터와 스케일링된 데이터를 전부 같이 학습시킨다면, 추가적인 스케일링 없이도 작동되는 분류기를 만들 수 있지 않을까란 생각을 했다. 결과는 다음과 같다. 여러 증강법을 사용했음에도 불구하고, 모든 예외를 처리하기엔 데이터셋이 부족했는지, 오히려 성능이 떨어진 모습을 보였다.

MNIST로만 학습한 모델
![image](https://github.com/Tonnonssi/MNISTCUSTOM-CNN-Classifier/assets/126959470/5b3fdb5a-ddac-43f8-8f27-20b3cdbf2379)
불규칙한 커스텀 데이터와 함께 학습시킨 모델
![image](https://github.com/Tonnonssi/MNISTCUSTOM-CNN-Classifier/assets/126959470/7ea59e04-7a96-4588-b911-96eb3c87b9ce)
MNIST만으로 학습 + 스케일링 적용
![image](https://github.com/Tonnonssi/MNISTCUSTOM-CNN-Classifier/assets/126959470/373681fb-9c6c-4997-a155-0b31e633ea75)
불규칙한 커스텀 데이터와 함께 학습 + 스케일링 적용
![image](https://github.com/Tonnonssi/MNISTCUSTOM-CNN-Classifier/assets/126959470/5aaa573e-49e8-4a3e-949d-bf02b2804b28)


