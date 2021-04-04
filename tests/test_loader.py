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
        assert link == f'{HOST}/assets/img.png'
        assert local_link == f'{destination}' \
                             f'/some-ru-site_files/assets-img.png'
        assert modified_page == _read_file(FIXTURE_FOLDER,
                                           'expected_web_page.html')


def test_loader():
    url = f'{HOST}'
    img_url = f'{HOST}/assets/img.png'

    data = _read_file(FIXTURE_FOLDER, 'web_page.html')
    img_data = _read_file(FIXTURE_FOLDER, 'assets/img.png', mode='rb')

    with requests_mock.Mocker() as mock:
        mock.get(url, text=data)
        mock.get(img_url, content=img_data)
        with tempfile.TemporaryDirectory() as tempdir:
            file_path = download(url, tempdir)

            file_folder = os.path.join(tempdir, 'some-ru_files')
            assert file_path.split('/')[-1] == 'some-ru.html'
            assert _read_file(file_folder, 'assets-img.png', mode='rb') == \
                   img_data
