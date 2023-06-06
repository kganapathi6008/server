import os
from bs4 import BeautifulSoup
from datastuff import datastuff
import pandas as pd
from cdcList2 import cdcList2
def cdcList(html_path):
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
        references_anchor = frame2_soup.find('a', {'name': 'TABLES'})
        if references_anchor is not None:
            references_table = references_anchor.find_next('table')

            if references_table is not None:
                # extract data from the table
                rows = references_table.find_all('tr')[1:]
                if len(rows) > 0:
                    first_row = rows[0]
                    columns = first_row.find_all('td')

                    if len(columns) > 1:
                        second_column = columns[1]
                        match_cdc = second_column.get_text().strip( )
                        match_cdc1 = match_cdc if match_cdc.endswith('CDC') else None
                        if match_cdc1 is not None:
                            key_value_list = []
                            # Remove the last three parts from the HTML path
                            html_path_parts = html_path.split("/")
                            updated_html_path = "/".join(html_path_parts[:-3])

                            # Append the desired path
                            desired_path = "/chg_dta_cptr_dfn/chgdtacptrDfn-list.htm"
                            updated_html_path += desired_path
                            key_value_list=cdcList2(updated_html_path,key_value_list)
                            # Create a new list for matched key-value pairs
                            ylist = []

                            # Iterate through key-value pairs in key_value_list
                            for key, value in key_value_list:
                                if key == match_cdc1:
                                    ylist.append(value)
                                    ylist.append(key)

                            return(ylist)


