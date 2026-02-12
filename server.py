import socket
import os
import sys
import json
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
                rawJson, buffer = buffer.split(b"\n", 1)
            decodedData = rawJson.decode()
            # clear the screen
            os.system("clear || cls")
            print(f"LENGTH OF RECIEVED DATA: {len(decodedData)}")
            print("JSON DATA:")
            print(decodedData)
            print("LOADED JSON DATA:")
            loadedJsonData = json.loads(decodedData)
            # Print the loaded Json data neatly
            # first for the face buttons
            print(f"X pressed: {loadedJsonData["faceButtons"][0]}")
            if loadedJsonData["faceButtons"][0] == 1:
                emulatedGamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
            else:
                emulatedGamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
            print(f"O pressed: {loadedJsonData["faceButtons"][1]}")
            if loadedJsonData["faceButtons"][1] == 1:
                emulatedGamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_B)
            else:
                emulatedGamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_B)
            print(f"Square pressed: {loadedJsonData["faceButtons"][2]}")

            if loadedJsonData["faceButtons"][2] == 1:
                emulatedGamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_X)
            else:
                emulatedGamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_X)

            print(f"Triangle pressed: {loadedJsonData["faceButtons"][3]}")

            if loadedJsonData["faceButtons"][3] == 1:
                emulatedGamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_Y)
            else:
                emulatedGamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_Y)

            # next for the d-pad
            print(f"Up button pressed: {loadedJsonData["dPadState"][0]}")

            if loadedJsonData["dPadState"][0] == 1:
                emulatedGamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_UP)
            else:
                emulatedGamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_UP)
            
            print(f"Down button pressed: {loadedJsonData["dPadState"][1]}")

            if loadedJsonData["dPadState"][1] == 1:
                emulatedGamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_DOWN)
            else:
                emulatedGamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_DOWN)

            print(f"Left button pressed: {loadedJsonData["dPadState"][2]}")

            if loadedJsonData["dPadState"][2] == 1:
                emulatedGamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_LEFT)
            else:
                emulatedGamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_LEFT)

            print(f"Right button pressed: {loadedJsonData["dPadState"][3]}")

            if loadedJsonData["dPadState"][3] == 1:
                emulatedGamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_RIGHT)
            else:
                emulatedGamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_RIGHT)

            # the bumpers
            print(f"Left Bumper: {loadedJsonData["bumperState"][0]}")

            if loadedJsonData["bumperState"][0] == 1:
                emulatedGamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER)
            else:
                emulatedGamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER)

            print(f"Right Bumper: {loadedJsonData["bumperState"][1]}")

            if loadedJsonData["bumperState"][1] == 1:
                emulatedGamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_SHOULDER)
            else:
                emulatedGamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_SHOULDER)

            # the triggers
            print(f"Left Trigger: {loadedJsonData["triggerState"][0]}")
            emulatedGamepad.left_trigger_float(
                value_float=((loadedJsonData["triggerState"][0] + 1) / 2))
            print(f"Right Trigger: {loadedJsonData["triggerState"][1]}")
            emulatedGamepad.right_trigger_float(
                value_float=((loadedJsonData["triggerState"][1] + 1) / 2))
            # left stick
            print(f"Left stick: x: {loadedJsonData["leftStickState"][0]} y: {loadedJsonData["leftStickState"][1]}")
            emulatedGamepad.left_joystick_float(
                x_value_float=loadedJsonData["leftStickState"][0], 
                y_value_float=-loadedJsonData["leftStickState"][1])
            # right stick
            print(f"Right stick: x: {loadedJsonData["rightStickState"][0]} y: {loadedJsonData["rightStickState"][1]}")
            emulatedGamepad.right_joystick_float(
                x_value_float=loadedJsonData["rightStickState"][0], 
                y_value_float=-loadedJsonData["rightStickState"][1])
            emulatedGamepad.update()


            
