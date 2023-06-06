import os
from bs4 import BeautifulSoup
import pandas as pd
from user_def_2 import user_def_2


def user_def(html_path, df):
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
        references_anchor1 = frame2_soup.find('a', {'name': 'USER DEFINED FUNCTIONS'})
        references_anchor2 = frame2_soup.find('a', {'name': 'REGISTERED DATA SETS'})

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
                    rows = table.find_all('tr')[1:]  # start from second row
                    for row in rows:
                        cols = row.find_all('td')
                        if len(cols) >= 1:
                            user_defined_func = cols[0].text.strip()

                            funcret = cols[2].text.strip()

                            url_user_def_2 = cols[0].find('a').get('href')


                            user_def_url = html_path.rsplit("/", 4)[0] + "/" + url_user_def_2.lstrip("../../")


                            df = user_def_2(user_def_url, df, user_defined_func, funcret)

                # concatenate the extracted data with the existing dataframe
                new_data_df = pd.DataFrame(data)
                df = pd.concat([new_data_df, df], ignore_index=True)

        else:
            print("Required anchor tags not found")
    else:
        print("Second frame tag not found")

    return df
