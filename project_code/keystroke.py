import numpy as np
from predict_transformer import KeystrokeTransformer
import torch
import joblib
import sys
import json

# 모델 및 스케일러 로드
index_to_label = joblib.load('index_to_label.pkl')
model = KeystrokeTransformer(input_dim=30, model_dim=64, num_heads=4, num_layers=3, num_classes=len(index_to_label))
model.load_state_dict(torch.load('keystroke_transformer_model.pth'))
model.eval()
scaler = joblib.load('scaler.pkl')

# 예측 함수 정의
def predict_user(keystroke_data):
    if len(keystroke_data) < 30:
        keystroke_data = np.pad(keystroke_data, (0, 30 - len(keystroke_data)), 'constant')
    
    keystroke_data_scaled = scaler.transform(np.array(keystroke_data).reshape(1, -1))
    keystroke_tensor = torch.tensor(keystroke_data_scaled, dtype=torch.float32)

    with torch.no_grad():
        output = model(keystroke_tensor)
        predicted_index = output.argmax(dim=1).item()

    predicted_user = index_to_label[predicted_index]
    return predicted_user

# 서버로부터 데이터 입력 받기
if __name__ == "__main__":
    # 표준 입력으로 JSON 형식의 키스트로크 데이터 수신
    try:
        input_data = sys.stdin.read()
        keystroke_data = json.loads(input_data)
    except json.JSONDecodeError:
        print("Invalid input data: JSON decoding failed")
        sys.exit(1)

    # 예측 수행
    if 'intervals' in keystroke_data and len(keystroke_data['intervals']) > 0:
        try:
            predicted_user = predict_user(keystroke_data['intervals'])
            print(f"예측된 사용자: {predicted_user}")
        except Exception as e:
            print(f"Prediction failed: {str(e)}")
    else:
        print("Invalid or insufficient keystroke data")