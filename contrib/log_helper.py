def log_error(error):
    import logging
    logger = logging.getLogger('django')
    logger.exception(error)


def log_tests(error):
    import logging
    logger = logging.getLogger('tests')
    logger.exception(error)