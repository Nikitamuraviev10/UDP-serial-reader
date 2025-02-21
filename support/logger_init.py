import logging
import sys
from pathlib import Path

def setup_logging():
    """Настройка корневого логгера для всего приложения"""
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)
    

    formatter = logging.Formatter(
        fmt="%(asctime)s | %(name)-25s | %(levelname)-8s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    handlers = [
        logging.FileHandler(
            filename=logs_dir / "app.log",
            encoding="utf-8"
        ),
        logging.StreamHandler(sys.stdout)
    ]


    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    
    for handler in handlers:
        handler.setFormatter(formatter)
        root_logger.addHandler(handler)


    logger = logging.getLogger(__name__)
    logger.info("Logging system initialized")


setup_logging()
