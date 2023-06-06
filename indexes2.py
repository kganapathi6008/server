import os
import pandas as pd
from bs4 import BeautifulSoup
import requests
from indexes3 import indexes3
import urllib
from urllib.parse import urljoin
import os
def indexes2(url,index_name,target_table,data_index):
    html_path = url

    # Read the HTML file
    with open(html_path, 'rb') as f:
        html_bytes = f.read()

    # Decode the HTML file using utf-16 encoding
    html = html_bytes.decode('utf-16')

    # Create a BeautifulSoup object from the HTML
    soup = BeautifulSoup(html, 'html.parser')

    # Find the second frame tag
    frame2 = soup.find_all('frame')[1]

    if frame2 is not None:
        # Get the src attribute of the second frame tag
        frame2_src = frame2['src']

        # Read the HTML file pointed to by the src attribute
        with open(os.path.join(os.path.dirname(html_path), frame2_src), 'rb') as f:
            frame2_bytes = f.read()

        # Decode the HTML file using utf-16 encoding
        frame2_html = frame2_bytes.decode('utf-8')


        # Create a BeautifulSoup object from the HTML in the second frame
        frame2_soup = BeautifulSoup(frame2_html, 'html.parser')
        # find the table tag that follows the "GENERAL" anchor tag
        general_anchor = frame2_soup.find('a', {'name': 'GENERAL'})
        if general_anchor is not None:
            general_table = general_anchor.find_next('table')

            # get the data rows for the required columns
            required_ths = ["Index System Name:"]

            for tr in general_table.find_all('tr'):
                th = tr.find('th')
                if th and th.text.strip() in required_ths:
                    if th.text.strip() == 'Index System Name:':
                        td = tr.find('td')
                        if td is not None:
                            index_table = td.text.strip()
        references_anchor = frame2_soup.find('a', {'name': 'DETAILS'})


        if references_anchor is not None:
            references_table = references_anchor.find_next('table')

            # Find all the rows in the table, starting from the second row
            rows = references_table.find_all('tr')[1:]
            for row in rows:
                cols = row.find_all('td')
                if len(cols) >= 1:
                    index_name = cols[1].text.strip()
                    sequence= cols[0].text.strip()
                    sequence=str(int(sequence) // 10)
                    url_index = cols[1].find('a').get('href')


                    dir_path = html_path
                    dir_path = os.path.dirname(html_path)
                    for _ in range(1):
                        dir_path = os.path.dirname(dir_path)

                    #url_index = url_index[3:]
                    url_index=url_index.lstrip("../")



                    url_index1 = os.path.join(dir_path, url_index)

                    #C:\Users\USER\Downloads\RODS\data_mgt
                    #../ data_elems / ADDRSCRDAT.htm
                    #data_elems / ADDRSCRDAT.htm
                    #C:\Users\USER\Downloads\RODS\data_mgt\data_elems / ADDRSCRDAT.htm
                    #C:\Users\USER\Downloads\RODS\data_mgt

                    #url_index1 = dir_path.rsplit("/", 4)[0] + "/" + url_index.lstrip("../../")



                    data_index=indexes3(url_index1,index_table,target_table,index_name,sequence,data_index)

    return data_index

