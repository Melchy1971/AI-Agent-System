from __future__ import annotations
import logging
import logging.config
from pathlib import Path
import yaml


def setup_logging(config_path: str = "config/logging.yaml") -> None:
    path = Path(config_path)
    if path.exists():
        with path.open() as f:
            cfg = yaml.safe_load(f)
        logging.config.dictConfig(cfg)
    else:
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        )


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)
