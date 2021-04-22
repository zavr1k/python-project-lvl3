from page_loader.request import perform_request


def download_file(resource_url, resource_destination):
    response = perform_request(resource_url)

    if response.encoding is not None:
        mode = 'w'
        resource_data = response.text
    else:
        mode = 'wb'
        resource_data = response.content
    with open(resource_destination, mode) as f:
        f.write(resource_data)


def save_html_page(data, page_name):
    with open(page_name, 'w') as page:
        page.write(data)
