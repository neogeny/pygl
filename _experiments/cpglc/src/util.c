#include <stdlib.h>
#include <stdio.h>
#include "util.h"


void _error(const char* msg) {
    printf("ERROR: %s", msg);
    exit(1);
}
