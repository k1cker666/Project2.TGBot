import inspect
import logging

from loguru import logger


class InterceptHandler(logging.Handler):
    def emit(self, record: logging.LogRecord) -> None:

        level: str | int
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        frame, depth = inspect.currentframe(), 0
        while frame and (
            depth == 0 or frame.f_code.co_filename == logging.__file__
        ):
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )


logget_config = logging.basicConfig(
    handlers=[InterceptHandler()], level=logging.INFO, force=True
)
logger_httpx = logging.getLogger("httpx").setLevel(logging.WARNING)
logger_main = logging.getLogger(__name__)
