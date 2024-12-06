const express = require('express');
const bodyParser = require('body-parser');
const fs = require('fs');
const { spawn } = require('child_process');
const path = require('path');
const cors = require('cors');
const bcrypt = require('bcrypt'); // bcrypt 모듈 추가

const app = express();
const PORT = 3000;
const USERS_FILE = path.join(__dirname, 'user.json');

// 사용자 정보를 메모리에 로드하는 함수
const loadUsers = () => {
    if (fs.existsSync(USERS_FILE)) {
        const data = fs.readFileSync(USERS_FILE, 'utf-8');
        return JSON.parse(data);
    }
    return {};
};

// 사용자 정보를 파일에 저장하는 함수
const saveUsers = (users) => {
    try {
        fs.writeFileSync(USERS_FILE, JSON.stringify(users, null, 2));
        console.log('회원가입 정보가 저장되었습니다:', users);
    } catch (error) {
        console.error('회원가입 정보 저장 중 오류 발생:', error);
    }
};

// 사용자 정보를 메모리에 로드
let users = loadUsers();

app.use(cors());
app.use('/static', express.static(path.join(__dirname, 'public')));
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

// 로그인 페이지 제공
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'signup.html'));
});

// 메뉴 페이지 제공
app.get('/menu', (req, res) => {
    res.sendFile(path.join(__dirname, 'public/menu.html'));
});

// 프로필 페이지 제공
app.get('/profile.html', (req, res) => {
    res.sendFile(path.join(__dirname, 'public/profile.html'));
});

// 채팅방 페이지 제공
app.get('/index.html', (req, res) => {
    res.sendFile(path.join(__dirname, 'public/index.html'));
});

// 회원가입 라우트 설정
app.post('/signup', async (req, res) => {
    const { username, password } = req.body;
    const passwordRegex = /^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]+$/;

    if (users[username]) {
        return res.status(400).send('회원가입 실패: 이미 존재하는 사용자 이름입니다.');
    }
    if (!passwordRegex.test(password)) {
        return res.status(400).send('회원가입 실패: 비밀번호는 영어와 숫자의 조합이어야 합니다.');
    }
    if (!username || !password) {
        return res.status(400).send('회원가입 실패: 사용자 이름과 비밀번호를 입력해주세요.');
    }

    try {
        // 비밀번호 해시화
        const hashedPassword = await bcrypt.hash(password, 10);
        users[username] = { password: hashedPassword, isVerified: false };
        saveUsers(users);
        res.status(200).send('회원가입 성공');
    } catch (error) {
        console.error('회원가입 중 오류 발생:', error);
        res.status(500).send('회원가입 중 오류가 발생했습니다.');
    }
});

// 로그인 라우트 설정
app.post('/login', async (req, res) => {
    const { username, password } = req.body;
    const user = users[username];

    if (user && await bcrypt.compare(password, user.password)) {
        res.redirect('/menu');
    } else {
        res.status(401).send('로그인 실패: 잘못된 사용자 이름 또는 비밀번호입니다.');
    }
});

// 키스트로크 데이터 수집 실행
app.get('/keystroke', (req, res) => {
    const pythonProcess = spawn('python3', [path.join(__dirname, 'key1.py')]);

    pythonProcess.stdout.on('data', (data) => {
        console.log(`stdout: ${data}`);
    });

    pythonProcess.stderr.on('data', (data) => {
        console.error(`stderr: ${data}`);
    });

    pythonProcess.on('close', (code) => {
        console.log(`child process exited with code ${code}`);
    });

    res.send('키스트로크 데이터 수집이 시작되었습니다. 창을 확인하세요.');
});

// 키스트로크 데이터를 받아 예측 수행
app.post('/predict', (req, res) => {
    console.log('Received keystroke data:', req.body);
    const keystrokeData = req.body;

    if (!keystrokeData || !keystrokeData.intervals || keystrokeData.intervals.length === 0) {
        console.error('No valid keystroke data provided');
        return res.status(400).json({ error: 'No valid keystroke data provided', user: '알 수 없음' });
    }

    const pythonProcess = spawn('python3', [path.join(__dirname, 'predict_transformer.py')]);
    pythonProcess.stdin.write(JSON.stringify(keystrokeData));
    pythonProcess.stdin.end();

    let predictedUser = '';
    pythonProcess.stdout.on('data', (data) => {
        console.log('Python script output:', data.toString());
        predictedUser += data.toString();
    });

    pythonProcess.stderr.on('data', (data) => {
        console.error(`Python script stderr: ${data}`);
    });

    pythonProcess.on('close', (code) => {
        console.log(`Python script exited with code ${code}`);
        if (code !== 0) {
            console.error('Python script execution failed');
            return res.status(500).json({ error: 'Prediction failed', user: '알 수 없음' });
        }
        console.log('Predicted user:', predictedUser.trim());
        res.json({ user: predictedUser.trim() });
    });
});

app.listen(PORT, () => {
    console.log(`Server running on http://localhost:${PORT}`);
});
