
## UoI-CSE-MYY505 lab04

## KONSTANTINOS_DIONISIOS LAMANIAKOU

**TODO - Update your name in this readme. Leave 1 space after the ## to preserve the text formating (markdown)**



## Problem statement:

Write two Risc-V subroutines:
 * str\_ge - compares two strings (addresses in a0, a1) and returns 1 (in a0) if the string in a0 is "greater or equal" the one in a1; otherwise returns 0. Greater or equal is in lexicographic order.

 * recCheck - Checks if an array of strings (i.e. array of addresses to strings) is lexicographically sorted. Returns 1 if it is, 0 if it is not. This subroutine must be recursive and call str\_ge. The inputs are the address of the array (a0) and the size of the array (a1)
 
## Files to work on
* `lab04.s` 
* `README.md` to add your name
      
## Running 
* To run the program interactively, start Ripes and load lab04.s
* To run the test execute the python script Lab04Test.py


## Notes
* Make sure your solution assembles and runs. **There are no points for code that doesn't assemble**.
* Make sure your last push is before the deadline. Your last push will be considered as your final submission.
* If you need a deadline extension for any reason, use the [provided form.](https://forms.gle/zH4BnL5TvYBdvMYK9)
* Post questions on [Edstem!](https://edstem.org/us/courses/28701/discussion/).
