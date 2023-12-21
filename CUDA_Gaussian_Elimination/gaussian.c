//#include <time.h>
//LIB "linalg.lib";
LIB "matrix.lib";

system("--ticks-per-sec",1000); // set timer resolution to ms

//clock_t start, end;
//double cpu_time_used;


ring r=0,(x),dp;

//matrix A[n][m]=1,3,-1,4,2,5,-1,3,1,3,-1,4,0,4,-3,1,-3,1,-5,-2;
int n = 499;
int m = n+1;

timer=1; // The time of each command is printed
int t = timer;

// Create the matrix
//matrix A[n][m] = 2,  1, -1,  8,
//                 -3, -1,  2, -11,
//                 -2,  1,  2, -3;

matrix A[n][m];

int counter = 1; // Start counter from 1

for (int i = 1; i <= n; i++) {
    for (int j = 1; j <= m; j++) {
        A[i, j] = counter; // Assign the current counter value to the matrix element
        counter++; // Increment the counter
    }
}

t = timer-t;
print("How long does it take to create a matrix");
t;

// A is now filled with numbers from 1 to 9900

//printf("Print A:\n")

print(A);
print("");

timer=0;
//
t=timer;

list Z = gauss_row(A,1);   //construct P,U,S s.t. P*A=U*S

print("timing after doing gaussian elimiation");

timer-t;
