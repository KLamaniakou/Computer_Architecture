.data			

data: .word 1			

.text			

     la 	x10	data	

     li 	x11	0	

     li 	x9	-1	

loop:			

l1:  lw 	x5	0(x10)	

l2:  add	x5	x5	x5

l3:  beq	x5	x9	found

l4:  addi	x10	x10	4

l5:  sw 	x5	-4(x10)	

l6:  bne	x10	x11	loop

found:			

l7:  add	x10	x0	x0

out:			

l8:  addi	x17	x0	10

l9:  ecall