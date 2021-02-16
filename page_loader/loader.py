import requests
import re
import os.path


def get_full_name(url: str, directory: str) -> str:
    without_schema = re.sub(r'http[s]?://', '', url)
    words = list(re.sub(r'[\W_]', ' ', without_schema).rstrip().split(' '))
    file_name = f"{'-'.join(words)}.html"
    full_path = os.path.join(directory, file_name)
    return full_path


def download(url: str, name_dir: str) -> str:
    r = requests.get(url)
    file_name = get_full_name(url, name_dir)
    with open(file_name, 'w') as file:
        file.write(r.text)
    return file_name
