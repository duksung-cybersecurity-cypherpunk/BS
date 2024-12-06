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
window.geometry("350x350")
window.title("키 입력 및 저장")
window.option_add("*Font", "고운돋음")

# 키 입력을 받을 Entry 위젯 생성
input_entry = tk.Text(window, height=10, width=40)
input_entry.pack()
input_entry.focus_set()

# 데이터 개수를 보여줄 Label 생성
count_label = tk.Label(window, text="입력된 데이터 개수: 0", font=("고운돋음", 12))
count_label.pack()

# 키 입력 이벤트 핸들러 함수 등록
input_entry.bind("<Key>", on_key_press)

# 데이터 저장 버튼 생성
save_button = tk.Button(window, text="데이터 저장", width=15, height=2, command=save_to_excel)
save_button.pack()

window.mainloop()