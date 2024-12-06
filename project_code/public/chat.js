const socket = io();
let keystrokes = [];
let lastKeyTime = Date.now();

// 키스트로크 데이터 수집
document.getElementById('chatInput').addEventListener('keydown', (event) => {
    const currentTime = Date.now();
    const timeDiff = currentTime - lastKeyTime;
    lastKeyTime = currentTime;

    // 눌린 키와 시간 차이를 객체로 저장
    keystrokes.push({ key: event.key, timeDiff });
});

// 메시지 전송 버튼 클릭 시
document.getElementById('sendButton').addEventListener('click', () => {
    const message = document.getElementById('chatInput').value;
    const username = 'your_username';  // 실제 사용자의 이름을 입력하세요
    const room = 'default_room';  // 방 이름을 설정하세요

    // 서버에 메시지와 키스트로크 전송
    socket.emit('chat message', { room, username, message, keystrokes });
    keystrokes = [];  // 전송 후 초기화
});

// 예측 결과 수신 시
socket.on('user prediction', (data) => {
    const { predictedUser } = data;

    // 사용자 예측 팝업 표시
    alert(`예측된 사용자: ${predictedUser}`);
});
