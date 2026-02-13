import socket
import os
import sys
import json
import controller_pb2
import pyvjoystick.vigem as vg


emulatedGamepad = vg.VX360Gamepad()

# big thanks to fsadannn for helping me figure out how to map values of one range to another!!
def interpolateTriggerValues(oldMin, oldMax, newMin, newMax, value):
    
    if oldMin == oldMax:
        return newMin
    interpolatedValue = ((value - oldMin) * (newMax - newMin) / (oldMax - oldMin)) + newMin
    
    return interpolatedValue

clientPort = 4096
buffer = b""

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as recieverSocket:
    recieverSocket.bind(('0.0.0.0', clientPort))
    recieverSocket.listen() # allow a server to begin listening in AKA the server is now picking up what the client is putting down
    conn, addr = recieverSocket.accept() # not completely sure what this does, but afaik it stops the program from continuing until a client connects to it
    with conn: # while a connection is valid it will continue the loop
        while True: 
            recievedData = conn.recv(1024) # this loop will only send data when it is recieved (google blocking call for more info)
            if not recievedData: # if nothing is recieved
                break
            buffer += recievedData
            # split the buffer by every newline
            while b"\n" in buffer:
                rawData, buffer = buffer.split(b"\n", 1)
            decodedData = controller_pb2.controllerState()
            decodedData.ParseFromString(rawData)
            # clear the screen
            os.system("clear || cls")
            print(f"LENGTH OF RECIEVED DATA: {len(buffer)}")
            print("RAW DATA:")
            print(decodedData)
            print("PROCESSED DATA:")
            # Print the loaded Json data neatly
            # first for the face buttons
            print(f"X pressed: {decodedData.faceX}")
            if decodedData.faceX == 1:
                emulatedGamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
            else:
                emulatedGamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
            print(f"O pressed: {decodedData.faceO}")
            if decodedData.faceO == 1:
                emulatedGamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_B)
            else:
                emulatedGamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_B)
            print(f"Square pressed: {decodedData.faceSquare}")

            if decodedData.faceSquare == 1:
                emulatedGamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_X)
            else:
                emulatedGamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_X)

            print(f"Triangle pressed: {decodedData.faceTriangle}")

            if decodedData.faceTriangle == 1:
                emulatedGamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_Y)
            else:
                emulatedGamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_Y)

            # next for the d-pad
            print(f"Up button pressed: {decodedData.upState}")

            if decodedData.upState == 1:
                emulatedGamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_UP)
            else:
                emulatedGamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_UP)
            
            print(f"Down button pressed: {decodedData.dpadDown}")

            if decodedData.dpadDown == 1:
                emulatedGamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_DOWN)
            else:
                emulatedGamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_DOWN)

            print(f"Left button pressed: {decodedData.dpadLeft}")

            if decodedData.dpadLeft == 1:
                emulatedGamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_LEFT)
            else:
                emulatedGamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_LEFT)

            print(f"Right button pressed: {decodedData.dpadRight}")

            if decodedData.dpadRight == 1:
                emulatedGamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_RIGHT)
            else:
                emulatedGamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_RIGHT)

            # the bumpers
            print(f"Left Bumper: {decodedData.leftBumper}")

            if decodedData.leftBumper == 1:
                emulatedGamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER)
            else:
                emulatedGamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER)

            print(f"Right Bumper: {decodedData.rightBumper}")

            if decodedData.rightBumper == 1:
                emulatedGamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_SHOULDER)
            else:
                emulatedGamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_SHOULDER)

            # the triggers
            print(f"Left Trigger: {decodedData.leftTrigger}")
            emulatedGamepad.left_trigger_float(
                value_float=(interpolateTriggerValues(-1, 1, 0, 1, decodedData.leftTrigger)))
            print(f"Right Trigger: {decodedData.rightTrigger}")
            emulatedGamepad.right_trigger_float(
                value_float=(interpolateTriggerValues(-1, 1, 0, 1, decodedData.rightTrigger)))
            # left stick
            print(f"Left stick: x: {decodedData.leftStickX} y: {decodedData.leftStickY}")
            emulatedGamepad.left_joystick_float(
                x_value_float=decodedData.leftStickX, 
                y_value_float=-decodedData.leftStickY)
            
            if decodedData.leftButton == 1:
                emulatedGamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_THUMB)
            else:
                emulatedGamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_THUMB)

            # right stick
            print(f"Right stick: x: {decodedData.rightStickX} y: {decodedData.rightStickY}")
            emulatedGamepad.right_joystick_float(
                x_value_float=decodedData.rightStickX, 
                y_value_float=-decodedData.rightStickY)
            
            if decodedData.rightButton == 1:
                emulatedGamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_THUMB)
            else:
                emulatedGamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_THUMB)

            emulatedGamepad.update()


            
