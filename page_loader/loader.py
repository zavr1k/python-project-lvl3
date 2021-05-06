import logging
import os
from pathlib import Path

import requests
from progress.bar import Bar

from page_loader.page_processor import process_page
from page_loader.request import perform_request
from page_loader.storage import save_html_page, \
    download_file


def download(url: str, destination: str) -> str:
    logging.debug('Checking destination: %s', destination)
    check_access(destination)

    html_page_data = perform_request(url).text

    modified_page, page_path, file_folder_path, resources \
        = process_page(html_page_data, url, destination)

    number_of_resources = len(resources)

    logging.debug('Resources list (%s): \n%s', number_of_resources,
                  '\n\n'.join([
                      f'url: {resource_url} '
                      f'\ndestination: {resource_destination}'
                      for resource_url, resource_destination in resources
                    ]))

    with Bar('Processing', max=number_of_resources + 1) as bar:

        save_html_page(modified_page, page_path)
        bar.next()

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
                finally:
                    bar.next()

    return page_path


def check_access(path_dir):
    if not os.path.exists(path_dir):
        raise FileExistsError(f'No such file or directory: {path_dir}')

    if not os.path.isdir(path_dir):
        raise NotADirectoryError(f'Not a directory: {path_dir}')

    if not os.access(path_dir, os.W_OK):
        raise PermissionError(
            f'You not allowed to write in this directory: {path_dir}')
