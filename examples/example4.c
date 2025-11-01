#include <stdio.h>

int main(int argc, int argv[]) {
    char a = 15;
    char b = 5 + a;
    char c = argv[0];
    char d = argv[1];
    if (c < d) {
        printf("%d", a-b+c);
    } else {
        if (d > b) {
            printf("%d", b+d);
        }
        else {
            if (c == 15) {
                printf("%d", c-d);
            }
        }
    }
    return 0;
}