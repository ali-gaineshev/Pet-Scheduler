# app/config/logger_config

import logging


class CustomHandler(logging.StreamHandler):
    def emit(self, record):
        if record.levelno == logging.ERROR:
            record.exc_info = True
        super().emit(record)


def setup_logger(name):
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    ch = CustomHandler()
    ch.setLevel(logging.DEBUG)

    formatter = logging.Formatter("%(name)s  -- [%(asctime)s] - %(levelname)s - %(message)s", "%d/%b/%Y %H:%M:%S")
    ch.setFormatter(formatter)

    logger.addHandler(ch)

    return logger
