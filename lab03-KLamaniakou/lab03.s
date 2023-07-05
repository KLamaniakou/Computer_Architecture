# Conversion of RGB888 image to RGB565
# lab03 of MYY505 - Computer Architecture
# Department of Computer Engineering, University of Ioannina
# Aris Efthymiou

# This directive declares subroutines. Do not remove it!
.globl rgb888_to_rgb565, showImage

.data

image888:  # A rainbow-like image Red->Green->Blue->Red
    .byte 255, 0,     0
    .byte 255,  85,   0
    .byte 255, 170,   0
    .byte 255, 255,   0
    .byte 170, 255,   0
    .byte  85, 255,   0
    .byte   0, 255,   0
    .byte   0, 255,  85
    .byte   0, 255, 170
    .byte   0, 255, 255
    .byte   0, 170, 255
    .byte   0,  85, 255
    .byte   0,   0, 255
    .byte  85,   0, 255
    .byte 170,   0, 255
    .byte 255,   0, 255
    .byte 255,   0, 170
    .byte 255,   0,  85
    .byte 255,   0,   0
# repeat the above 5 times
    .byte 255, 0,     0, 255,  85,   0 255, 170,   0, 255, 255,   0, 170, 255,   0, 85, 255,   0, 0, 255,   0, 0, 255,  85, 0, 255, 170, 0, 255, 255, 0, 170, 255, 0,  85, 255, 0,   0, 255, 85,   0, 255, 170,   0, 255, 255,   0, 255, 255,   0, 170, 255,   0,  85, 255,   0,   0
    .byte 255, 0,     0, 255,  85,   0 255, 170,   0, 255, 255,   0, 170, 255,   0, 85, 255,   0, 0, 255,   0, 0, 255,  85, 0, 255, 170, 0, 255, 255, 0, 170, 255, 0,  85, 255, 0,   0, 255, 85,   0, 255, 170,   0, 255, 255,   0, 255, 255,   0, 170, 255,   0,  85, 255,   0,   0
    .byte 255, 0,     0, 255,  85,   0 255, 170,   0, 255, 255,   0, 170, 255,   0, 85, 255,   0, 0, 255,   0, 0, 255,  85, 0, 255, 170, 0, 255, 255, 0, 170, 255, 0,  85, 255, 0,   0, 255, 85,   0, 255, 170,   0, 255, 255,   0, 255, 255,   0, 170, 255,   0,  85, 255,   0,   0
    .byte 255, 0,     0, 255,  85,   0 255, 170,   0, 255, 255,   0, 170, 255,   0, 85, 255,   0, 0, 255,   0, 0, 255,  85, 0, 255, 170, 0, 255, 255, 0, 170, 255, 0,  85, 255, 0,   0, 255, 85,   0, 255, 170,   0, 255, 255,   0, 255, 255,   0, 170, 255,   0,  85, 255,   0,   0
    .byte 255, 0,     0, 255,  85,   0 255, 170,   0, 255, 255,   0, 170, 255,   0, 85, 255,   0, 0, 255,   0, 0, 255,  85, 0, 255, 170, 0, 255, 255, 0, 170, 255, 0,  85, 255, 0,   0, 255, 85,   0, 255, 170,   0, 255, 255,   0, 255, 255,   0, 170, 255,   0,  85, 255,   0,   0

image565:
    .zero 512  # leave a 0.5Kibyte free space

.text
# -------- This is just for fun.
# Ripes has a LED matrix in I/O tab. To enable it:
# - Go to the I/O tab and double click on LED Matrix.
# - Change the Height and Width (at top-right part of I/O window),
#     to the size of the image888 (6, 19 in this example)
# - This will enable the LED matrix
# - Uncomment the following and you should see the image on the LED matrix!
#    la   a0, image888
#    li   a1, LED_MATRIX_0_BASE
#    li   a2, LED_MATRIX_0_WIDTH
#    li   a3, LED_MATRIX_0_HEIGHT
#    jal  zero, showImage
# ----- This is where the fun part ends!

    la   a0, image888
    la   a3, image565
    li   a1, 19 # width
    li   a2,  6 # height
    jal  ra, rgb888_to_rgb565

    addi a7, zero, 10 
    ecall

# ----------------------------------------
# Subroutine showImage
# a0 - image to display on Ripes' LED matrix
# a1 - Base address of LED matrix
# a2 - Width of the image and the LED matrix
# a3 - Height of the image and the LED matrix
# Caution: Assumes the image and LED matrix have the
# same dimensions!
showImage:
    mul  a4, a2,   a3 # size of the image in pixels (width * height)
loopShowImage:
    beq  a4, zero, returnShowImage
    lbu  t0, 0(a0) # get red
    lbu  t1, 1(a0) # get green
    lbu  t2, 2(a0) # get blue
    slli t0, t0,   16  # place red at the 3rd byte of "led" word
    slli t1, t1,   8   #   green at the 2nd
    or   t2, t2,   t1  # combine green, blue
    or   t2, t2,   t0  # Add red to the above
    sw   t2, 0(a1)     # let there be light at this pixel
    addi a0, a0,   3   # move on to the next image pixel
    addi a1, a1,   4   # move on to the next LED
    addi a4, a4,   -1  # decrement pixel counter
    j    loopShowImage
returnShowImage:
    jalr zero, ra, 0
# ----------------------------------------

rgb888_to_rgb565:
# ----------------------------------------
# Write your code here.
# You may move the "return" instruction (jalr zero, ra, 0).
    mul a4,a2,a1
    loop:
        beq a4,zero,exit
        lbu  t2, 0(a0) # get red
        lbu  t3, 1(a0) # get green
        lbu  t4, 2(a0) # get blue
        andi t2,t2,248 #mask to take the bits we want
        andi t3,t3,252 #mask to take the bits we want
        andi t4,t4,248 #mask to take the bits we want
        add t5,t3,zero #use a temporary variable before make changes for the green
        andi t5,t5,28 # mask to take the bits we want
        slli t5,t5,3 #slide left 3 to make the combine
        srli t4,t4,3 # slide right 3 to compine with t5
        or t6,t5,t4 #combine between t5 t4 (green blue)
        sb t6,0(a3) #store the after combination to a3
        srli t3,t3,5 #take the first green and slide 5
        or t6,t2,t3 #combine between t2 t3 (red blue)
        sb t6,1(a3) #store the after combination to a3
        addi a4,a4,-1 #decrease width counter
        addi a3,a3,2 #increse a3 
        addi a0, a0,3  # move on to the next image pixel
        j loop # jump to loop
    exit:
        jalr zero, ra, 0


