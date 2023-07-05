
## UoI-CSE-MYY505 lab02

## KONSTANTINOS-DIONUSIOS LAMANIAKOU

**TODO - Update your name in this readme. Leave 1 space after the ## to preserve the text formating (markdown)**



## Problem statement:
Given an array of 32-bit words (address in a0, size, number of elements, in a1) and a search value (in a2), find (and store in s0) the *address* of the *last* occurence of the search value in the array, or 0 (null ptr), if not found. The array size (a1) may be 0. Your code should handle that and respond with a 0 in s0, meaning "not found".

Important:
* You must provide the memory *address* of the array element, not the index!
E.g. if the array contains 1,0,1,12,0,1,4 a2=1 and a0 = 0x10000000, at the end of execution s0 should be 0x10000014, not 5!
* If there are multple matches, the address of the *last* array element is what is expected.
E.g. if the array contains 1,0,1,12,0,1,4 a2=1, and a0 = 0x10000000, at the end of execution s0 should be 0x10000014 (index 5), not 0x10000000 (index 0), nor 0x10000008 (index 2).

Automated testing in Lab02Test.py using python myy505Utils functions
 
## Files to work on
* `lab02.s` 
* `Lab02Test.py` 
* `README.md` to add your name<br/>
Please **DO NOT MODIFY** any other files. 
      
## Running 
* To run the program interactively, start Ripes and load lab02.s
* To run the test execute the python script Lab02Test.py


## Notes
* Make sure your solution assembles and runs. **There are no points for code that doesn't assemble**.
* Make sure your last push is before the deadline. Your last push will be considered as your final submission.
* If you need a deadline extension for any reason, use the [provided form.](https://forms.gle/zH4BnL5TvYBdvMYK9)
* Post questions on [Edstem!](https://edstem.org/us/courses/28701/discussion/).
