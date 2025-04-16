from defix_package_logger import logger


def main():
    logger.error('Logging', extra={
        'msg_code': 'CRITICAL_ERROR'
    } | {'xid': '-'})


if __name__ == "__main__":
    main()
