#!/usr/bin/env python
# backend
# WS server example that synchronizes state across clients

import asyncio
import json
import websockets

# USERS dict would be [user ID:user's websockets]
USERS = {}
async def chat(websocket, path):
    # handshake
    await websocket.send(json.dumps({"type": "handshake"}))
    async for message in websocket:
        data = json.loads(message)
        print("data",data)
        message = ''
        # user send data
        if data["type"] == 'send':
            name = '404'
            for k, v in USERS.items():
                if v == websocket:
                    name = k
            if len(USERS) != 0:  # asyncio.wait doesn't accept an empty list
                message = json.dumps(
                   {"type": "user", "content": data["content"], "from": name})
        #user login
        elif data["type"] == 'login':
            USERS[data["content"]] = websocket #Register websocket to each user name
            if len(USERS) != 0:  # asyncio.wait doesn't accept an empty list
                message = json.dumps(
                   {"type": "login", "content": data["content"], "user_list": list(USERS.keys())})
        #user logout
        elif data["type"] == 'logout':
            del USERS[data["content"]]
            if len(USERS) != 0:  # asyncio.wait doesn't accept an empty list
                message = json.dumps(
                   {"type": "logout", "content": data["content"], "user_list": list(USERS.keys())})

        # broadcast
        await asyncio.wait([user.send(message) for user in USERS.values()])


start_server = websockets.serve(chat, "127.0.0.1", 1234)

# As the function name suggests, is to let the tasks in registered parameter be executed, and then close it when the tasks are completed  
asyncio.get_event_loop().run_until_complete(start_server) 
 #As soon as this function is executed, the Event Loop will always be executed and will not be closed, unless loop.stop() appears in the program to stop
asyncio.get_event_loop().run_forever()