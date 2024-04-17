import logging
import os
import re
import importlib.util
from typing import LiteralString

from fastapi import Header, HTTPException, Security, FastAPI, APIRouter


def validate_token(authorization: str = Header(...), secret_key: str = "YourSecretKey"):
    if not authorization or not authorization.startswith('Bearer '):
        raise HTTPException(status_code=401, detail="Token is missing or invalid")

    token = authorization.split(' ')[1]
    if token != secret_key:
        raise HTTPException(status_code=401, detail="Token is invalid")

    return token  # This could be a decoded token payload if JWT is used


def convert_to_url_params(input_string: str):
    """
    Convert placeholders in the given string from the format `$variable` to `{variable}`
    for FastAPI route compatibility.
    """
    pattern = r'\$([a-zA-Z0-9_]+)'
    result = re.sub(pattern, r'{\1}', input_string)
    return result


def load_routes(app: FastAPI, path: str):
    """
    Load Python modules as route handlers from a specified directory into the FastAPI app.
    This includes handling files at the root of the directory for base ('/') routes.
    """
    logging.info(f"Trying to load routes from {path}...")
    router = APIRouter()  # Central router for collecting routes

    for root, dirs, files in os.walk(path, followlinks=False):
        is_base_directory = (root == path)
        if is_base_directory:
            # Handle files directly in the base path as root handlers
            for file_name in files:
                if file_name.endswith('.py') and file_name[:-3] in (
                        "get", "post", "put", "delete", "options", "head", "patch"):
                    method = file_name[:-3]
                    module_file_path = os.path.join(root, file_name)
                    load_route(app, router, module_file_path, method, "/")

        # Handle subdirectories
        for found_dir in dirs:
            entry_point = os.path.join(root, found_dir)
            route_path = os.path.relpath(entry_point, start=path).replace("\\", "/")

            for method in ("get", "post", "put", "delete", "options", "head", "patch", "ws"):
                module_file_path = os.path.join(entry_point, f"{method}.py")
                if os.path.exists(module_file_path):
                    load_route(
                        app=app,
                        router=router,
                        module_file_path=module_file_path,
                        method=method,
                        route_path=route_path
                    )

    # Include the centralized router in the main app after all routes have been added
    app.include_router(router)


def load_route(app: FastAPI, router: APIRouter, module_file_path: str, method: str, route_path: str):
    """
    Load a single route handler from a Python file and add it to the given router.
    """

    spec = importlib.util.spec_from_file_location("module_name", module_file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    api_route_path = f"/{convert_to_url_params(route_path).strip('/')}"

    if method == "ws":
        logging.info(f"Adding WebSockets on {api_route_path}")
        router.websocket(api_route_path)
        app.add_websocket_route(api_route_path, module.handler)
    else:
        logging.info(f"Adding {method.upper()} {api_route_path if api_route_path != '/' else 'root (/)'}")
        logging.info(f"Loading {module_file_path}")

        meta = getattr(module, 'meta', {})

        if meta:
            logging.info(f"Adding meta data: {meta}")

        router.add_api_route(
            path=api_route_path,
            endpoint=module.handler,
            methods=[method.upper()],
            **meta
        )
