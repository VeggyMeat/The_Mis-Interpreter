#include <stdio.h>

int main(int argc, int argv[]) {
    char a = 10;
    char b = 10 + a;
    char c = argv[0];
    printf("%d", a+b+c);
    return 0;
}