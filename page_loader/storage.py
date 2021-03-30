from page_loader.request import perform_request
from requests.exceptions import InvalidSchema, MissingSchema
import os


def download_files(files: list[tuple]):
    for file in files:
        try:
            with open(file[1], 'wb') as f:
                f.write(perform_request(file[0]).content)
        except (InvalidSchema, MissingSchema):
            pass


def save_html_page(data, page_name):
    with open(page_name, 'w') as page:
        page.write(data)


def create_directory(dir_path: str) -> None:
    os.mkdir(dir_path, mode=0o777)
