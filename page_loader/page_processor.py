from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import re
from os import path

RESOURCE_ELEMENTS_ATTRIBUTES_MAP = {
    'img': 'src',
    'link': 'href',
    'script': 'src'
}


def process_page(html, url, destination):
    parsed_url = urlparse(url)
    url_without_scheme = f'{parsed_url.netloc}{parsed_url.path}'

    sanitized_name = _sanitize_string(url_without_scheme)
    page_name = f'{sanitized_name}.html'
    full_page_name = path.join(destination, page_name)
    file_folder_name = f'{path.join(destination, sanitized_name)}_files'

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
        link_path, extension = path.splitext(
            f'{urlparse(absolut_source_link).path}')
        local_link = f'{file_folder_name}/' \
                     f'{_sanitize_string(_cut_string(link_path))}' \
                     f'{extension}'
        element.attrs[source] = local_link
        resources.append((absolut_source_link, local_link))

    modified_page = soup.prettify(formatter='html5')

    return modified_page, full_page_name, file_folder_name, resources


def _retrieve_elements(page_url, soup, resources_to_retrieve):
    resources_to_download = []
    for element in _filter_by_elements(soup, resources_to_retrieve):
        source_link = \
            element.get(RESOURCE_ELEMENTS_ATTRIBUTES_MAP[element.name])
        absolute_source_link = urljoin(page_url, source_link)
        if urlparse(page_url).netloc == urlparse(absolute_source_link).netloc:
            resources_to_download.append(element)
    return resources_to_download


def _cut_string(string):
    if len(string) > 100:
        return string[:100]
    return string


def _sanitize_string(string):
    return re.sub(r'[\W_]', '-', string.strip('/'))


def _filter_by_elements(soup, resources_attributes_map):
    return soup.find_all(
        lambda element:
        element.name in resources_attributes_map and element.get(
            resources_attributes_map[element.name])
    )
