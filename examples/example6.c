#include <stdio.h>

int main(int argc, int argv[]) {
    char a = argv[0];
    if (a > 0) {
        printf("%d", a * a);
    } else {
        printf("%d", (0 - 1) * a * a);
    }
    return 0;
}