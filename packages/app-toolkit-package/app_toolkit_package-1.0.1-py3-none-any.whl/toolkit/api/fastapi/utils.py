from collections.abc import Coroutine
from typing import Any

from fastapi import HTTPException, Request, Response, status

from ...repo.db.exceptions import NotFound

CLIENT_NO_CACHE = {
    "Cache-Control": "no-cache, no-store, must-revalidate",
    "Pragma": "no-cache",
    "Expires": "0",
}


def set_headers_no_client_cache(response: Response) -> Response:
    """Helper function for FastAPI endpoints."""
    response.headers.update(CLIENT_NO_CACHE)
    return response


def get_client_info(request: Request) -> dict[str, Any]:
    """Helper function for FastAPI endpoints."""
    return dict(
        host=request.client.host,
        port=request.client.port,
    )


async def try_return(
    return_coro: Coroutine,
    possible_exception=NotFound,
    raise_status_code: int = status.HTTP_404_NOT_FOUND,
) -> Any:
    """Helper function for FastAPI endpoints."""
    try:
        return await return_coro
    except possible_exception as e:
        raise HTTPException(status_code=raise_status_code, detail=e.msg)
