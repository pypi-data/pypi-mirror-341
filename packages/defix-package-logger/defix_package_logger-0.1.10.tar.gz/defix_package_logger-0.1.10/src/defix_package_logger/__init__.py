import os
import logging
from .json_formatter import formatter as json_formatter, JSON_FORMATTER_CONFIG
from .string_formatter import formatter as string_formatter, StringFormatter, STRING_FORMATTER_CONFIG

is_local = os.getenv('ENV') in ['local', None, '']

logger = logging.getLogger()
logger.setLevel(logging.DEBUG if os.getenv('LOG_DEBUG') else logging.INFO)

log_handler = logging.StreamHandler()
log_handler.setFormatter(string_formatter if is_local else json_formatter)

logger.addHandler(log_handler)

FORMATTER_CONFIG = STRING_FORMATTER_CONFIG if is_local else JSON_FORMATTER_CONFIG

__all__ = ['logger', 'StringFormatter', 'FORMATTER_CONFIG']
