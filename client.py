import asyncio
import websockets

async def chat_client(room_id: int):
    uri = f"ws://localhost:8000/chat/ws/{room_id}?parent_id={parent_id}"
    async with websockets.connect(uri) as websocket:
        async def send_status_request():
            while True:
                # Request chat room status every 5 seconds
                await websocket.send("status_request")
                await asyncio.sleep(5)

        async def receive_messages():
            while True:
                message = await websocket.recv()
                print(f"Received: {message}")

        asyncio.create_task(send_status_request())
        await receive_messages()

if __name__ == "__main__":
    room_id = 1  # example room_id as integer
    asyncio.run(chat_client(room_id))


# import asyncio
# import websockets

# async def chat_client(room_id: int):
#     uri = f"ws://localhost:8000/chat/ws/{room_id}"
#     async with websockets.connect(uri) as websocket:
#         while True:
#             message = input("Enter message: ")
#             await websocket.send(message)
#             response = await websocket.recv()
#             print(f"Received: {response}")

# if __name__ == "__main__":
#     room_id = 1  # example room_id as integer
#     asyncio.run(chat_client(room_id))

