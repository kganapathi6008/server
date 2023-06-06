import os
from bs4 import BeautifulSoup
import pandas as pd
from exceldata import extract_data
from last_section import last_section
def push2(name_url1,name_txt,df,count,target_table):
    html_path=name_url1
    row_index = 0
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
        references_anchor = frame2_soup.find('a', {'name': 'MAPPING'})
        if references_anchor is not None:
            references_table = references_anchor.find_next('table')

            if references_table is not None:
                # extract data from the table
                rows = references_table.find_all('tr')[1:]  # start from second row
                # Extract data from the second column and put it in the 18th column of the dataframe df
                for row in rows:
                    columns = row.find_all('td')
                    if len(columns) >= 2:
                        data = columns[1].text.strip()
                        match_it=columns[0].text.strip()
                        #matching_row_indices = df[(df['Target Columns'] == match_it)
                                                  #& (df['Target Table'] == target_table)].index
                        matching_row_indices = df[df['Target Columns'] == match_it].index

                        if count == 1:
                            df.loc[(df['Target Table'] == target_table) & (
                                df.index.isin(matching_row_indices)), 'Push Table Columns1'] = data
                            df.loc[(df['Target Table'] == target_table) & (
                                df.index.isin(matching_row_indices)), 'Push Table Name1'] = name_txt
                        elif count == 2:
                            df.loc[(df['Target Table'] == target_table) & (
                                df.index.isin(matching_row_indices)), 'Push Table Columns2'] = data
                            df.loc[(df['Target Table'] == target_table) & (
                                df.index.isin(matching_row_indices)), 'Push Table Name2'] = name_txt

                        row_index += 1
            return df,count




