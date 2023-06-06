import os
from bs4 import BeautifulSoup
from datastuff import datastuff
import pandas as pd
from cdcList3 import cdcList3
def cdcList2(html_path,key_value_list):
    with open(html_path, 'rb') as f:
        html_bytes = f.read()

    # decode the HTML file using utf-16 encoding
    html = html_bytes.decode('utf-16')

    # create a BeautifulSoup object from the HTML
    soup = BeautifulSoup(html, 'html.parser')
    # Find all the <a> links with class="NAV"


    nav_links = soup.find_all('a', class_='NAV')

    # Print the href attributes of the found links
    for link in nav_links:
        href1 = link.get('href')
        cdc_url = html_path.rsplit("/", 1)[0] + "/" + href1.lstrip("./")
        cdcList3(cdc_url,key_value_list)
    return key_value_list
