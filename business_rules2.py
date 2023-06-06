import os
from bs4 import BeautifulSoup
import pandas as pd

def business_rules_2(url_collect,header_list,data_list):
    businessHeader=os.path.splitext(os.path.basename(url_collect))[0]


    html_path = url_collect

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
        frame2_html = frame2_bytes.decode('utf-16')

        # Create a BeautifulSoup object from the HTML in the second frame
        frame2_soup = BeautifulSoup(frame2_html, 'html.parser')

        # Find the table tag that follows the "References" anchor tag
        references_anchor = frame2_soup.find('a', {'name': 'RULES'})
        if references_anchor is not None:
            references_table = references_anchor.find_next('table')
            if references_table is not None:
                # Find all the rows in the table, starting from the second row
                table_rows = references_table.find_all('tr')[1:]

                all_row_data = []
                for row in table_rows:
                    columns = row.find_all('td')

                    # Extract data from the first 4 columns
                    row_data = []
                    for i in range(4):
                        row_data.append(columns[i].text.strip())

                    # Add row data to all_row_data
                    all_row_data += row_data

                # Concatenate all_row_data into a single string
                all_data = " ".join(all_row_data)

                # Append all_data to data_list
                data_list.append(all_data)
                # Append businessHeader to header_list
                header_list.append(businessHeader)


    # Return both lists as a tuple

    return header_list, data_list