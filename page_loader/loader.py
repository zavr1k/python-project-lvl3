from page_loader.storage import save_html_page, \
    download_files, create_directory
from page_loader.request import perform_request
from page_loader.page_processor import process_page


def download(url: str, destination: str) -> str:
    html_page_data = perform_request(url).text

    modified_page, full_page_name, file_folder_name, files_to_download \
        = process_page(html_page_data, url, destination)

    create_directory(file_folder_name)
    download_files(files_to_download)
    save_html_page(modified_page, full_page_name)

    return full_page_name


# URL = 'https://ekobeton35.ru/'
# URL = 'https://bravobeton.com'
# URL = 'https://ru.hexlet.io/'
# URL = 'https://wiki.manjaro.org/index.php/Main_Page'
#
# download(URL, '/home/santon')
