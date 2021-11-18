import uvicorn
from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from starlette.websockets import WebSocketDisconnect

app = FastAPI()
html = """
<!DOCTYPE html>
<html>
    <head>
        <title>RELABS TEST CASE</title>
    </head>
    <body>
        <h1>RELABS TEST CASE</h1>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            const ws = new WebSocket("ws://localhost:8000/ws");
            ws.onmessage = (event) => {
                const messages = document.getElementById('messages');
                const message = document.createElement('li');
                const data = JSON.parse(event.data)
                const messageData = `${data.id}. ${data.message}`
                const content = document.createTextNode(messageData);
                message.appendChild(content);
                messages.appendChild(message);
            };
            const sendMessage = (event) => {
                const input = document.getElementById("messageText");
                data = {message: input.value};
                ws.send(JSON.stringify(data));
                input.value = '';
                event.preventDefault();
            };
        </script>
    </body>
</html>
"""


@app.get("/")
async def get():
    return HTMLResponse(html)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    c = 1
    await websocket.accept()
    while True:
        try:
            data = await websocket.receive_json()
        except WebSocketDisconnect:
            return
        data["id"] = c
        await websocket.send_json(data)
        c += 1


if __name__ == "__main__":
    uvicorn.run("__main__:app", reload=True, host="127.0.0.1", port=8000)
