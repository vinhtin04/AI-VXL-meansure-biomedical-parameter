import numpy as np
import pandas as pd
from scipy.signal import find_peaks

# Đọc tín hiệu PCG từ file CSV
file_path = 'pcg-output.csv'
data = pd.read_csv(file_path)

# Kiểm tra cấu trúc file
if 'D8_PCG' not in data.columns:
    raise ValueError("File không chứa cột 'D8_PCG'. Hãy kiểm tra lại file đầu vào!")

# Lấy tín hiệu từ cột 'D8_PCG'
pcg_signal = data['D8_PCG'].values  # Chuyển đổi tín hiệu sang mảng 1D

sampling_rate = 1000  # Tần số lấy mẫu (Hz)

# Tìm các đỉnh trong tín hiệu
# Điều chỉnh các tham số height và distance nếu cần
peaks, _ = find_peaks(pcg_signal, height=0.5, distance=sampling_rate * 0.5)

# Tính RR intervals (khoảng thời gian giữa các đỉnh)
rr_intervals = np.diff(peaks) / sampling_rate  # Tính bằng giây

# Kiểm tra nếu không có đỉnh hoặc khoảng thời gian
if len(rr_intervals) == 0:
    raise ValueError("Không tìm thấy đủ số lượng đỉnh để tính nhịp tim.")

# Tính nhịp tim trung bình
average_rr = np.mean(rr_intervals)  # Khoảng thời gian trung bình
heart_rate = 60 / average_rr  # BPM (Beats Per Minute)

# Kết quả
print(f"Số lượng đỉnh tìm được: {len(peaks)}")
print(f"Nhịp tim trung bình: {heart_rate:.2f} BPM")
