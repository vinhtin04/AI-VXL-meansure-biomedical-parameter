import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Đọc dữ liệu từ file CSV
file_path = 'pcgdata.csv'
dataECG = pd.read_csv(file_path)

file_path = 'pcgdata.csv'
dataPCG = pd.read_csv(file_path)

file_path = 'pcgdata.csv'
dataPPG = pd.read_csv(file_path)
# Giả sử 'signal' là cột chứa dữ liệu cần xử lý
#------------------------------------------------------------------------------
# Tính chiều dài của dữ liệu signal
length = len(dataECG)

# Tính phần dư khi chia length cho 32
remainder = length % 32

# Nếu phần dư khác 0, bỏ phần dư ở cuối
if remainder != 0:
    data = dataECG.iloc[:-(remainder + 1)]

# Lưu dữ liệu đã xử lý vào file CSV mới
output_file_path = 'ecg_signal1.csv'
data.to_csv(output_file_path, index=False)

data = pd.read_csv('ecg_signal1.csv')
ecg_signal = data.iloc[:, 0].values

# Đọc lại dữ liệu từ file CSV đã lưu----------------------------------
file_path = 'pcgdata.csv'
dataPCG = pd.read_csv(file_path)

# Giả sử 'signal' là cột chứa dữ liệu cần xử lý

# Tính chiều dài của dữ liệu signal
length = len(dataPCG)

# Tính phần dư khi chia length cho 32
remainder = length % 32

# Nếu phần dư khác 0, bỏ phần dư ở cuối
if remainder != 0:
    data = dataPCG.iloc[:-(remainder + 1)]

# Lưu dữ liệu đã xử lý vào file CSV mới
output_file_path = 'pcgsignal.csv'
data.to_csv(output_file_path, index=False)

data = pd.read_csv('pcgsignal.csv')
pcg_signal = data.iloc[:, 0].values

#--------------------------------------------------------------------------
length = len(dataPPG)

# Tính phần dư khi chia length cho 32
remainder = length % 32

# Nếu phần dư khác 0, bỏ phần dư ở cuối
if remainder != 0:
    data = dataECG.iloc[:-(remainder + 1)]

# Lưu dữ liệu đã xử lý vào file CSV mới
output_file_path = 'ppg_signal.csv'
data.to_csv(output_file_path, index=False)

data = pd.read_csv('ppg_signal.csv')
ppg_signal = data.iloc[:, 0].values
 

 #------------------------------------
# Định nghĩa bộ lọc db4
db4_low_pass_filter = [-0.010597401784997278, 0.032883011666982945, 0.030841381835986965, -0.18703481171888114, -0.02798376941698385, 0.6308807679295904, 0.7148465705525415, 0.23037781330885523]
db4_high_pass_filter = [-0.23037781330885523, 0.7148465705525415, -0.6308807679295904, -0.02798376941698385, 0.18703481171888114, 0.030841381835986965, -0.032883011666982945, -0.010597401784997278]

rdb4_low_pass_filter = [0.23037781330885523, 0.7148465705525415, 0.6308807679295904, -0.02798376941698385, -0.18703481171888114, 0.030841381835986965, 0.032883011666982945, -0.010597401784997278]
rdb4_high_pass_filter = [-0.010597401784997278, -0.032883011666982945, 0.030841381835986965, 0.18703481171888114, -0.02798376941698385, -0.6308807679295904, 0.7148465705525415, -0.23037781330885523]
#db4_low_pass_filter = [ -0.0106 ,   0.0329  ,  0.0308   ,-0.1870 ,  -0.0280  ,  0.6309  ,  0.7148 ,   0.2304]

#db4_high_pass_filter = [ -0.2304 ,   0.7148,   -0.6309 ,  -0.0280  ,  0.1870  ,  0.0308  , -0.0329  , -0.0106]


# Phân tích tín hiệu
def apply_filter_and_downsample(signal, filter):
    filtered_signal = np.convolve(signal, filter, mode='sym')
    downsampled_signal = filtered_signal[1::2]
    return downsampled_signal

# mầu input 8000

cA1 = apply_filter_and_downsample(ecg_signal, db4_low_pass_filter) #4000 mẫu
cD1 = apply_filter_and_downsample(ecg_signal, db4_high_pass_filter)

cA2 = apply_filter_and_downsample(cA1, db4_low_pass_filter)
cD2 = apply_filter_and_downsample(cA1, db4_high_pass_filter)

cA3 = apply_filter_and_downsample(cA2, db4_low_pass_filter)
cD3 = apply_filter_and_downsample(cA2, db4_high_pass_filter)

cA4 = apply_filter_and_downsample(cA3, db4_low_pass_filter)
cD4 = apply_filter_and_downsample(cA3, db4_high_pass_filter)

cA5 = apply_filter_and_downsample(cA4, db4_low_pass_filter)
cD5 = apply_filter_and_downsample(cA4, db4_high_pass_filter)

#--------------------------------------------------------------
# Hàm lấy mẫu lên
# Tăng mẫu cD1 và cD2


cD1_upsampled = np.zeros(2 * len(cD1)) #từ 4000 lên 8000 mẫu
cD1_upsampled[0::2] = cD1

cD2_upsampled = np.zeros(2 * len(cD2)) #4000 mẫu
cD2_upsampled[0::2] = cD2

cD3_upsampled = np.zeros(2 * len(cD3))
cD3_upsampled[0::2] = cD3  

cD4_upsampled = np.zeros(2 * len(cD4))
cD4_upsampled[0::2] =  cD4 

cD5_upsampled = np.zeros(2 * len(cD5))
cD5_upsampled[0::2] =  cD5

cA1_upsampled = np.zeros(2 * len(cA1))
cA1_upsampled[0::2] = cA1 

cA2_upsampled = np.zeros(2 * len(cA2))
cA2_upsampled[0::2] = cA2 

cA3_upsampled = np.zeros(2 * len(cA3))
cA3_upsampled[0::2] = cA3 

cA4_upsampled = np.zeros(2 * len(cA4))
cA4_upsampled[0::2] = cA4 

cA5_upsampled = np.zeros(2 * len(cA5))
cA5_upsampled[0::2] = cA5 

# Kết hợp cD1_upsampled và cD2_upsampled

def apply_filter_and_downsamplee(signal, filter):
    filtered_signal = np.convolve(signal, filter, mode='sym')
    return filtered_signal

D1u = apply_filter_and_downsamplee(cD1_upsampled, rdb4_high_pass_filter) #8000 mẫu
D2u = apply_filter_and_downsamplee(cD2_upsampled, rdb4_high_pass_filter)
D3u = apply_filter_and_downsamplee(cD3_upsampled, rdb4_high_pass_filter)
D4u = apply_filter_and_downsamplee(cD4_upsampled, rdb4_high_pass_filter)
D5u = apply_filter_and_downsamplee(cD5_upsampled, rdb4_high_pass_filter)

A1u = apply_filter_and_downsamplee(cA1_upsampled, rdb4_low_pass_filter)  
A2u = apply_filter_and_downsamplee(cA2_upsampled, rdb4_low_pass_filter)
A3u = apply_filter_and_downsamplee(cA3_upsampled, rdb4_low_pass_filter)
A4u = apply_filter_and_downsamplee(cA4_upsampled, rdb4_low_pass_filter)
A5u = apply_filter_and_downsamplee(cA5_upsampled, rdb4_low_pass_filter)

def combine_signals(*signals):
    combined_signal = np.zeros(max(len(signal) for signal in signals))
    for signal in signals:
        combined_signal[:len(signal)] += signal
    return combined_signal


cA4g = A5u + D5u 

cA4g_upsampled = np.zeros(2 * len(cA4g))
cA4g_upsampled[0::2] = cA4g
cA4g = apply_filter_and_downsamplee(cA4_upsampled, rdb4_low_pass_filter)

cA3g = cA4g + D4u #4000 mẫu

cA3g_upsampled = np.zeros(2 * len(cA3g))
cA3g_upsampled[0::2] = cA3g
cA3g = apply_filter_and_downsamplee(cA3_upsampled, rdb4_low_pass_filter)

cA2g = cA3g + D3u

cA2g_upsampled = np.zeros(2 * len(cA2g))
cA2g_upsampled[0::2] = cA2g
cA2g = apply_filter_and_downsamplee(cA2_upsampled, rdb4_low_pass_filter)

cA1g = A2u + D2u

cA1g_upsampled = np.zeros(2 * len(cA1g))
cA1g_upsampled[0::2] = cA1g
cA1g = apply_filter_and_downsamplee(cA1_upsampled, rdb4_low_pass_filter)
 
s = cA1g


# Tái tạo D5a
A5a_upsampled = np.zeros(2 * len(cA5) - 1) # 
A5a_upsampled[0::2] = cA5
A5a = apply_filter_and_downsamplee(A5a_upsampled, rdb4_low_pass_filter)

# Tái tạo D5b
A5b_upsampled = np.zeros(2 * len(A5a) - 1) # 4000 mẫu
A5b_upsampled[0::2] = A5a
A5b = apply_filter_and_downsamplee(A5b_upsampled, rdb4_low_pass_filter)

# Tái tạo D5c
A5c_upsampled = np.zeros(2 * len(A5b) - 1) # 4000 mẫu
A5c_upsampled[0::2] = A5b
A5c = apply_filter_and_downsamplee(A5c_upsampled, rdb4_low_pass_filter)

# Tái tạo D5d
A5d_upsampled = np.zeros(2 * len(A5c) - 1) # 4000 mẫu
A5d_upsampled[0::2] = A5c
A5d = apply_filter_and_downsamplee(A5d_upsampled, rdb4_low_pass_filter)

# Tái tạo D5e
A5e_upsampled = np.zeros(2 * len(A5d) - 1) # 4000 mẫu
A5e_upsampled[0::2] = A5d
A5e = apply_filter_and_downsamplee(A5e_upsampled, rdb4_low_pass_filter)

D5a_upsampled = np.zeros(2 * len(cD5) - 1) # 4000 mẫu
D5a_upsampled[0::2] = cD5
D5a = apply_filter_and_downsamplee(D5a_upsampled, rdb4_high_pass_filter)

D5b_upsampled = np.zeros(2 * len(D5a) - 1) # 4000 mẫu
D5b_upsampled[0::2] = D5a
D5b = apply_filter_and_downsamplee(D5b_upsampled, rdb4_low_pass_filter)

# Bước xử lý cho D5c
D5c_upsampled = np.zeros(2 * len(D5b) - 1) # 8000 mẫu
D5c_upsampled[0::2] = D5b
D5c = apply_filter_and_downsamplee(D5c_upsampled, rdb4_low_pass_filter)

# Bước xử lý cho D5d
D5d_upsampled = np.zeros(2 * len(D5c) - 1) # 16000 mẫu
D5d_upsampled[0::2] = D5c
D5d = apply_filter_and_downsamplee(D5d_upsampled, rdb4_low_pass_filter)

# Bước xử lý cho D5e
D5e_upsampled = np.zeros(2 * len(D5d) - 1) # 32000 mẫu
D5e_upsampled[0::2] = D5d
D5e = apply_filter_and_downsamplee(D5e_upsampled, rdb4_low_pass_filter)

D4a_upsampled = np.zeros(2 * len(cD4) - 1) # 4000 mẫu
D4a_upsampled[0::2] = cD4
D4a = apply_filter_and_downsamplee(D4a_upsampled, rdb4_high_pass_filter)

# Bước xử lý cho D4b
D4b_upsampled = np.zeros(2 * len(D4a) - 1) # 8000 mẫu
D4b_upsampled[0::2] = D4a
D4b = apply_filter_and_downsamplee(D4b_upsampled, rdb4_low_pass_filter)

# Bước xử lý cho D4c
D4c_upsampled = np.zeros(2 * len(D4b) - 1) # 16000 mẫu
D4c_upsampled[0::2] = D4b
D4c = apply_filter_and_downsamplee(D4c_upsampled, rdb4_low_pass_filter)

# Bước xử lý cho D4d
D4d_upsampled = np.zeros(2 * len(D4c) - 1) # 32000 mẫu
D4d_upsampled[0::2] = D4c
D4d = apply_filter_and_downsamplee(D4d_upsampled, rdb4_low_pass_filter)

# Bước xử lý cho D3a
D3a_upsampled = np.zeros(2 * len(cD3) - 1) # 4000 mẫu
D3a_upsampled[0::2] = cD3
D3a = apply_filter_and_downsamplee(D3a_upsampled, rdb4_high_pass_filter)

# Bước xử lý cho D3b
D3b_upsampled = np.zeros(2 * len(D3a) - 1) # 8000 mẫu
D3b_upsampled[0::2] = D3a
D3b = apply_filter_and_downsamplee(D3b_upsampled, rdb4_low_pass_filter)

# Bước xử lý cho D3c
D3c_upsampled = np.zeros(2 * len(D3b) - 1) # 16000 mẫu
D3c_upsampled[0::2] = D3b
D3c = apply_filter_and_downsamplee(D3c_upsampled, rdb4_low_pass_filter)
 
# Bước xử lý cho D2a
D2a_upsampled = np.zeros(2 * len(cD2) - 1) # 4000 mẫu (giả sử cD2 có 2000 mẫu)
D2a_upsampled[0::2] = cD2
D2a = apply_filter_and_downsamplee(D2a_upsampled, rdb4_high_pass_filter)

# Bước xử lý cho D2b
D2b_upsampled = np.zeros(2 * len(D2a) - 1) # 8000 mẫu
D2b_upsampled[0::2] = D2a
D2b = apply_filter_and_downsamplee(D2b_upsampled, rdb4_high_pass_filter)

# Bước xử lý cho D1a
D1a_upsampled = np.zeros(2 * len(cD1) - 1) # 4000 mẫu (giả sử cD1 có 2000 mẫu)
D1a_upsampled[0::2] = cD1
D1a = apply_filter_and_downsamplee(D1a_upsampled, rdb4_high_pass_filter)

SumECG = combine_signals(D1a,D2b,D3c,D4d,D5e,A5e)
# Điều chỉnh độ dài của các tín hiệu chi tiết và xấp xỉ để khớp với tín hiệu gốc



# PPG
# Đọc dữ liệu từ file CSV

cA1PCG = apply_filter_and_downsample(pcg_signal, db4_low_pass_filter) #4000 mẫu
cD1PCG = apply_filter_and_downsample(pcg_signal, db4_high_pass_filter)

cA2PCG = apply_filter_and_downsample(cA1PCG, db4_low_pass_filter)
cD2PCG = apply_filter_and_downsample(cD1PCG, db4_high_pass_filter)

cA3PCG = apply_filter_and_downsample(cA2PCG, db4_low_pass_filter)
cD3PCG = apply_filter_and_downsample(cD2PCG, db4_high_pass_filter)


A5PCGa_upsampled = np.zeros(2 * len(cA2PCG) - 1) # 4000 mẫu
A5PCGa_upsampled[0::2] = cA2PCG
A5PCGa = apply_filter_and_downsamplee(A5PCGa_upsampled, rdb4_low_pass_filter)

# Tái tạo D5b
A5PCGb_upsampled = np.zeros(2 * len(A5PCGa) - 1) # 4000 mẫu
A5PCGb_upsampled[0::2] = A5PCGa
A5PCGb = apply_filter_and_downsamplee(A5PCGb_upsampled, rdb4_low_pass_filter)


D2PCGa_upsampled = np.zeros(2 * len(cD2PCG) - 1) # 4000 mẫu (giả sử cD2 có 2000 mẫu)
D2PCGa_upsampled[0::2] = cD2PCG
D2PCGa = apply_filter_and_downsamplee(D2PCGa_upsampled, rdb4_high_pass_filter)

# Bước xử lý cho D2b
D2PCGb_upsampled = np.zeros(2 * len(D2PCGa) - 1) # 8000 mẫu
D2PCGb_upsampled[0::2] = D2PCGa
D2PCGb = apply_filter_and_downsamplee(D2PCGb_upsampled, rdb4_low_pass_filter)

# Bước xử lý cho D1a
D1PCGa_upsampled = np.zeros(2 * len(cD1PCG) - 1) # 4000 mẫu (giả sử cD1 có 2000 mẫu)
D1PCGa_upsampled[0::2] = cD1PCG
D1PCGa = apply_filter_and_downsamplee(D1PCGa_upsampled, rdb4_high_pass_filter)

SumPCG = combine_signals(D1PCGa,D2PCGb,A5PCGb)

#---------------------------------------------------------------------------

# Applying filters and downsampling to PPG signal
cA1PPG = apply_filter_and_downsample(ppg_signal, db4_low_pass_filter) # 4000 samples
cD1PPG = apply_filter_and_downsample(ppg_signal, db4_high_pass_filter)

cA2PPG = apply_filter_and_downsample(cA1PPG, db4_low_pass_filter)
cD2PPG = apply_filter_and_downsample(cD1PPG, db4_high_pass_filter)

# Reconstructing A5
A5PPGa_upsampled = np.zeros(2 * len(cA2PPG) - 1) # 4000 samples
A5PPGa_upsampled[0::2] = cA2PPG
A5PPGa = apply_filter_and_downsamplee(A5PPGa_upsampled, rdb4_low_pass_filter)

# Reconstructing A5b
A5PPGb_upsampled = np.zeros(2 * len(A5PPGa) - 1) # 4000 samples
A5PPGb_upsampled[0::2] = A5PPGa
A5PPGb = apply_filter_and_downsamplee(A5PPGb_upsampled, rdb4_low_pass_filter)

# Processing D2a
D2PPGa_upsampled = np.zeros(2 * len(cD2PPG) - 1) # 4000 samples (assuming cD2 has 2000 samples)
D2PPGa_upsampled[0::2] = cD2PPG
D2PPGa = apply_filter_and_downsamplee(D2PPGa_upsampled, rdb4_high_pass_filter)

# Processing D2b
D2PPGb_upsampled = np.zeros(2 * len(D2PPGa) - 1) # 8000 samples
D2PPGb_upsampled[0::2] = D2PPGa
D2PPGb = apply_filter_and_downsamplee(D2PPGb_upsampled, rdb4_low_pass_filter)

# Processing D1a
D1PPGa_upsampled = np.zeros(2 * len(cD1PPG) - 1) # 4000 samples (assuming cD1 has 2000 samples)
D1PPGa_upsampled[0::2] = cD1PPG
D1PPGa = apply_filter_and_downsamplee(D1PPGa_upsampled, rdb4_high_pass_filter)

# Combining the signals
SumPPG = combine_signals(D1PPGa, D2PPGb, A5PPGb)

# Hiển thị tín hiệu gốc và tín hiệu tái tạo
plt.figure(figsize=(6, 10))

plt.subplot(3, 1, 1)
plt.plot(SumECG, color='blue')
plt.title('Tín hiệu PPG ban đầu')

plt.subplot(3, 1, 2 )
plt.plot(SumPPG, color='red', linewidth=2)
plt.title('Tín hiệu sau khi khôi phục từ cA và cD')

plt.subplot(3, 1, 3)
plt.plot(s, color='green', linewidth=1)
plt.title('So sánh tin hiệu ban đầu và tín hiệu khôi phục')




plt.tight_layout()
plt.show()



# Bước 4: Lưu dữ liệu cD3 vào file CSV mới
output_file_path = 'D3_PCG.csv'

# Chuyển cD3 thành DataFrame của Pandas để dễ dàng lưu thành CSV
cD3_df = pd.DataFrame(cD3, columns=['D2PCGa'])

# Lưu DataFrame vào file CSV
cD3_df.to_csv(output_file_path, index=False)

print(f"Dữ liệu cD3 đã được lưu vào {output_file_path}")
