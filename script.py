"""========== script.py ==========

  This is the only file you need to modify in order
  to get a working mdl project (for now).

  my_main.c will serve as the interpreter for mdl.
  When an mdl script goes through a lexer and parser, 
  the resulting operations will be in the array op[].

  Your job is to go through each entry in op and perform
  the required action from the list below:

  frames: set num_frames for animation

  basename: set name for animation

  vary: manipluate knob values between two given frames
        over a specified interval

  set: set a knob to a given value
  
  setknobs: set all knobs to a given value

  push: push a new origin matrix onto the origin stack
  
  pop: remove the top matrix on the origin stack

  move/scale/rotate: create a transformation matrix 
                     based on the provided values, then 
		     multiply the current top of the
		     origins stack by it.

  box/sphere/torus: create a solid object based on the
                    provided values. Store that in a 
		    temporary matrix, multiply it by the
		    current top of the origins stack, then
		    call draw_polygons.

  line: create a line based on the provided values. Store 
        that in a temporary matrix, multiply it by the
	current top of the origins stack, then call draw_lines.

  save: call save_extension with the provided filename

  display: view the image live
  
  jdyrlandweaver
  ========================="""


import copy
import mdl
from display import *
from matrix import *
from draw import *
from sys import exit

"""======== first_pass( commands, symbols ) ==========

  Checks the commands array for any animation commands
  (frames, basename, vary)
  
  Should set num_frames and basename if the frames 
  or basename commands are present

  If vary is found, but frames is not, the entire
  program should exit.

  If frames is found, but basename is not, set name
  to some default value, and print out a message
  with the name being used.

  jdyrlandweaver
  ==================== """
basename = ""
frames = 0
knobs = []

def first_pass( commands ):
    global frames
    global knobs
    global basename

    found = False
    knobNames=[]
    for command in commands:
        if command[0] == "frames":
            frames = int(command[1])
            found = True
        elif command[0] == "basename":
            print "new basename: "+str(command[1])
            basename +=command[1]
            found = True
        elif command[0] == "vary":
            knobNames.append(command[1])
            found = True
    if found and frames == 0:
        print "frames set to 0... program exiting..."
        exit()
    if found and knobNames == []:
        print "knobs not found... program exiting..."
        exit()
    if found and basename == "":
        print "no basename found...\n defaulting basename to lazyBum"
        exit()
    for x in range(frames):
        knobs.append({})
        for name in knobNames:
            knobs[x][name] = 0
    return found

"""======== second_pass( commands ) ==========

  In order to set the knobs for animation, we need to keep
  a seaprate value for each knob for each frame. We can do
  this by using an array of dictionaries. Each array index
  will correspond to a frame (eg. knobs[0] would be the first
  frame, knobs[2] would be the 3rd frame and so on).

  Each index should contain a dictionary of knob values, each
  key will be a knob name, and each value will be the knob's
  value for that frame.

  Go through the command array, and when you find vary, go 
  from knobs[0] to knobs[frames-1] and add (or modify) the
  dictionary corresponding to the given knob with the
  appropirate value. 
  ===================="""
def second_pass( commands, num_frames ):
    global knobs
    global frames
    global basename

    for command in commands:

        if command[0] == "vary":
            print "vary found"
            knobName = command[1]
            startFrame = int(command[2])
            endFrame = int(command[3])
            startVal = float(command[4])
            endVal = float(command[5])
            deltaFrames = 1.0 + endFrame - endVal
            if endVal > startVal:
                deltaVals = endVal - startVal
                delta = deltaVals / deltaFrames
            else:
                deltaVals = startVal - endVal
                delta = -2 * deltaVals / deltaFrames
            print endFrame
            print startFrame

            if endFrame >= 0 and startFrame < endFrame and endFrame < num_frames:
                cur = startFrame
                val = startVal
                while cur <= endFrame:
                    knobs[cur][knobName] = val
                    val += delta
                    cur += 1                
            else:
                print "vary frames out of range. Exiting..."
                exit()
        else:
            print "not a vary"

def runCommands(localCommands, frameNum, animated):
    commands = copy.deepcopy(localCommands)
    print "FRAME: "+str(frameNum)
#    print knobs[frameNum]

    global basename
    global frames
    global knobs

    color = [255, 255, 255]
    tmp = new_matrix()
    ident( tmp )
    
    stack = [ tmp ]
    screen = new_screen()    

    if animated:
        if frameNum == 0:
            commands.append(["save",basename+"000"+str(frameNum)+".png"])
        elif frameNum < 10:
            commands.append(["save",basename+"00"+str(frameNum)+".png"])
        elif frameNum < 100:
            commands.append(["save",basename+"0"+str(frameNum)+".png"])
        elif frameNum < 1000:
            commands.append(["save",basename+str(frameNum)+".png"])
        com = 0
        for command in commands:
            p = 0
            for param in command:
                if param in knobs[frameNum]:
                    #print "param: "+ str(param)
                    #print commands[com][p]
                    commands[com][p] = knobs[frameNum][param]
                    p2 = 1
                    while p2 < len(commands[com]) - 1:
                        print "p2: "+str(p2)
                        try:
                            commands[com][p2] = knobs[frameNum][param] * float(commands[com][p2])
                        except:
                            pass
                        p2+=1
                p+=1
            com+=1
    print commands

    for command in commands:
        if command[0] == "pop":
            stack.pop()
            if not stack:
                stack = [ tmp ]

        if command[0] == "push":
            stack.append( stack[-1][:] )

        if command[0] == "save":
            save_extension(screen, command[1])

        if command[0] == "display":
            display(screen)

        if command[0] == "sphere":
            m = []
            add_sphere(m, command[1], command[2], command[3], command[4], 5)
            matrix_mult(stack[-1], m)
            draw_polygons( m, screen, color )

        if command[0] == "torus":
            m = []
            add_torus(m, command[1], command[2], command[3], command[4], command[5], 5)
            matrix_mult(stack[-1], m)
            draw_polygons( m, screen, color )

        if command[0] == "box":                
            m = []
            add_box(m, *command[1:])
            matrix_mult(stack[-1], m)
            draw_polygons( m, screen, color )
        if command[0] == "line":
            m = []
            add_edge(m, *command[1:])
            matrix_mult(stack[-1], m)
            draw_lines( m, screen, color )

        if command[0] == "bezier":
            m = []
            add_curve(m, command[1], command[2], command[3], command[4], command[5], command[6], command[7], command[8], .05, 'bezier')
            matrix_mult(stack[-1], m)
            draw_lines( m, screen, color )

        if command[0] == "hermite":
            m = []
            add_curve(m, command[1], command[2], command[3], command[4], command[5], command[6], command[7], command[8], .05, 'hermite')
            matrix_mult(stack[-1], m)
            draw_lines( m, screen, color )

        if command[0] == "circle":
            m = []
            add_circle(m, command[1], command[2], command[3], command[4], .05)
            matrix_mult(stack[-1], m)
            draw_lines( m, screen, color )

        if command[0] == "move":                
            xval = command[1]
            yval = command[2]
            zval = command[3]
                    
            t = make_translate(xval, yval, zval)
            matrix_mult( stack[-1], t )
            stack[-1] = t

        if command[0] == "scale":
            xval = command[1]
            yval = command[2]
            zval = command[3]

            t = make_scale(xval, yval, zval)
            matrix_mult( stack[-1], t )
            stack[-1] = t
            
        if command[0] == "rotate":
            print command
            angle = command[2] * (math.pi / 180)

            if command[1] == 'x':
                t = make_rotX( angle )
            elif command[1] == 'y':
                t = make_rotY( angle )
            elif command[1] == 'z':
                t = make_rotZ( angle )            
                
            matrix_mult( stack[-1], t )
            stack[-1] = t

            
def run(filename):
    global basename
    global frames
    global knobs

    """
    This function runs an mdl script
    """
    p = mdl.parseFile(filename)

    if p:
        (commands, symbols) = p
    else:
        print "Parsing failed."
        return

    commands = list(commands)
    cur = 0
    for x in commands:
        commands[cur] = list(commands[cur])
        cur+=1

    animated = first_pass(commands)
    second_pass(commands,frames)
    print frames
    print knobs
    print "basename " +basename

#    runCommands(commands, 30, animated)

    for frameNum in range(frames):
        runCommands(commands,frameNum,animated)
