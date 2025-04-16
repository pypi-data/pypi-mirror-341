import logging
from logging.handlers import SocketHandler, RotatingFileHandler
from pathlib import Path
import shutil
import os

# log_level = {
#     "debug": logging.DEBUG,
#     "info": logging.INFO,
#     "warning": logging.WARNING,
#     "error": logging.ERROR,
#     "critical": logging.CRITICAL,
# }


class Settings:
    path: Path = Path("./logs")

    filehandler_separated: bool = False
    filehandler_separated_level: int = logging.DEBUG

    filehandler_all: bool = False
    filehandler_all_level: int = logging.DEBUG

    streamhandler: bool = False
    streamhandler_level: int = logging.INFO

    cutelog: bool = True
    cutelog_settings: str = f"127.0.0.1:19996"
    cutelog_level: int = logging.DEBUG


__init = False
__path: Path | None = None
__socket_handler: logging.Handler | None = None


def init():
    global __path
    global __socket_handler
    global __init

    if Settings.filehandler_separated or Settings.filehandler_all:
        __path = Path(Settings.path)
        Path(__path).mkdir(parents=True, exist_ok=True)
        files = os.listdir(__path)

        for file in files:
            if file != ".gitkeep":
                try:
                    shutil.rmtree(__path / file, ignore_errors=True)
                except:
                    os.remove(__path / file)

    if Settings.cutelog:
        ip = Settings.cutelog_settings.split(":")[0]
        port = int(Settings.cutelog_settings.split(":")[1])
        __socket_handler = SocketHandler(ip, port)
        __socket_handler.setLevel(Settings.cutelog_level)

    __init = True


def get_logger(name: str) -> logging.Logger:
    if not __init:
        init()

    if logging.Logger.manager.loggerDict.get(name):
        return logging.Logger.manager.loggerDict.get(name)

    formatter = logging.Formatter(f"%(asctime)s %(levelname)-8s: {name}: %(message)s")

    # noinspection PyShadowingNames
    log = logging.getLogger(name)
    log.setLevel(logging.DEBUG)

    if Settings.cutelog:
        log.addHandler(__socket_handler)

    if Settings.filehandler_separated:
        path = __path / f"{name}.log"
        file_handler = RotatingFileHandler(filename=path, mode="a", encoding="utf-8")
        file_handler.setFormatter(formatter)
        file_handler.setLevel(Settings.filehandler_separated_level)
        log.addHandler(file_handler)

    if Settings.filehandler_all:
        path = __path / f"All.log"
        file_handler_all = RotatingFileHandler(filename=path, mode="a", encoding="utf-8")
        file_handler_all.setFormatter(formatter)
        file_handler_all.setLevel(Settings.filehandler_all_level)
        log.addHandler(file_handler_all)

    if Settings.streamhandler:
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        stream_handler.setLevel(Settings.streamhandler_level)
        log.addHandler(stream_handler)

    return log




