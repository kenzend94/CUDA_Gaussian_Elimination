#include <iostream>
#include <fstream>
#include <sstream>
#include <iomanip>
#include <string>
#include <vector>

double convertToDecimal(const std::string& str) {
    size_t slashPos = str.find('/');
    if (slashPos != std::string::npos) {
        double numerator = std::stod(str.substr(0, slashPos));
        double denominator = std::stod(str.substr(slashPos + 1));
        return numerator / denominator;
    }
    return std::stod(str);
}

int main() {
    std::ifstream file("data.txt");
    if (!file.is_open()) {
        std::cerr << "Error opening file" << std::endl;
        return 1;
    }

    int numVariables;

    // Read the number of variables
    file >> numVariables;
    std::vector<std::vector<double>> matrix(numVariables, std::vector<double>(numVariables + 1));

    for (int i = 0; i < numVariables; ++i) {
        for (int j = 0; j <= numVariables; ++j) {

            // Read the value as a string
            std::string valueStr;

            // If we are at the last column, read until the end of the line
            file >> valueStr;
            matrix[i][j] = convertToDecimal(valueStr);
        }
    }

    file.close();

    std::cout << "Number of variables = " << numVariables << std::endl;

    // Print the matrix
    for (const auto& row : matrix) {
        for (double value : row) {
            std::cout << std::fixed << std::setprecision(6) << "[" << value << "] ";
        }
        std::cout << std::endl;
    }

    return 0;
}
