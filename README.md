# MNIST CUSTOM-CNN-Classifier

MNIST 데이터 셋을 이용하여 CNN 신경망 학습, 숫자 분류기 제작, 개인 데이터 셋 수집 후 재학습의 과정이 들어있다. CNN 신경망을 공부하는 도중 생기는 여러가지 문제점과 구현하고자 하는 기능들을 추가했다. 

## Code Structure

**`01. HandWritingClassifier`** : MNIST 데이터로 학습시킨 신경망을 기반으로 만든 숫자 분류기 

**`02. DataAugmentation`** : 개인 데이터 셋을 증강시키는 코드 (여러 문제가 있어, 04 버전에서 해결함.)

**`03. Visualization`** : 히트맵으로 경향성 확인

**`04. Augmentation`** : 02에 있었던 여러 문제들을 해결함 

`**05. trainercode.ipynb**` : 개인데이터셋, MNIST를 이용해 재학습하는 코드

**`01. HandWritingClassifier_final`** : 가장 성능이 좋은 신경망을 적용한 숫자 분류기+시각화 코드 포함
