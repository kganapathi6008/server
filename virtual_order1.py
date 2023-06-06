import os
from bs4 import BeautifulSoup
import pandas as pd

from queue import Queue

def virtual_order1(html_path, user_choice, data_df):
    # read the HTML file
    df2 = pd.DataFrame(columns=['Name', 'Long Name', 'Description'])
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
        general_anchor = frame2_soup.find('a', {'name': 'SEQUENCE'})
        # find the table tag that follows the "Virtual Elements" anchor tag
        references_anchor = frame2_soup.find('a', {'name': 'VIRTUAL ELEMENTS'})
        references_anchor1 = frame2_soup.find('a', {'name': 'VIRTUAL CONSTANTS'})
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
                list_VF = []
                for row in rows:
                    cols = row.find_all('td')

                    vf_go_to_queue = cols[0].text.strip()
                    list_VF.append(vf_go_to_queue)

                if general_anchor is not None:
                    references_table = general_anchor.find_next('table')

                    if references_table is not None:
                        q = Queue()
                        q1= Queue()
                        # extract data from the table
                        rows = references_table.find_all('tr')[1:]  # start from second row
                        for row in rows:
                            cols = row.find_all('td')

                            link_text = cols[0].text.strip()

                            if link_text in list_VF:
                                q.put(link_text)

            else:
               q=Queue


    return q

