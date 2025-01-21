import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense


class AtopicModel:
    def __init__(self, data):
        self.data = data
        self.scaler = MinMaxScaler()
        self.model = None

    def preprocess_data(self):
        # 'Date' 컬럼을 datetime 형식으로 변환
        self.data['Date'] = pd.to_datetime(self.data['Date'], errors='coerce')

        # 잘못된 날짜를 제거
        self.data = self.data.dropna(subset=['Date'])

        # 새로운 특성 생성
        self.data['Temperature_Change'] = self.data['Temperature'].diff().fillna(0)
        self.data['Humidity'] = self.data['Humidity'].fillna(self.data['Humidity'].mean())

        # 특성 스케일링
        self.data[['Humidity', 'Temperature_Change']] = self.scaler.fit_transform(
            self.data[['Humidity', 'Temperature_Change']]
        )

        # 인덱스 재설정
        self.data.reset_index(drop=True, inplace=True)

    def create_sequences(self, sequence_length=30):
        X, y = [], []
        for i in range(len(self.data) - sequence_length):
            # 'Humidity', 'Temperature_Change' 특성 사용
            X.append(self.data.iloc[i:i + sequence_length][['Humidity', 'Temperature_Change']].values)
            # 다음 시점의 타겟값 추가
            y.append(self.data.iloc[i + sequence_length][['Humidity', 'Temperature_Change']].values)
        return np.array(X), np.array(y)

    def build_model(self, sequence_length=30):
        # LSTM 모델 생성
        model = Sequential([
            LSTM(50, return_sequences=True, input_shape=(sequence_length, 2)),  # 2개의 특성
            LSTM(50),
            Dense(2)  # 'Humidity', 'Temperature_Change' 예측
        ])
        model.compile(optimizer="adam", loss="mse")
        return model

    def train_model(self, X_train, y_train, epochs=10, batch_size=16):
        if self.model is None:
            self.model = self.build_model(X_train.shape[1])
        self.model.fit(X_train, y_train, epochs=epochs, batch_size=batch_size)

    def predict(self, recent_data):
        if self.model is None:
            raise ValueError("모델이 아직 학습되지 않았습니다. 학습 후 예측을 시도하세요.")

        # 입력 데이터 형태 확인
        if len(recent_data.shape) != 3:
            raise ValueError(f"3D 배열 입력이 필요합니다. 현재 입력 모양: {recent_data.shape}.")

        # 예측 수행
        predicted_scaled = self.model.predict(recent_data)
        # 각각의 타겟값 스케일링 복원
        humidity = self.scaler.inverse_transform([[predicted_scaled[0][0], 0]])[0][0]
        temp_change = self.scaler.inverse_transform([[0, predicted_scaled[0][1]]])[0][1]
        return humidity, temp_change



