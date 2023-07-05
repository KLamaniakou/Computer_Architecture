# Introduction to Risc-V assembly programming using Ripes (https://github.com/mortbopet/Ripes)
# for MYY505 - Computer Architecture
# Aris Efthymiou
# Department of Computer Engineering, University of Ioannina

# These are comments! Anything up to the end of line is ignored

        .data     # An assembler **directive**. What follows is data 
                  #  so it is stored in the data memory section (0x10000000)

matric: # Words ending with ':' are **labels**
        # The common convention is to write labels starting from the leftmost column.
        # Try to keep label names short
        .word 5110  # This directive reserves enough space for a word in memory.
                  #  and initializes it with the specific value.
matricplus1:
        .word 0   

var1:
        .word 1

array:
        .word 10, 9, 8, 7, 6, 5, 4, 3, 2, 1 # Array of 10 words
                  # A comma-separated list of numbers can be used after .word
                  # and similar directives. 
                  # See the memory tab in Ripes to see how they are stored

var2:
        .byte -1

str1:
        .string "This is a string" # The end of the string is marked by a
                  # 0 - valued byte, which is represented as '\0'. 
                  # Null-terminated string is the usual term for this.
                  # See how it looks in the memory tab of Ripes
        
        .text     # Another assembler direcrive. what follows is code
                  #  so it is stored in the text memory section (0x00000000)
     
        
        # Instructions are indented a few spaces to the right
        #   (so that we can see the labels more clearly)
        # Instruction operands are indented a few spaces, so that the
        #    instruction type is more visible.
      
        la         a0, matric      # a0 gets the **address** of matric
                                   # Note: this is address **not** value of matric
        la         a1, var1        # a1 gets address of var1
        la         a2, array       # get address of array into a2
                                   # This is called the **base** of the array
        la         a3, var2        # Get address of var2

prog:   # Labels in code are used for control flow: if/then/else, loops, etc.
        #  In this case the label is required for the course's automated
        #  test.
        # Labels do not take up space in memory. They are only used by the assembler

        lw         s0, 0(a0)     # s0 gets the value of matric.a0 has the address of matric
        
        lw         s1, 0(a1)       # s1 gets the value of var1. a1 has the address of var1
        add        s1, s1,   s0    # s1 = var1 + s0
        sw         s1, 4(a0)       # matricplus1 = var1 + s0
        
        sw         s0, 0xc(a2)     # Store s0 to the 4th element of array
                                   # Note the use of offset (0xc = 12 = 3*4)
                                   # addresses of array elements (32bit words each):
                                   # array[0]  - array + 0
                                   # array[1]  - array + 4
                                   # array[2]  - array + 8
                                   # array[3]  - array + 12
                                     
        addi       t1, a2,   0x10  # Note: address arithmetic.
                                   #  Calculates address of 5th element of array
        sw         t1, 0(a1)       # var1 = address of 5th element of array 
                                   # Note: we can store addresses 
                                   #   in memory just like we do with real data!
        
        lb         s2, 0(a3)       # Get value of var2, sign-extended to 32 bits, to s2
        lbu        s3, 0(a3)       # Get value of var2, zero-extended to 32 bits, to s3
        
exit: 
        addi       a7, zero, 10   # system service 10 is exit 
        ecall                     # we are outa here.
        
###############################################################################

