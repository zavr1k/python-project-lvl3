from bs4 import BeautifulSoup
from urllib.parse import urlparse
import re
from os import path


def process_page(html, url, destination):
    parsed_url = urlparse(url)
    url_without_scheme = f'{parsed_url.netloc}{parsed_url.path}'

    sanitized_name = _sanitize_string(url_without_scheme)
    page_name = f'{sanitized_name}.html'
    full_page_name = path.join(destination, page_name)
    file_folder_name = f'{path.join(destination, sanitized_name)}_files'

    resources = []

    soup = BeautifulSoup(html, 'html.parser')

    img_tags = soup.find_all('img')
    for tag in img_tags:
        link = tag.attrs['src']
        parsed_link = urlparse(link)
        link_path, extension = path.splitext(
            f'{parsed_link.netloc}{parsed_link.path}')
        if len(link_path) > 80:
            link_path = _cut_string(link_path)
        local_link = f'{file_folder_name}/' \
                     f'{_sanitize_string(link_path)}{extension}'
        tag.attrs['src'] = local_link
        resources.append((link, local_link))

    modified_page = soup.prettify(formatter='html5')

    return modified_page, full_page_name, file_folder_name, resources


def _sanitize_string(string):
    return re.sub(r'[\W_]', '-', string.strip('/'))


def _cut_string(string):
    return string[:80]
