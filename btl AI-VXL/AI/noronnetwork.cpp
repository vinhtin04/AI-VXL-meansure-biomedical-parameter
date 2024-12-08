#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <time.h>

#define INPUT_SIZE 10000    // Số điểm tín hiệu đầu vào
#define HIDDEN_SIZE 16    // Số nơ-ron trong lớp ẩn
#define OUTPUT_SIZE 1     // Số đầu ra (nhịp tim)
#define LEARNING_RATE 0.01
#define EPOCHS 1000

// Hàm kích hoạt ReLU
float relu(float x) {
    return x > 0 ? x : 0;
}

// Đạo hàm ReLU
float relu_derivative(float x) {
    return x > 0 ? 1 : 0;
}

// Hàm kích hoạt sigmoid
float sigmoid(float x) {
    return 1.0 / (1.0 + exp(-x));
}

// Đạo hàm sigmoid
float sigmoid_derivative(float x) {
    return x * (1 - x);
}

// Hàm khởi tạo trọng số ngẫu nhiên
void initialize_weights(float *weights, int size) {
    for (int i = 0; i < size; i++) {
        weights[i] = ((float)rand() / RAND_MAX) - 0.5; // Giá trị từ -0.5 đến 0.5
    }
}

// Lớp Dense
void dense_layer(float *input, float *weights, float *biases, float *output, int input_size, int output_size) {
    for (int i = 0; i < output_size; i++) {
        output[i] = biases[i];
        for (int j = 0; j < input_size; j++) {
            output[i] += input[j] * weights[i * input_size + j];
        }
        output[i] = relu(output[i]); // Kích hoạt ReLU
    }
}

// Huấn luyện mạng
void train(float *input, float *hidden_weights, float *hidden_biases, 
           float *output_weights, float *output_biases, float target, int input_size) {
    float hidden_output[HIDDEN_SIZE];
    float final_output[OUTPUT_SIZE];

    // Forward pass
    dense_layer(input, hidden_weights, hidden_biases, hidden_output, input_size, HIDDEN_SIZE);

    float sum_output = output_biases[0];
    for (int i = 0; i < HIDDEN_SIZE; i++) {
        sum_output += hidden_output[i] * output_weights[i];
    }
    final_output[0] = sigmoid(sum_output);

    // Tính lỗi
    float error = target - final_output[0];
    float output_gradient = error * sigmoid_derivative(final_output[0]);

    // Cập nhật trọng số lớp đầu ra
    for (int i = 0; i < HIDDEN_SIZE; i++) {
        output_weights[i] += LEARNING_RATE * output_gradient * hidden_output[i];
    }
    output_biases[0] += LEARNING_RATE * output_gradient;

    // Cập nhật trọng số lớp ẩn
    for (int i = 0; i < HIDDEN_SIZE; i++) {
        float hidden_gradient = output_gradient * output_weights[i] * relu_derivative(hidden_output[i]);
        for (int j = 0; j < input_size; j++) {
            hidden_weights[i * input_size + j] += LEARNING_RATE * hidden_gradient * input[j];
        }
        hidden_biases[i] += LEARNING_RATE * hidden_gradient;
    }
}

int main() {
    srand(time(NULL));

    // Tín hiệu PPG đầu vào (giả lập tín hiệu thô)
    float input[INPUT_SIZE];
    for (int i = 0; i < INPUT_SIZE; i++) {
        input[i] = ((float)rand() / RAND_MAX); // Giá trị ngẫu nhiên giả lập
    }

    // Mục tiêu đầu ra (nhịp tim thật giả lập)
    float target = 75.0; // Nhịp tim giả lập (75 bpm)

    // Khởi tạo trọng số và bias
    float hidden_weights[INPUT_SIZE * HIDDEN_SIZE];
    float hidden_biases[HIDDEN_SIZE];
    float output_weights[HIDDEN_SIZE];
    float output_biases[OUTPUT_SIZE];

    initialize_weights(hidden_weights, INPUT_SIZE * HIDDEN_SIZE);
    initialize_weights(hidden_biases, HIDDEN_SIZE);
    initialize_weights(output_weights, HIDDEN_SIZE);
    initialize_weights(output_biases, OUTPUT_SIZE);

    // Huấn luyện mạng
    for (int epoch = 0; epoch < EPOCHS; epoch++) {
        train(input, hidden_weights, hidden_biases, output_weights, output_biases, target, INPUT_SIZE);
        if (epoch % 100 == 0) {
            printf("Epoch %d completed\n", epoch);
        }
    }

    // In trọng số và bias cuối cùng
    printf("\nTrọng số và bias lớp ẩn:\n");
    for (int i = 0; i < HIDDEN_SIZE; i++) {
        printf("Bias[%d]: %.4f\n", i, hidden_biases[i]);
        for (int j = 0; j < INPUT_SIZE; j++) {
            printf("Weight[%d][%d]: %.4f ", i, j, hidden_weights[i * INPUT_SIZE + j]);
        }
        printf("\n");
    }

    printf("\nTrọng số và bias lớp đầu ra:\n");
    for (int i = 0; i < HIDDEN_SIZE; i++) {
        printf("Output Weight[%d]: %.4f\n", i, output_weights[i]);
    }
    printf("Output Bias: %.4f\n", output_biases[0]);

    return 0;
}
