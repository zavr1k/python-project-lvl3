import os
import tempfile

import requests
import requests_mock

from page_loader.loader import download


def _read_file(*path_parts, mode='r'):
    with open(os.path.join(*path_parts), mode) as file:
        return file.read()


def test_loader():
    url = 'https://test.ru/some-free_courses'
    with requests_mock.Mocker() as mock:
        mock.get(url, text="TEST")
        with tempfile.TemporaryDirectory() as tempdir:
            file_path = download(url, tempdir)
            assert 'test-ru-some-free-courses.html' == file_path.split('/')[-1]
            page = requests.get('https://test.ru/some-free_courses')
            assert _read_file(file_path) == page.text
