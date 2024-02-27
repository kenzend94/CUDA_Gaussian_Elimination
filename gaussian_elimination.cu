#include <iostream>
#include <cmath>
#include <cuda_runtime.h>
#include <iomanip>
#include <fstream>
#include <chrono>
#include <string>
#include <vector>
#include <unistd.h>

using namespace std;


// define shouldPrint to print the matrix at each step
bool shouldPrint = true;

// define data_file to read the matrix from a file
const char *data_file = "data/data30.txt";

// Define a small threshold value
const double EPSILON = 1e-10;

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

// Function to convert a string fraction to decimal
double fractionToDecimal(const string& frac) {
    istringstream iss(frac);
    double num, denom = 1;
    char slash;
    iss >> num >> slash >> denom;
    if (denom != 0) return num / denom;
    return num; // Handle non-fraction case
}

// Function to print the matrix with fractions
void printFractionMatrix(const vector<string>& mat, int numvar) {
    for (int i = 0; i < numvar; i++) {
        for (int j = 0; j <= numvar; j++) {
            cout << setw(10) << mat[i * (numvar + 1) + j] << " ";
        }
        cout << endl;
    }
    cout << endl;
}

double parseFraction(const string& frac) {
    size_t slashPos = frac.find('/');
    if (slashPos != string::npos) {
        double numerator = stod(frac.substr(0, slashPos));
        double denominator = stod(frac.substr(slashPos + 1));
        if (denominator != 0) return numerator / denominator;
    }
    return stod(frac); // Handle non-fraction case
}

// Function to find the greatest common divisor (GCD)
int gcd(int a, int b) {
    if (b == 0) {
        return a;
    }
    return gcd(b, a % b);
}

// Function to convert a decimal to a fraction
void decimalToFrac(double value, int &numerator, int &denominator) {
    // Check if the value is close to an integer
    double diff = fabs(value - round(value));
    if (diff < EPSILON) {
        numerator = static_cast<int>(round(value));
        denominator = 1;
        return; // Early return as the number is effectively an integer
    }

    const double precision = 1E-6; // Precision for the conversion
    double integral = floor(value);
    double frac = value - integral;
    const int max_denominator = 10000; // Limits the denominator size

    // Initialize denominator as 1
    int lower_n = 0;
    int lower_d = 1;
    int upper_n = 1;
    int upper_d = 1;

    while (lower_d <= max_denominator && upper_d <= max_denominator) {
        int middle_n = lower_n + upper_n;
        int middle_d = lower_d + upper_d;

        if (fabs(frac - (double)middle_n / middle_d) < precision) {
            if (middle_d > max_denominator) {
                if (lower_d > upper_d) {
                    lower_n = upper_n;
                    lower_d = upper_d;
                }
                break;
            }

            lower_n = upper_n = middle_n;
            lower_d = upper_d = middle_d;
        } else if (frac > (double)middle_n / middle_d) {
            lower_n = middle_n;
            lower_d = middle_d;
        } else {
            upper_n = middle_n;
            upper_d = middle_d;
        }
    }

    // Adjust fraction to combine with the integral part
    numerator = (int)integral * lower_d + lower_n;
    denominator = lower_d;

    // Reduce the fraction
    int commonDivisor = gcd(abs(numerator), denominator);
    numerator /= commonDivisor;
    denominator /= commonDivisor;
}

// Function to print the matrix
void printMatrix(double *mat, int numvar) {
    for (int i = 0; i < numvar; i++) {
        for (int j = 0; j <= numvar; j++) {
            // Convert each element to fraction
            int numerator, denominator;
            decimalToFrac(mat[i * (numvar + 1) + j], numerator, denominator);
            
            // Check if the value is smaller than EPSILON in absolute terms
            if (fabs(mat[i * (numvar + 1) + j]) < EPSILON) {
                cout << setw(10) << 0 << " ";
            } else {
                // Display as a fraction
                if (denominator == 1) { // Print as an integer if the denominator is 1
                    cout << setw(10) << numerator << " ";
                } else { // Otherwise, print as a fraction
                    cout << setw(10) << numerator << "/" << denominator << " ";
                }
            }
        }
        cout << endl;
    }
    cout << endl;
}


// Forward elimination function with an option to print matrix at each step
void forwardElim(double *mat, int numvar, bool printSteps) {
    double *d_mat;
    size_t size = numvar * (numvar + 1) * sizeof(double);
    cudaMalloc(&d_mat, size);
    cudaMemcpy(d_mat, mat, size, cudaMemcpyHostToDevice);

    dim3 block(256);
    dim3 grid((numvar + block.x - 1) / block.x);

    for (int k = 0; k < numvar; k++) {
        forwardElimKernel<<<grid, block>>>(d_mat, numvar, k);
        cudaDeviceSynchronize();

        if (printSteps) {
            // Copy back the matrix to the host to print
            cudaMemcpy(mat, d_mat, size, cudaMemcpyDeviceToHost);
            cout << "Matrix after step " << k << ":" << endl;
            printMatrix(mat, numvar);
        }
    }

    if (!printSteps) {
        cudaMemcpy(mat, d_mat, size, cudaMemcpyDeviceToHost);
    }
    cudaFree(d_mat);
}


// 
void backSub(double *mat, int numvar) {
    double *x = new double[numvar];  // Dynamically allocate array for solution

    // Start the timer
    auto start = chrono::high_resolution_clock::now();

    for (int i = numvar - 1; i >= 0; i--) {
        x[i] = mat[i * (numvar + 1) + numvar];
        for (int j = i + 1; j < numvar; j++) {
            x[i] -= mat[i * (numvar + 1) + j] * x[j];
        }
        x[i] /= mat[i * (numvar + 1) + i];
    }
    // Stop the timer
    auto end = chrono::high_resolution_clock::now();

    // Calculate the duration
    auto duration = chrono::duration_cast<chrono::nanoseconds>(end - start);


    cout << "\nSolution for the system:\n";
    for (int i = 0; i < numvar; i++)
        cout << "X" << i << " = " << x[i] << endl;

    // Uncomment the following code to print the solution as fractions
    // for (int i = 0; i < numvar; i++) {
    //     int numerator, denominator;
    //     decimalToFrac(x[i], numerator, denominator);
    //     cout << "X" << i << " = " << numerator << "/" << denominator << endl;
    // }

    cout << "\nTime taken for back substitution: " << duration.count() << " nanoseconds" << endl;

    delete[] x; // Free the dynamically allocated memory
}


// Main function
int main() {
    ifstream file(data_file);
    if (!file.is_open()) {
        cerr << "Error opening file" << endl;
        return -1;
    }

    int numvar;
    file >> numvar;

    vector<string> matStr(numvar * (numvar + 1));
    string frac; // Temporary string to store fraction input

    // Read the matrix data as fractions or decimal numbers
    for (int i = 0; i < numvar; i++) {
        for (int j = 0; j <= numvar; j++) {
            file >> frac;
            matStr[i * (numvar + 1) + j] = frac;
        }
    }

    file.close();

    // Print the input matrix as fractions or decimal numbers
    cout << "Input Matrix:\n";
    printFractionMatrix(matStr, numvar);

    // Convert the string representations to decimal values for calculations
    double *mat = new double[numvar * (numvar + 1)];
    for (int i = 0; i < numvar * (numvar + 1); ++i) {
        mat[i] = fractionToDecimal(matStr[i]);
    }

    // Perform Gaussian elimination
    forwardElim(mat, numvar, shouldPrint);

    // Perform back substitution and print the results
    backSub(mat, numvar);

    // Free the dynamically allocated memory
    delete[] mat;

    return 0;
}
