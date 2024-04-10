from loguru import logger

logger.add(format="{time} {level} {message}", level="INFO")
