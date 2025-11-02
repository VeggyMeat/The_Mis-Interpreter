#include <stdio.h>

int main(int argc, int argv[]) {
    char a = 15;
    char b = 5 + a;
    char c = argv[0];
    char d = argv[1];
    char e = argv[2];
    if (a > d) {
        printf("%d", c * d + e);
    } else {
        if (e < a) {
            printf("%d", a * b);
        }
    }
    return 0;
}