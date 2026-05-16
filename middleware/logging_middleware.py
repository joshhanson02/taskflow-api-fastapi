import time
import logging

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger(__name__)


class LoggingMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):

        start_time = time.time()

        method = request.method
        path = request.url.path
        client_ip = (
            request.client.host
            if request.client
            else "unknown"
        )

        logger.info(
            f"Incoming request | "
            f"IP={client_ip} "
            f"Method={method} "
            f"Path={path}"
        )

        try:
            response = await call_next(request)

        except Exception as e:

            logger.exception(
                f"Unhandled exception | "
                f"Method={method} "
                f"Path={path} "
                f"Error={str(e)}"
            )

            raise e

        process_time = time.time() - start_time

        status_code = response.status_code

        log_message = (
            f"Completed response | "
            f"Status={status_code} "
            f"Duration={process_time:.4f}s"
        )

        if status_code >= 500:
            logger.error(log_message)

        elif status_code >= 400:
            logger.warning(log_message)

        else:
            logger.info(log_message)

        return response
