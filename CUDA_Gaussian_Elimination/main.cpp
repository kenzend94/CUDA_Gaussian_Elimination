#include<stdio.h>
#include "common.h"
#include<stdlib.h>

#define USE_CLOCK

#ifdef USE_CLOCK
#include <time.h>
#endif

int main(int argc, char** argv)
{
    float* a_h = NULL;
    float* b_h = NULL;
    float* result, sum, rvalue;
    int numvar, j;

    #ifdef USE_CLOCK
        clock_t start, end;
        double cpu_time_used;
    #endif

    numvar = 0;

    // Reading the file to copy values 
    printf("\t\tShowing the data read from file\n\n");
    getvalue(&a_h, &numvar);

    //Allocating memory on host for b_h 
    b_h = (float*)malloc(sizeof(float) * numvar * (numvar + 1));

    #ifdef USE_CLOCK
        start = clock();
    #endif

    //Calling device function to copy data to device 
    DeviceFunc(a_h, numvar, b_h);

    #ifdef USE_CLOCK
        end = clock();
        cpu_time_used = ((double) (end - start)) / CLOCKS_PER_SEC;
    #endif

    //Showing the data 
    printf("\n\n");

    for (int i = 0; i < numvar; i++)
    {
        for (int j = 0; j < numvar + 1; j++)
        {
            printf("%f\n", b_h[i * (numvar + 1) + j]);
        }
        printf("\n");
    }

    //Using Back substitution method 
    result = (float*)malloc(sizeof(float) * (numvar));
    for (int i = 0; i < numvar; i++)
    {
        result[i] = 1.0;
    }

    for (int i = numvar - 1; i >= 0; i--)
    {
        sum = 0.0;

        for (j = numvar - 1; j > i; j--)
        {
            sum = sum + result[j] * b_h[i * (numvar + 1) + j];
        }
        rvalue = b_h[i * (numvar + 1) + numvar] - sum;
        result[i] = rvalue / b_h[i * (numvar + 1) + j];
    }

    //Displaying the result 
    printf("\n\t\tVALUES OF VARIABLES\n\n");
    for (int i = 0; i < numvar; i++)
    {
        printf("[X%d] = %+f\n", i, result[i]);
    }

    #ifdef USE_CLOCK
        printf("Time taken for DeviceFunc: %f seconds\n", cpu_time_used);
    #endif

    // _getch(); 
    // scanf("%d", &j);

    
    return 0;
}