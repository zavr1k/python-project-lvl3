import logging
import re
from os import path
from urllib.parse import urlparse, urljoin

from bs4 import BeautifulSoup

RESOURCE_ELEMENTS_ATTRIBUTES_MAP = {
    'img': 'src',
    'link': 'href',
    'script': 'src'
}


def process_page(html, url, destination):
    logging.debug('Start page process url - %s, destination - %s',
                  url, destination)

    parsed_url = urlparse(url)
    url_without_scheme = f'{parsed_url.netloc}{parsed_url.path}'
    sanitized_name = _sanitize_string(url_without_scheme)
    page_name = f'{sanitized_name}.html'
    logging.debug('Page name: %s', page_name)

    page_path = path.join(destination, page_name)
    logging.debug('Page path: %s', page_path)

    file_folder_name = f'{sanitized_name}_files'
    logging.debug('Files folder name: %s', file_folder_name)

    file_folder_path = path.join(destination, file_folder_name)
    logging.debug('File folder path: %s', file_folder_path)

    resources = []

    soup = BeautifulSoup(html, 'html.parser')

    resources_to_download = _retrieve_elements(
        url,
        soup,
        RESOURCE_ELEMENTS_ATTRIBUTES_MAP
    )
    for element in resources_to_download:
        source = RESOURCE_ELEMENTS_ATTRIBUTES_MAP[element.name]
        source_link = element.get(source)
        absolut_source_link = urljoin(url, source_link)

        parsed_source_link = urlparse(absolut_source_link)
        link_path, extension = path.splitext(
            f'{parsed_source_link.netloc}{parsed_source_link.path}')

        file_name = f'{_sanitize_string(link_path)[:100]}' \
                    f'{extension}'
        local_link = path.join(file_folder_name, file_name)

        element.attrs[source] = local_link
        resource_local_path = path.join(destination, local_link)
        resources.append((absolut_source_link, resource_local_path))

    modified_page = soup.prettify(formatter='html5')

    return modified_page, page_path, file_folder_path, resources


def _retrieve_elements(page_url, soup, resources_to_retrieve):
    resources_to_download = []
    for element in _filter_by_elements(soup, resources_to_retrieve):
        source_link = \
            element.get(resources_to_retrieve[element.name])

        absolute_source_link = urljoin(page_url, source_link)
        parsed_page_url = urlparse(page_url)
        parsed_source_link = urlparse(absolute_source_link)
        if not parsed_page_url.netloc == parsed_source_link.netloc:
            logging.warning('%s is external, skipping',
                            absolute_source_link)
        elif parsed_source_link.path in {'', '/'}:
            logging.warning('%s is page link, skipping ',
                            absolute_source_link)
        else:
            resources_to_download.append(element)
            logging.info('%s added to download list',
                         absolute_source_link)
    return resources_to_download


def _sanitize_string(string):
    return re.sub(r'[\W_]', '-', string.strip('/'))


def _filter_by_elements(soup, resources_attributes_map):
    return soup.find_all(
        lambda element:
        element.name in resources_attributes_map and element.get(
            resources_attributes_map[element.name])
    )
