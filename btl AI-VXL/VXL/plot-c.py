import matplotlib.pyplot as plt
import pandas as pd

# Đọc file CSV vào dataframe
filename = "datac.csv"  # Thay bằng tên file của bạn
data = pd.read_csv(filename)

ecg_signal = data.iloc[:, 6].values

# Hiển thị 5 dòng đầu tiên để kiểm tra
print("Dữ liệu từ file CSV:")
print(data.head())


# Lặp qua từng cột ngoại trừ cột đầu tiên (Time)
# Thêm tiêu đề và nhãn
plt.figure(figsize=(14, 10))

plt.subplot(1, 1, 1)
plt.plot(ecg_signal, color='blue', label='ECG Signal')  # Đường tín hiệu màu xanh dương
plt.legend()
plt.title("ECG Signal")

plt.tight_layout()
plt.show()
