import logging

logging.basicConfig(
    name="BackendLogger",
    filename="logs.txt",
    filemode="a",
    level=logging.INFO,
    format="%(asctime)s | %(name)s | %(levelname)s | %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
)
logger = logging.getLogger()

import logging

from src.contexts.shared.domain import Logger


class LoggingLogger(Logger):
    def __init__(
        self,
        *,
        name: str,
        filename: str,
        filemode: str,
        level: str,
        format_: str,
        date_format: str,
    ) -> None:
        logging.basicConfig(
            filename=filename,
            filemode=filemode,
            format=format_,
            datefmt=date_format,
            level=self._get_level(level=level),
        )
        self.logger = logging.getLogger(name=name)

    @staticmethod
    def _get_level(level: str) -> int:
        return {
            "debug": logging.DEBUG,
            "error": logging.ERROR,
            "info": logging.INFO,
        }.get(level, logging.DEBUG)

    def debug(self, *, message: str):
        self.logger.debug(message)

    def error(self, *, message: str):
        self.logger.error(message)

    def info(self, *, message: str):
        self.logger.info(message)


logger = LoggingLogger(
    name="BackendLogger",
    filename="logs.txt",
    filemode="a",
    level=logging.INFO,
    format="%(asctime)s | %(name)s | %(levelname)s | %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
)
