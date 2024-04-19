import mistune
from fastapi import WebSocket


async def handler(websocket: WebSocket):
    chat_id = websocket.scope['path_params']['chat_id']

    await websocket.accept()

    await websocket.send_text(f"Connected to chat [{chat_id}]")

    try:
        while True:
            data = await websocket.receive_text()

            # check if the message is empty
            if not data:
                continue

            # check if the message is a command that starts with `/`
            if data.startswith('/'):
                # check if the command is `/exit`
                if data == '/exit':
                    await websocket.send_text("Exiting chat...")
                    break
                # check if the command is `/clear`
                elif data == '/clear':
                    await websocket.send_text("Clearing chat...")
                    continue
                # check if the command is `/help`
                elif data == '/help':
                    await websocket.send_text(mistune.html("""#### Available commands:\n\n/exit - Exit chat\n\n/clear - Clear chat\n\n/help - Display this message""".strip()))
                    continue
                # if the command is not recognized
                else:
                    await websocket.send_text(f"Unknown command: {data}")
                    continue

            await websocket.send_text(f"[{chat_id}]: {data}")
    except Exception as e:
        await websocket.close()
        print(f"WebSocket closed with exception: {e}")
