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
![softmax_unimproved.png](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/75f4cab0-3036-40c4-8a5e-c07a31ae06b1/softmax_unimproved.png)

![softmax_improved.png](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/f3ed7ac6-dca5-49e8-896c-d883b6fcaf2e/softmax_improved.png)


### 02. 확대 방식을 바꾼 숫자 분류기
회전, 확대와 같은 증강기법을 적용하는 과정에서 데이터 타입 변환에 따른 스택오버플로우 문제가 발생한다. 이 문제를 해결하자, 1을 잘 인식하지 못하던 기존의 문제가 해결되는 모습을 보였다. 

![확대 정규화를 적용하지 않은 예측 모델](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/e4a587ed-9b72-4297-8467-9fbf22fce6cb/unimproved_01.png)

확대 정규화를 적용하지 않은 예측 모델

![리팩토링한 확대 정규화를 적용한 모델](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/1e3b2999-edd4-4124-b7d2-c8d436649075/improved_01.png)

리팩토링한 확대 정규화를 적용한 모델


### 03. MNIST+Custom 데이터로 학습시킨 모델
불규칙한 사이즈의 데이터와 스케일링된 데이터를 전부 같이 학습시킨다면, 추가적인 스케일링 없이도 작동되는 분류기를 만들 수 있지 않을까란 생각을 했다. 결과는 다음과 같다. 여러 증강법을 사용했음에도 불구하고, 모든 예외를 처리하기엔 데이터셋이 부족했는지, 오히려 성능이 떨어진 모습을 보였다.

![MNIST데이터만으로 학습한 모델](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/b6af8080-03e8-4b8d-9620-457a14b5ec3a/unimproved_01.png)

MNIST데이터만으로 학습한 모델

![불규칙한 데이터와 같이 학습시킨 모델](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/793f8a02-8642-4d5d-bb77-363972bdf23a/unimproved_heatmap_02.png)

불규칙한 데이터와 같이 학습시킨 모델

![MNIST만으로 학습 + 스케일링 적용](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/30343f2d-dd7f-4508-b75f-4cc712024f7f/improved_01.png)

MNIST만으로 학습 + 스케일링 적용

![불규칙한 데이터와 같이 학습 + 스케일링](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/80f3327b-d8be-492d-93d1-eb0465dd05cc/improved_heatmap_02.png)

불규칙한 데이터와 같이 학습 + 스케일링
