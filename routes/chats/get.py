from fastapi.templating import Jinja2Templates


async def handler():
    templates = Jinja2Templates(directory="templates")

    return templates.TemplateResponse("chat.html", {
        "request": {},
        "title": "Chat",
        "user": "John Doe"
    })
