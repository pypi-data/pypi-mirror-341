from defix_package_logger import logger


def main():
    logger.error('Logging', exc_info=ValueError('val'), extra={
        'msg_code': 'CRITICAL_ERROR'
    } | {'xid': '-', 'custom': 'cus', 'custom': {'22': '12'}})


if __name__ == "__main__":
    main()
