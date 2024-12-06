# BS
작품소개
"무생체" 프로젝트는 사용자의 키스트로크 데이터를 기반으로 실시간으로 예측된 사용자를 식별하는 시스템입니다. 이 시스템은 사용자의 타자 입력 속도와 패턴을 분석하여 예측 모델을 통해 사용자를 식별하고, 이를 실시간 채팅 애플리케이션에 반영하는 기능을 제공합니다. 이를 통해 사용자 인증 및 예측이 가능하며, 채팅 애플리케이션에서 사용자 경험을 향상시킬 수 있습니다.

작품 특징
실시간 키스트로크 분석: 사용자가 타이핑할 때마다 실시간으로 키스트로크 데이터를 수집하고, 이를 분석하여 예측된 사용자를 실시간으로 제공합니다.
Transformer 모델을 활용한 예측: 사용자의 타자 패턴을 학습하기 위해 Transformer 모델을 사용하며, 이 모델은 입력된 키스트로크 데이터를 바탕으로 정확한 사용자 예측을 제공합니다.
채팅 애플리케이션 통합: 예측된 사용자는 실시간 채팅 애플리케이션의 인터페이스에 표시됩니다. 사용자가 타이핑할 때마다 예측된 결과가 업데이트됩니다.
데이터 기반 사용자 인증: 키스트로크 분석을 통해 인증된 사용자가 올바르게 예측되면, 채팅에 참여할 수 있게 되는 시스템입니다.
Python과 JavaScript의 결합: 예측 모델은 Python으로 훈련되며, 실시간 웹 애플리케이션은 JavaScript로 구현되어, 두 기술이 유기적으로 결합되어 작동합니다.

기술 스택
프론트엔드:
HTML, CSS, JavaScript
사용자 인터페이스(UI)와 실시간 데이터 처리
백엔드:
Node.js, Express.js
채팅 애플리케이션의 서버 측 로직 및 데이터 흐름 처리
예측 모델:
Python, PyTorch
Transformer 모델을 활용하여 키스트로크 데이터를 분석하고 사용자 예측
데이터 처리:
Scikit-learn (데이터 스케일링 및 전처리)
파일 처리:
JSON 파일을 사용하여 사용자 데이터 및 예측 결과 저장

실행방법
1. 프로젝트 클론
git clone https://github.com/your-username/musaengche.git
cd musaengche
2. Node.js 의존성 설치
npm install
3. Python 의존성 설치 
requirements.txt 파일을 사용하여 Python 의존성을 설치합니다.
pip install -r requirements.txt
4. 모델 훈련 
Transformer 모델을 훈련시키기 위해 train_transformer.py 파일을 실행합니다.
python train_transformer.py
5. 서버실행
Node.js 서버를 실행하려면 아래 명령어를 입력합니다.
node server.js
6. 채팅 애플리케이션 실행 웹 브라우저에서 http://localhost:3000에 접속하여, 실시간으로 타이핑을 입력하고 예측된 사용자를 확인할 수 있습니다.

musaengche/
├── public/
│   ├── index.html        # 채팅 애플리케이션 HTML 파일, 사용자 인터페이스 제공
│   ├── keystroke.js      # 키스트로크 데이터 수집 및 예측 처리 JavaScript 파일
│   └── styles.css        # CSS 스타일시트, 애플리케이션의 디자인을 정의
├── server.js             # Node.js 서버 코드, 클라이언트 요청 처리 및 응답 전송
├── predict_transformer.py # 훈련된 모델을 사용하여 실시간 예측을 수행하는 Python 코드
├── train_transformer.py   # Transformer 모델을 훈련시키는 Python 코드
├── scaler.pkl            # 데이터 스케일러를 저장한 파일, 모델 입력 데이터 전처리
├── label_to_index.pkl    # 레이블을 인덱스로 매핑한 파일, 예측된 레이블을 효율적으로 처리
├── index_to_label.pkl    # 인덱스를 레이블로 매핑한 파일, 예측 결과를 해석하기 위해 사용
└── user.json             # 사용자 정보 저장 파일, 로그인 상태 및 예측된 사용자 정보 포함
