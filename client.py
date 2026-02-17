import socket
import pygame
import json
import controller_pb2
import copy
import time


pygame.init()
print("")
host = input("Input host ip: ") # The ip of the person who will connect to you
port = input("Input host port: ") # the port
deadZone = 0.1
controllerServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientController = pygame.joystick.Joystick(0) #the number is an id value idk what it's for rn
# AF_INET means an ipv4 socket, and sock_stream means a good two way socket
controllerServer.connect((host, int(port)))
# host is a string that stores the ip address of the server we want to connect to
# first, we pass connect the host ip, and the port. I choose 4096 because it is likely unused and has a nice ring to it
# with this, we are now connected to the port

# next step is to send commands

#controllerServer.send('SIX SEVEN SIX SEVEN SIX SEVEN'.encode())
# send a message to our server

# code to record button inputs and send them goes here:

controllerState = controller_pb2.controllerState()

lastSentState = controller_pb2.controllerState()
while True:
    time.sleep(1/30)
    for event in pygame.event.get(): #everytime an event comes up in pygame, execute below
        #get face buttons state
        ecksState = clientController.get_button(0)
        oState = clientController.get_button(1)
        squareState = clientController.get_button(2)
        triangleState = clientController.get_button(3)
        # get dpad state
        upState = clientController.get_button(11)
        downState = clientController.get_button(12)
        leftState = clientController.get_button(13)
        rightState = clientController.get_button(14)
        # get trigger and bumper state
        leftBumperState = clientController.get_button(9)
        leftTriggerState = clientController.get_axis(4)
        rightBumperState = clientController.get_button(10)
        rightTriggerState = clientController.get_axis(5)
        leftStickX = 0
        leftStickY = 0
        rightStickX = 0
        rightStickY = 0
        # get sticks state
        tempLeftStickX = clientController.get_axis(0)

        if (-deadZone < tempLeftStickX < deadZone) == False:
            leftStickX = tempLeftStickX

        tempLeftStickY = clientController.get_axis(1)

        if (-deadZone < tempLeftStickY < deadZone) == False:
            leftStickY = tempLeftStickY

        tempRightStickX = clientController.get_axis(2)

        if (-deadZone < tempRightStickX < deadZone) == False:
            rightStickX = tempRightStickX
            
        tempRightStickY = clientController.get_axis(3)

        if (-deadZone < tempRightStickY < deadZone) == False:
            rightStickY = tempRightStickY

        leftStickButton = clientController.get_button(7)
        rightStickButton = clientController.get_button(8)

        controllerState.faceX = ecksState
        controllerState.faceO = oState
        controllerState.faceSquare = squareState
        controllerState.faceTriangle = triangleState

        controllerState.upState = upState
        controllerState.dpadDown = downState
        controllerState.dpadLeft = leftState
        controllerState.dpadRight = rightState

        controllerState.leftBumper = leftBumperState
        controllerState.rightBumper = rightBumperState

        controllerState.leftTrigger = leftTriggerState
        controllerState.rightTrigger = rightTriggerState

        controllerState.leftButton = leftStickButton
        controllerState.rightButton = rightStickButton

        controllerState.leftStickX = leftStickX
        controllerState.leftStickY = leftStickY

        controllerState.rightStickX = rightStickX
        controllerState.rightStickY = rightStickY

        

        '''controllerState = {
            "faceButtons": [ecksState, oState, squareState, triangleState],
            "dPadState": [upState, downState, leftState, rightState],
            "bumperState": [leftBumperState, rightBumperState],
            "triggerState": [leftTriggerState, rightTriggerState],
            "leftStickState": [leftStickX, leftStickY],
            "rightStickState": [rightStickX, rightStickY]
        }'''
        #controllerState = f"{ecksState}{oState}{squareState}{triangleState}{upState}{downState}{leftState}{rightState}"
        
        if controllerState != lastSentState:
            lastSentState = copy.deepcopy(controllerState)
            # change to sendall to make sure all data is transmitted correctly
            # add the newline thingie
            toSend = controllerState.SerializeToString()
            controllerServer.sendall(toSend + b'\n')
