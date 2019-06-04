#include <stdlib.h>
#include "util.h"
#include "collections.h"

deque_t* deque_new(size_t size){
    deque_t* deque = MALLOC(size + sizeof(deque_t)) ;
    deque->size = size;
    deque->front = 0;
    deque->len = 0;
    return deque;
}

#define FIT(d, n) ((n) % d->size)
#define REAR(d) FIT(d, d->front + d->len)

int deque_len(deque_t* deque) {
    return deque->len;
}

int deque_empty(deque_t* deque) {
    return deque->len == 0;
}

int deque_full(deque_t* deque) {
    return deque_len(deque) == deque->size;
}

void deque_push(deque_t* deque, void* value) {
    if (deque_full(deque))
        ERROR("dqueue is full");
    deque->block[REAR(deque)]= value;
    ++deque->len;
}

void* deque_pop(deque_t* deque) {
    if (deque_empty(deque))
        ERROR("dqueue is empty");
    --deque->len;
    return deque->block[FIT(deque, deque->front++)];
}

