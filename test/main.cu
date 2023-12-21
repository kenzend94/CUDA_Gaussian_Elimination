#include <cuda_runtime.h>
#include <stdio.h>
#include <cmath>

// ... [CUDA kernel forwardElimKernel defined here] ...
// cuda kernel for forwardElimKernel define
__global__ void forwardElimKernel(double *mat, int numvar, int k) {
    int i = blockIdx.x * blockDim.x + threadIdx.x;
    if (i > k && i < numvar) {
        double term = mat[i * (numvar + 1) + k] / mat[k * (numvar + 1) + k];
        for (int j = k; j < numvar + 1; j++) {
            mat[i * (numvar + 1) + j] -= term * mat[k * (numvar + 1) + j];
        }
    }
}

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
    }

    cudaMemcpy(mat, d_mat, size, cudaMemcpyDeviceToHost);
    cudaFree(d_mat);
}

// ... [rest of your host code, including backSub function] ...

// function to calculate the values of the unknowns
void backSub(double mat[N][N+1])
{
    double x[N];  // An array to store solution
 
    /* Start calculating from last equation up to the
       first */
    for (int i = N-1; i >= 0; i--)
    {
        /* start with the RHS of the equation */
        x[i] = mat[i][N];
 
        /* Initialize j to i+1 since matrix is upper
           triangular*/
        for (int j=i+1; j<N; j++)
        {
            /* subtract all the lhs values
             * except the coefficient of the variable
             * whose value is being calculated */
            x[i] -= mat[i][j]*x[j];
        }
 
        /* divide the RHS by the coefficient of the
           unknown being calculated */
        x[i] = x[i]/mat[i][i];
    }
 
    printf("\nSolution for the system:\n");
    for (int i=0; i<N; i++)
        printf("%lf\n", x[i]);
}


int main() {
    double mat[N][N+1] = { /* ... your matrix data ... */ };
    
    // Call forward elimination
    forwardElim((double *)mat, N);

    // Perform back substitution on the host
    backSub(mat);

    return 0;
}
