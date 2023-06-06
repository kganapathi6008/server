import os
from bs4 import BeautifulSoup
import pandas as pd
def source_tables2(source_link,source_sql,df_source):
    html_path = source_link

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
        general_anchor = frame2_soup.find('a', {'name': 'GENERAL'})
        if general_anchor is not None:
            general_table = general_anchor.find_next('table')

            # get the data rows for the required columns
            required_ths = ["System Name:"]

            for tr in general_table.find_all('tr'):
                th = tr.find('th')
                if th and th.text.strip() in required_ths:
                    if th.text.strip() == 'System Name:':
                        td = tr.find('td')
                        if td is not None:
                            needed = td.text.strip()
                            needed = needed[:2] + '.' + needed[2:]
            source_tab_list = { 'Source Columns': needed, 'Source SQL Column Name': source_sql}
                            #new_data = pd.DataFrame(source_tab_list)
                            #df_source = pd.concat([df_source, new_data], ignore_index=False)
            df_source = pd.concat([df_source, pd.DataFrame(source_tab_list, index=[0])])
                            #f = df.reset_index(drop=True)
            return df_source


