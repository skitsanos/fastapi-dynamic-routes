from fastapi import Header


async def handler(x_custom_header: str = Header(None, alias="X-Custom-Header")):
    # Use the custom header value in your logic
    return {"header_value": x_custom_header}
