let timestamps = [];

function collectKeystroke(event) {
    const currentTime = new Date().getTime();
    if (timestamps.length > 0) {
        const lastTime = timestamps[timestamps.length - 1];
        const interval = (currentTime - lastTime) / 1000;  // 초 단위로 계산
        timestamps.push(currentTime);
        console.log(`Keystroke interval: ${interval} seconds`);
    } else {
        timestamps.push(currentTime);  // 첫 번째 키스트로크 시간 저장
    }
}

function sendKeystrokeData() {
    console.log('Send button clicked');  // 버튼 클릭 시 호출 확인

    if (timestamps.length < 2) {
        alert('충분한 키스트로크 데이터를 받지 못했습니다. 키 입력을 더 진행해 주세요.');
        return;
    }

    const intervals = [];
    for (let i = 1; i < timestamps.length; i++) {
        intervals.push((timestamps[i] - timestamps[i - 1]) / 1000);  // 키스트로크 간 시간 간격
    }

    const keystrokeData = {
        intervals: intervals,
    };

    console.log('Sending keystroke data:', keystrokeData);  // 전송 데이터 확인

    // 서버로 데이터 전송
    fetch('/predict', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(keystrokeData),
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        console.log('Predicted user:', data.user);
        addMessageToChatWindow(`예측된 사용자: ${data.user}`, 'bot');
    })
    .catch((error) => {
        console.error('Error:', error);
    });

    // 타이핑 데이터 초기화
    timestamps = [];
}

// 채팅 메시지 추가 함수
function addMessageToChatWindow(message, sender) {
    const chatWindow = document.getElementById('chat-window');
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('chat-message', sender);
    messageDiv.innerText = message;
    chatWindow.appendChild(messageDiv);
    chatWindow.scrollTop = chatWindow.scrollHeight;
}

// HTML에서 전송 버튼에 이벤트 연결 (send-button과 message-input ID가 있는지 확인)
document.getElementById('send-button').addEventListener('click', sendKeystrokeData);
document.getElementById('message-input').addEventListener('keydown', collectKeystroke);