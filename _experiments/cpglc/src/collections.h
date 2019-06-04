//
// Created by Apalala on 2019-06-03.
//

#ifndef CPGLC_COLLECTIONS_H
#define CPGLC_COLLECTIONS_H

typedef struct {
    int size, len;
    int front, rear;
    void* block[];
} deque_t;

deque_t* deque_new(size_t size);
int deque_len(deque_t* deque);
int deque_empty(deque_t* deque);
int deque_full(deque_t* deque);
void deque_push(deque_t* deque, void* value);
void* deque_pop(deque_t* deque);


#endif //CPGLC_COLLECTIONS_H
