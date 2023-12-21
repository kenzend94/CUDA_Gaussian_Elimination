#include <iostream>
#include <fstream>
#include <sstream>
#include <string>

using namespace std;

string data_file_name = "data/data100.txt";

string constructOutputFileName(const string& inputFilePath) {
    // Extract the file name from the input file path
    size_t pos = inputFilePath.find_last_of("/\\");
    string fileName = (pos != string::npos) ? inputFilePath.substr(pos + 1) : inputFilePath;

    // Prefix the file name with "Singular_" and return the new path
    return inputFilePath.substr(0, pos + 1) + "Singular_" + fileName;
}

int main() {
    string inputFilePath = data_file_name; // Path to the input file
    string outputFilePath = constructOutputFileName(inputFilePath);

    ifstream inputFile(inputFilePath);
    ofstream outputFile(outputFilePath);
    
    if (!inputFile.is_open() || !outputFile.is_open()) {
        cerr << "Unable to open file(s)";
        return 1;
    }

    string line;
    bool isFirstLine = true;
    
    // Skip the first line
    getline(inputFile, line);

    while (getline(inputFile, line)) {
        if (!isFirstLine) {
            outputFile << ", " << endl;
        }

        istringstream iss(line);
        int number;
        bool isFirstNumber = true;

        while (iss >> number) {
            if (!isFirstNumber) {
                outputFile << ", ";
            }
            outputFile << number;
            isFirstNumber = false;
        }

        isFirstLine = false;
    }

    outputFile << ";";

    inputFile.close();
    outputFile.close();

    return 0;
}
