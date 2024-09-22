from typing import Any, Callable, Awaitable, Dict
from urllib.parse import parse_qs


async def parse_query_string(
    query_string: bytes
) -> dict:
    return parse_qs(query_string.decode("utf-8"))


async def send_answer(
    send: Callable[[dict], Any],
    status_code: int,
    message: str,
    content_type: str = "text/plain"
) -> None:

    body = message.encode('utf-8')

    headers = [
        (b"content-type", content_type.encode("utf-8")),
        (b"content-length", str(len(body)).encode("utf-8")),
    ]

    await send({
        "type": "http.response.start",
        "status": status_code,
        "headers": headers,
    })

    await send({
        "type": "http.response.body",
        "body": body,
    })


async def validate_method(
    scope: Dict[str, Any],
    send: Callable[[dict], Awaitable[None]],
    expected_method: str = "GET"
) -> bool:
    if scope.get("method") != expected_method:
        await send_answer(send, 404, "404 Not Found")
        return False
    return True


def is_int(n):
    try:
        int(n)
        return True
    except ValueError:
        return False
