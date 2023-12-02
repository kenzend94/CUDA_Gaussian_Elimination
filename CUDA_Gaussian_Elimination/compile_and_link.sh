#!/bin/bash

# Compile the CUDA and C++ files
nvcc -c DeviceFunc.cu -o DeviceFunc.o
nvcc -c Kernel.cu -o Kernel.o
nvcc -c fread.cpp -o fread.o
nvcc -c main.cpp -o main.o

# Link the object files into a single executable
nvcc DeviceFunc.o Kernel.o fread.o main.o -o program

# Optional: print a success message
echo "Compilation and linking completed successfully."
