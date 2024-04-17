import logging
import socket

from fastapi import FastAPI, WebSocket

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
load_routes(app, 'routes')
