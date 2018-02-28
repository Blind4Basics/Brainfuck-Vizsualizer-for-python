# -*- coding: utf-8 -*-

"""
Created on Mon Oct 23 21:59:51 2017

BrainFuck tape, pointer & output vizualizer

@author: Blind4Basics - for CodeWars
"""




# -----------------------------------------------------------------
#   Debugging commands usable in the BF code:
#
#       '?' char in the code to choose the debugging points.
#           You cnan name the check points with r'\w+' characters after the ?
#       '!' char to switch on/off the full debugging (print at the execution of each segment)
#
#
#   Other global switches available:
#
#        ALL:         vizualisation at each step of the code (each segment)
#        DEACTIVATE:  force the deactivation of the vizualisation whatever is found in the code or the other switches are
#        CHAR_MODE:   if True, the tape will display ascii chars instead of numbers (Note: unprintable chars won't show up...)
#        LIMITER:     interrupt the executions after this number of printing
#
# -----------------------------------------------------------------



code = """

[put some BF code here]

>++++
?WHAT_HERE
[[>]+<[<]>-]
?EXPAND
>[->[>]>+<<[<]>]
?CONCAT

"""

#------------------------------------------------------------
#   Test cases:
#
#  'inputs' and corresponding 'expected' values
#    EOF char automatically added at the end of each input
#------------------------------------------------------------

inputs = [""]
exp = [""]

""" GLOBAL SWITCHES """
ALL        = False
DEACTIVATE = False
CHAR_MODE  = False
LIMITER    = 80



import re

def brainFuckInterpreter(code, prog):

    def updateVizu(cmdSegment=''):

        if DEACTIVATE: return

        def formatLst(lst, charMod=False):
            formStr = "{: >" + str(max(map(len, map(str, data)), default=1)) + "}"
            return "[{}]".format(', '.join(formStr.format(chr(v) if charMod else v) for v in lst))

        countDisplay[0] += 1                                        # Update the number of display already done (cf. LIMITER)
        vizu[-1][lastP[0]] = 0                                      # Erase the previous position of the pointer
        vizu[-1][p] = 1                                             # Place the pointer at the current position
        lastP[0] = p                                                # archive the current position of the pointer
        vizu[0] = c[0]                                              # archive the current command

        out = ''.join(output)
        cmd,tape,point = vizu
        print( "\n\n{}{}   tape\n{}   p\nout = '{}'".format(cmdSegment and cmdSegment+"\n",
                                                            formatLst(tape, CHAR_MODE),
                                                            formatLst(point),
                                                            out) )
        if LIMITER >= 0 and LIMITER == countDisplay[0]: raise Exception("Too much printing: LIMITER = {}".format(LIMITER))


    def tapeLenUpdater():                                           # Make the tape length consistent with the actual position of the pointer (even if no value yet in the cells)
        if p >= len(data):
            data.extend( [0] * (p-len(data)+1) )
            vizu[-1].extend( [0] * (len(data)-len(vizu[-1])) )
        elif p < 0:
            raise Exception("out of tape")


    def getNextInput():                                             # Simulate getting u'0000' when trying to get an input char after their exhaustion
        try:
            return ord(next(prog))
        except StopIteration:
            return 0


    p, lastP, i = 0, [0], 0                                         # p = pointer / lastP = previous P position (mutated) / i = segment of code index
    data = [0]                                                      # Tape initialization

    SWITCH, countDisplay = False, [0]                               # SWITCH: control for the "!" cmd swtich / countDisplay = control for LIMITER (as list to mutate it from a subroutine)
    output, vizu = [], ['', data, [0]]                              # vizu: [cmd, tape, pointer list]

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
        elif c[0] == '?' and not (ALL or SWITCH): updateVizu(c)                             # check point found

        if ALL or SWITCH: updateVizu(c)             # Vizualisation for swithes (avoid double printing for check points)

        if c[0] == '!': SWITCH = not SWITCH                         # Update '!' swtich state
        #--------------------

        i += 1
    print(len(data))
    return ''.join(output)


#--------------------
#  LAUNCH THE TESTS
#--------------------

EOF = chr(0)
for p,e in zip(inputs,exp):
    print("Input: ", p)
    act = brainFuckInterpreter(code, p+EOF)

    print("Input: ", p)                        # remainder of the input
    print(act, " should be ", e)               # print actual/expected before assertion
    assert act == e

    print("SUCCESS\n---\n")

