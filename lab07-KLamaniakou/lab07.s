# lab07.s - move a "ball" in the LED matrix using the D-pad. 
#  The ball is normally white and turns red when it reaches the edge of the matrix.
# To run this program, make sure that you have instantiated a "D-pad"
# and a "LED Matrix" peripheral in the "I/O" tab.

.data
# Any memory-based data are held here

.text
# Code segment
li s0,LED_MATRIX_0_BASE  #first dot of led matrix
add t4,zero,zero   #counter for allblack
li s1,LED_MATRIX_0_SIZE   #size of led matrix
allblack:
    beq t4,s1,main  #check if the led matrix has end
    li a1,0x000000  #color black
    sw a1,0(s0)   #get the dot black
    addi t4,t4,4  #counter++
    addi s0,s0,4  #matrix base++
    j allblack
main:
    li s0,LED_MATRIX_0_BASE  #first dot of led matrix
    la s1,LED_MATRIX_0_SIZE  #size of led matrix
    addi t0,zero,10   #the position of first dot for right/left counter
    addi t1,zero,20    #end right
    addi t2,zero,1     #end left
    addi t3,zero,10    #the position of first dot for up/down counter
    addi t4,zero,19    #end up
    addi t5,zero,0     #end down
    addi s0,s0,0x2f4  #set the first dot
    li a1,0x000000 #black
    li a0,0xFFFFFF #white
    li a2,0xff0000 #red
    sw a0,0(s0)  #set the first dot white
loop:
    addi t6,zero,1  #endless loop
    lw s3,D_PAD_0_RIGHT
    lw s4,D_PAD_0_LEFT
    lw s5,D_PAD_0_UP
    lw s6,D_PAD_0_DOWN
    beq s3,t6,right  #check if right is 1
    beq s4,t6,left   #check if left is 1
    beq s5,t6,up     #check if up is 1
    beq s6,t6,down   #check if down is 1
    j loop
up:
    addi t3,t3,1
    bgt t3,t4,endup  #end of led matrix up
    sw a1,0(s0)   
    addi s0,s0,-80
    beq t3,t4,upred  #the last dot get red
    beq t0,t1,upred  #the last dot right and up get red
    beq t0,t2,upred  #the last dot left and up get red
    sw a0,0(s0)
    j checkup   #check if up is zero
down:
    addi t3,t3,-1
    blt t3,t5,enddown  #end of led matrix down
    sw a1,0(s0)   
    addi s0,s0,80
    beq t0,t1,downred   #the last dot right and down get red
    beq t3,t5,downred  #the last dot get red
    beq t0,t2,downred   #the last dot left and dwon get red
    sw a0,0(s0)
    j checkdown
right:
    addi t0,t0,1
    bgt t0,t1,endright  #end of led matrix right
    sw a1,0(s0)   
    addi s0,s0,4
    beq t3,t4,rred  #the last dot right and up get red
    beq t0,t1,rred  #the last dot get red
    beq t3,t5,rred  #the last dot right and down get red
    sw a0,0(s0)
    j checkright
left:
    addi t0,t0,-1
    blt t0,t2,endleft  #end of led matrix left
    sw a1,0(s0)
    addi s0,s0,-4
    beq t3,t4,lred #the last dot left and up get red
    beq t0,t2,lred #the last dot get red
    beq t3,t5,lred #the last dot left and down get red
    sw a0,0(s0)
    j checkleft
rred:
    sw a2,0(s0) #right red 
    j checkright
lred:
    sw a2,0(s0) #left red
    j checkleft
upred:
    sw a2,0(s0) #up red
    j checkup
downred:
    sw a2,0(s0) #down red
    j checkdown
endright:
    addi t6,zero,1  #end of right ask only up/down/left
    lw s5,D_PAD_0_UP
    lw s6,D_PAD_0_DOWN
    lw s4,D_PAD_0_LEFT
    beq s4,t6,left
    beq s5,t6,up
    beq s6,t6,down
    j endright
endleft:
    addi t6,zero,1  #end of left ask only up/down/right 
    lw s5,D_PAD_0_UP
    lw s6,D_PAD_0_DOWN
    lw s3,D_PAD_0_RIGHT
    beq s3,t6,right
    beq s5,t6,up
    beq s6,t6,down
    j endleft
endup:
    addi t6,zero,1  #end of up ask only left/right/down
    lw s6,D_PAD_0_DOWN
    lw s4,D_PAD_0_LEFT
    lw s3,D_PAD_0_RIGHT
    beq s3,t6,right
    beq s4,t6,left
    beq s6,t6,down
    j endup
enddown:
    addi t6,zero,1 #end of down ask only left/right/up
    lw s4,D_PAD_0_LEFT
    lw s5,D_PAD_0_UP
    lw s3,D_PAD_0_RIGHT
    beq s3,t6,right
    beq s4,t6,left
    beq s5,t6,up
    j enddown  
checkup:
    addi t6,zero,1
    lw s5,D_PAD_0_UP #check if up is 0 
    beq s5,zero,loop # then go to loop and check if its 1 again
    lw s6,D_PAD_0_DOWN  #is its not 0 ask others
    lw s4,D_PAD_0_LEFT
    lw s3,D_PAD_0_RIGHT
    beq s3,t6,right  #ask if right/left/down is 1
    beq s4,t6,left
    beq s6,t6,down
    j checkup  #the only way to get out is if up gets 0 or others get 1
checkdown:
    addi t6,zero,1
    lw s6,D_PAD_0_DOWN #check if down is 0
    beq s6,zero,loop # then go to loop and check if its 1 again
    lw s5,D_PAD_0_UP
    lw s4,D_PAD_0_LEFT #is its not 0 ask others
    lw s3,D_PAD_0_RIGHT
    beq s3,t6,right #ask if right/left/down is 1
    beq s4,t6,left
    beq s5,t6,up
    j checkdown #the only way to get out is if down gets 0 or others get 1
checkleft:
    addi t6,zero,1
    lw s4,D_PAD_0_LEFT #check if left is 0
    beq s4,zero,loop # then go to loop and check if its 1 again
    lw s6,D_PAD_0_DOWN
    lw s5,D_PAD_0_UP #is its not 0 ask others
    lw s3,D_PAD_0_RIGHT
    beq s3,t6,right #ask if right/left/down is 1
    beq s5,t6,up
    beq s6,t6,down
    j checkleft #the only way to get out is if left gets 0 or others get 1
checkright:
    addi t6,zero,1
    lw s3,D_PAD_0_RIGHT #check if right is 0
    beq s3,zero,loop # then go to loop and check if its 1 again
    lw s5,D_PAD_0_UP
    lw s4,D_PAD_0_LEFT #is its not 0 ask others
    lw s6,D_PAD_0_DOWN
    beq s6,t6,right #ask if right/left/down is 1
    beq s4,t6,left
    beq s5,t6,up
    j checkright #the only way to get out is if right gets 0 or others get 1