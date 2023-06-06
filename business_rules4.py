import os
from bs4 import BeautifulSoup
import pandas as pd
def business_rules4(html_path,header_list,data_list,bus_rule_name):
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
        references_anchor = frame2_soup.find('a', {'name': 'RULES'})
        if references_anchor is not None:
            references_table = references_anchor.find_next('table')

            if references_table is not None:

            # extract data from the table
                rows = references_table.find_all('tr')[1:]  # start from second row
                data = []
                for row in rows:
                    cols = row.find_all('td')
                    if len(cols) >= 1:
                        data.append(cols[0].text.strip())
                        data.append(cols[1].text.strip())
                        data.append(cols[2].text.strip())
                        data.append(cols[3].text.strip())
                # Use list comprehension to remove empty strings
                cleaned_data = [x for x in data if x != '']

                # Concatenate remaining strings with spaces between them
                result = ' '.join(cleaned_data)
                header_list.append(bus_rule_name)
                data_list.append(result)
    return header_list, data_list