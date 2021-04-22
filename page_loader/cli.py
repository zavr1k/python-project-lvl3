import argparse
import os


def init_argparse():
    parser = argparse.ArgumentParser(description="Page loader")
    parser.add_argument('url', type=str)
    parser.add_argument('--output', '-o',
                        type=str,
                        help='Path to directory',
                        default=os.getcwd())
    parser.add_argument('--log-level',
                        type=str,
                        help='Set level for logger',
                        default='ERROR',
                        choices={'DEBUG', 'INFO', 'WARNING'}
                        )
    return parser
