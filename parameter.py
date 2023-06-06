import os
from bs4 import BeautifulSoup
import pandas as pd

def parameter(html_path,data_para):
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
        references_anchor = frame2_soup.find('a', {'name': 'PARAMETERS'})
        references_anchor1 = frame2_soup.find('a', {'name': 'USERS'})
        if references_anchor is not None and references_anchor1 is not None:
            virtual_function_tables = None
            for sibling in references_anchor.next_siblings:
                if sibling == references_anchor1:
                    break
                if hasattr(sibling, 'name') and sibling.name == 'table':
                    virtual_function_tables = sibling
                    break
            if virtual_function_tables:


                rows = virtual_function_tables.find_all('tr')[1:]  # start from second row
                data = []
                for row in rows:

                    cols = row.find_all('td')
                    name = cols[0].text.strip()
                    description = cols[1].text.strip()
                    type = cols[2].text.strip()
                    length = cols[3].text.strip()
                    decimals= cols[4].text.strip()
                    new_row = {
                                   'Name': name, 'Description': description,'Type': type, 'Length':length,
                                   'Decimals': decimals}

                    data_para = pd.concat([data_para, pd.DataFrame(new_row, index=[0])])


    return data_para
