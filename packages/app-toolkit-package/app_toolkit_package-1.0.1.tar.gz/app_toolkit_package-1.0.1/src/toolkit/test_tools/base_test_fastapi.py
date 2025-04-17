from enum import Enum
from typing import TypeAlias

from fastapi import APIRouter
from httpx import AsyncClient, Response

# from src.main import app
from ..types_app import _AS, _F, Any, TypeResponseJson
from .mixins import check_db, setup_db
from .utils import assert_equal

__all__ = [
    "request",
    "API_Router",
    "BaseTest_API",
    "HTTPMethod",
    "TypeHTTPMethod",
]


class API_Router:
    router: APIRouter


class HTTPMethod(Enum):
    DELETE, GET, PATCH, POST, PUT = range(5)

    @classmethod
    def get_member_names(cls):
        return map(str.lower, cls._member_names_)


TypeHTTPMethod: TypeAlias = HTTPMethod | str


def check_response(
    *,
    response: Response,
    expected_status_code: int = 200,
    expected_response_json: TypeResponseJson = None,
) -> Response:
    assert response.status_code == expected_status_code, (
        response.status_code,
        response.json(),
    )
    if expected_response_json is not None:
        assert_equal(response.json(), expected_response_json)
    return response


def reverse(
    *,
    router: APIRouter | None = None,
    path_func: _F,
    **path_params,
) -> str:
    if router is None:
        router = API_Router.router
    return router.url_path_for(path_func.__name__, **path_params)


def get_http_method(http_method: TypeHTTPMethod) -> str:
    if isinstance(http_method, HTTPMethod):
        http_method = http_method.name.lower()
    elif isinstance(http_method, str):
        http_method = http_method.lower()
    else:
        raise ValueError(f"Invalid HTTP method type {type(http_method)}")
    if http_method not in HTTPMethod.get_member_names():
        raise ValueError(f"Invalid HTTP method {http_method}")
    return http_method


async def request(
    async_client: AsyncClient,
    *,
    router: APIRouter | None = None,
    http_method: TypeHTTPMethod,
    path_func: _F,
    expected_status_code: int = 200,
    expected_response_json: TypeResponseJson = None,
    query_params: dict[str, Any] | None = None,
    json: dict[str, Any] | None = None,
    **path_params,
) -> Response:
    return check_response(
        expected_status_code=expected_status_code,
        expected_response_json=expected_response_json,
        response=await getattr(async_client, get_http_method(http_method))(
            url=reverse(router=router, path_func=path_func, **path_params),
            params=query_params,
            **(dict(json=json) if json is not None else {}),
        ),
    )


class BaseTest_API:
    router: APIRouter | None = None
    http_method: TypeHTTPMethod
    path_func: _F  # type: ignore [valid-type]
    path_params: dict[str, Any] = {}
    query_params: dict[str, Any] | None = None
    json: dict[str, Any] | None = None
    expected_status_code: int = 200
    expected_response_json: dict[str, Any] | None = None
    expected_response_headers: dict[str, str] = {}

    async def test__endpoint(
        self, async_client: AsyncClient, get_test_session: _AS
    ) -> None:
        await setup_db(self, get_test_session)
        response = await request(
            async_client,
            router=self.router,
            http_method=self.http_method,
            path_func=self.path_func,
            **self.path_params,
            query_params=self.query_params,
            json=self.json,
            expected_status_code=self.expected_status_code,
            expected_response_json=self.expected_response_json,
        )
        for k, v in self.expected_response_headers.items():
            assert_equal(response.headers.get(k), v)
        await check_db(self, get_test_session, response)
