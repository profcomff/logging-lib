import http
import math
import time

from starlette.middleware.base import RequestResponseEndpoint, BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from starlette.types import Message, ASGIApp
import logging

from logger.models import RequestJsonLogSchema


class LoggingMiddleware(BaseHTTPMiddleware):

    EMPTY_VALUE = "None"
    logger: logging.Logger
    port: str
    """
    Middleware для обработки запросов и ответов с целью журналирования
    """

    def __init__(self, app: ASGIApp, port: str, logger: logging.Logger):
        super().__init__(app)
        self.port = port
        self.logger = logger

    @staticmethod
    async def set_body(request: Request, body: bytes) -> None:
        async def receive() -> Message:
            return {"type": "http.request", "body": body}

        request._receive = receive

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint, *args, **kwargs
    ):
        start_time = time.time()
        exception_object = None

        server: tuple = request.get("server", ("localhost", self.port))
        request_headers: dict = dict(request.headers.items())
        try:
            response = await call_next(request)
        except Exception as ex:
            response_body = bytes(http.HTTPStatus.INTERNAL_SERVER_ERROR.phrase.encode())
            response = Response(
                content=response_body,
                status_code=http.HTTPStatus.INTERNAL_SERVER_ERROR.real,
            )
            exception_object = ex
            response_headers = {}
        else:
            response_headers = dict(response.headers.items())
            response_body = response.body
            response = Response(
                content=response_body,
                status_code=response.status_code,
                headers=dict(response.headers),
                media_type=response.media_type,
            )
        duration_ms: int = math.ceil((time.time() - start_time) * 1000)
        request_json_fields = RequestJsonLogSchema(
            level_name = "INFO" if 1<= response.status_code <= 499 else "ERROR",
            request_uri=str(request.url),
            request_referer=request_headers.get(
                "referer", LoggingMiddleware.EMPTY_VALUE
            ),
            request_method=request.method,
            request_path=request.url.path,
            request_host=f"{server[0]}:{server[1]}",
            request_size=int(request_headers.get("content-length", 0)),
            request_content_type=request_headers.get(
                "content-type", LoggingMiddleware.EMPTY_VALUE
            ),
            request_direction="in",
            remote_ip=request.client[0],
            remote_port=request.client[1],
            response_status_code=response.status_code,
            response_size=int(response_headers.get("content-length", 0)),
            duration_ms=duration_ms,
        ).dict()
        message = (
            f'{"Ошибка" if exception_object else "Ответ"} '
            f"с кодом {response.status_code} "
            f'на запрос {request.method} "{str(request.url)}"'
        )
        self.logger.info(
            message,
            extra={
                "request_json_fields": request_json_fields,
                "to_mask": True,
            },
            exc_info=exception_object,
        )
        return response
