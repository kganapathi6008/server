import os
from bs4 import BeautifulSoup
import pandas as pd
from source_tables1 import source_tables1
def source_tables(html_path):
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

        # find the table tag that follows the "USER DEFINED FUNCTIONS" anchor tag
        references_anchor1 = frame2_soup.find('a', {'name': 'TABLES'})
        references_anchor2 = frame2_soup.find('a', {'name': 'SEQUENCE'})
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
                dataframes1 = []
                headingxx=[]
                for table in user_defined_tables:
                    rows = table.find_all('tr')[1:]  # start from second row
                    for row in rows:
                        cols = row.find_all('td')
                        if len(cols) >= 1:
                            source_table_name = cols[0].text.strip()
                            dir_path=html_path
                            dir_path = os.path.dirname(html_path)
                            #print(dir_path)


                            source_table_link = cols[0].find('a').get('href')

                            source_table_link=source_table_link.lstrip("./")
                            #print(source_table_link)
                            source_link = os.path.join(dir_path,source_table_link)
                            #print(dir_path)
                            #print(source_link)
                            #print(html_path)
                            heading = cols[0].text.strip()

                            df_source=source_tables1(source_link,heading)

                            headingxx.append(heading)
                            dataframes1.append(df_source)


                return dataframes1,headingxx
