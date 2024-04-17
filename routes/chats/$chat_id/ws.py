from fastapi import WebSocket


async def handler(websocket:WebSocket):
    chat_id = websocket.scope['path_params']['chat_id']

    await websocket.accept()

    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Message received [{chat_id}]: {data}")
    except Exception as e:
        await websocket.close()
        print(f"WebSocket closed with exception: {e}")
