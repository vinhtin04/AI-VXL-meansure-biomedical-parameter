import serial
import matplotlib.pyplot as plt
import mplcursors
import numpy as np
import pandas as pd
from scipy.signal import butter, filtfilt,find_peaks

# Thiết lập kết nối serial
try:
    ser = serial.Serial('COM5', 115200)
except AttributeError:
    raise ImportError("loi pyserial")

ir_data = []
red_data = []

try:
    while True:
        # Đọc một dòng từ serial
        line = ser.readline().decode('utf-8').strip()
        if line:
            print(line)
            # Phân tích dữ liệu
            parts = line.split(',')
            if len(parts) == 2:
                try:
                    ir_value = int(parts[1].strip())
                    red_value = int(parts[0].strip())
                    ir_data.append(ir_value)
                    red_data.append(red_value)
                except ValueError as e:
                    print(f"Error parsing line: {line}, error: {e}")
            else:
                print(f"Invalid line format: {line}")
        
        # Dừng sau n lần đọc (hoặc thay đổi điều kiện tùy ý)
        if len(ir_data) >= 4000:
            break

finally:
    ser.close()


#lật mảng (do tín hiệu ppg khi đo được là tín hiệu ngược)
ir_data_flip = np.flip(ir_data)
red_data_flip = np.flip(red_data)



def split_and_extract_middle(data):
    # Chia mảng thành 4 phần gần bằng nhau
    n = len(data)
    quarter = n // 4
    start_index = quarter
    end_index = n - quarter if n % 4 == 0 else n - quarter + 1

    # Trả về phần giữa của mảng
    return data[start_index:end_index]

# Mẫu mảng data
# Áp dụng hàm và in ra phần giữa
red_data_mid = split_and_extract_middle(red_data_flip)
ir_data_mid = split_and_extract_middle(ir_data_flip)



fs=250
window_size = int(fs * 0.1)


# Áp dụng bộ lọc Butterworth 
order = 4  # Độ bậc của bộ lọc
cutoff_frequency = 12  # Tần số cắt (đơn vị: Hz)
nyquist_frequency = 0.5*fs 
normal_cutoff = cutoff_frequency / nyquist_frequency
b, a = butter(order, normal_cutoff, btype='low', analog=False)

ppg_red_data_filtered = filtfilt(b, a, red_data_mid)
ppg_ir_data_filtered = filtfilt(b, a, ir_data_mid)



def calculate_spo2(red_data, ir_data):
    # Tính DC và AC của tín hiệu
    red_dc = np.mean(red_data)
    ir_dc = np.mean(ir_data)

    red_ac = red_data - red_dc
    ir_ac = ir_data - ir_dc

    # Tìm các đỉnh (peaks) của tín hiệu
    peaks_red, _ = find_peaks(red_ac)
    peaks_ir, _ = find_peaks(ir_ac)

    # Tính AC của tín hiệu là độ lệch chuẩn của phần AC
    red_ac_std = np.std(red_ac[peaks_red])
    ir_ac_std = np.std(ir_ac[peaks_ir])

    # Tính tỷ lệ R
    R = (red_ac_std / red_dc) / (ir_ac_std / ir_dc)

    # Tính SpO2
    spo2 = 110 - 25 * R
    return spo2

spo2 = calculate_spo2(ppg_red_data_filtered, ppg_ir_data_filtered)


# Create subplots
fig,ax1 = plt.subplots(1, 1, figsize=(12, 12))

# Vẽ đồ thị PPG 
ax1.plot(red_data_mid, label='PPG_RED Data')
# ax1.plot(ir_data_mid, label='PPG_IR Data')
ax1.plot(ppg_red_data_filtered, label='Filtered PPG_RED Data', alpha=0.8, lw=3)
ax1.plot(ppg_ir_data_filtered, label='Filtered PPG_IR Data', alpha=0.8, lw=3)
ax1.legend()
ax1.set_ylabel('Giá Trị PPG')
ax1.set_title(f'PPG Data, SpO2: {spo2:.2f}%')

# Sử dụng mplcursors để hiển thị giá trị khi di chuyển chuột qua điểm trên đồ thị
cursor1 = mplcursors.cursor(ax1, hover=True)

# Định dạng hiển thị giá trị trên đồ thị
cursor1.connect("add", lambda sel: sel.annotation.set_text(f'PPG: {sel.target[1]:.2f}'))

plt.tight_layout()
plt.show()
1