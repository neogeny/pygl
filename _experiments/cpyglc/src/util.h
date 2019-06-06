//
// Created by Apalala on 2019-06-03.
//

#ifndef CPYGL_UTIL_H
#define CPYGL_UTIL_H

#include "gc/gc.h"

#define MALLOC(sz) GC_MALLOC(sz)
#define NEW(t) GC_NEW(t)
#define FREE(sz)

#define ERROR(msg) _error(msg);

void _error(const char* msg);


#endif //CPYGL_UTIL_H
