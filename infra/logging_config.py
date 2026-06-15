# infra/logging_config.py

import logging
from pathlib import Path
from logging.handlers import RotatingFileHandler
from infra.app_paths import change_root_folder


def configure_logging():

    # log_dir = get_app_data_folder() / "logs"
    log_dir = change_root_folder("logs")
    log_dir.mkdir(parents=True, exist_ok=True)

    log_file = log_dir / "application.log"

    handler = RotatingFileHandler(
        filename=log_file,
        maxBytes=5_000_000,
        backupCount=10,
        encoding="utf-8"
    )

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    handler.setFormatter(formatter)

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)

    if not root_logger.handlers:
        root_logger.addHandler(handler)

        