def download_pag_to_file(file_path, soup):
    with open(file_path, "w") as textfile:
        textfile.write(soup.prettify().encode('utf8'))

