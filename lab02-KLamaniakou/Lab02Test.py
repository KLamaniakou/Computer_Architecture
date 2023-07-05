#!/usr/bin/env python3

import sys
# caution: path[0] is reserved for script path (or '' in REPL)
sys.path.insert(1, '../myy505Utils')

from myy505TesterLib import *

def offsetOfLast(li, number):
    # reverse the list (li[::-1]) and find the 1st index of "number"
    #  then calculate actual index and multiply by 4 to get offset
    # source: https://stackoverflow.com/questions/6890170/how-to-find-the-last-occurrence-of-an-item-in-a-python-list
    return (len(li) - 1 - li[::-1].index(number))*4

def simAndCheck(strList, searchVal):
    # convert stingList to a python list
    arrayList = eval('[' + strList +']')
    arraySize = len(arrayList)
    # rough number of expected assembly instructions, to catch infinite loops
    maxSteps = arraySize * 50 + 100

    # Note: venus allows empty .word directives, so this works with empty strList!
    newLabels = {
        "array" : '.word ' + strList
    }

    # The main code to run. Circumvents the initial code of the original program
    #  The jal instruction will be explained later in the course.
    newMainCode  = '\tla   a0, array \n'
    newMainCode += '\tli   a1, ' + str(arraySize) + '\n'
    newMainCode += '\tli   a2, ' + str(searchVal) + '\n'
    newMainCode += '\tjal  ra, prog\n'

    if arraySize > 0 and (searchVal in arrayList):
        # get expected offset from start of array
        expectedOffset = offsetOfLast(arrayList, searchVal)
        expected = [
            ('r',  's0', 'v', 'array + '+str(expectedOffset), 's0 should be the address of array + an offset of '+str(expectedOffset)+'.'),
        ]
    else:
        expected = [
            ('r',  's0', 'v', '0', 's0 should be 0 (not found or empty array).'),
        ]

    # Check for modifications to array
    for i in range(0, arraySize):
        val = arrayList[i]
        if val < 0:
          expType = 'sw'
        else:
          expType = 'uw'
        expected.append((expType, 'array+'+str(i*4), 'v', str(val), 'Unexpected value in array['+str(i)+'].'))

    filename = 'lab02.s'
    (labelMap, coreDumpData, returncode, errors, simout, regCheck) = runSim(filename, newLabels, newMainCode, randRegs=['s0'], savedRegs={}, simSteps=maxSteps, lab1Hack=True)
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

tests = [
('',              0, "Empty array, nothing can match"),
('1',             1, "Single matching element"),
('1',             2, "Single non-matching element"),
('11, 11, 1',     1, "Match last element"),
('10, 2, -5',    10, "Match first element"),
('1, -1, 11',    -1, "Match a negative number"),
('10, 2, 20',    30, "No match"),
('10, 2, 10, 4', 10, "Double match test"),
('2, 2, 10, 2',   2, "Tripple match test"),
]
for (strList, searchVal, testName) in tests:
    print("--- Errors in test "+testName+' ---')
    try:
        simAndCheck(strList, searchVal)
    except:
        print("skipped")
