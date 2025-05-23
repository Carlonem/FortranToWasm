
# FortranToWasm - A Fortran To WASM Template

<div align="justify">

This project shows an example of how to compile Fortran code to WebAssembly (WASM) and run it in a web browser using the process proposed by [Dr George W Stagg](https://gws.phd/posts/fortran_wasm/). **Note**: This is the first part of a Raylib-Flang-WASM implementation.

## Overview

 It uses a C wrapper to interface between Fortran and JavaScript, providing a clean way to call Fortran functions from the browser environment. The project includes a Python-based build system that uses Docker to handle the compilation toolchain.

## Features

- Fortran code compilation to WebAssembly via [LLVM/Flang](https://gws.phd/posts/fortran_wasm/).
- [C wrapper](https://gws.phd/posts/fortran_wasm/) functions to facilitate Fortran-JavaScript interoperability.
- Web interface to call Fortran functions from the browser.
- Detailed logging system for debugging and tracing.
- Compilation process automation with Docker.

## Project Structure

```
project/
│
├── fortranToWasm.py        # Python build script
├── src/                    # Source code directory
│   ├── main.f90            # Fortran main program
│   ├── fixed_integer.f90   # Fortran module with functions
│   ├── wrapper.c           # C wrapper functions
│   ├── index.html          # Web interface (used to build)
│   └── Makefile            # Build configuration
├── build/                  # Build output directory (created during build)
│   ├── fortran.js          # Generated JavaScript loader
│   ├── fortran.wasm        # WebAssembly binary
│   ├── compile.log         # Compilation log
│   └── index.html          # Web interface
└── cache/                  # Cache directory for Emscripten (created during build)
```

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/Carlonem/FortranToWasm.git
   cd FortranToWasm
   ```

2. Get the following Docker image (use **dev** for now):
   ```
   docker pull ghcr.io/r-wasm/flang-wasm:dev
   ```

3. Run the build script:

     > **Note**: The first run may take longer as the cache is being built. Subsequent runs will be much faster.
   ```
   python fortranToWasm.py
   ```


4. Start a local web server to serve the files:
   ```
   python -m http.server
   ```

5. Open your browser and navigate to:
   ```
   http://localhost:8000
   ```


## Building the Project

The `fortranToWasm.py` script handles the full build process:

1. Creates build and cache directories
2. Sets up appropriate permissions
3. Runs the Docker container with the build environment
4. Executes `make all` in the src directory
5. Logs all outputs for debugging

The build process creates:
- A JavaScript loader file (`fortran.js`)
- A WebAssembly binary (`fortran.wasm`)
- A detailed compilation log (`compile.log`)

## How It Works

### Compilation Process

1. The Python script runs a Docker container with the LLVM/Flang toolchain
2. Fortran code is compiled to LLVM IR
3. The C wrapper functions are compiled and linked
4. Emscripten compiles everything to WebAssembly and generates JavaScript bindings

### Runtime Operation

1. The browser loads the WebAssembly module via the JavaScript loader
2. C wrapper functions provide an interface between JavaScript and Fortran
3. JavaScript uses Emscripten's `cwrap` to create callable JavaScript functions
4. These functions can then call the compiled Fortran code

### C Wrapper Functions

The project uses two main C wrapper functions:

1. `get_fixed_integer_wrapper` - Calls a Fortran function that computes a fixed integer based on an input parameter
2. `start_wrapper` - Calls the main Fortran program

## Troubleshooting

Since I couldn't directly pass the main program to the WebAssembly compilation, I used the following solution to maintain compatibility with gfortran while allowing integration with Emscripten:

```fortran
! Module containing the main program functionality
! Fortran requires a main program for complete compilation
module program_module
    use iso_c_binding
    use my_module
    implicit none
    
contains

    ! Main subroutine that serves as the program entry point
    ! Bound to C for Emscripten compatibility using bind(C, name="start")
    ! This is the ON version for Emscripten
    subroutine fortran_main() bind(C, name="start")
        implicit none
        write(*,*) 'program start from fortran_main', func()
    end subroutine fortran_main
end module program_module

! Traditional Fortran main program
! This section is OFF when compiling with Emscripten
! Does not respond to C bindings
program main
    use program_module
    implicit none

    ! Always use subroutine for compatibility
    call fortran_main()
end program main
```
This approach uses a module with a C-bound subroutine that serves as the entry point for WebAssembly, while still maintaining a traditional Fortran program structure that works with standard compilers like gfortran.

### Common Issues

1. **Docker not running**  
   Error message: "docker command not found"  
   Solution: Install Docker and make sure the service is running

2. **Permission issues**  
   Error message: "Permission denied" during build  
   Solution: Ensure you have write permissions to the project directory

3. **Module loading failure**  
   Error message: "Failed to load: FortranModule not defined"  
   Solution: Check that the build process completed successfully and that `fortran.js` was created

4. **Function not found**  
   Error message: "Cannot call unknown function"  
   Solution: Verify that the function names in the C wrapper match those referenced in JavaScript

### Logs

Two types of logs are available:

1. **Compilation Log** - Shows the output from the build process
2. **Runtime Log** - Shows real-time operation, function calls, and errors

Access both logs using the toggle buttons in the web interface.

## Performance Considerations

- Initial load may be slow due to WebAssembly compilation
- Once loaded, function calls are very fast
- The cache directory improves subsequent build times

## References

- [LLVM/Flang](https://github.com/r-wasm/flang-wasm)
- [Patching LLVM Flang to output WebAssembly objects](https://gws.phd/posts/fortran_wasm/)
- [Full-Stack-Fortran](https://github.com/StarGate01/Full-Stack-Fortran)
- [FORTRAN In The Browser](https://chrz.de/2020/04/21/fortran-in-the-browser/)
- [Using Fortran on Cloudflare Workers](https://blog.cloudflare.com/using-fortran-on-cloudflare-workers/)
- [Fortiche](https://github.com/cloudflare/fortiche)
- [raylib-fortran-wasm](https://github.com/michaelfiber/hello-raylib-wasm)
- [hello-raylib-wasm](https://github.com/michaelfiber/hello-raylib-wasm)
---

## GNU AFFERO GENERAL PUBLIC LICENSE

    This file is part of Entity Editor - EE.

    Entity Editor - EE is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    any later version.

    Entity Editor - EE is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with Entity Editor - EE. If not, see <http://www.gnu.org/licenses/>.

    Author: Carlonem <carlonem.dev@gmail.com>

</div>