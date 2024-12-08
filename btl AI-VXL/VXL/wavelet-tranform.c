#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define FILTER_SIZE 8
#define MAX_ROWS 8000
#define MAX_COLUMNS 9

// Bộ lọc db4
double db4_low_pass_filter[FILTER_SIZE] = {-0.0106, 0.0329, 0.0308, -0.1870, -0.0280, 0.6309, 0.7148, 0.2304};
double db4_high_pass_filter[FILTER_SIZE] = {-0.23037781330885523, 0.7148465705525415, -0.6308807679295904, -0.02798376941698385, 0.18703481171888114, 0.030841381835986965, -0.032883011666982945, -0.010597401784997278};
double rdb4_low_pass_filter[FILTER_SIZE] = {0.23037781330885523, 0.7148465705525415, 0.6308807679295904, -0.02798376941698385, -0.18703481171888114, 0.030841381835986965, 0.032883011666982945, -0.010597401784997278};
double rdb4_high_pass_filter[FILTER_SIZE] = {-0.010597401784997278, -0.032883011666982945, 0.030841381835986965, 0.18703481171888114, -0.02798376941698385, -0.6308807679295904, 0.7148465705525415, -0.23037781330885523};
// Hàm đọc file CSV
void read_csv_to_array(const char *filename, double data[MAX_ROWS][MAX_COLUMNS], int *row_count) {
    FILE *file = fopen(filename, "r");
    if (!file) {
        perror("Không thể mở file");
        exit(EXIT_FAILURE);
    }

    char line[4096];
    int line_number = 0;

    while (fgets(line, sizeof(line), file)) {
        if (strlen(line) <= 1) continue;
        if (line_number >= MAX_ROWS) break;

        char *token = strtok(line, ",");
        int column_count = 0;
        while (token && column_count < MAX_COLUMNS) {
            data[line_number][column_count++] = atof(token);
            token = strtok(NULL, ",");
        }
        line_number++;
    }

    *row_count = line_number;
    fclose(file);
}

// Các hàm tính tích chập và lọc như trước
void convolve2D(double signal[][MAX_COLUMNS], int col_idx, int signal_len, double *filter, int filter_len, double *result) {
    int output_len = signal_len + filter_len - 1;

    for (int i = 0; i < output_len; i++) {
        result[i] = 0.0;
        for (int j = 0; j < filter_len; j++) {
            if (i - j >= 0 && i - j < signal_len) {
                result[i] += signal[i - j][col_idx] * filter[j];
            }
        }
    }
}

void convolve1D(double signal[], int signal_len, double *filter, int filter_len, double *result) {
    int output_len = signal_len + filter_len - 1;

    for (int i = 0; i < output_len; i++) {
        result[i] = 0.0;
        for (int j = 0; j < filter_len; j++) {
            if (i - j >= 0 && i - j < signal_len) {
                result[i] += signal[i - j] * filter[j];
            }
        }
    }
}

void filter_and_downsample2D(double signal[][MAX_COLUMNS], int col_idx, int signal_len, double *filter, int filter_len, double *result, int *result_len) {
    int filtered_len = signal_len + filter_len - 1;
    double *filtered_signal = (double *)malloc(filtered_len * sizeof(double));

    convolve2D(signal, col_idx, signal_len, filter, filter_len, filtered_signal);

    int index = 0;
    for (int i = 0; i < filtered_len; i += 2) {
        result[index++] = filtered_signal[i];
    }

    *result_len = index;
    free(filtered_signal);
}

void filter_and_downsample1D(double signal[], int signal_len, double *filter, int filter_len, double *result, int *result_len) {
    int filtered_len = signal_len + filter_len - 1;
    double *filtered_signal = (double *)malloc(filtered_len * sizeof(double));

    convolve1D(signal, signal_len, filter, filter_len, filtered_signal);

    int index = 0;
    for (int i = 0; i < filtered_len; i += 2) {
        result[index++] = filtered_signal[i];
    }

    *result_len = index;
    free(filtered_signal);
}

int main() {
    double data[MAX_ROWS][MAX_COLUMNS];
    int row_count = 0;

    // Đọc dữ liệu từ file CSV
    read_csv_to_array("data.csv", data, &row_count);
    int signal_len = row_count;

    // Khởi tạo mảng chứa các hệ số
    double cA[5][2*MAX_ROWS], cD[5][2*MAX_ROWS];
    int cAd[5] = {0}, cDd[5] = {0};


    // Lọc và giảm kích thước lần đầu
    filter_and_downsample2D(data, 6, signal_len, db4_low_pass_filter, FILTER_SIZE, cA[0], &cAd[0]);
    filter_and_downsample2D(data, 6, signal_len, db4_high_pass_filter, FILTER_SIZE, cD[0], &cDd[0]);

    // Lọc và giảm kích thước cho các mức tiếp theo
    for (int i = 1; i < 5; i++) {
        filter_and_downsample1D(cA[i - 1], cAd[i - 1], db4_low_pass_filter, FILTER_SIZE, cA[i], &cAd[i]);
        filter_and_downsample1D(cA[i - 1], cAd[i - 1], db4_high_pass_filter, FILTER_SIZE, cD[i], &cDd[i]);
    }

    // Ghi kết quả vào file CSV
    FILE *output_file = fopen("pcg-output-c.csv", "w");
    if (!output_file) {
        perror("Không thể mở file để ghi");
        return EXIT_FAILURE;
    }

    int level = 2;  // Mức bạn muốn ghi kết quả
    fprintf(output_file, "Index,Filtered_Signal\n");
    for (int i = 0; i < cAd[level - 1]; i++) {
        fprintf(output_file, "%d,%.6lf\n", i, cA[level - 1][i]);
    }

    fclose(output_file);
    printf("Kết quả đã được ghi vào file 'pcg-output-c.csv'\n");


 //    double Au[5][MAX_ROWS], Du[5][MAX_ROWS];
  //  int Aud[5] = {0}, Dud[5] = {0};



    return 0;
}
