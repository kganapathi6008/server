import os
from urllib.parse import urljoin
import pandas as pd
from bs4 import BeautifulSoup
import requests
from indexes2 import indexes2
def indexes(url,data_index):


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
        frame2_html = frame2_bytes.decode('utf-16')

        # Create a BeautifulSoup object from the HTML in the second frame
        frame2_soup = BeautifulSoup(frame2_html, 'html.parser')
        # find the table tag that follows the "GENERAL" anchor tag
        general_anchor = frame2_soup.find('a', {'name': 'General'})
        if general_anchor is not None:
            general_table = general_anchor.find_next('table')

            # get the data rows for the required columns
            required_ths = ["System Name"]

            for tr in general_table.find_all('tr'):
                tds = tr.find_all('td')  # Find all td elements in the row
                if len(tds) >= 2:  # Ensure that the row has at least two td elements
                    if tds[0].text.strip() in required_ths:
                        target_table = tds[1].text.strip()  # Extract the text from the second td element



        # Find the table tag that follows the "References" anchor tag
        references_anchor1 = frame2_soup.find('a', {'name': 'Indexes'})
        references_anchor2 = frame2_soup.find('a', {'name': 'Authorities'})
        if references_anchor1 is not None and references_anchor2 is not None:
            user_defined_tables = []
            for sibling in references_anchor1.next_siblings:
                if sibling == references_anchor2:
                    break
                if hasattr(sibling, 'name') and sibling.name == 'table':
                    user_defined_tables.append(sibling)

            if user_defined_tables:
                # extract data from the table
                data = []
                for table in user_defined_tables:
                    rows = table.find_all('tr')[1:]
                    for row in rows:
                        cells = row.find_all('td')

                        # Extract the URL from the first column of the row
                        index_name = cells[1].text.strip()
                        nav_link = cells[1].find('a', {'class': 'NAV'})
                        if nav_link:
                            nav_url = os.path.join(os.path.dirname(html_path), nav_link['href'])
                            nav_url = f"{os.path.abspath(nav_url)}"

                            # Extract the text from the seventh column of the row


                            data_index=indexes2(nav_url,index_name,target_table,data_index)

    return data_index