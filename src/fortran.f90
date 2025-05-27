module my_module
    use iso_c_binding
    implicit none
    integer(c_int), parameter :: a = 0, b = 9000000
    integer(c_int) :: c = 123

contains
    ! Iterative function that performs a basic calculation
    ! @return Returns the result of (i - b + c) after iterating from a to b
    function func()
        implicit none
        integer(c_int) :: i , func

        ! Iterate through the range [a, b]
        do i = a, b
            func = i - b + c 
        end do

    end function func

    ! Function to process an input integer value
    ! Must be bound to C for the C wrapper using bind(C, name="get_fixed_integer")
    ! @param[in] num Input integer to be processed
    ! @return Returns the input number multiplied by func() result
    function get_fixed_integer(num) bind(C, name="get_fixed_integer") result(fixed_val)
        use iso_c_binding
        implicit none
        integer(c_int), value :: num  ! Input parameter
        integer(c_int) :: fixed_val

        ! Multiply input number by the result of func()
        fixed_val = num * func()
        write(*,*) ' Done', a, b, c

    end function get_fixed_integer

end module my_module

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
        integer, parameter :: n = 10
        integer :: numbers(1:n,1:n) = 0, io_unit = 13, i, j, io_status
        
        ! Attempt to read the file
        write(*,*) "Attempt to read the file"
        open(unit=io_unit, file='/data/file.txt', status='old', iostat=io_status)
        if (io_status /= 0) then
            write(*,*) 'Error opening file /data/file.txt, status:', io_status
            return
        end if
        write(*,*) 'File opened successfully'
        
        do i = 1, n
            read(io_unit,*) (numbers(i,j), j=1,n)
            write(*,*) (numbers(i,j), j=1,n)
        end do
        close(io_unit)
        
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
