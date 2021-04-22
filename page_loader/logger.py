import logging


def setup_logger(level):
    logging.basicConfig(
        level=level,
        format='[%(asctime)s] [%(levelname)s] [%(filename)s]: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
