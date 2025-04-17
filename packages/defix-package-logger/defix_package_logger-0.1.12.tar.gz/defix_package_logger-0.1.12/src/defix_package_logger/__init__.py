import os
import logging
from .json_formatter import formatter as json_formatter, JSON_FORMATTER_CONFIG
from .string_formatter import formatter as string_formatter, StringFormatter, STRING_FORMATTER_CONFIG

is_local = os.getenv('ENV') in ['local', None, '']

logger = logging.getLogger()
logger.setLevel(logging.DEBUG if os.getenv('LOG_DEBUG') else logging.INFO)

log_handler = logging.StreamHandler()

if is_local:
    original_makeRecord = logging.Logger.makeRecord

    def make_record_with_extra(self, name, level, fn, lno, msg, args, exc_info, func=None, extra=None, sinfo=None):
        record = original_makeRecord(
            self, name, level, fn, lno, msg, args, exc_info, func, extra, sinfo)
        record._extra = extra
        return record

    logging.Logger.makeRecord = make_record_with_extra

    log_handler.setFormatter(string_formatter)
else:
    log_handler.setFormatter(json_formatter)

logger.addHandler(log_handler)

FORMATTER_CONFIG = STRING_FORMATTER_CONFIG if is_local else JSON_FORMATTER_CONFIG

__all__ = ['logger', 'StringFormatter', 'FORMATTER_CONFIG']
