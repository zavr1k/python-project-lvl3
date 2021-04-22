import logging
import os

import requests
from pathlib import Path

from page_loader.storage import save_html_page, \
    download_file
from page_loader.request import perform_request
from page_loader.page_processor import process_page


def download(url: str, destination: str) -> str:
    logging.debug('Checking destination: %s', destination)
    check_access(destination)

    logging.debug('Performing request: %s', url)
    html_page_data = perform_request(url).text

    modified_page, page_path, file_folder_path, resources \
        = process_page(html_page_data, url, destination)

    logging.debug('Resources list: \n%s', '\n\n'.join([
        f'url: {resource_url} \ndestination: {resource_destination}'
        for resource_url, resource_destination in resources
        ]))

    save_html_page(modified_page, page_path)

    if resources:
        Path(file_folder_path).mkdir(exist_ok=True)
        logging.info('Folder was created, path: %s', file_folder_path)

        for resource_url, resource_destination in resources:
            try:
                download_file(resource_url, resource_destination)
                logging.debug('Saving: %s', resource_destination)
            except requests.exceptions.HTTPError as e:
                logging.warning(str(e))
                continue

    return page_path


def check_access(path_dir):
    if not os.path.exists(path_dir):
        raise FileExistsError(f'No such file or directory: {path_dir}')

    if not os.path.isdir(path_dir):
        raise NotADirectoryError(f'Not a directory: {path_dir}')

    if not os.access(path_dir, os.W_OK):
        raise PermissionError(
            f'You not allowed to write in this directory: {path_dir}')
