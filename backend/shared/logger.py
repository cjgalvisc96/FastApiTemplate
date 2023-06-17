import logging
from backend.shared import ILogger
class LoggingLogger(ILogger):
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
            level=self._get_level(level=level),
            format=format_,
            datefmt=date_format,
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
