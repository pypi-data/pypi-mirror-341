import os
import socket
import traceback
from pythonjsonlogger.json import JsonFormatter
from pythonjsonlogger.core import RESERVED_ATTRS

JSON_FORMATTER_CONFIG = {
    'fmt': '{message}{asctime}{levelno}{exc_info}',
    'style': '{',
    'datefmt': '%Y-%m-%dT%H:%M:%S%z',
    '()': 'pythonjsonlogger.jsonlogger.JsonFormatter',
    'rename_fields': {
        'asctime': 'timestamp',
        'message': 'msg',
        'levelno': 'level',
        'exc_info': 'exception'
    },
    'reserved_attrs': RESERVED_ATTRS+['color_message', 'exc_info'],
    'static_fields': {
        'name': os.getenv('APP_NAME'),
        'pid': os.getpid(),
        'hostname': socket.gethostname()
    }
}


class CustomJsonFormatter(JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super(CustomJsonFormatter, self).add_fields(
            log_record, record, message_dict)

        if record.exc_info:
            log_record['exception'] = {
                'type': record.exc_info[0].__name__,
                'message': str(record.exc_info[1]),
                'traceback': traceback.format_exception(*record.exc_info)
            }


formatter = CustomJsonFormatter(
    JSON_FORMATTER_CONFIG['fmt'],
    style=JSON_FORMATTER_CONFIG['style'],
    static_fields=JSON_FORMATTER_CONFIG['static_fields'],
    rename_fields=JSON_FORMATTER_CONFIG['rename_fields'],
    reserved_attrs=JSON_FORMATTER_CONFIG['reserved_attrs'],
    datefmt=JSON_FORMATTER_CONFIG['datefmt']
)
