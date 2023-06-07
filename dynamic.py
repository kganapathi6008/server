import os
from bs4 import BeautifulSoup
from datastuff import datastuff
import pandas as pd
import zipfile
import shutil
from datetime import datetime

from automation101 import get_urls


def dynamic(fileUrl, folder_path, filename):
    modified_fileUrl = fileUrl + "/data_aq/ext_grp/extgrp-list.htm"
    html_path = modified_fileUrl

    with open(html_path, 'rb') as f:
        html_bytes = f.read()

    # decode the HTML file using utf-16 encoding
    html = html_bytes.decode('utf-16')

    # create a BeautifulSoup object from the HTML
    soup = BeautifulSoup(html, 'html.parser')
    # Find all the <a> links with class="NAV"

    html_paths = []
    nav_links = soup.find_all('a', class_='NAV')
    for link in nav_links:
        href1 = link.get('href')
        fileUrl1 = html_path.rsplit("/", 1)[0] + "/" + href1.lstrip("./")
        html_paths.append(fileUrl1)

    # Create a new folder with the desired name and current timestamp
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    new_folder_name = f"{filename}_extract_{timestamp}"
    new_folder_path = os.path.join(folder_path, new_folder_name)
    os.makedirs(new_folder_path, exist_ok=True)

    get_urls(html_paths, new_folder_path, fileUrl)

    # Zip the folder at new_folder_path
    zip_path = os.path.join(folder_path, f"{filename}_extract_{timestamp}.zip")
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(new_folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                arc_name = os.path.relpath(file_path, new_folder_path)
                zipf.write(file_path, arcname=arc_name)

    # Delete the 'extract' folder
    shutil.rmtree(new_folder_path)



    return zip_path
