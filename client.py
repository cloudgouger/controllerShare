import socket
import pygame
import json

pygame.init()
print("Input host ip: ")
host = input() # The ip of the person who will connect to you
controllerServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientController = pygame.joystick.Joystick(0) #the number is an id value idk what it's for rn
# AF_INET means an ipv4 socket, and sock_stream means a good two way socket
controllerServer.connect((host, 4096))
# host is a string that stores the ip address of the server we want to connect to
# first, we pass connect the host ip, and the port. I choose 4096 because it is likely unused and has a nice ring to it
# with this, we are now connected to the port

# next step is to send commands

#controllerServer.send('SIX SEVEN SIX SEVEN SIX SEVEN'.encode())
# send a message to our server

# code to record button inputs and send them goes here:

print(clientController.get_numhats())
lastSentState = []
while True:
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
        # get sticks state
        leftStickX = clientController.get_axis(0)
        leftStickY = clientController.get_axis(1)
        rightStickX = clientController.get_axis(2)
        rightStickY = clientController.get_axis(3)
        controllerState = {
            "faceButtons": [ecksState, oState, squareState, triangleState],
            "dPadState": [upState, downState, leftState, rightState],
            "bumperState": [leftBumperState, rightBumperState],
            "triggerState": [leftTriggerState, rightTriggerState],
            "leftStickState": [leftStickX, leftStickY],
            "rightStickState": [rightStickX, rightStickY]
        }
        #controllerState = f"{ecksState}{oState}{squareState}{triangleState}{upState}{downState}{leftState}{rightState}"
        
        if controllerState != lastSentState:
            lastSentState = controllerState.copy()
            # change to sendall to make sure all data is transmitted correctly
            # add the newline thingie
            controllerServer.sendall((json.dumps(controllerState)).encode("utf-8") + b'\n')
ow 