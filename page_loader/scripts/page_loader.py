#!usr/bin/env python
from page_loader.cli import init_argparse
from page_loader.loader import download


def main():
    parser = init_argparse()
    args = parser.parse_args()
    print(download(args.url, args.output))


if __name__ == "__main__":
    main()
