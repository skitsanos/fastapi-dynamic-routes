import logging
import socket
import time

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles

from utils.router import load_routes

hostname = socket.gethostname()
logging.basicConfig(
    level=logging.DEBUG,  # Set the desired logging level
    format=f'%(asctime)s [%(levelname)s] {hostname} %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)

app = FastAPI()


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


app.mount("/assets", StaticFiles(directory="templates/assets"), name="assets")

load_routes(app, 'routes')
