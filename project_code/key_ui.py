import tkinter as tk
from tkinter import filedialog
from datetime import datetime
import pandas as pd

# 키 입력과 입력된 시간을 저장할 리스트
key_inputs = []
timestamps = []
input_count = 0  # 데이터 개수를 카운트할 변수

def on_key_press(event):
    global input_count
    if event.keysym == 'Return':
        # 엔터 키를 누르면 현재 입력된 키와 타임스탬프를 저장하고 리스트 초기화
        save_current_input()
        input_entry.delete('1.0', tk.END)  # 입력 필드 초기화
        input_count += 1  # 데이터 개수 증가
        count_label.config(text=f"입력된 데이터 개수: {input_count}")  # 라벨 업데이트
    else:
        key = event.char
        current_time = datetime.now().strftime('%S.%f')[:-3]
        key_inputs.append(key)
        timestamps.append(current_time)

def save_current_input():
    if key_inputs:
        global all_key_inputs, all_timestamps
        if len(all_key_inputs) == 0:  # 첫 번째 입력
            all_key_inputs.append(key_inputs.copy())
            all_timestamps.append(timestamps.copy())
        else:  # 두 번째 입력부터
            all_key_inputs.append([''] * len(key_inputs))  # 키는 빈 리스트 추가
            all_timestamps.append(timestamps.copy())

        # 현재 입력 초기화
        key_inputs.clear()
        timestamps.clear()

def save_to_excel():
    # 파일 저장 대화상자를 통해 파일 경로를 선택
    file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")])
    if file_path:
        # 데이터 준비
        data = []
        for keys, times in zip(all_key_inputs, all_timestamps):
            data.append(keys)  # 키를 가로로 정렬
            data.append(times)  # 타임스탬프 추가

        # DataFrame으로 변환
        df = pd.DataFrame(data)
        
        # 엑셀 파일로 저장
        df.to_excel(file_path, index=False, header=False)
        print(f"키 입력 데이터를 엑셀 파일로 저장했습니다: {file_path}")
        
        # 리스트 초기화
        all_key_inputs.clear()
        all_timestamps.clear()

# 전역변수 초기화
all_key_inputs = []
all_timestamps = []

window = tk.Tk()
window.geometry("400x500")
window.title("키 입력 및 저장")
window.configure(bg="#f5f5f5")  # 배경색 설정

# 컨테이너 프레임
container = tk.Frame(window, bg="white", bd=2, relief="groove")
container.pack(pady=30, padx=20, fill="both", expand=True)

# 상단 타이틀 라벨
title_label = tk.Label(container, text="키 입력을 기록하고 저장하기", font=("Arial", 16, "bold"), bg="white", fg="#333333")
title_label.pack(pady=(20, 10))

# 내비게이션 라벨
nav_frame = tk.Frame(container, bg="white")
nav_frame.pack(pady=(5, 15))

home_label = tk.Label(nav_frame, text="홈", font=("Arial", 10, "bold"), fg="#6e45e2", bg="white", cursor="hand2")
home_label.pack(side="left", padx=10)
profile_label = tk.Label(nav_frame, text="프로필", font=("Arial", 10, "bold"), fg="#6e45e2", bg="white", cursor="hand2")
profile_label.pack(side="left", padx=10)
logout_label = tk.Label(nav_frame, text="로그아웃", font=("Arial", 10, "bold"), fg="#6e45e2", bg="white", cursor="hand2")
logout_label.pack(side="left", padx=10)

# 키 입력을 받을 텍스트 필드
input_entry = tk.Text(container, height=10, width=40, wrap=tk.WORD, font=("Arial", 12), padx=10, pady=10, bg="#f9f9f9", relief="flat", bd=1)
input_entry.pack(pady=(0, 10))
input_entry.focus_set()

# 데이터 개수를 보여줄 라벨
count_label = tk.Label(container, text="입력된 데이터 개수: 0", font=("Arial", 12), bg="white", fg="#333333")
count_label.pack(pady=(5, 15))

# 데이터 저장 버튼
save_button = tk.Button(container, text="데이터 저장", command=save_to_excel, font=("Arial", 12, "bold"), bg="#6e45e2", fg="white", relief="flat", bd=0, width=20, height=2)
save_button.pack(pady=(5, 10))

# 하단 푸터
footer_label = tk.Label(container, text="BS 팀 졸업 프로젝트", font=("Arial", 10), bg="white", fg="#666666")
footer_label.pack(pady=(20, 10))

# 키 입력 이벤트 핸들러 함수 등록
input_entry.bind("<Key>", on_key_press)

window.mainloop()
