
.data

array: .word 1, 0, 1, 12, 0, 1, 4

.text

    la a0, array 
    li a1, 7   
    li a2, 1
prog:
#-----------------------------
# Write your code here!
    add t0,zero,zero #t0 is counter to check if we have run through the entire list
    add t1,zero,zero #t1 to help as take the elements 
    add s0,zero,zero #s0 to save the last address
    loop:
        beq t0,a1,done # check if t0 is equal to a1 ,if he has gone through the whole list go to done
        # t1 = a0+4*i
        slli t1,t0,2 
        add t1,t1,a0 
        lw t2,0(t1) #load first element of t1 to t2
        addi t0,t0,1 #increase t0(counter) by 1
        beq t2,a2,exit_found #check if t2 is equal to a2,go to label exit_found
        j loop #jump to label loop
    exit_found:
        add s0,t1,zero # add result to s0
        bne t0,a1,loop # if t0 is not equal to a1 go to label loop(if the list is not finished)
# Do not remove the prog label or write code above it!
#-----------------------------
done:
    addi a7, zero, 10 
    ecall
