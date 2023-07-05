#!/usr/bin/env python3

import re
import tempfile
import subprocess
from random import randint
import os
import json

# Register names to register numbers
regNameMap = {
   'zero' : 0,  'ra'   : 1,  'sp'   : 2,  'gp'   : 3, 'tp'   : 4,
   't0'   : 5,  't1'   : 6,  't2'   : 7,
   's0'   : 8,  'fp'   : 8,  's1'   : 9,
   'a0'   : 10, 'a1'   : 11, 'a2'   : 12, 'a3'   : 13,
   'a4'   : 14, 'a5'   : 15, 'a6'   : 16, 'a7'   : 17,
   's2'   : 18, 's3'   : 19, 's4'   : 20, 's5'   : 21,
   's6'   : 22, 's7'   : 23, 's8'   : 24, 's9'   : 25,
   's10'  : 26, 's11'  : 27,
   't3'   : 28, 't4'   : 29, 't5'   : 30, 't6'   : 31
}

def twos_comp(val, bits):
    """compute the 2's complement of int value val"""
    if (val & (1 << (bits - 1))) != 0: # if sign bit is set e.g., 8bit: 128-255
        val = val - (1 << bits)        # compute negative value
    return val 

def memGetValue(coreDumpData, address, size=4, littleEndian=True, signed=False):
    """
        Access size bytes from address and return the value.
        Has support for little/big endian stored data.
        Can provide the value as a signed number.
        Raises a ValueError if the address is not in the coreDump dictionary
    """
    #address, size in number of bytes (1 - byte, 2 - half, 4 - word), littleEndian, signed
    outVal = 0
    i = 0
    while i < size:
        memVal = coreDumpData["memory"].get(str(address))
        if memVal is not None:
            if littleEndian:
                outVal += memVal << (8 * i)
            else:
                outVal <<= 8;
                outVal += memVal
        else:
            raise ValueError("No data at address")
        address += 1
        i += 1
    if signed:
        outVal = twos_comp(outVal, 8*size)
    return outVal


def memGetString(coreDumpData, address, size=0):
    """
        Get a string from address, up to size chars long.
        size = 0, means read up to the end of string (the '\0' char)
        Raises a ValueError if the address is not in the coreDump dictionary
    """
    outS = ""
    # emulate a do - while loop
    cond = True
    while cond:
        memVal = coreDumpData["memory"].get(str(address))
        # if this is '\0', the end of string, the test below will fail and it won't be added to the output string
        if memVal:
            outS += chr(memVal)
        elif memVal is None:
            raise ValueError("No data at address")
        address += 1
        size -= 1
        cond = (size != 0) # if size, was 0, this will be True as size will now be -1
        cond = cond and (memVal != 0)
    return outS
   

# Default values for s registers. These are set before running a subroutine and are checked
#  after the subroutine returns
default_savedRegs = {
    "s0"  : "0x121",
    "s1"  : "0x122",
    "s2"  : "0x123",
    "s3"  : "0x124",
    "s4"  : "0x125",
    "s5"  : "0x126",
    "s6"  : "0x127",
    "s7"  : "0x128",
    "s8"  : "0x129",
    "s9"  : "0x12a",
    "s10" : "0x12b",
    "s11" : "0x12c",
}

# Callee - preserved registers. They are assigned random values to
#  catch code reliance on the simulator clearing them at the beginning of simulation
default_randRegs = [ "t0", "t1", "t2", "t3", "t4", "t5", "t6", "ra",
             "a0", "a1", "a2", "a3", "a4", "a5", "a6", "a7"]


def isLabel(name, labelList):
    """ Returns if a string is a declared label """
    return name in labelList

def assembleSetRegs(regDict, labelList):
    """
       Generates code to set registers in a dictionary of string: string pairs,
       where the first string is a register name and the second is the value.
       The 2nd string can be a label, which will generate a la instruction,
       or a constant (in whatever format the assembler accepts), which
       generates an li instruction
    """
    generatedCode = ""
    for reg in regDict.keys():
        if isLabel(regDict[reg], labelList):
            generatedCode += "\tla "
        else:
            generatedCode += "\tli "
        generatedCode += reg + ", " + regDict[reg] + "\n"
    return generatedCode 

def randomizeRegs(regList):
    """
        Generates code which initializes the regs in regList to random numbers
    """
    generatedCode = ""
    for reg in regList:
        generatedCode += "\tli " + reg + ", " + str(randint(1, 0xffff)) + "\n"
    return generatedCode

def dumpLabelAddresses(allDataLabelNames):
    # IMPORTANT. The order is as in the source code and then the new labels, which where not in the
    #  original code, in the order written to the newLabels dict
    generatedCode = "\t#Dump all label addresses to simulator's stdout\n"
    for label in allDataLabelNames:
        # Add code to print to std out the addresses of the labels, so I can pick them up later!
        generatedCode += "\tla  a1, " + label + "\n"
        generatedCode += "\tli  a0, 34"    + "\n"  # print hex
        generatedCode += "\tecall"         + "\n"
        generatedCode += "\tli  a1, '\\n'" + "\n"
        generatedCode += "\tli  a0, 11"    + "\n"  # print char (new line)
        generatedCode += "\tecall"         + "\n"
    return generatedCode

# Save a0, a1 to stack. Print a1, then read a0 from stack into a1 and print it too. Restore the stack pointer. 
#   The drawback is that I modify the stack, but there is no automatic way to examine it, in view of
#   the sort of stack abuse I've seen all these years...
# Other ideas: 
#  - move a0, a1 to float regs, but the conversion will not be perfect and I may get different values back
#  - do a proper OS ISR save of all regs, but that's complicated and might not be supported in the simulator
#  - just save a0 on the stack and get it from the codedump. However, the student code may move the sp to
#    unexpected address, and we wouldn't know where to look for a0!
def dump_a1_a0():
    generatedCode  = "\t#Dump a0 and a1 into simulator's stdout\n"
    generatedCode += "\taddi  sp, sp,    -8\n"
    generatedCode += "\tsw    a1, 4(sp)\n"
    generatedCode += "\tsw    a0, 0(sp)\n"
    # Add a new line, so that any previous messages are in a separate line
    generatedCode += "\tli  a1, '\\n'" + "\n"
    generatedCode += "\tli  a0, 11"    + "\n"  # print char (new line)
    generatedCode += "\tecall"         + "\n"
    generatedCode += "\t# print a1\n"
    generatedCode += "\tlw    a1, 4(sp)  # get original a1 from stack\n"
    generatedCode += "\tli    a0, 34     # print the value of a1 in hex\n"
    generatedCode += "\tecall\n"
    generatedCode += "\tli  a1, '\\n'" + "\n"
    generatedCode += "\tli  a0, 11"    + "\n"  # print char (new line)
    generatedCode += "\tecall"         + "\n"
    generatedCode += "\tlw    a1, 0(sp)  # get original a0 from stack\n"
    generatedCode += "\tli    a0, 34   # print hex\n"
    generatedCode += "\tecall\n"
    generatedCode += "\tli  a1, '\\n'" + "\n"
    generatedCode += "\tli  a0, 11"    + "\n"  # print char (new line)
    generatedCode += "\tecall"         + "\n"
    generatedCode += "\tlw    a1,  4(sp)\n"
    generatedCode += "\tlw    a0,  0(sp)\n"
    generatedCode += "\taddi  sp,  sp,   8\n"
    return generatedCode
    
def exitCall():
    return "\tli  a0, 10\n" + "\tecall\n"

def parseLabels(originalSourceCode, newLabels):
    """
      - Finds all label names and stores them in a list (first item of the returned triple) 
      - For labels (keys) in the newLabels dict, finds the source code line where the label
        starts (2nd item in the returned triple) and the line where it ends (+1), (in the 3rd
        item of the returned triple).
    """
    # Find the lines of code for each label of interest
    # A "label region" ends at/when:
    #    end of data segment: .text
    #    another label is defined:  a word followed by a :
    #    an align directive is found: ".align"
    #    a global directive is found ?? : ".globl"
    # BUG: if a string contains something that looks like a label declaration, or .text, etc,
    #    this function thinks it is a label declaration and ends the current label region!

    lineStart = {}
    lineEnd = {}
    allDataLabelNames = [];
    dataSegment = re.compile("\.data")
    textSegment = re.compile("\.text")
    labelDeclPattern = re.compile("(\w+):")
    endRegion = re.compile("(\.text)|(\.align)|(\.globl)|(\w:)")
    inLabelRegion = False
    inDataSegment = False
    currentLabel = None
    for i in range(len(originalSourceCode)):
        if dataSegment.search(originalSourceCode[i]):
            inDataSegment = True;  
        if inDataSegment:
            m = labelDeclPattern.search(originalSourceCode[i])
            if m:
                if inLabelRegion:
                    # The end of a previous label, that I want to modify
                    lineEnd[currentLabel] = i-1; #The end is one line up
                    inLabelRegion = False
                if m.group(1) in newLabels.keys():
                    # found a label, which is to be modified
                    currentLabel = m.group(1)
                    lineStart[currentLabel] = i
                    inLabelRegion = True
                allDataLabelNames.append(m.group(1))
            elif endRegion.search(originalSourceCode[i]):
                if inLabelRegion:
                    lineEnd[currentLabel] = i-1;  # The end is one line up
                    inLabelRegion = False
        if textSegment.search(originalSourceCode[i]):
            inDataSegment = False;  
    return (allDataLabelNames, lineStart, lineEnd)


def instrumentCode(filename, newLabels, randRegs, savedRegs, newMainCode, lab1Hack=False):
    """
       Converts the assembly code in filename into a version to be simulated.
       A dict of labels is given which may overwrite or add new labels in the data section
       Code is output initializing a list of registers (randRegs) with random values
       Code is output to initialize a dict of register (savedRegs) to specific values (which can be checked at the end of simulation
       Returns the filename of the converted assembly file and a list of the code's data labels
    """
    with open(filename, 'r') as sourceFile:
        originalSourceCode = sourceFile.read().splitlines()

    # Replace old "main" 
    for i in range(len(originalSourceCode)):
        originalSourceCode[i] = re.sub(r'\bmain\b', "main_old", originalSourceCode[i])

    (allDataLabelNames, lineStart, lineEnd) = parseLabels(originalSourceCode, newLabels)
    modifiedSourceCode = []
    copiedLabel = False
    currentLabel = None
    skipLine = False
    for i in range(len(originalSourceCode)):
        for label in lineStart.keys():
            if i == lineStart[label]:
              skipLine = True;
              copiedLabel = False
              currentLabel = label
              break
        if skipLine:
            if not copiedLabel:
                modifiedSourceCode.append(currentLabel + ": " + newLabels[currentLabel])
                copiedLabel = True
                newLabels.pop(currentLabel, None)
        if re.search("\.text", originalSourceCode[i]):
            # Add any remaining labels in the data segment
            for label in newLabels.keys():
                modifiedSourceCode.append(label + ": " + newLabels[label])
            # Add the .text line
            modifiedSourceCode.append(originalSourceCode[i])
            modifiedSourceCode.append("main: # this is the modified main")

            allDataLabelNames.extend(list(newLabels.keys()))

            # Venus starts executing right after .text
            #  so the modified main, must be placed here and it must end with an exit ecall,
            #   which means a0, cannot be checked!
            modifiedSourceCode.append(dumpLabelAddresses(allDataLabelNames))
            modifiedSourceCode.append("\t#Add code to randomize initial values of caller-preserved registers")
            modifiedSourceCode.append(randomizeRegs(randRegs))
            modifiedSourceCode.append("\t#Add code to set any registers required by the tester")
            modifiedSourceCode.append(assembleSetRegs(savedRegs, allDataLabelNames))
            modifiedSourceCode.append(newMainCode)
            modifiedSourceCode.append(dump_a1_a0())
            modifiedSourceCode.append(exitCall())
        elif not skipLine:
            modifiedSourceCode.append(originalSourceCode[i])
        if currentLabel and (i == lineEnd[currentLabel]):
            copiedLabel = False
            skipLine = False
            currentLabel = None
    if lab1Hack:
        modifiedSourceCode.append('jr ra')
    with tempfile.NamedTemporaryFile(mode="w+",delete=False) as fp:
        #print(fp.name)
        for line in modifiedSourceCode:
            fp.write(line +"\n")
        fp.flush()

    return (fp.name, allDataLabelNames)



def runSim(filename, newLabels, newMainCode, randRegs=[], savedRegs=default_savedRegs, simSteps=-1, lab1Hack=False):
    """
        Converts an assembly code file (see instrumentCode), runs the simulation and reads the simulation results:
        - gets the addresses of all labels (labelMap)
        - the final contents of the memory and the register file (codeDumpData)
        - the simulator exit code, stderr (as a list) and the stdout (as a list, with the label, and final register values removed)
    """
    # Instrument the code, to include user modifications, initialize registers, dump label addresses and
    #  the final values of a0, a1 into stdout
    (asmFile, allDataLabelNames) = instrumentCode(filename, newLabels, randRegs+default_randRegs, savedRegs, newMainCode, lab1Hack)

    # Run the simulation
    simCmd = ['java', '-jar', '../myy505Utils/'+'venus-jvm-latest.jar', '-it', '-cc', '-cdf', 'dumpFile', '-ms', str(simSteps), asmFile]
    # -it - detect modifications to code and stop
    # -cc - calling convention checker. NOTE: Function label must be declared in .globl
    # -ms - Run for the specified number of steps. (negative means forever)
    # TODO: I can add timeout here!
    out = subprocess.run(simCmd, capture_output=True, text=True)

    errors = out.stderr.splitlines()

    # Delete the instrumented temp file
    os.remove(asmFile)

    simOut = out.stdout.splitlines()
    if out.returncode != 0:
        print("------------- WARNING SOMETHING IS WRONG -------------")
        print("SIMULATION OUTPUT:")
        print(simOut)
        print("SIMULATION SDTERR:")
        print(errors)
        print("------------------------------------------------------")

    # Generate the map of label : address
    lineNo = 0
    labelMap = {}
    for label in allDataLabelNames:
        labelMap[label] = int(simOut[lineNo], base=16)
        lineNo += 1

    with open("dumpFile", 'r') as cdf:
        coreDumpData = json.load(cdf)
        # remove the float part of the registers.
        coreDumpData["registers"].pop("floating", None)

    regValues = coreDumpData['registers']['integer']
    # Get a0, a1, from the simulator output, as the dumpfile is not what we want
    #  and store them in the coreDump dict
    regValues[str(regNameMap['a0'])] = int(simOut[-1], base=16)
    regValues[str(regNameMap['a1'])] = int(simOut[-2], base=16)

    # Check if saved registers are preserved. Done here because we have the savedRegs dict at hand...
    regCheck = []
    for reg in savedRegs.keys():
        # guess base, so I can use hex or decimal. It won't work with chars, e.g. '\n' though
        if regValues[str(regNameMap[reg])] != int(savedRegs[reg], base=0):
            regCheck.append("Saved reg %s not restored. Expected %s, got %s" %(reg, savedRegs[reg], regValues[str(regNameMap[reg])]))
    return (labelMap, coreDumpData, out.returncode, errors, simOut[lineNo:-2], regCheck)



def evalLabelExpression(expression, labelMap):
    """
    Evaluates an expression which may contain labels and returns the, integer, result
    """
    # Also handles hex representation
    for label in labelMap.keys():
        if re.search(r'\b%s\b'%(label), expression):
            # replace the label with a Python dict access, which will get eval'ed at the end
            expression = re.sub(r'\b%s\b'%(label), "labelMap[\"%s\"]" %(label), expression)
    return eval(expression)

def checkSimResults(expected, coreDumpData, labelMap):
    """
        Compares the expected values of registers and memory, described in a list of tupples (expected)
        Returns a list of assertion-style messages describing the failed comparisons
    """
    regValues = coreDumpData['registers']['integer']
    check = []
    for e in expected:
        if e[2] == "v":
            expectedV =  evalLabelExpression(e[3], labelMap)
            if e[0] == "r": #register
                if re.search("[a-z]", e[1]): # register name
                    reg = str(regNameMap[e[1]])
                else:
                    reg = e[1]
                if regValues[reg] != expectedV:
                    check.append(e[4] + " Got %d, expected %d (%s)" %(regValues[reg], expectedV, e[3]))
            else:
                if e[0] == "sb": #signed byte
                    size = 1
                    signed = True
                elif e[0] == "ub":
                    size = 1
                    signed = False
                elif e[0] == "sh": #signed half
                    size = 2
                    signed = True
                elif e[0] == "uh":
                    size = 2
                    signed = False
                elif e[0] == "sw":
                    size = 4
                    signed = True
                elif e[0] == "uw":
                    size = 4
                    signed = False
                else:
                    raise ValueError("Error in expected value structure")
                # calculate the address, as int
                address =  evalLabelExpression(e[1], labelMap)
                simVal = memGetValue(coreDumpData, address, size, True, signed)
                if simVal != expectedV:
                    check.append(e[4] + " Got %d, expected %d (%s)" %(simVal, expectedV, e[3]))
        elif e[2] == "s":
            # Assume e[1] is memory address, ignore e[0]
            address =  evalLabelExpression(e[1], labelMap)
            simStr = memGetString(coreDumpData, address)
            if simStr != e[3]:
                check.append(e[4] + " Got %s, expected %s" %(simStr, e[3]))
        else:
            raise ValueError("Error in expected value structure")
    return check
