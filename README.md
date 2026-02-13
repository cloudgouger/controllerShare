# controllerShare

Send your controller inputs to another computer across the network using controllerShare (name wip)

Requirements for server
- ViGEm Bus driver
- pyvjoystick
- Protobuf
- Windows


Requirements for Client
- PyGame
- Protobuf
- Any OS works as long as it supports both of those dependencies

Currently supports local IP input (internet IP theoretically should work, if not, use ZeroTier) and has only been tested with dualsense.

## How to use
1. Start up the client on one PC and the server on another. The client PC should be the one that will actually have the controller connected and the server is the one who will recieve the inputs and emulate them.
2. Once you start up the server and the client, input the server's IP and port into the client
3. Your server should start printing out the values being recieved as soon as they change. You can now use this as a controller in any app


### To-do list
- only send buffer if thumbsticks move past a threshold compared to last state
- ~~use protobuf/grcp instead of json~~
- add menu button support
- Add gui

Major Milestones:
- Working (Febuary 11th, 2026)
- Low-Latency protobuf and L3 R3 implemented (Febuary 12th and 13th, 2026)
