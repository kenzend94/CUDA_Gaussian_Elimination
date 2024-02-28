# Applying F4 Polynomial Division Using GPU Computing
## Abstract
This project explores the application of GPU (Graphics Processing Unit) computing for the F4 algorithm in polynomial division, focusing on the Gaussian elimination process to compute a row-echelon form. We compare the performance of GPUs against CPUs (Central Processing Units), demonstrating the superior parallel processing capabilities of GPUs for handling large matrices.
## Installation
### Prerequisites
- CUDA Toolkit (for GPU computations)
- Singular (for CPU computations)
- C and C++ compilers
- Linux operating system

### Setting Up CUDA Toolkit
1. **CUDA Toolkit**: Follow the installation guide on the official NVIDIA website to install the CUDA Toolkit. The installation guide provides detailed instructions for Linux operating system:
    - [Linux Installation Guide](https://docs.nvidia.com/cuda/cuda-installation-guide-linux/index.html)

2. **Singular**: Download and install Singular from [here](https://www.singular.uni-kl.de/index.php/singular-download.html).

## Usage
### Data Preparation and Conversion
Before comparing the performance of GPU and CPU computations, we need to have a large matrix to work with. Instead of typing a random numbers into a file, we make a C++ program to generate a random matrix and convert it into a format compatible with our GPU program. You can set the size of the square matrix by changing the number on the line 10 of the generate_matrix_file.cpp file.
```bash
string filename = "data/data60.txt";
```

After setting the size of the matrix, compile and run the program with the following command:
```bash
g++ -o generate_matrix_file generate_matrix_file.cpp
./generate_matrix_file
```

On the folder data, you will find a file with the name data60.txt. This file contains a random 60x60 matrix. You can change the size of the matrix by changing the number on the line 10 of the generate_matrix_file.cpp file.

Since the time constrains of this project, we didn't make our Singular program can read the format compatible with our GPU program. We need to convert the data to a format compatible with Singular using the provided convert_data_to_Singular_data.cpp C++ file. Compile and run it with the following command:
```bash
g++ -o convert_data_to_Singular_data convert_data_to_Singular_data.cpp
./convert_data_to_Singular_data
```
After running the program, you will find a file with the name Singular_data60.txt in the data folder. This file contains the matrix in a format compatible with Singular.

### Running the Programs
#### GPU Computations
Before running the GPU program, you need to specify the input file in the gaussian_elimination.cu file. Open the file and change the data_file variable to the desired file name. For example:

```bash
const char *data_file = "data/data30.txt";
```

After setting the input file, compile and run the program with the following commands:
```bash
nvcc -o gaussian_elimination gaussian_elimination.cu
./gaussian_elimination
```

Instead of typing 'nvcc -o gaussian_elimination gaussian_elimination.cu' and './gaussian_elimination' every time you want to run the program, you can compile or compile and run the program with the following command:
```bash
make
```
or
```bash
make run
```


The program will print the output of the Gaussian elimination process, including the time taken for the computation.

Output image:

#### CPU Computations
For CPU computations, we need to copy the content of Singular_data60.txt from data folder to the Singular_gaussian.c file and replace it with the current matrix on the line 8 of the Singular_gaussian.c file.
```bash
matrix A[n][n+1] = 
```
After setting the input file, run the program with the following command:
```bash
Singular Singular_gaussian.c
```
The program will print the output of the Gaussian elimination process, including the time taken for the computation.

Output image:

## Results
The results of the comparison between GPU and CPU run times are presented in the table below:

| Matrix Size | GPU Time (ms) | CPU Time (ms) |
|-------------|---------------|---------------|
| 3 x 4       | 88            | 0             |
| 16 x 17     | 90            | 240           |
| 27 x 28     | 95            | 1580          |
| 30 x 31     | 92            | 2320          |
| 60 x 61     | 90            | 48870         |
| 90 x 91     | 90            | 363940        |
| 120 x 121   | 90            | 1492430       |
| 150 x 151   | 96            | 4509850       |

The results show that the GPU computations consistently outperform the CPU computations, especially for larger matrix sizes. The GPU time remains relatively constant, while the CPU time increases significantly with the matrix size.

## Verification
To ensure the accuracy of the results, we cross-referenced the output of our GPU program with solutions from an established online tool, [OnlineMSchool Gaussian elimination calculator](https://onlinemschool.com/math/assistance/equation/gaus/). The results were consistent, confirming the accuracy of our GPU computations.

## Authors
- Khoi Nguyen
- Jeniffer Limondo
- Jamen Tenney
