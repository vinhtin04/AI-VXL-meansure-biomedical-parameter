import pywt
import matplotlib.pyplot as plt

# Lấy hàm wavelet Daubechies 4 (db4)
wavelet = pywt.Wavelet('db4')

# Khởi tạo đồ thị
plt.figure(figsize=(10, 8))

# Vẽ tín hiệu wavelet cho từng cấp độ (1 đến 4)
for level in range(1, 5):
    phi, psi, x = wavelet.wavefun(level=level)  # Tính toán hàm wavelet ở cấp độ cụ thể
    plt.subplot(2, 2, level)
    plt.plot(x, psi, label=f'Level {level} (Wavelet Function)', color='blue')
    plt.axhline(0, color='gray', linestyle='--', linewidth=0.8)
    plt.title(f'Hàm Wavelet Daubechies 4 - Cấp {level}')
    plt.xlabel('Thời gian')
    plt.ylabel('Biên độ')
    plt.legend()
    plt.grid(True)

# Hiển thị đồ thị
plt.tight_layout()
plt.show()
