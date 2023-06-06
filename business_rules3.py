import os
from bs4 import BeautifulSoup
import pandas as pd
from business_rules4 import business_rules4
def business_rules3(html_path,header_list,data_list):
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

        # find the table tag that follows the "Virtual Elements" anchor tag
        references_anchor = frame2_soup.find('a', {'name': 'TABLES'})
        if references_anchor is not None:
            references_table = references_anchor.find_next('table')

            if references_table is not None:
                # extract data from the table
                rows = references_table.find_all('tr')[1:]  # start from second row
                rows_list = []
                for row in rows:
                    cols = row.find_all('td')
                    if len(cols) >= 1:
                        bus_rule_name = cols[0].text.strip()
                        bus_rule_url=cols[0].find('a').get('href')
                        user_def_url1 = html_path.rsplit("/", 1)[0] + "/" + bus_rule_url.lstrip("./")
                        header_list,data_list=business_rules4(user_def_url1,header_list,data_list,bus_rule_name)
    return header_list, data_list