LIB "linalg.lib";
LIB "matrix.lib";

ring r=0,(x),dp;
int n = 3;
int m = n+1;

// Create the matrix
matrix A[n][m] = 2,  1, -1,  8,
                -3, -1,  2, -11,
                -2,  1,  2, -3;

print(A);

list Z = gauss_row(A,1);   // Perform Gaussian elimination

matrix U = Z[2]; // Upper triangular matrix
U;

matrix S = Z[3]; // Scaling matrix
S;

// Back substitution to solve Ux = S
vector x = back_subst(U, S);

// Output the solution
for (int i = 1; i <= n; i++) {
    printf("x%d = %s\n", i, string(x[i]));
}

// Function for back substitution
vector back_subst(matrix U, matrix S) {
    int n = nrows(U);
    vector x[n];
    for (int i = n; i > 0; i--) {
        number sum = S[i][ncols(S)];
        for (int j = i + 1; j <= n; j++) {
            sum = sum - U[i][j] * x[j];
        }
        x[i] = sum / U[i][i];
    }
    return(x);
}

quit;
