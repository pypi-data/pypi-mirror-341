import os
import sys
import logging
import colorlog
from logging import handlers
from typing import Optional, TypeVar, cast

SUCCESS = 25
logging.addLevelName(SUCCESS, "SUCCESS")


class Logger(logging.Logger):
    def success(self, msg, *args, **kwargs):
        if self.isEnabledFor(SUCCESS):
            self._log(SUCCESS, msg, args, **kwargs)


logging.setLoggerClass(Logger)
LoggerType = TypeVar("LoggerType", bound=Logger)


def _set_console_handler(_logger: Logger, console_level: str,
                         console_fmt: str) -> Logger:
    console_handler = logging.StreamHandler()
    console_handler.setLevel(console_level)
    green = {
        "DEBUG": "green",
        "INFO": "green",
        "SUCCESS": "green",
        "WARNING": "green",
        "ERROR": "green",
        "CRITICAL": "green",
    }
    bold_cyan = {
        "DEBUG": "bold_cyan",
        "INFO": "bold_cyan",
        "SUCCESS": "bold_cyan",
        "WARNING": "bold_cyan",
        "ERROR": "bold_cyan",
        "CRITICAL": "bold_cyan",
    }
    log_colors = {
        "DEBUG": "light_blue",
        "INFO": "light_white",
        "SUCCESS": "light_green",
        "WARNING": "light_yellow",
        "ERROR": "light_red",
        "CRITICAL": "bg_red,light_white",
    }
    secondary_log_colors = dict(
        asctime=green,
        name=bold_cyan,
        levelname=log_colors,
        process=bold_cyan,
        processName=bold_cyan,
        thread=bold_cyan,
        threadName=bold_cyan,
        pathname=bold_cyan,
        funcName=bold_cyan,
        lineno=bold_cyan,
        message=log_colors,
    )
    console_formatter = colorlog.ColoredFormatter(
        console_fmt,
        secondary_log_colors=secondary_log_colors,
    )
    console_handler.setFormatter(console_formatter)
    _logger.addHandler(console_handler)
    return _logger


def _set_file_handler(_logger: Logger, file_level: str,
                      file_path: str, file_mode: str, file_max_bytes: int, file_backup_count: int, file_encoding: str,
                      file_fmt: str) -> Logger:
    file_handler = handlers.RotatingFileHandler(
        file_path,
        mode=file_mode, maxBytes=file_max_bytes, backupCount=file_backup_count, encoding=file_encoding
    )
    file_handler.setLevel(file_level)
    file_formatter = logging.Formatter(file_fmt)
    file_handler.setFormatter(file_formatter)
    _logger.addHandler(file_handler)
    return _logger


def get_logger(
        name: Optional[str] = None,
        level: str = "DEBUG",
        to_console: bool = True,
        console_level: str = "DEBUG",
        console_fmt: str = (
                "%(asctime_log_color)s%(asctime)s %(reset)s| "
                "%(name_log_color)s%(name)s %(reset)s| "
                "%(levelname_log_color)s%(levelname)s %(reset)s| "
                # "%(process_log_color)sProcess: %(process)d %(processName_log_color)s(%(processName)s) %(reset)s| "
                # "%(thread_log_color)sThread: %(thread)d %(threadName_log_color)s(%(threadName)s) %(reset)s| "
                # "%(pathname_log_color)s%(pathname)s %(reset)s| "
                "%(funcName_log_color)s%(funcName)s:%(lineno)d %(reset)s- "
                "%(message_log_color)s%(message)s"
        ),
        to_file: bool = False,
        file_level: str = "DEBUG",
        file_path: Optional[str] = None,
        file_mode: str = "a",
        file_max_bytes: int = 10 * 1024 * 1024,
        file_backup_count: int = 20,
        file_encoding: str = "utf8",
        file_fmt: str = (
                "%(asctime)s | "
                "%(name)s | "
                "%(levelname)s | "
                # "Process: %(process)d (%(processName)s) | "
                # "Thread: %(thread)d (%(threadName)s) | "
                # "%(pathname)s | "
                "%(funcName)s:%(lineno)d - "
                "%(message)s"
        ),
) -> Logger:
    _path = os.path.abspath(sys.argv[0])
    _name = os.path.basename(_path)
    _prefix = os.path.splitext(_name)[0]
    _file_name = _prefix + ".log"
    _file_dir = os.path.dirname(_path)
    _file_path = os.path.join(_file_dir, _file_name)

    if name is None:
        name = _prefix
    _logger = cast(LoggerType, logging.getLogger(name))
    _logger.setLevel(level)

    if to_console:
        console_handler_exists = any(isinstance(handler, logging.StreamHandler) for handler in _logger.handlers)
        if not console_handler_exists:
            _set_console_handler(_logger,
                                 console_level=console_level,
                                 console_fmt=console_fmt)
    else:
        for handler in _logger.handlers:
            if isinstance(handler, logging.StreamHandler):
                _logger.removeHandler(handler)

    if to_file:
        file_handler_exists = any(isinstance(handler, handlers.RotatingFileHandler) for handler in _logger.handlers)
        if not file_handler_exists:
            if file_path is None:
                file_path = _file_path
            _set_file_handler(_logger,
                              file_level=file_level,
                              file_path=file_path, file_mode=file_mode, file_max_bytes=file_max_bytes,
                              file_backup_count=file_backup_count, file_encoding=file_encoding,
                              file_fmt=file_fmt)
    else:
        for handler in _logger.handlers:
            if isinstance(handler, logging.FileHandler):
                _logger.removeHandler(handler)

    return _logger


logger = get_logger()

__all__ = [
    "Logger",
    "get_logger",
    "logger"
]
