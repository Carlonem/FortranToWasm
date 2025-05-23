#include <emscripten.h>

// Declaration of Fortran functions to be called from C
extern int get_fixed_integer(int num);
extern void start(void);

// C wrappers to be exported to JavaScript
// These wrappers allow calling Fortran functions from JavaScript
EMSCRIPTEN_KEEPALIVE
int get_fixed_integer_wrapper(int num) {
    return get_fixed_integer(num);
}

// Wrapper for the main program
EMSCRIPTEN_KEEPALIVE
void start_wrapper(void) {
    start();
}