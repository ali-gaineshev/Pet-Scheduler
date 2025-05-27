# app/config/logger_config

import logging


def setup_logger(name, debug_enabled=False):
    # Create logger
    logger = logging.getLogger(name)

    if debug_enabled:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)  # Set a higher level to ignore debug messages

    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG if debug_enabled else logging.INFO)

    formatter = logging.Formatter("%(name)s  -- [%(asctime)s] - %(levelname)s - %(message)s", "%d/%b/%Y %H:%M:%S")
    ch.setFormatter(formatter)

    logger.addHandler(ch)

    return logger

# Example usage:
DEBUG_ENABLED = True  # or False, depending on whether you want to enable debug logging
LOGGER = setup_logger('my_logger', debug_enabled=DEBUG_ENABLED)
LOGGER.debug('This is a debug message')
LOGGER.info('This is an info message')
LOGGER.error('This is an error message')
