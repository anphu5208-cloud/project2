// 060206013975_Baitap1.cpp : This file contains the 'main' function. Program execution begins and ends there.
//

#include <iostream>
using namespace std;
#include <fstream>
#include <string>
using namespace std;

int main() {
    cout << "==060206013975-Nguyen Hoa An Phu==\n";

    ifstream file("dataa.txt");
    if (!file.is_open()) {
        cout << "Khong the mo file dataa.txt\n";
        return 1;
    }

    string line;
    int count = 0;

    cout << "Cac dong bat dau bang \"-\":\n";
    while (getline(file, line)) {
        count++;
        if (line.compare(0, 1, "-") == 0) {
            cout << line << endl;
        }
    }

    cout << "\nTong so dong trong file: " << count << endl;

    file.close();
    return 0;
}
