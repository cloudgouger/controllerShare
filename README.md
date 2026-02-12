# controllerShare

Send your controller inputs to another computer across the network using controllerShare (name wip)

Requirements for server
- ViGEm Bus driver
- pyvjoystick
- Windows


Requirements for Client
- PyGame
- Any OS works as long as it had PyGame

## How to use
1. Start up the client on one PC and the server on another. The client PC should be the one that will actually have the controller connected and the server is the one who will recieve the inputs and emulate them.
2. Once you start up the server and the client, input the server's IP into the client
3. Your server should start printing out the values being recieved as soon as they change. You can now use this as a controller in any app


### To-do list
- only send buffer if thumbsticks move past a threshold compared to last state
- use protobuf/grcp instead of json
