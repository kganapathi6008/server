import os
from bs4 import BeautifulSoup
from datastuff import datastuff
import pandas as pd
def sql_table(df,html_path):
    with open(html_path, 'rb') as f:
        html_bytes = f.read()

    # decode the HTML file using utf-16 encoding
    html = html_bytes.decode('utf-16')

    # create a BeautifulSoup object from the HTML
    soup = BeautifulSoup(html, 'html.parser')
    list_list=[]
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

        # find the table tag that follows the "References" anchor tag
        references_anchor1 = frame2_soup.find('a', {'name': 'DATA ELEMENTS'})
        references_anchor2 = frame2_soup.find('a', {'name': 'EXTERNAL CALLS'})
        if references_anchor1 is not None and references_anchor2 is not None:
            user_defined_tables = []
            for sibling in references_anchor1.next_siblings:
                if sibling == references_anchor2:
                    break
                if hasattr(sibling, 'name') and sibling.name == 'table':
                    user_defined_tables.append(sibling)

            if user_defined_tables:
                new_column_values = []
                # extract data from the table
                data = []
                for table in user_defined_tables:
                    rows = table.find_all('tr')[1:]  # start from second row
                    for row in rows:
                        cols = row.find_all('td')
                        if len(cols) >= 1:
                            name_to_match = cols[0].text.strip()
                            for idx, value in df.iloc[:, 2].items():
                                if value == name_to_match:
                                    # Print the corresponding value from the second column

                                    df.at[idx, "Source SQL Column Name"] = cols[2].text.strip()
                                    #new_column_values.append(cols[2].text.strip())
                #df.insert(12, "Source SQL Column Name", new_column_values)
            return df
