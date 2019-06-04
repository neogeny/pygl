cmake_minimum_required(VERSION 3.14)
project(cpglc C)

set(CMAKE_C_STANDARD 99)

include_directories(/usr/local/include/)
link_libraries(/usr/local/lib/libgc.dylib)
add_executable(cpglc src/main.c src/collections.h src/util.h src/collections.c src/util.c)
