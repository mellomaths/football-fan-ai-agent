import logging


def create_logger(
    name: str,
    add_console_handler: bool = True,
    add_file_handler: bool = True,
) -> logging.Logger:
    """
    Create a custom logger for the application.
    The logger will log messages to both the console and a file.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)  # capture all levels DEBUG and above
    formatter = logging.Formatter(
        fmt="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    if logger.hasHandlers():
        # If the logger already has handlers, remove them to avoid duplicate logs
        for handler in logger.handlers[:]:
            logger.removeHandler(handler)

    # Console handler
    if add_console_handler:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)  # only INFO and above on console
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    # File handler
    if add_file_handler:
        file_handler = logging.FileHandler("app.log", mode="a")
        file_handler.setLevel(logging.DEBUG)  # log everything into the file
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger
