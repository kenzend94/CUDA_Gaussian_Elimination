#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#define USE_CLOCK

#ifdef USE_CLOCK
#include <time.h>
#endif

void swap_rows(float *matrix, int row1, int row2, int numvar) {
    for (int i = 0; i <= numvar; i++) {
        float temp = matrix[row1 * (numvar + 1) + i];
        matrix[row1 * (numvar + 1) + i] = matrix[row2 * (numvar + 1) + i];
        matrix[row2 * (numvar + 1) + i] = temp;
    }
}

int main() {
    int numvar = 3;
    float matrix[3][4] = {
        {2, -2, 9, -16},
        {-2, 1, -6, 11},
        {1, -1, 3, -5}
    };

#ifdef USE_CLOCK
    clock_t start, end;
    start = clock();
#endif

    // Gaussian elimination with partial pivoting
    for (int i = 0; i < numvar; i++) {
        // Partial pivoting
        int maxRow = i;
        float maxVal = fabs(matrix[i][i]);
        for (int k = i + 1; k < numvar; k++) {
            if (fabs(matrix[k][i]) > maxVal) {
                maxVal = fabs(matrix[k][i]);
                maxRow = k;
            }
        }

        // Swap rows
        if (i != maxRow) {
            swap_rows((float *)matrix, i, maxRow, numvar);
        }

        // Check for singularity
        if (fabs(matrix[i][i]) < 1e-8) {
            printf("Matrix is singular or nearly singular\n");
            return -1;
        }

        // Elimination
        for (int k = i + 1; k < numvar; k++) {
            float factor = matrix[k][i] / matrix[i][i];
            for (int j = i; j <= numvar; j++) {
                matrix[k][j] -= factor * matrix[i][j];
            }
        }
    }

    // Back substitution
    float solution[numvar];
    for (int i = numvar - 1; i >= 0; i--) {
        solution[i] = matrix[i][numvar];
        for (int j = i + 1; j < numvar; j++) {
            solution[i] -= matrix[i][j] * solution[j];
        }
        solution[i] /= matrix[i][i];
    }

#ifdef USE_CLOCK
    end = clock();
    double cpu_time_used = ((double)(end - start)) / CLOCKS_PER_SEC;
    printf("Time taken: %f seconds\n", cpu_time_used);
#endif

    // Displaying the result
    printf("\nSolution:\n");
    for (int i = 0; i < numvar; i++) {
        printf("X%d = %f\n", i + 1, solution[i]);
    }

    return 0;
}
