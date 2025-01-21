class AtopicView:
    @staticmethod
    def display_results(predicted_humidity, predicted_temp_change, language='en'):
        if language == 'ko':
            print(f"\n예측된 습도: {predicted_humidity:.2f}%")
            print(f"예측된 온도 변화: {predicted_temp_change:.2f}°C")

            if predicted_humidity > 70:
                print("경고: 높은 습도는 아토피 피부염을 유발할 수 있습니다!")
            if abs(predicted_temp_change) > 5:
                print("경고: 급격한 온도 변화는 아토피 피부염을 유발할 수 있습니다!")
        else:
            print(f"\nPredicted Humidity: {predicted_humidity:.2f}%")
            print(f"Predicted Temperature Change: {predicted_temp_change:.2f}°C")

            if predicted_humidity > 70:
                print("Warning: High humidity levels can trigger atopic dermatitis!")
            if abs(predicted_temp_change) > 5:
                print("Warning: Significant temperature change can trigger atopic dermatitis!")

    @staticmethod
    def plot_data(data, columns=None, title="Temperature and Humidity over Time"):
        import matplotlib.pyplot as plt

        if columns is None:
            columns = ['Temperature', 'Humidity']

        plt.figure(figsize=(10, 5))
        for column in columns:
            if column in data.columns:
                plt.plot(data.index, data[column], label=column)
            else:
                print(f"Warning: Column '{column}' not found in data.")

        plt.title(title)
        plt.xlabel("Date")
        plt.ylabel("Value")
        plt.legend()
        plt.show()

    @staticmethod
    def save_results_to_file(results, filename="results.txt"):
        try:
            with open(filename, 'w') as file:
                for key, value in results.items():
                    file.write(f"{key}: {value}\n")
            print(f"Results saved to {filename}")
        except Exception as e:
            print(f"Error saving results: {e}")
