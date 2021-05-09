import os
import tempfile
import pytest
import requests

from pathlib import Path
import requests_mock

from page_loader.loader import download
from page_loader.page_processor import _sanitize_string, process_page


FIXTURE_FOLDER = Path(__file__).parent.absolute().joinpath('fixtures')
HOST = 'https://some.ru'


def _read_file(*path_parts, mode='r'):
    with open(os.path.join(*path_parts), mode) as file:
        return file.read()


def test_invalid_destination():
    with tempfile.TemporaryDirectory() as tempdir:

        with pytest.raises(PermissionError):
            os.chmod(tempdir, 0o400)
            download(HOST, tempdir)

        with tempfile.NamedTemporaryFile() as tem_file:
            with pytest.raises(NotADirectoryError):
                download(HOST, tem_file.name)

        with pytest.raises(FileExistsError):
            download(HOST, 'tempdir')


def test_invalid_url():
    with tempfile.TemporaryDirectory() as tempdir:
        with pytest.raises(requests.exceptions.MissingSchema):
            download('site.ru', tempdir)


def test_connection_error():
    with requests_mock.Mocker() as mock:
        mock.get(HOST, exc=requests.exceptions.ConnectionError)

        with tempfile.TemporaryDirectory() as tempdir:
            with pytest.raises(requests.exceptions.ConnectionError):
                download(HOST, tempdir)


@pytest.mark.parametrize('status_code', [400, 500])
def test_http_error(status_code):
    with requests_mock.Mocker() as mock:
        mock.get(HOST, status_code=status_code)

        with tempfile.TemporaryDirectory() as tempdir:
            with pytest.raises(requests.exceptions.HTTPError):
                download(HOST, tempdir)


def test_string_sanitize():
    assert _sanitize_string('web/page.ru') == 'web-page-ru'
    assert _sanitize_string('some#web!page.ru') == \
           'some-web-page-ru'


def test_page_processor():
    url = f'{HOST}/site'
    destination = 'dest'
    web_page_data = _read_file(FIXTURE_FOLDER, 'web_page.html')

    modified_page_data, page_name, file_folder_path, resources \
        = process_page(web_page_data, url, destination)

    assert page_name == f'{destination}/some-ru-site.html'

    assert file_folder_path == f'{destination}/some-ru-site_files'

    expected_web_page_data = \
        _read_file(FIXTURE_FOLDER, 'expected_web_page.html')

    assert modified_page_data == expected_web_page_data


def test_loader():
    url = f'{HOST}'
    img_url = f'{HOST}/assets/img.png'
    css_url = f'{HOST}/assets/application.css'
    js_url = f'{HOST}/assets/runtime.js'

    data = _read_file(FIXTURE_FOLDER, 'web_page.html')
    img_data = _read_file(FIXTURE_FOLDER, 'assets/img.png', mode='rb')
    css_data = _read_file(FIXTURE_FOLDER, 'assets/application.css', mode='r')
    js_data = _read_file(FIXTURE_FOLDER, 'assets/runtime.js', mode='r')

    with requests_mock.Mocker() as mock:
        mock.get(url, text=data)
        mock.get(img_url, content=img_data)
        mock.get(css_url, text=css_data)
        mock.get(js_url, text=js_data)

        with tempfile.TemporaryDirectory() as tempdir:
            file_path = download(url, tempdir)

            file_folder = os.path.join(tempdir, 'some-ru_files')
            assert file_path.split('/')[-1] == 'some-ru.html'

            assert _read_file(file_folder,
                              'some-ru-assets-img.png',
                              mode='rb'
                              ) == img_data

            assert _read_file(file_folder,
                              'some-ru-assets-application.css',
                              mode='r'
                              ) == css_data

            assert _read_file(file_folder,
                              'some-ru-assets-runtime.js',
                              mode='r'
                              ) == js_data
