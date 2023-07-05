#!/usr/bin/env python3

import sys
# caution: path[0] is reserved for script path (or '' in REPL)
sys.path.insert(1, '../myy505Utils')

from myy505TesterLib import *

newLabels = {
    "maria"    : '.string "Maria"',
    "markos"   : '.string "Markos"',
    "marios"   : '.string "Marios"',
    "marianna" : '.string "Marianna"',
    "Mahsa"    : '.string "Mahsa"',
    "empty"    : '.string ""',
    "Karim"    : '.string "Karim"',
    "Naveen"   : '.string "Naveen"',

    "arraySorted"  : '.word maria, marianna, marios, markos',
    "arraySOdd"    : '.word maria, marianna, marios, markos, Naveen',
    "arrayS1"      : '.word Mahsa',          
    "arrayNLast"   : '.word maria, marianna, marios, markos, Karim',
    "arraySEmpty"  : '.word empty, Mahsa, Naveen', # sorted
    "arrayNEmpty"  : '.word empty, Mahsa, Karim',  # not sorted
    "arrayNreverse": '.word Naveen, maria, Mahsa',  # not sorted
}


def simAndCheck(a0, a1, sub, expectedReturn, message):
    # rough number of expected assembly instructions, to catch infinite loops
    maxSteps = 1000

    # The main code to run. Circumvents the initial code of the original program
    #  The jal instruction will be explained later in the course.
    newMainCode  = '\tla   a0, %s \n' %a0
    if sub == "str_ge":
        newMainCode += '\tla   a1, %s \n' %a1
    else:
        newMainCode += '\tli   a1, %s \n' %a1
    newMainCode += '\tjal  ra, %s \n' %sub

    expected = [ ('r',  'a0', 'v', str(expectedReturn), message) ]

    filename = 'lab04.s'
    (labelMap, coreDumpData, returncode, errors, simout, regCheck) = runSim(filename, newLabels, newMainCode, simSteps=maxSteps, lab1Hack=False)
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
    results = checkSimResults(expected, coreDumpData, labelMap)
    if results:
        for line in checkSimResults(expected, coreDumpData, labelMap):
            print(line)
        return True
    else:
        return False

tests= [
('maria',    'marios', 'str_ge', 0, "str_ge(maria, marios)"),
('marianna', 'maria',  'str_ge', 1, "str_ge(marianna, maria)"),
('empty',    'empty',  'str_ge', 1, 'str_ge("", "")'),
('maria',    'empty',  'str_ge', 1, 'str_ge(maria, "")'),
('arraySorted', '4',  'recCheck', 1, 'recCheck(arraySorted, 4)'),
('arraySOdd',   '5',  'recCheck', 1, 'recCheck(arraySOdd, 5)'),
('arrayS1',     '1',  'recCheck', 1, 'recCheck(arrayS1, 1)'),
('arrayNLast',  '5',  'recCheck', 0, 'recCheck(arrayNLast, 5)'),
('arrayNLast',  '4',  'recCheck', 1, 'recCheck(arrayNLast, **4**)'),
('arraySEmpty', '3',  'recCheck', 1, 'recCheck(arraySEmpty, 3)'),
('arrayNEmpty', '3',  'recCheck', 0, 'recCheck(arrayNEmpty, 3)'),
('arrayNreverse', '3','recCheck', 0, 'recCheck(arrayNreverse, 3)'),
]
faults = False
for (a0, a1, sub, expVal, msg) in tests:
    # Note the "or" below stops running at first fault!
    try:
        faults = faults or simAndCheck(a0, a1, sub, expVal, msg)
    except Exception as e:
        #print("Exception: " + str(e))
        faults = True

if not faults:
    print("All tests pass")
