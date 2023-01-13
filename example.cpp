#include <iostream>
using namespace std;

/*
Notes on C++:

Every line ends with a semicolon

Single line comments are "//"

Functions are made in this format:

return_type function_name() {
  inside_code;
}

In C++ a function must return something unless it is void
Function type detremined waht will be returned

Types of functions are:
int
double
char
string
bool
And if you don't want to return anything "void"

While format doesn't matter in C++ it is still best practice to use new lines and indentation
*/

int first_var = 1; // Variables can be created and defined in the same line...

int second_var; // ...or delcared and defined in seperate lines
second_var = 2;

first_var = 3; // Variable type is not needed in redefinition

void Function1() { // Example of function definition
  cout << "I am a function";
}

int main() {
  cout << "Hello World!"; 
  Function1(); // Example of calling a function
  return 0;
}
