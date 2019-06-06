#include <stdio.h>
#include <gc.h>
#include "collections.h"

int main() {
//    GC_init();
    printf("Hello, World!\n");

    deque_t* deque = deque_new(2);
    printf("len %d %d\n", deque_len(deque), deque->front);

    int x = 2;
    deque_push(deque, &x);
    printf("len %d %d\n", deque_len(deque), deque->front);

    int* y = (int*) deque_pop(deque);
    printf("len %d %d\n", deque_len(deque), deque->front);
    printf("popped==%d\n", *y);

    int values[] = {2, 3};
    for(int i = 0; i < 2; i++) {
        deque_push(deque, &values[i]);
        printf("len %d %d\n", deque_len(deque), deque->front);
    }

    y = (int*) deque_pop(deque);
    printf("len %d %d\n", deque_len(deque), deque->front);
    printf("popped==%d\n", *y);

    y = (int*) deque_pop(deque);
    printf("len %d %d\n", deque_len(deque), deque->front);
    printf("popped==%d\n", *y);

    int values2[] = {4, 5};
    for(int i = 0; i < 2; i++) {
        deque_push(deque, &values2[i]);
        printf("len %d %d\n", deque_len(deque), deque->front);
    }

    while (!deque_empty(deque)) {
        y = (int*) deque_pop(deque);
        printf("len %d %d\n", deque_len(deque), deque->front);
        printf("popped==%d\n", *y);
    }

    return 0;
}