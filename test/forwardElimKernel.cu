__global__ void forwardElimKernel(double *mat, int numvar, int k) {
    int idx = blockDim.x * blockIdx.x + threadIdx.x + k + 1;
    if (idx < numvar) {
        double factor = mat[idx * (numvar + 1) + k] / mat[k * (numvar + 1) + k];
        for (int j = k; j <= numvar; j++) {
            mat[idx * (numvar + 1) + j] -= factor * mat[k * (numvar + 1) + j];
        }
    }
}
