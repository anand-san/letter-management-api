import sys
from loguru import logger


def setup_logging():
    logger.remove()  # Remove default handler
    logger.add(
        sys.stderr,
        format="{time} {level} {message}",
        filter="my_rag_project",
        level="INFO",
    )
    logger.add(
        "logs/file_{time}.log",
        rotation="500 MB",
        retention="10 days",
        format="{time} {level} {message}",
        filter="my_rag_project",
        level="DEBUG",
    )


# Call this function at the start of your application
setup_logging()
