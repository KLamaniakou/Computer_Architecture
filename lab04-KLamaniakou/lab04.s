
.globl str_ge, recCheck

.data

maria:    .string "Maria"
markos:   .string "Markos"
marios:   .string "Marios"
marianna: .string "Marianna"
.align 4  # make sure the string arrays are aligned to words (easier to see in ripes memory view)

# These are string arrays
# The labels below are replaced by the respective addresses
arraySorted:    .word maria, marianna, marios, markos
arrayNotSorted: .word marianna, markos, maria


.text

            la   a0, arrayNotSorted
            li   a1,4
            jal  recCheck

            li   a7, 10
            ecall
            

str_ge: 
#---------
# Write the subroutine code here
#  You may move jr ra   if you wish.
#---------  
add t0,zero,zero
add t1,zero,zero
loop:
    lb t0,0(a0)  #load the first char
    lb t1,0(a1)  #load the second char
    blt t0,t1,ze  #if t0 is less than t1 return 0
    bne t0,t1,one  # if its not equal t0 with t1 return 1
    beq  t0,zero,out    #end of char 
    beq  t1,zero,out   #end of char
    addi a1,a1,1    #move on to the next character 
    addi a0,a0,1    #move on to the next character
    j loop

out: 
    beq t0,t1,one    #if its equal go to one
    j ze              #else go to ze  
ze:
    add a0,zero,zero #return 0
    jr ra  
one:
    addi a0,zero,1 #return 1
    jr ra
 
#----------------------------------------------------------------------------
# recCheck(array, size)
# if size == 0 or size == 1
#     return 1
# if str_ge(array[1], array[0])      # if first two items in ascending order,
#     return recCheck(&(array[1]), size-1)  # check from 2nd element onwards
# else
#     return 0
#---------
# Write the subroutine code here
#  You may move jr ra   if you wish.
#---------
   
recCheck:
    addi sp, sp, -12
	sw   ra, 8(sp)
	sw   a1, 4(sp)       #store a1(size)
	sw   a0, 0(sp)       #store a0(array address)
    addi t3,zero,2
    blt a1,t3,return     #if size = 0 or size = 1  
    lw t0,0(a0)           #first element
    lw t1,4(a0)           #second element
    add a1,zero,t0       #load to a1
    add a0,zero,t1       #load to a0
    jal str_ge            
    beq a0,zero,zer    #if a0 is zero go to zero
    lw a1,4(sp)       #load the size
    addi a1, a1, -1     # size -1
    lw a0,0(sp)         #load the a0 address of the array
    addi a0,a0,4        #move a0 to take the next element
    jal recCheck
    lw ra ,8(sp)
    addi sp,sp,12
    jr ra
    
zer:
    add a0,zero,zero  
    lw ra, 8(sp)        
    addi sp,sp,12 
    jr ra       #return 0
    
return:
    addi a0,zero,1 
    lw ra ,8(sp)
    addi sp,sp,12
    jr   ra   #return 1
