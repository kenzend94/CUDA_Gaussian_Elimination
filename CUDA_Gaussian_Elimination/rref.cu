#include <iostream>
#include <cmath>
#include <cuda_runtime.h>
#include <iomanip>
#include <fstream>

using namespace std;

#define N 3  // Number of unknowns

// Define a small threshold value
const double EPSILON = 1e-12;

// CUDA kernel for forward elimination
__global__ void forwardElimKernel(double *mat, int numvar, int k) {
    int idx = blockDim.x * blockIdx.x + threadIdx.x + k + 1;
    if (idx < numvar) {
        double factor = mat[idx * (numvar + 1) + k] / mat[k * (numvar + 1) + k];
        for (int j = k; j <= numvar; j++) {
            mat[idx * (numvar + 1) + j] -= factor * mat[k * (numvar + 1) + j];
        }
    }
}

void makeRREF(double *mat, int numvar) {
    // Normalize diagonal elements to 1
    for (int i = 0; i < numvar; ++i) {
        double diagVal = mat[i * (numvar + 1) + i];
        if (diagVal != 0) { // Avoid division by zero
            for (int j = 0; j <= numvar; ++j) {
                mat[i * (numvar + 1) + j] /= diagVal;
            }
        }
    }

    // Zero out elements above the diagonal
    for (int i = numvar - 1; i >= 0; --i) {
        for (int j = i - 1; j >= 0; --j) {
            double factor = mat[j * (numvar + 1) + i];
            for (int k = 0; k <= numvar; ++k) {
                mat[j * (numvar + 1) + k] -= factor * mat[i * (numvar + 1) + k];
            }
        }
    }
}


// Function to print the matrix
void printMatrix(double *mat, int numvar) {
    for (int i = 0; i < numvar; i++) {
        for (int j = 0; j <= numvar; j++) {
            // Check if the value is smaller than EPSILON in absolute terms
            if (fabs(mat[i * (numvar + 1) + j]) < EPSILON) {
                cout << setw(10) << 0 << " ";
            } else {
                cout << setw(10) << mat[i * (numvar + 1) + j] << " ";
            }
        }
        cout << endl;
    }
    cout << endl;
}


// // Forward elimination on the GPU
// void forwardElim(double *mat, int numvar) {
//     double *d_mat;
//     size_t size = numvar * (numvar + 1) * sizeof(double);
//     cudaMalloc(&d_mat, size);
//     cudaMemcpy(d_mat, mat, size, cudaMemcpyHostToDevice);

//     dim3 block(256);
//     dim3 grid((numvar + block.x - 1) / block.x);

//     for (int k = 0; k < numvar; k++) {
//         forwardElimKernel<<<grid, block>>>(d_mat, numvar, k);
//         cudaDeviceSynchronize();
//     }

//     cudaMemcpy(mat, d_mat, size, cudaMemcpyDeviceToHost);
//     cudaFree(d_mat);
// }

// Print version will make it slower
// Modified forwardElim function to print matrix at each step with CUDA
void forwardElim(double *mat, int numvar) {
    double *d_mat;
    size_t size = numvar * (numvar + 1) * sizeof(double);
    cudaMalloc(&d_mat, size);
    cudaMemcpy(d_mat, mat, size, cudaMemcpyHostToDevice);

    dim3 block(256);
    dim3 grid((numvar + block.x - 1) / block.x);

    for (int k = 0; k < numvar; k++) {
        forwardElimKernel<<<grid, block>>>(d_mat, numvar, k);
        cudaDeviceSynchronize();

        // Copy back the matrix to the host to print
        cudaMemcpy(mat, d_mat, size, cudaMemcpyDeviceToHost);
        cout << "Matrix after step " << k << ":" << endl;
        printMatrix(mat, numvar);
    }

    cudaMemcpy(mat, d_mat, size, cudaMemcpyDeviceToHost);
    cudaFree(d_mat);
}


// Function for back substitution
// void backSub(double mat[N][N+1]) {
//     double x[N];  // An array to store solution

//     for (int i = N-1; i >= 0; i--) {
//         x[i] = mat[i][N];
//         for (int j=i+1; j<N; j++) {
//             x[i] -= mat[i][j]*x[j];
//         }
//         x[i] = x[i]/mat[i][i];
//     }

//     cout << "\nSolution for the system:\n";
//     for (int i=0; i<N; i++)
//         cout << "X" << i << " = " << x[i] << endl;
// }

    void backSub(double *mat) {
        double x[N];  // An array to store solution

        for (int i = N-1; i >= 0; i--) {
            x[i] = mat[i * (N + 1) + N];
            for (int j=i+1; j<N; j++) {
                x[i] -= mat[i * (N + 1) + j] * x[j];
            }
            x[i] = x[i] / mat[i * (N + 1) + i];
        }

        cout << "\nSolution for the system:\n";
        for (int i=0; i<N; i++)
            cout << "X" << i << " = " << x[i] << endl;
    }

// Main function

int main() {
    ifstream file("data5.txt");
    if (!file.is_open()) {
        cerr << "Error opening file" << endl;
        return -1;
    }

    int numvar;
    file >> numvar;

    // Dynamically allocate memory for the matrix
    double *mat = new double[numvar * (numvar + 1)];

    // Read the matrix data
    for (int i = 0; i < numvar; i++) {
        for (int j = 0; j <= numvar; j++) {
            file >> mat[i * (numvar + 1) + j];
        }
    }

    // print matrix
    cout << "Input Matrix:\n";
    for (int i = 0; i < numvar; i++) {
        for (int j = 0; j <= numvar; j++) {
            cout << mat[i * (numvar + 1) + j] << " ";
        }
        cout << endl;
    }
    // why cout << endl; here?
    // cout << endl;


    file.close();

    // Call forward elimination and back substitution
    forwardElim(mat, numvar);
    // Function for back substitution
    backSub(mat);
    makeRREF(mat, numvar); // Transform to RREF

    cout << "Matrix in RREF:" << endl;
    printMatrix(mat, numvar);

    // Free the dynamically allocated memory
    delete[] mat;

    return 0;
}