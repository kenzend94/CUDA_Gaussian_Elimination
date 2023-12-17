#include <iostream>
#include <fstream>

int main() {
    std::ofstream file("data2.txt"); // Create and open a text file

    if (!file) {
        std::cerr << "Error opening file for writing." << std::endl;
        return 1;
    }

    int n = 499;
    int m = n + 1;

    file << n << std::endl; // Write the value of n to the first line

    int number = 1; // Starting number for the sequence

    for (int i = 0; i < n; i++) { // Outer loop runs n times
        for (int j = 0; j < m; j++) { // Inner loop runs m times
            file << number++; // Write the number
            if (j < m - 1) {
                file << " "; // Space between numbers, not after the last number
            }
        }
        file << std::endl; // Newline after each row of numbers
    }

    file.close(); // Close the file

    return 0;
}
