import logging
import socket

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

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

app.mount("/assets", StaticFiles(directory="templates/assets"), name="assets")

load_routes(app, 'routes')
