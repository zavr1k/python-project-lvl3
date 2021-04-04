from page_loader.request import perform_request
import os


def download_files(files: list[tuple]):
    for file in files:
        response = perform_request(file[0])
        if response.encoding == 'utf-8':
            mode = 'w'
        else:
            mode = 'wb'
        with open(file[1], mode) as f:
            f.write(response.content)


def save_html_page(data, page_name):
    with open(page_name, 'w') as page:
        page.write(data)


def create_directory(dir_path: str) -> None:
    os.mkdir(dir_path, mode=0o777)
