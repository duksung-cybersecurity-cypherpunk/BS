import pandas as pd
import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import joblib
import numpy as np  # NumPy를 사용하기 위해 추가
import sys
import json
import os

# 데이터 로드
data = pd.read_excel('train_data.xlsx')  # 엑셀 파일에서 데이터 로드

X = data.drop('user', axis=1).values
y = data['user'].values

# 레이블 인코딩
unique_labels = list(set(y))
label_to_index = {label: idx for idx, label in enumerate(unique_labels)}
index_to_label = {idx: label for label, idx in label_to_index.items()}
y_encoded = [label_to_index[label] for label in y]

# 데이터 스케일링
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# 데이터 분할
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y_encoded, test_size=0.2)

# 모델 정의
class KeystrokeTransformer(nn.Module):
    def __init__(self, input_dim, model_dim, num_heads, num_layers, num_classes):
        super(KeystrokeTransformer, self).__init__()
        self.embedding = nn.Linear(input_dim, model_dim)
        self.transformer = nn.Transformer(d_model=model_dim, nhead=num_heads, num_encoder_layers=num_layers, batch_first=True)
        self.fc_out = nn.Linear(model_dim, num_classes)  # output_dim은 예측할 클래스 수

    def forward(self, src):
        src = self.embedding(src.unsqueeze(1))  # 입력 데이터를 임베딩 (batch_size, 1, model_dim)
        src = src.transpose(0, 1)  # (1, batch_size, model_dim)로 변환
        x = self.transformer(src, src)  # 트랜스포머 레이어 통과
        x = x.mean(dim=0)  # 평균값을 통해 최종 출력
        x = self.fc_out(x)  # 선형 변환을 통해 최종 출력
        return x

# 모델 초기화
input_dim = X_train.shape[1]
model = KeystrokeTransformer(input_dim=input_dim, model_dim=256, num_heads=8, num_layers=6, num_classes=len(index_to_label))

# 가중치 로드
try:
    model.load_state_dict(torch.load('keystroke_transformer_model.pth'))
    model.eval()  # 예측 모드 설정
    #print("모델 가중치가 성공적으로 로드되었습니다.")
except Exception as e:
    print(f"모델 가중치 로드 실패: {str(e)}")
    # 가중치 로드 실패 시에도 프로그램 종료하지 않고, 새롭게 훈련하도록 설정
    print("새로운 모델 훈련을 시작합니다.")

# 손실 함수 및 최적화 알고리즘
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# 모델 훈련
num_epochs = 30
for epoch in range(num_epochs):
    model.train()
    optimizer.zero_grad()
    outputs = model(torch.tensor(X_train, dtype=torch.float32))
    loss = criterion(outputs, torch.tensor(y_train, dtype=torch.long))
    loss.backward()
    optimizer.step()
    #print(f'Epoch {epoch + 1}/{num_epochs}, Loss: {loss.item()}')

# 모델 저장
torch.save(model.state_dict(), 'keystroke_transformer_model.pth')

# 스케일러 저장
joblib.dump(scaler, 'scaler.pkl')

# 레이블 매핑 저장
joblib.dump(label_to_index, 'label_to_index.pkl')
joblib.dump(index_to_label, 'index_to_label.pkl')

# 예측 함수 정의
def predict_user(keystroke_data):
    # 키스트로크 데이터가 30개보다 적다면 패딩 추가
    if len(keystroke_data) < 30:
        keystroke_data = np.pad(keystroke_data, (0, 30 - len(keystroke_data)), 'constant')
    else:
        keystroke_data = keystroke_data[:30]  # 최대 30개로 자름
    
    # 스케일링 처리
    keystroke_data_scaled = scaler.transform(np.array(keystroke_data).reshape(1, -1))
    
    # 텐서로 변환
    keystroke_tensor = torch.tensor(keystroke_data_scaled, dtype=torch.float32)
    
    # 예측 수행
    with torch.no_grad():
        output = model(keystroke_tensor)
        predicted_index = output.argmax(dim=1).item()

    # 인덱스를 사용자 이름으로 변환
    predicted_user = index_to_label[predicted_index]
    
    return predicted_user

# 서버로부터 데이터 입력 받기
if __name__ == "__main__":
    sys.stdout.reconfigure(encoding='utf-8')
    try:
        input_data = sys.stdin.read()
        keystroke_data = json.loads(input_data)
        #print("Received keystroke data:", keystroke_data)  # 데이터 수신 로그 추가
    except json.JSONDecodeError as e:
        #print(f"Invalid input data: JSON decoding failed - {str(e)}")
        sys.exit(1)

    # 예측 수행
    if 'intervals' in keystroke_data and len(keystroke_data['intervals']) > 0:
        try:
            predicted_user = predict_user(keystroke_data['intervals'])
            sys.stdout.write(predicted_user + "\n")
        except Exception as e:
            print(f"Prediction failed: {e}")
            sys.exit(1)
    else:
        print("Invalid or insufficient keystroke data")
        sys.exit(1)
