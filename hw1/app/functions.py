from .utils import (
    is_int, 
    send_answer, 
    validate_method, 
    parse_query_string
)

from typing import Any, Callable, Awaitable, Dict
import json


async def factorial(
    scope: Dict[str, Any],
    receive: Callable[[], Awaitable[dict]],
    send: Callable[[dict], Awaitable[None]]
) -> None:

    if not await validate_method(scope, send):
        return

    query_string = scope.get("query_string")
    if not query_string:
        await send_answer(send, 422, "422 Unprocessable Entity")
        return

    params = await parse_query_string(query_string)
    n_values = params.get('n')

    if not n_values:
        await send_answer(send, 422, "422 Unprocessable Entity")
        return

    n_str = n_values[0]
    if not is_int(n_str):
        await send_answer(send, 422, "422 Unprocessable Entity")
        return

    n = int(n_str)
    if n < 0:
        await send_answer(send, 400, "400 Bad Request")
        return

    result = 1
    for i in range(2, n + 1):
        result *= i

    response = json.dumps({"result": result})
    await send_answer(send, 200, response, content_type="application/json")


async def fibonacci(
    scope: Dict[str, Any],
    receive: Callable[[], Awaitable[dict]],
    send: Callable[[dict], Awaitable[None]]
) -> None:

    if not await validate_method(scope, send):
        return

    path = scope.get("path", "")
    parts = path.strip("/").split("/")
    
    if len(parts) != 2 or not is_int(parts[1]):
        await send_answer(send, 422, "422 Unprocessable Entity")
        return

    n = int(parts[1])
    if n < 0:
        await send_answer(send, 400, "400 Bad Request")
        return

    if n == 0:
        fib = 0
    elif n in (1, 2):
        fib = 1
    else:
        a, b = 1, 1
        for _ in range(3, n + 1):
            a, b = b, a + b
        fib = b

    response = json.dumps({"result": fib})
    await send_answer(send, 200, response, content_type="application/json")


async def mean(
    scope: Dict[str, Any],
    receive: Callable[[], Awaitable[dict]],
    send: Callable[[dict], Awaitable[None]]
) -> None:

    if not await validate_method(scope, send):
        return

    request = await receive()
    body = request.get("body", b"")

    if not body:
        await send_answer(send, 422, "422 Unprocessable Entity")
        return

    try:
        data = json.loads(body)
    except json.JSONDecodeError:
        await send_answer(send, 422, "422 Unprocessable Entity")
        return

    if not isinstance(data, list) or not data:
        await send_answer(send, 400, "400 Bad Request")
        return

    float_sum = .0
    for el in data:
        if not isinstance(el, (int, float)):
            await send_answer(send, 422, "422 Unprocessable Entity")
            return
        float_sum += el

    mean_value = float_sum / len(data)
    response = json.dumps({"result": mean_value})
    await send_answer(send, 200, response, content_type="application/json")