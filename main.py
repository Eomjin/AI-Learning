from controllers.controller import AtopicApp
import tkinter as tk
import pandas as pd
import numpy as np

def load_data():
    # 예시 데이터 생성
    np.random.seed(42)
    dates = pd.date_range(start="2025-01-01", periods=365, freq="D")
    temperatures = np.sin(np.linspace(0, 2 * np.pi, 365)) * 10 + 20 + np.random.normal(0, 2, 365)
    humidity = np.random.normal(50, 15, 365)

    data = pd.DataFrame({"Date": dates, "Temperature": temperatures, "Humidity": humidity})
    data.set_index("Date", inplace=True)
    return data

if __name__ == "__main__":
    data = load_data()

    root = tk.Tk()
    app = AtopicApp(root, data)
    root.mainloop()
