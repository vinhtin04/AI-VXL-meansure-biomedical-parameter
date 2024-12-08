import csv

def txt_to_csv(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as txt_file:
        lines = txt_file.readlines()

    # Tách các dòng dựa trên ký tự phân tách (ví dụ: dấu phẩy hoặc tab)
    data = [line.strip().split() for line in lines]

    # Thay thế các giá trị trống bằng '0'
    for row in data:
        for i in range(len(row)):
            if row[i] == '':
                row[i] = '0'

    # Ghi dữ liệu vào tệp CSV
    with open(output_file, 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerows(data)

# Đường dẫn tệp
input_txt = 'PCG.txt'  # Tệp txt đầu vào
output_csv = 'datac.csv'  # Tệp csv đầu ra

# Gọi hàm
txt_to_csv(input_txt, output_csv)
