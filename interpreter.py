import sys
import os
import numpy as np

DEBUG = False
PRINT_CELL_AT_THE_END = False

storage = [0]
ptr = 0

fileptr = 0
while_stack = []


def Right():
    global ptr
    ptr += 1
    if len(storage) <= ptr: storage.append(0)
    
def Left():
    global ptr
    ptr = 0 if ptr <= 0 else ptr - 1
    
def Plus():
    global storage
    global ptr
    storage[ptr] = storage[ptr] + 1 if storage[ptr] < 255 else 0

def Minus():
    global storage
    global ptr
    storage[ptr] = storage[ptr] - 1 if storage[ptr] > 0 else 255
    
def Printchar():
    global storage
    global ptr
    print(chr(storage[ptr]),end='')
    
def Readchar():
    global storage
    global ptr
    storage[ptr] = ord(sys.stdin.read(1))

def WhileStart():
    global storage
    global ptr
    global fileptr
    global while_stack
    if storage[ptr] == 0:
        return True
    else:
        while_stack.append(fileptr)

def WhileEnd():
    global fileptr
    global while_stack
    global storage
    global ptr
    if storage[ptr] == 0:
        while_stack.pop()
        return 0
    return fileptr - while_stack.pop() + 1

def PrintErr(*msg):
    print(*msg,file=sys.stderr)

def PrintHelp():
    print("Usage:", sys.argv[0], "input_file",file=sys.stderr)



def Main(inFileName):
    global fileptr    
    
    file = open(inFileName, 'rb')
    
    #all syntax
    syntax = {b'>':Right,
          b'<':Left,
          b'+':Plus,
          b'-':Minus,
          b'.':Printchar,
          b',':Readchar,
          b'[':WhileStart,
          b']':WhileEnd}
    
    #for skiping loops
    skip = False
    bracket_counter = 0
    
    while 1:    
        # readby character
        char = file.read(1) 
        fileptr = fileptr + 1
        
        if not char:
            break
        
        #interpret values
        if char in syntax:
            if not skip:
                ret = syntax[char]()
                if ret != None:
                    if ret == True:
                        skip = True 
                        bracket_counter = bracket_counter + 1
                    else:
                        file.seek(-ret,1)
                        fileptr = fileptr - ret       
            else:
                if char == b'[':
                    bracket_counter = bracket_counter + 1
                if char == b']':
                    bracket_counter =  bracket_counter - 1
                if bracket_counter == 0:
                    skip = False        
            
        if DEBUG:
            PrintErr(storage," - ",char)
    
    if bracket_counter != 0:
        PrintErr("Wrong syntax - no closing bracket -> ']'")
    
    if PRINT_CELL_AT_THE_END:
        PrintErr("\n",storage,"\n")
    
    file.close()
    
if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Wrong arguments, no input file")
        PrintHelp()
    else:
        if not os.path.exists(sys.argv[1]):
            PrintErr("Cannot open input file: ", sys.argv[1])
            PrintHelp()
        else:
            Main(sys.argv[1])