import argparse
import os


def init_argparse():
    parser = argparse.ArgumentParser(description="Page loader")
    parser.add_argument('url', type=str)
    parser.add_argument('--output', type=str,
                        help='Path to directory',
                        default=os.getcwd())
    return parser
