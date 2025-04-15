import logging
import os


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger that is disabled by default but can be enabled via environment variables.

    To enable logging for a specific logger, set the environment variable:
    LOG_{LOGGER_NAME_UPPERCASE}=1

    Example: For logger "composable_dataloader", set LOG_COMPOSABLE_DATALOADER=1

    Args:
        name: Name of the logger

    Returns:
        logger: Logger instance
    """
    logger = logging.getLogger(name)

    env_var_name = f"LOG_{name.upper()}"

    if os.environ.get(env_var_name):
        # Set up normal handler if environment variable is set
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    else:
        # Use NullHandler by default (suppress logs)
        logger.addHandler(logging.NullHandler())
        logger.setLevel(logging.WARNING)

    return logger


logger = get_logger("composable_dataloader")  # singleton logger instance
