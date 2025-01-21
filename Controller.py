import tkinter as tk
from tkinter import messagebox
import pandas as pd

class AtopicApp:
    def __init__(self, root, data):
        self.root = root
        self.data = data
        self.root.title("아토피 발현도 예측")

        # 입력창 UI
        tk.Label(root, text="날짜를 입력하세요 (YYYY-MM-DD):").grid(row=0, column=0, padx=10, pady=10)
        self.date_entry = tk.Entry(root)
        self.date_entry.grid(row=0, column=1, padx=10, pady=10)

        self.predict_button = tk.Button(root, text="예측하기", command=self.predict)
        self.predict_button.grid(row=1, column=0, columnspan=2, pady=10)

        self.result_label = tk.Label(root, text="", fg="blue")
        self.result_label.grid(row=2, column=0, columnspan=2, pady=10)

    def predict(self):
        # 사용자 입력 날짜 가져오기
        date_input = self.date_entry.get()
        try:
            date = pd.to_datetime(date_input)
        except ValueError:
            messagebox.showerror("입력 오류", "날짜 형식이 잘못되었습니다. YYYY-MM-DD 형식으로 입력해주세요.")
            return

        # 데이터에서 해당 날짜 확인
        if date not in self.data.index:
            messagebox.showerror("데이터 없음", "입력한 날짜의 데이터를 찾을 수 없습니다.")
            return

        # 예측 데이터 가져오기
        weather = self.data.loc[date]
        temperature = weather['Temperature']
        humidity = weather['Humidity']

        # 결과 메시지 작성
        condition = "건조" if humidity < 50 else "습함"
        advice = "날씨가 많이 건조하게 느껴질 겁니다. 연고를 바르거나 약을 드시는 것을 추천하고 평소에 보습에 신경쓰시길 바랍니다." if humidity < 50 else "습도가 높으니 간지러움 발병에 주의 하십시오."
        result_text = f"오늘의 날씨: {condition}, 온도: {temperature:.1f}°C, 습도: {humidity:.0f}%\n{advice}"

        # 결과 출력
        self.result_label.config(text=result_text)
