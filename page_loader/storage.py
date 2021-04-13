from page_loader.request import perform_request
import os
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter(
    '%(levelname)s:%(asctime)s:%(filename)s:%(funcName)s:%(message)s')

file_handler = logging.FileHandler('debug.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


def download_files(files: list[tuple]):
    for file in files:
        response = perform_request(file[0])
        if response.encoding is not None:
            mode = 'w'
            resource_data = response.text
        else:
            mode = 'wb'
            resource_data = response.content
        with open(file[1], mode) as f:
            f.write(resource_data)


def save_html_page(data, page_name):
    with open(page_name, 'w') as page:
        page.write(data)


def create_directory(dir_path: str) -> None:
    try:
        os.mkdir(dir_path, mode=0o777)
        logger.info("File %s was created", dir_path)
    except FileExistsError:
        logger.warning("File %s already exists", dir_path)
        pass
