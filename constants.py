import os
from bs4 import BeautifulSoup
import pandas as pd
from constants2 import constants2


def constants(html_path,data_const):
    # read the HTML file

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
        # find the table tag that follows the "Constants" anchor tag
        references_anchor = frame2_soup.find('a', {'name': 'VIRTUAL CONSTANTS'})
        references_anchor1 = frame2_soup.find('a', {'name': 'DATA ELEMENTS'})
        if references_anchor is not None and references_anchor1 is not None:
            virtual_function_tables = None
            for sibling in references_anchor.next_siblings:
                if sibling == references_anchor1:
                    break
                if hasattr(sibling, 'name') and sibling.name == 'table':
                    virtual_function_tables = sibling
                    break
            if virtual_function_tables:
                # extract data from the table
                rows = virtual_function_tables.find_all('tr')[1:]  # start from second row
                data = []
                for row in rows:
                    cols = row.find_all('td')
                    if len(cols) >= 1:
                        user_defined_func = cols[0].text.strip()
                        url = cols[0].find('a').get('href')


                        dir_path = '/'.join(html_path.split('/')[:-1])

                        # Replace the last path component with user_choice and append the modified url
                        url = dir_path+ '/' + url.split('/')[-1]
                        leg_th=cols[2].text.strip()
                        data_type=cols[4].text.strip()
                        data_elm=cols[5].text.strip()
                        data_const=constants2(url,data_const,leg_th,data_type,data_elm)

            
        else:
            print("Required anchor tags not found.")
    else:
            print(" Second frame not found.")
    return data_const




