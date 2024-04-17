import logging
import socket

import uvicorn

hostname = socket.gethostname()
logging.basicConfig(
    level=logging.DEBUG,  # Set the desired logging level
    format=f'%(asctime)s [%(levelname)s] {hostname} %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)

if __name__ == "__main__":
    uvicorn.run(
        app="server:app",
        reload=True,
        host="127.0.0.1",
        port=8000,
        log_level="debug",
        log_config=None  # Disables Uvicorn's default logging configuration
    )
