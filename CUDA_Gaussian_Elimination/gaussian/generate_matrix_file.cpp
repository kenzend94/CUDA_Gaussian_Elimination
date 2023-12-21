#include <iostream>
#include <fstream>
#include <cstdlib> // For rand() and srand()
#include <ctime>   // For time()
#include <string>
#include <regex>

using namespace std;

string filename = "data/data60.txt";

int extractNumberFromFilename(const string& filename) {
    regex pattern(R"(data(\d+)\.txt)");
    smatch matches;

    if (regex_search(filename, matches, pattern) && matches.size() > 1) {
        return stoi(matches.str(1));
    }
    return -1; // Return -1 if no number is found
}

int main() {
    
    int n = extractNumberFromFilename(filename);

    if (n == -1) {
        cerr << "Error: Number not found in filename." << endl;
        return 1;
    }

    ofstream file(filename);

    if (!file) {
        cerr << "Error opening file for writing." << endl;
        return 1;
    }

    srand(time(NULL)); // Initialize random seed

    int m = n + 1;

    file << n << endl;

    for (int i = 0; i < n; i++) {
        for (int j = 0; j < m; j++) {
            int random_number = rand() % 51 - 25; // Generate a random number between -25 and 25
            file << random_number;
            if (j < m - 1) {
                file << " "; // Space between numbers, not after the last number
            }
        }
        file << endl;
    }

    file.close();

    return 0;
}
