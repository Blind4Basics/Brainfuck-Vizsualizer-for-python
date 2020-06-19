# -*- coding: utf-8 -*-

"""
Created on Mon Oct 23 21:59:51 2017

BrainFuck tape, pointer & output vizualizer

@author: Blind4Basics - for CodeWars



-----------------------------------------------------------------

   Debugging commands usable in the BF code itself:

       '?' char in the code to choose the debugging points.
           You can name the check points with r'\w+' characters after the ?:
                "?printThere"
       '!' char to switch on/off the full debugging mode, meaning, print at the
            execution of each segment (see the interpreter notes below)


   Other global switches available:

        ALL:         vizualisation at each step of the code (each segment)
        DEACTIVATE:  force the deactivation of the vizualisation whatever is found in the code or the other switches are
        CHAR_MODE:   if True, the tape will display ascii chars instead of numbers (Note: unprintable chars won't show up...)
        LIMITER:     interrupt the executions after this number of printing


-----------------------------------------------------------------

    About the BF interpreter used:

        "Segments":

            The instructions are executed by "segments" of identical consecutive
            command characters other than control flow ones (meaning, only "+-<>"):

                '[->+<]'    -> 6 segments
                '>>>>><<<'  -> 2 segments
                '>> >> >'   -> 3 segments


        Configuation data:

            ADD_EOF:            Automatically adds an EOF char at the end of the input
                                stream, if set to True (=default).
            RAISE_IF_NO_INPUT:  Raise an exception of ',' is used while the input
                                stream has already been consumed entirely.
                                (default: False -> return \0 instead)
            LOW_TAPE_IDX:       Raises an exception if the pointer goes below this value
                                (default: 0)
            HIGH_TAPE_IDX:      Raises an exception if the pointer goes above this value
                                (default: infinity)




"""



import re

def brainFuckInterpreter(code, prog):

    def updateVizu(cmdSegment=''):
        nonlocal countDisplay, lastP
        if DEACTIVATE: return

        def formatLst(lst, charMod=False):
            formStr = "{: >" + str(max(map(len, map(str, data)), default=1)) + "}"
            return "[{}]".format(', '.join(formStr.format(chr(v) if charMod else v) for v in lst))

        def formatPointerLst(s):
            return s.translate(str.maketrans(',[]01','    *'))


        countDisplay += 1                                           # Update the number of display already done (cf. LIMITER)
        vizu[-1][lastP] = 0                                         # Erase the previous position of the pointer
        vizu[-1][p] = 1                                             # Place the pointer at the current position
        lastP = p                                                   # archive the current position of the pointer

        out = ''.join(output)
        tape,point = vizu
        print( "\n\n{}tape:    {}\npointer: {}\nout = '{}'".format(
                    cmdSegment and cmdSegment+"\n",
                    formatLst(tape, CHAR_MODE),
                    formatPointerLst(formatLst(point)),
                    out
                ))
        if LIMITER >= 0 and LIMITER == countDisplay: raise Exception("Too much printing: LIMITER = {}".format(LIMITER))


    def tapeLenUpdater():                                           # Make the tape length consistent with the actual position of the pointer (even if no value yet in the cells)
        if p < LOW_TAPE_IDX or p> HIGH_TAPE_IDX:
            raise Exception("out of tape: "+str(p))

        if p >= len(data):
            data.extend( [0] * (p-len(data)+1) )
            vizu[-1].extend( [0] * (len(data)-len(vizu[-1])) )


    def getNextInput():                                             # Simulate getting u'0000' when trying to get an input char after their exhaustion
        try:
            return ord(next(prog))
        except StopIteration:
            if RAISE_IF_NO_INPUT: raise Exception("Input stream empty...")
            return 0


    p, lastP, i = 0, 0, 0                                           # p = pointer / lastP = previous P position (mutated) / i = segment of code index
    data = [0]                                                      # Tape initialization

    SWITCH, countDisplay = False, 0                                 # SWITCH: control for the "!" cmd swtich / countDisplay = control for LIMITER (as list to mutate it from a subroutine)
    output, vizu = [], [data, [0]]                                  # vizu: [cmd, tape, pointer list]

    prog = iter(prog)
    code = re.findall(r'\++|<+|>+|-+|[,.[\]]|\?\w*|!', code)        # Make the executions more compact by using only segments of identical commands (=> '++++', '<<<', '[', '-', ']', check points with identifiers...)

    while 0 <= i < len(code):
        if p < 0: print(p)
        c = code[i]
        if False: print(c, data, p)                                 # activate manually. Only for debugging of the vizualiser itself...

        if   c[0] == '+': data[p] = (data[p] + len(c)) % 256
        elif c[0] == '-': data[p] = (data[p] - len(c)) % 256
        elif c[0] == '>': p += len(c) ; tapeLenUpdater()
        elif c[0] == '<': p -= len(c) ; tapeLenUpdater()
        elif c[0] == '.': output.append(chr(data[p]))
        elif c[0] == ',': data[p] = getNextInput()
        elif c[0] == '[':
            if not data[p]:
                depth = 1
                while depth > 0:
                    i += 1
                    c = code[i]
                    if c == '[': depth += 1
                    elif c== ']': depth -= 1
        elif c == ']':
            if data[p]:
                depth = 1
                while depth > 0:
                    i -= 1
                    c = code[i]
                    if c == ']': depth += 1
                    elif c == '[': depth -= 1


        # Vizualisation commands/executions
        #--------------------
        if c[0] == '!':                  SWITCH = not SWITCH
        if c[0] == '?' or ALL or SWITCH: updateVizu(c)
        #--------------------

        i += 1

    return ''.join(output)


def runTests(inputs, exp, code):
    print('\n----------------------------------\nProgram:\n\n{}\n\n----------------------------------\n\n'.format(code))

    EOF = chr(0)*ADD_EOF
    for p,e in zip(inputs,exp):
        print("Input: ", p)
        act = brainFuckInterpreter(code, p+EOF)

        print("Input: ", p)                                    # reminder of the input
        print(repr(act), " should be ", repr(e))               # print actual/expected before assertion
        assert act == e

        print("SUCCESS\n---\n")



#-----------------------------------------------------------



code = """
[Your BF code here]

>>,. ?WhatIs_Here
[->>+>+<<<]
?TapeNow
>>.
?WithOut
"""

#-----------------------------------------------------------

""" GLOBAL SWITCHES """

ALL               = False
DEACTIVATE        = False
CHAR_MODE         = False
LIMITER           = 80
LOW_TAPE_IDX      = 0
HIGH_TAPE_IDX     = float('inf')
ADD_EOF           = True
RAISE_IF_NO_INPUT = False


#------------------------------------------------------------
#   Tests:
#
#  'inputs' and corresponding 'expected' values
#    EOF char automatically added at the end of each input
#------------------------------------------------------------

inputs = ("aba", 'x')
exps   = ['aa', 'xx']

runTests(inputs, exps, code)



"""
Example of informations printed to stdout:

        ----------------------------------
        Programme:


        [Your BF code here]

        >>,. ?WhatIs_Here
        [->>+>+<<<]
        ?TapeNow
        >>.
        ?WithOut


        ----------------------------------


        Input:  a


        ?WhatIs_Here
        tape:    [ 0,  0, 97]
        pointer:           *
        out = 'a'


        ?TapeNow
        tape:    [ 0,  0,  0,  0, 97, 97]
        pointer:           *
        out = 'a'


        ?WithOut
        tape:    [ 0,  0,  0,  0, 97, 97]
        pointer:                   *
        out = 'aa'
        Input:  a
        'aa'  should be  'aa'
        SUCCESS
        ---

        Input:  x


        ?WhatIs_Here
        tape:    [  0,   0, 120]
        pointer:              *
        out = 'x'


        ?TapeNow
        tape:    [  0,   0,   0,   0, 120, 120]
        pointer:              *
        out = 'x'


        ?WithOut
        tape:    [  0,   0,   0,   0, 120, 120]
        pointer:                        *
        out = 'xx'
        Input:  x
        'xx'  should be  'xx'
        SUCCESS
        ---

"""
