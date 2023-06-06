import os
from bs4 import BeautifulSoup
from datastuff import datastuff
import pandas as pd
def cdcList3(html_path,key_value_list):
    with open(html_path, 'rb') as f:
        html_bytes = f.read()

    # decode the HTML file using utf-16 encoding
    html = html_bytes.decode('utf-16')

    # create a BeautifulSoup object from the HTML
    soup = BeautifulSoup(html, 'html.parser')
    # find the second frame tag
    frame2 = soup.find_all('frame')[1]

    if frame2 is not None:
        # get the src attribute of the second frame tag
        frame2_src = frame2['src']

        # read the HTML file pointed to by the src attribute
        with open(os.path.join(os.path.dirname(html_path), frame2_src), 'rb') as f:
            frame2_bytes = f.read()

        # decode the HTML file using utf-16 encoding
        frame2_html = frame2_bytes.decode('utf-16')

        # create a BeautifulSoup object from the HTML in the second frame
        frame2_soup = BeautifulSoup(frame2_html, 'html.parser')

        # find the table tag that follows the "USER DEFINED FUNCTIONS" anchor tag
        references_anchor = frame2_soup.find('a', {'name': 'GENERAL'})
        general_anchor = frame2_soup.find('a', {'name': 'OUTPUT'})
        if general_anchor is not None:
            general_table = general_anchor.find_next('table')

            # get the data rows for the required columns
            required_ths = ["Table:"]
            cdc_key=''
            cdc_value=''
            data_rows = []
            allow_null_values = ""
            default_value = ""
            length = ""
            for tr in general_table.find_all('tr'):
                th = tr.find('th')
                if th and th.text.strip() in required_ths:
                    if th.text.strip() == 'Table:':
                        td = tr.find('td')
                        if td is not None:
                            cdc_key = td.text.strip()

        if references_anchor is not None:
            general_table1 = references_anchor.find_next('table')

            # get the data rows for the required columns
            required_ths = ["Table:"]
            data_rows = []
            allow_null_values = ""
            default_value = ""
            length = ""
            for tr in general_table1.find_all('tr'):
                th = tr.find('th')
                if th and th.text.strip() in required_ths:
                    if th.text.strip() == 'Table:':
                        td = tr.find('td')
                        if td is not None:
                            cdc_value = td.text.strip()

            key_value_list.append((cdc_key, cdc_value))  # Append key-value pair
        return key_value_list



