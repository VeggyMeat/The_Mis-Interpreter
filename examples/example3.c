#include <stdio.h>

int main(int argc, int argv[]) {
    char a = 10;
    char b = 10 + a;
    char c = argv[0];
    if (c > 5) {
        printf("%d", a * b + c);
    }
    else {
        printf("%d", 12);
    }
    return 0;
}