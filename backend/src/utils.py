import logging
import logging.config
from pathlib import Path

import yaml


def setup_logging() -> None:
    config_file = (get_backend_root_directory() / "log_config.yaml").resolve()
    logging.info(f"loading logging config from {config_file=}")
    with open(config_file, "r") as file:
        config = yaml.safe_load(file)
        logging.config.dictConfig(config)
    logging.info("logging module configured")


def get_backend_root_directory() -> Path:
    """Returns the backend service root directory path."""
    # return (get_project_root_directory() / "backend").resolve()
    return Path(__file__).parent.parent.resolve()


def get_project_root_directory() -> Path:
    """Returns the project root directory path."""
    return Path(__file__).parent.parent.parent.resolve()


def get_all_subclasses(cls):
    return set(cls.__subclasses__()).union(
        [s for c in cls.__subclasses__() for s in get_all_subclasses(c)]
    )
