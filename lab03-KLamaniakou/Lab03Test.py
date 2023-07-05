#!/usr/bin/env python3

import sys
# caution: path[0] is reserved for script path (or '' in REPL)
sys.path.insert(1, '../myy505Utils')

from myy505TesterLib import *

newLabels = {
    "image565"    : '.space 512',  # replace so Venus does not break
    "emptyImage"  : '.byte 0',
    "onePixelImg" : '.byte 0x55, 0xaa, 0xab',
    "oneRowImg"   : '.byte 0x55, 0xaa, 0xab, 0x00, 0x65, 0xba, 0xcd, 0xbe, 0xef',
    "oneColImg"   : '.byte 0xde, 0xad, 0xca, 0xff, 0xee, 0xba, 0xda, 0x55, 0x00',
    "outEmpty"    : '.space 16',  # This is for venus. For ripes use .zero in place of .space!
    "outOne"      : '.space 16',  # This is for venus. For ripes use .zero in place of .space!
    "outRow"      : '.space 16',  # This is for venus. For ripes use .zero in place of .space!
    "outCol"      : '.space 16',  # This is for venus. For ripes use .zero in place of .space!
}

# Original test
newMainCode  = '\tla   a0, image888\n'
newMainCode += '\tla   a3, image565\n'
newMainCode += '\tli   a1, 19\n'
newMainCode += '\tli   a2, 6\n'
newMainCode += '\tjal  ra, rgb888_to_rgb565\n'
# empty Image
newMainCode += '\tla   a0, emptyImage\n'
newMainCode += '\tla   a3, outEmpty\n'
newMainCode += '\tli   a1, 0\n'
newMainCode += '\tli   a2, 0\n'
newMainCode += '\tjal  ra, rgb888_to_rgb565\n'
# One pixel image
newMainCode += '\tla   a0, onePixelImg\n'
newMainCode += '\tla   a3, outOne\n'
newMainCode += '\tli   a1, 1\n'
newMainCode += '\tli   a2, 1\n'
newMainCode += '\tjal  ra, rgb888_to_rgb565\n'
# One row
newMainCode += '\tla   a0, oneRowImg\n'
newMainCode += '\tla   a3, outRow\n'
newMainCode += '\tli   a1, 3\n'
newMainCode += '\tli   a2, 1\n'
newMainCode += '\tjal  ra, rgb888_to_rgb565\n'
# One column
newMainCode += '\tla   a0, oneColImg\n'
newMainCode += '\tla   a3, outCol\n'
newMainCode += '\tli   a1, 1\n'
newMainCode += '\tli   a2, 3\n'
newMainCode += '\tjal  ra, rgb888_to_rgb565\n'
 
# Check the output for the original test
rainbowList = [0, 248, 160, 250, 64, 253, 224, 255, 224, 175, 224, 87, 224, 7, 234, 7, 245, 7, 255, 7, 95, 5, 191, 2, 31, 0, 31, 80, 31, 168, 31, 248, 21, 248, 10, 248, 0, 248]
expected = []
for row in range(0, 6):
    for i in range(0, len(rainbowList)):
        val = rainbowList[i]
        expected.append(('ub', 'image565+'+str(row*len(rainbowList)+i), 'v', str(val), 'Unexpected value in image565['+str(row*len(rainbowList)+i)+'].'))

# 0x55, 0x55
expected.append(('ub', 'outOne',   'v', str(0x55), 'Unexpected value in outOne[0].'))
expected.append(('ub', 'outOne+1', 'v', str(0x55), 'Unexpected value in outOne[1].'))

#0x55, 0x55, 0x03, 0x37, 0xcd, 0xfd
expected.append(('ub', 'outRow',   'v', str(0x55), 'Unexpected value in outRow[0].'))
expected.append(('ub', 'outRow+1', 'v', str(0x55), 'Unexpected value in outRow[1].'))
expected.append(('ub', 'outRow+2', 'v', str(0x37), 'Unexpected value in outRow[2].'))
expected.append(('ub', 'outRow+3', 'v', str(0x03), 'Unexpected value in outRow[3].'))
expected.append(('ub', 'outRow+4', 'v', str(0xfd), 'Unexpected value in outRow[4].'))
expected.append(('ub', 'outRow+5', 'v', str(0xcd), 'Unexpected value in outRow[5].'))

#0xdd, 0x79, 0xff, 0x77, 0xdc, 0xa0
expected.append(('ub', 'outCol',   'v', str(0x79), 'Unexpected value in outCol[0].'))
expected.append(('ub', 'outCol+1', 'v', str(0xdd), 'Unexpected value in outCol[1].'))
expected.append(('ub', 'outCol+2', 'v', str(0x77), 'Unexpected value in outCol[2].'))
expected.append(('ub', 'outCol+3', 'v', str(0xff), 'Unexpected value in outCol[3].'))
expected.append(('ub', 'outCol+4', 'v', str(0xa0), 'Unexpected value in outCol[4].'))
expected.append(('ub', 'outCol+5', 'v', str(0xda), 'Unexpected value in outCol[5].'))

# estimate
maxSteps = 10000

filename = 'lab03.s'
try:
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
    for line in checkSimResults(expected, coreDumpData, labelMap):
        print(line)
except:
    print("Simulation failed")
