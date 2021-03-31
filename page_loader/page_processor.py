from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import re
from os import path

RESOURCE_ELEMENTS_ATTRIBUTES_MAP = {
    'img': 'src'
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

    img_tags = _filter_by_elements(soup, RESOURCE_ELEMENTS_ATTRIBUTES_MAP)
    for tag in img_tags:
        source_link = tag.get(RESOURCE_ELEMENTS_ATTRIBUTES_MAP[tag.name])
        absolute_source_link = urljoin(url, source_link)
        parsed_source_link = urlparse(absolute_source_link)
        link_path, extension = path.splitext(f'{parsed_source_link.path}')
        local_link = f'{file_folder_name}/' \
                     f'{_sanitize_string(_cut_string(link_path))}{extension}'
        tag.attrs['src'] = local_link
        resources.append((absolute_source_link, local_link))

    modified_page = soup.prettify(formatter='html5')

    return modified_page, full_page_name, file_folder_name, resources


def _cut_string(string):
    if len(string) > 100:
        return string[:100]
    return string


def _sanitize_string(string):
    return re.sub(r'[\W_]', '-', string.strip('/'))


def _filter_by_elements(soup, resources_attributes_map):
    return soup.find_all(
        lambda element: element.name in resources_attributes_map and element.get(
            resources_attributes_map[element.name]
        )
    )
