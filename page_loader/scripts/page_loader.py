#!usr/bin/env python
import logging
import sys

from page_loader.cli import init_argparse
from page_loader.loader import download
from page_loader.logger import setup_logger


def _parse_arguments():
    parser = init_argparse()
    args = parser.parse_args()

    return args.url, args.output, args.log_level


def main():
    url, output, log_level = _parse_arguments()
    setup_logger(log_level)
    try:
        file_path = download(url, output)
        logging.info('Page was downloaded: %s', file_path)
        print(file_path)
    except Exception as e:
        logging.error(e)
        sys.exit(1)


if __name__ == '__main__':
    main()
