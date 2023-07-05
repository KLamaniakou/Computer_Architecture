#!/usr/bin/env python3

import sys
# caution: path[0] is reserved for script path (or '' in REPL)
sys.path.insert(1, '../myy505Utils')

from myy505TesterLib import *

################################################################
# CHANGE THIS TO YOUR MATRIC NUMBER
################################################################
matricNumber = 5110

# Modifications/additions to the data labels of the program
newLabels = {
    "matric" : '.word '+ str(matricNumber)
}

# The main code to run. Circumvents the initial code of the original program
#  The jal instruction will be explained later in the course.
newMainCode = '''
        la   a0, matric     # a0 gets the **address** of matric
        la   a1, var1       # a1 gets address of var1
        la   a2, array      # get address of array into a2
        la   a3, var2       # Get address of var2`
        jal  ra, prog       # Jump-and-link to the 'prog' label
'''


expected = [
    # List of quintuples, of strings. Describes what to check and what is the expected value.
    # Contents of the quintaple:
    # - type of simulation object to read:
    #     r - Risc-V register
    #     [s|u][b|h|w] - signed/unsigned byte/half-word/word read from memory
    # - register name or register number (string), or address expression (which may contain label names)
    # - type of expected value:
    #     v - value, number
    #     s - string
    #    when string, the read simulation object must be memory only
    # - expected value. Can be an expression containing labels, or a string
    # - Message to display when the simulation does not match the expected value. The simulation and expected values are appended to the message automatically
    ('r',  'a0',      'v', 'matric', 'a0 should be the address of matric.'),
    ('r',  'a1',      'v', 'var1',   'a1 should be the address of var1.'),
    ('r',  'a2',      'v', 'array',  'a2 should be the address of array.'),
    ('r',  'a3',      'v', 'var2',   'a3 should be the address of var2.'),
    ('r',  's0',      'v', str(matricNumber),   's0 should be equal to your matric number.'),
    ('r',  's1',      'v', str(matricNumber+1), 's1 should be equal to your matric number + 1.'),
    ('r',  's2',      'v', '-1',     's2 should be -1.'),
    ('r',  's3',      'v', '255',    's3 should be 0xff.'),
    ('r',  't1',      'v', 'array+0x10', 't1 should be &array[4].'),
    ('uw', 'matric',  'v', str(matricNumber), 'matric should not be modified.'),
    ('uw', 'matric+4','v', str(matricNumber+1), 'matricplus1 should be matric + 1 (in memory).'),
    ('uw', 'var1',    'v', 'array+0x10', 'var1 should be &array[4] (in memory).'),
    ('ub', 'str1',    's', 'This is a string', 'str1 should not be modified.')
]

# Cannot compare arrays directly. Add a quintuple for each array element
for i in range(0,10):
    if i == 3:
       val = matricNumber
    else:
       val = 10-i
    expected.append(('uw', 'array+'+str(i*4), 'v', str(val), 'Unexpected value in array['+str(i)+'].'))

filename = 'lab01.s'
(labelMap, coreDumpData, returncode, errors, simout, regCheck) = runSim(filename, newLabels, newMainCode, savedRegs={}, simSteps=200, lab1Hack=True)
#print("Simulation returned %d" %(returncode))   # Print the simulator exit code. 0 should mean OK
#print("Stderr:") # The simulator standard error
#for line in errors:
#    print(line)
#print("stdout:") # The simulator standard output
#for line in simout:
#    print(line)
#print("Saved regs unexpected results:") # savedRegs={} here, so there is nothing to see.
#for line in regCheck:
#    print(line)
#print("Data labels:")  # The address (hex, decimal) for each data label
#for label in labelMap.keys():
#    print("%s 0x%x (%d)" %(label, labelMap[label], labelMap[label]))
#print("Integer registers at program exit") 
#for reg in coreDumpData['registers']['integer'].keys():
#    print("x%2s 0x%x (%d)" %(reg, coreDumpData['registers']['integer'][reg], coreDumpData['registers']['integer'][reg]))

# Check the expected results and print any differences
for line in checkSimResults(expected, coreDumpData, labelMap):
    print(line)
