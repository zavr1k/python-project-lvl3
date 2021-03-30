import os
import tempfile

from pathlib import Path
import requests_mock

from page_loader.loader import download
from page_loader.page_processor import _sanitize_string, process_page

FIXTURE_FOLDER = Path(__file__).parent.absolute().joinpath('fixtures')
HOST = 'https://some.ru'


def _read_file(*path_parts, mode='r'):
    with open(os.path.join(*path_parts), mode) as file:
        return file.read()


def test_string_sanitize():
    assert _sanitize_string('web/page.ru') == 'web-page-ru'
    assert _sanitize_string('some#web!page.ru') == \
           'some-web-page-ru'


def test_page_processor():
    url = f'{HOST}/site'
    destination = 'dest'
    web_page_data = _read_file(FIXTURE_FOLDER, 'web_page.html')

    modified_page, page_name, file_folder_name, resources \
        = process_page(web_page_data, url, destination)

    assert page_name == f'{destination}/some-ru-site.html'
    assert file_folder_name == f'{destination}/some-ru-site_files'
    for link, local_link in resources:
        assert link == 'assets/img.png'
        assert local_link == f'{destination}' \
                             f'/some-ru-site_files/assets-img.png'
        assert modified_page == _read_file(FIXTURE_FOLDER,
                                           'expected_web_page.html')
        print(resources)


def test_loader():
    url = f'{HOST}/site'
    with requests_mock.Mocker() as mock:
        mock.get(url, text=_read_file(os.path.join(FIXTURE_FOLDER,
                                                   'web_page.html')))
        with tempfile.TemporaryDirectory() as tempdir:
            file_path = download(url, tempdir)
            assert 'some-ru-site.html' == file_path.split('/')[-1]
            assert os.access(file_path, os.R_OK)
