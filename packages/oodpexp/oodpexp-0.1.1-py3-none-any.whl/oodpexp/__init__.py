def exp_21():
    a = '''#include <iostream>
using namespace std;

class Car {
private:
    string brand;
    int year;

public:
    // Method to set car details
    void setDetails(string b, int y) {
        brand = b;
        year = y;
    }

    // Method to display car details
    void displayDetails() {
        cout << "Car Brand: " << brand << endl;
        cout << "Manufacturing Year: " << year << endl;
    }
};

int main() {
    Car myCar;

    // Setting car details
    myCar.setDetails("Toyota", 2022);

    // Displaying car details
    myCar.displayDetails();

    return 0;
}

-------------------------------------------------------------------------------------------------------------'''
    return a


def exp_22():
    a='''#include <iostream>
using namespace std;

// Class definition
class Student {
private:
    string name;
    int age;

public:
    // Constructor
    Student(string n, int a);

    // Method declaration
    void display();
};

// Constructor definition outside the class
Student::Student(string n, int a) {
    name = n;
    age = a;
}

// Method definition outside the class
void Student::display() {
    cout << "Student Name: " << name << endl;
    cout << "Student Age: " << age << endl;
}

int main() {
    // Creating an object of Student class
    Student s1("Alice", 20);

    // Calling method
    s1.display();

    return 0;
}
----------------------------------------------------------------------------------------------------------------'''
    return a


def exp_23():
    a='''#include <iostream>
using namespace std;

// Class definition
class Adder {
private:
    int num1, num2;

public:
    // Constructor to initialize numbers
    Adder(int a, int b) {
        num1 = a;
        num2 = b;
    }

    // Method to add the two numbers
    int sum() {
        return num1 + num2;
    }
};

int main() {
    int a, b;

    // Taking input from user
    cout << "Enter two integers: ";
    cin >> a >> b;

    // Creating an object of Adder class
    Adder obj(a, b);

    // Displaying the sum
    cout << "Sum: " << obj.sum() << endl;

    return 0;
}
--------------------------------------------------------------------------------------------------------------'''
    return a


def exp_24():
    a='''#include <iostream>
using namespace std;

class Student {
private:
    string name;
    int age;
    int rollNo;

public:
    void getData() {
        cout << "Enter Name: ";
        cin >> name;
        cout << "Enter Age: ";
        cin >> age;
        cout << "Enter Roll No: ";
        cin >> rollNo;
    }

    void displayData() {
        cout << "\nStudent Information:\n";
        cout << "Name: " << name << "\nAge: " << age << "\nRoll No: " << rollNo << endl;
    }
};

int main() {
    Student s;
    s.getData();
    s.displayData();
    return 0;
}

----------------------------------------------------------------------------------------------------------------'''
    return a



def exp_25():
    a='''#include <iostream>
using namespace std;

class PrimeChecker {
private:
    int num;

public:
    void getNumber() {
        cout << "Enter a number: ";
        cin >> num;
    }

    bool isPrime() {
        if (num < 2) return false;
        for (int i = 2; i * i <= num; i++) {
            if (num % i == 0) return false;
        }
        return true;
    }
};

int main() {
    PrimeChecker p;
    p.getNumber();
    if (p.isPrime())
        cout << "The number is Prime.\n";
    else
        cout << "The number is Not Prime.\n";
    return 0;
}

-------------------------------------------------------------------------------------------------------------------'''
    return a



def exp_26():
    a='''#include <iostream>
using namespace std;

class Complex {
private:
    int real, imag;

public:
    Complex(int r = 0, int i = 0) {
        real = r;
        imag = i;
    }

    friend Complex add(Complex c1, Complex c2);

    void display() {
        cout << real << " + " << imag << "i" << endl;
    }
};

Complex add(Complex c1, Complex c2) {
    return Complex(c1.real + c2.real, c1.imag + c2.imag);
}

int main() {
    Complex c1(3, 4), c2(5, 6);
    Complex c3 = add(c1, c2);
    cout << "Sum of Complex Numbers: ";
    c3.display();
    return 0;
}

    -------------------------------------------------------------------------------------------------------------------'''

    return a



def exp_27():
    a='''#include <iostream>
using namespace std;

class Box {
private:
    int length, width, height;

public:
    // Default constructor (in case no dimensions are provided)
    Box() {
        length = 0;
        width = 0;
        height = 0;
    }

    // Parameterized constructor (sets custom dimensions)
    Box(int l, int w, int h) {
        length = l;
        width = w;
        height = h;
    }

    // Function to calculate volume of the box
    int volume() {
        return length * width * height;
    }

    // Getter functions to access box dimensions
    int getLength() {
        return length;
    }

    int getWidth() {
        return width;
    }

    int getHeight() {
        return height;
    }
};

int main() {
    // Creating a Box object with dimensions 5, 6, and 7
    Box b(5, 6, 7);

    // Displaying the dimensions of the box
    cout << "Box Dimensions:" << endl;
    cout << "Length: " << b.getLength() << endl;
    cout << "Width: " << b.getWidth() << endl;
    cout << "Height: " << b.getHeight() << endl;

    // Displaying the volume of the box
    cout << "Volume of Box: " << b.volume() << endl;

    return 0;
}

    -------------------------------------------------------------------------------------------------------------------'''
    return a



def exp_28():
    a='''#include <iostream>
using namespace std;

class Demo {
public:
    // Constructor: Called when an object of class is created
    Demo() {
        cout << "Constructor Called: Object Created\n";
    }

    // Destructor: Called when an object is destroyed (goes out of scope)
    ~Demo() {
        cout << "Destructor Called: Object Destroyed\n";
    }
};

int main() {
    // Creating an object of class Demo
    Demo d;

    // At the end of main(), d will go out of scope, triggering the destructor
    return 0;
}

    -------------------------------------------------------------------------------------------------------------------'''
    return a



def exp_29():
    a='''#include <iostream>
using namespace std;

class Person {
protected:
    string name;
    int age;

public:
    void getData() {
        cout << "Enter Name: ";
        cin >> name;
        cout << "Enter Age: ";
        cin >> age;
    }

    void displayData() {
        cout << "Name: " << name << ", Age: " << age << endl;
    }
};

class Patient : public Person {
private:
    string disease;

public:
    void getPatientData() {
        getData();
        cout << "Enter Disease: ";
        cin >> disease;
    }

    void displayPatientData() {
        displayData();
        cout << "Disease: " << disease << endl;
    }
};

int main() {
    Patient p;
    p.getPatientData();
    p.displayPatientData();
    return 0;
}

    -------------------------------------------------------------------------------------------------------------------'''
    return a



def exp_30():
    a='''#include <iostream>
using namespace std;

class Base {
private:
    // Private variable: Cannot be accessed directly outside the class
    int privateVar = 10;
    
protected:
    // Protected variable: Can be accessed within derived classes
    int protectedVar = 20;

public:
    // Public variable: Can be accessed from anywhere
    int publicVar = 30;

    // Getter for private variable (if needed)
    int getPrivateVar() {
        return privateVar;
    }
};

class Derived : public Base {
public:
    void display() {
        // cout << privateVar; // Not accessible as privateVar is private
        cout << "Protected Variable: " << protectedVar << endl; // Accessible because it's protected
        cout << "Public Variable: " << publicVar << endl; // Accessible because it's public
        cout << "Private Variable (via getter): " << getPrivateVar() << endl; // Access private using getter
    }
};

int main() {
    Derived d;
    d.display();
    return 0;
}


    -------------------------------------------------------------------------------------------------------------------'''
    return a



def exp_31():
    a='''#include <iostream>
using namespace std;

int main() {
    int n, sum = 0;

    cout << "=== Odd Natural Numbers & Their Sum ===" << endl;

    // Get input from user
    cout << "Enter how many odd numbers to display: ";
    cin >> n;

    // Validate input
    if (n <= 0) {
        cout << "Please enter a positive integer!" << endl;
        return 1;
    }

    cout << "\nFirst " << n << " odd natural numbers: ";

    // Loop to generate and sum odd numbers
    for (int i = 1; i <= n; i++) {
        int oddNumber = 2 * i - 1;
        cout << oddNumber << " ";
        sum += oddNumber;
    }

    cout << "\nSum of these odd numbers: " << sum << endl;
    cout << "=== Program Finished ===" << endl;

    return 0;
}


    -------------------------------------------------------------------------------------------------------------------'''
    return a



def exp_32():
    a='''#include <iostream>
using namespace std;

int main() {
    int num;

    cout << "=== Factor Finder ===" << endl;

    // Ask user for input
    cout << "Enter a positive number: ";
    cin >> num;

    // Validate input
    if (num <= 0) {
        cout << "Invalid input! Please enter a positive integer." << endl;
        return 1;
    }

    cout << "\nFactors of " << num << ": ";
    int factorCount = 0;

    // Loop to find all factors
    for (int i = 1; i <= num; i++) {
        if (num % i == 0) {
            cout << i << " ";
            factorCount++;
        }
    }

    // Show total number of factors
    cout << "\nTotal number of factors: " << factorCount << endl;

    cout << "=== Program Finished ===" << endl;
    return 0;
}

    -------------------------------------------------------------------------------------------------------------------'''
    return a



def exp_33():
    a='''#include <iostream>
#include <fstream>
#include <string>
using namespace std;

int main() {
    string filename = "data.txt";

    // Step 1: Write to the file
    ofstream outFile(filename);  // Opens file for writing (overwrites if it exists)

    if (!outFile) {
        cerr << "Error: Could not open file for writing." << endl;
        return 1;
    }

    outFile << "Hello, File Handling!\n";
    outFile << "This is the second line of text.\n";
    outFile.close();  // Always close the file when done writing
    cout << "Data written to file successfully.\n";

    // Step 2: Read from the file
    ifstream inFile(filename);  // Opens file for reading

    if (!inFile) {
        cerr << "Error: Could not open file for reading." << endl;
        return 1;
    }

    cout << "\n--- Reading from file ---\n";
    string line;
    while (getline(inFile, line)) {
        cout << line << endl;
    }
    cout << "--- End of file ---\n";

    inFile.close();  // Always close the file when done reading

    return 0;
}


    -------------------------------------------------------------------------------------------------------------------'''
    return a



def exp_34():
    a='''#include <iostream>
#include <fstream>
#include <string>

using namespace std;

int main() {
    int choice;

    cout << "=== Simple File Manager ===" << endl;

    do {
        // Display menu
        cout << "\nMenu:" << endl;
        cout << "1. Add Text to File" << endl;
        cout << "2. Display File Content" << endl;
        cout << "3. Exit" << endl;
        cout << "Enter your choice (1-3): ";
        cin >> choice;

        // Process user choice
        if (choice == 1) {
            // Open file in append mode
            ofstream file("data.txt", ios::app);
            if (!file) {
                cerr << "Error: Could not open file for writing." << endl;
                continue;
            }

            string text;
            cout << "Enter text to add: ";
            cin.ignore(); // Clear newline character from input buffer
            getline(cin, text);
            file << text << endl;

            cout << "Text added successfully!" << endl;
            file.close();
        } else if (choice == 2) {
            // Open file for reading
            ifstream file("data.txt");
            if (!file) {
                cerr << "Error: File does not exist or could not be opened." << endl;
                continue;
            }

            string line;
            cout << "\n--- File Content ---" << endl;
            while (getline(file, line)) {
                cout << line << endl;
            }
            cout << "--- End of File ---" << endl;
            file.close();
        } else if (choice == 3) {
            cout << "Exiting the program. Goodbye!" << endl;
        } else {
            cout << "Invalid choice. Please enter 1, 2, or 3." << endl;
        }

    } while (choice != 3);

    return 0;
}


    -------------------------------------------------------------------------------------------------------------------'''
    return a



def exp_35():
    a='''#include <iostream>
using namespace std;

// Template function to find the largest of two values
template <typename T>
T getLargest(T a, T b) {
    return (a > b) ? a : b;
}

int main() {
    cout << "=== Generic Largest Finder ===" << endl;

    // Integer comparison
    int int1, int2;
    cout << "\nEnter two integers:\n";
    cin >> int1 >> int2;
    cout << "Largest integer: " << getLargest(int1, int2) << endl;

    // Double comparison
    double double1, double2;
    cout << "\nEnter two decimal numbers:\n";
    cin >> double1 >> double2;
    cout << "Largest double: " << getLargest(double1, double2) << endl;

    // Character comparison
    char char1, char2;
    cout << "\nEnter two characters:\n";
    cin >> char1 >> char2;
    cout << "Largest character (based on ASCII): " << getLargest(char1, char2) << endl;

    cout << "\nProgram finished successfully." << endl;

    return 0;
}

    -------------------------------------------------------------------------------------------------------------------'''
    return a



def exp_36():
    a='''#include <iostream>
using namespace std;

template <typename T>
void swapData(T &a, T &b) {
    T temp = a;
    a = b;
    b = temp;
}

int main() {
    int x = 10, y = 20;
    cout << "Before swap: x = " << x << ", y = " << y << endl;
    swapData(x, y);
    cout << "After swap: x = " << x << ", y = " << y << endl;
    
    // Using swap with doubles as well
    double d1 = 3.14, d2 = 2.71;
    cout << "\nBefore swap: d1 = " << d1 << ", d2 = " << d2 << endl;
    swapData(d1, d2);
    cout << "After swap: d1 = " << d1 << ", d2 = " << d2 << endl;

    return 0;
}

    -------------------------------------------------------------------------------------------------------------------'''
    return a



def exp_37():
    a='''#include <iostream>
using namespace std;

template <typename T>
class Calculator {
public:
    T add(T a, T b) {
        return a + b;
    }
    T subtract(T a, T b) {
        return a - b;
    }
    T multiply(T a, T b) {
        return a * b;
    }
    T divide(T a, T b) {
        if (b == 0) {
            cout << "Error: Division by zero!" << endl;
            return 0;
        }
        return a / b;
    }
};

int main() {
    Calculator<double> calc;
    double a = 20.0, b = 10.0;
    
    cout << "Addition: " << calc.add(a, b) << endl;
    cout << "Subtraction: " << calc.subtract(a, b) << endl;
    cout << "Multiplication: " << calc.multiply(a, b) << endl;
    cout << "Division: " << calc.divide(a, b) << endl;
    
    return 0;
}

    -------------------------------------------------------------------------------------------------------------------'''
    return a



def exp_38():
    a='''#include <iostream>
using namespace std;

// Function to divide two integers with exception handling
double divide(int numerator, int denominator) {
    if (denominator == 0) {
        // Throwing a descriptive error message if denominator is zero
        throw "Error: Division by zero is not allowed.";
    }
    return static_cast<double>(numerator) / denominator;
}

int main() {
    int numerator;
    int denominator;

    cout << "=== Division Program with Exception Handling ===" << endl;

    // Asking user for input
    cout << "Enter the numerator: ";
    cin >> numerator;

    cout << "Enter the denominator: ";
    cin >> denominator;

    try {
        // Attempting the division
        double result = divide(numerator, denominator);
        cout << "Result: " << result << endl;
    }
    catch (const char* errorMessage) {
        // Catching and displaying the error message
        cout << "Exception caught: " << errorMessage << endl;
    }

    cout << "Program finished gracefully." << endl;

    return 0;
}


    -------------------------------------------------------------------------------------------------------------------'''
    return a


