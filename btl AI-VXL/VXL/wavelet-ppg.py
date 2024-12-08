import numpy as np
import pandas as pd
import pywt
import matplotlib.pyplot as plt

# Tải dữ liệu từ file CSV
inputdata = pd.read_csv('datac.csv')
fs = 1000

# Xác định độ dài của data
data_length = len(inputdata)
print(data_length)
# Tính phần dư của data khi chia cho 64
remainder = data_length % 64
# Nếu phần dư khác 0, bỏ phần dư ở cuối
dataa = inputdata.iloc[:data_length - remainder]
# Lưu dữ liệu đã xử lý vào file CSV mới
output_file_path = 'data.csv'
dataa.to_csv(output_file_path, index=False)

# Đọc data vừa chỉnh sửa
data = pd.read_csv('data.csv')

# Lấy data từ các cột trong file csv
ecg_signal = data.iloc[:, 7].values

# Bước 2: Định nghĩa wavelet
lendata = len(data)
wavelet = 'db4'

# Thực hiện phép phân tích wavelet cho tín hiệu ECG
cA_ecg = ecg_signal
coeffs_ecg = []
for i in range(9):
    cA_ecg, cD_ecg = pywt.dwt(cA_ecg, wavelet, mode='symmetric', axis=-1)
    coeffs_ecg.append((cA_ecg, cD_ecg))

# Tín hiệu ECG theo lv
level_ecg = 6
cA8_ecg, cD8_ecg = coeffs_ecg[level_ecg - 1]
A8_ecg = pywt.upcoef('a', cA8_ecg, wavelet, level=level_ecg, take=lendata)

# Vẽ tín hiệu
plt.figure(figsize=(14, 10))
plt.subplot(1, 1, 1)
plt.plot(A8_ecg, color='red', label='ECG Signal')  # Đường tín hiệu màu đỏ
plt.legend()
plt.title("ECG Signal")
plt.tight_layout()
plt.show()

# Tạo DataFrame chỉ chứa tín hiệu ECG
output_data = pd.DataFrame({
    'Indices': range(len(A8_ecg)),  # Tạo chỉ số từ 0 đến len(A8_ecg) - 1
    'A8_ECG': A8_ecg,               # Tín hiệu ECG đã phân tích
})

# Lưu dữ liệu vào file CSV
output_file_path = 'ppg-output.csv'
output_data.to_csv(output_file_path, index=False, encoding='utf-8')

print(f"Tín hiệu ECG đã được lưu vào {output_file_path}")
