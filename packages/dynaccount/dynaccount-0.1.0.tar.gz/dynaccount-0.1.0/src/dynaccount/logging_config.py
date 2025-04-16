import logging

def setup_logger(name, log_level='INFO'):
    log_levels = {
        'DEBUG': logging.DEBUG,
        'INFO': logging.INFO,
        'WARNING': logging.WARNING,
        'ERROR': logging.ERROR,
        'CRITICAL': logging.CRITICAL
    }
    log_level = log_levels.get(log_level.upper(), logging.INFO)

    logger = logging.getLogger(name)
    logger.setLevel(log_level)
    handler = logging.FileHandler('dynaccount.log')
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger