import json
import logging
import traceback
from copy import copy

STRING_FORMATTER_CONFIG = {
    'fmt': '{asctime} {levelprefix}  {message}{extra}{exception}',
    'style': '{',
    'datefmt': '%Y-%m-%dT%H:%M:%S%z',
    '()': 'defix_package_logger.StringFormatter'
}


class StringFormatter(logging.Formatter):
    def formatMessage(self, record: logging.LogRecord) -> str:
        recordcopy = copy(record)
        levelname = recordcopy.levelname
        recordcopy.__dict__["levelprefix"] = levelname + ":"

        extra_obj = {}
        extras = ['msg_code', 'xid', 'initializer', 'service']
        for extra in extras:
            if recordcopy.__dict__.get(extra) is not None:
                extra_obj[extra] = recordcopy.__dict__[extra]

        if len(extra_obj.keys()) > 0:
            recordcopy.__dict__['extra'] = '\n' + \
                json.dumps(extra_obj, indent=2)
        else:
            recordcopy.__dict__['extra'] = ''

        if recordcopy.exc_info:
            exception_info = {
                'type': recordcopy.exc_info[0].__name__,
                'message': str(recordcopy.exc_info[1]),
                'traceback': ''.join(traceback.format_exception(*recordcopy.exc_info))
            }
            recordcopy.__dict__['exception'] = '\nException:\n' + \
                json.dumps(exception_info, indent=2)
        else:
            recordcopy.__dict__['exception'] = ''

        return super().formatMessage(recordcopy)


formatter = StringFormatter(
    fmt=STRING_FORMATTER_CONFIG['fmt'],
    style=STRING_FORMATTER_CONFIG['style'],
    datefmt=STRING_FORMATTER_CONFIG['datefmt']
)
