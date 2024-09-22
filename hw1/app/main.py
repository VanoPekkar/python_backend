from .utils import send_answer
from .functions import factorial, fibonacci, mean


async def app(scope, receive, send) -> None:
    path = scope['path']

    if path == "/factorial":
        await factorial(scope, receive, send)
        return
    if path.startswith("/fibonacci"):
        await fibonacci(scope, receive, send)
        return
    if path == "/mean":
        await mean(scope, receive, send)
        return

    await send_answer(send, 404, "404 Not Found")
