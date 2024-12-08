import numpy as np
import pandas as pd
import pywt
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
import math as npmath
# Tải dữ liệu từ file CSV
inputdata = pd.read_csv('datac.csv')
fs = 1000

# Xác định độ dài của data
data_length = len(inputdata)
print(data_length)
# Tính phần dư của data khi chia cho 256
remainder = data_length % 64
# Nếu phần dư khác 0, bỏ phần dư ở cuối
dataa = inputdata.iloc[:data_length - remainder]
# Lưu dữ liệu đã xử lý vào file CSV mới
output_file_path = 'data.csv'
dataa.to_csv(output_file_path, index=False)

# Đọc data vừa chỉnh sửa
data = pd.read_csv('data.csv')

# Lấy data từ các cột trong file csv
pcg_signal = data.iloc[:, 6].values

# Bước 2: Định nghĩa wavelet
lendata = len(data)
wavelet = 'db4'

# Thực hiện phép phân tích wavelet cho tín hiệu PCG
cA_pcg = pcg_signal
coeffs_pcg = []
for i in range(9):
    cA_pcg, cD_pcg = pywt.dwt(cA_pcg, wavelet, mode='symmetric', axis=-1)
    coeffs_pcg.append((cA_pcg, cD_pcg))

# Mở gói các hệ số để vẽ tín hiệu PCG
level_pcg = 2

cA8_pcg, cD8_pcg = coeffs_pcg[level_pcg - 1]
D8_pcg = pywt.upcoef('d', cD8_pcg, wavelet, level= level_pcg, take = lendata)

plt.figure(figsize=(14, 10))

plt.subplot(1, 1, 1)
plt.plot(D8_pcg, color='blue', label='ECG Signal')  # Đường tín hiệu màu xanh dương
plt.legend()
plt.title("ECG Signal")

plt.tight_layout()
plt.show()

# Tạo DataFrame chỉ chứa các chỉ số và tín hiệu từ hai kênh
output_data = pd.DataFrame({
    'D8_PCG': D8_pcg,  # Tín hiệu PCG đã phân tích
})

# Lưu dữ liệu vào file CSV
output_file_path = 'pcg-output.csv'
output_data.to_csv(output_file_path, index=False, encoding='utf-8')

print(f"Tín hiệu ECG và PCG (không bao gồm đỉnh) đã được lưu vào {output_file_path}")
