import os
from bs4 import BeautifulSoup
import pandas as pd
from secondlast import second_last

def last_section(nav_url, df, my_list,user_choice):
    # set the path to the HTML file
    html_path = nav_url

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

        # find the anchor tag with name "INTERFACEMAPPINGDETAILS"
        mapping_details_anchor = frame2_soup.find('a', {'name': 'INTERFACEMAPPINGDETAILS'})

        if mapping_details_anchor is not None:
            # find the table tag that follows the anchor tag
            mapping_details_table = mapping_details_anchor.find_next('table')

            # iterate through each row in the table
            for row in mapping_details_table.find_all('tr'):
                # find the second column in the row
                second_column = row.find_all('td')[1] if len(row.find_all('td')) >= 2 else None

                if second_column is not None:
                    # extract the text from the second column
                    text = second_column.text.strip()

                    # check if the text matches the user_choice variable
                    if text == user_choice:
                        # find the fourth column in the row
                        fourth_column = row.find_all('td')[3] if len(row.find_all('td')) >= 4 else None

                        if fourth_column is not None:
                            # extract the text and URL from the fourth column
                            text = fourth_column.text.strip()
                            url = fourth_column.find('a')

                            if url is not None:
                                # convert the URL to the desired format
                                url_href = url['href'].replace('-RDS-', '')

                                html_path = html_path.replace("/", os.path.sep)

                                # Extract the parent directory from html_path
                                parent_dir = os.path.dirname(html_path)

                                # Join the parent directory with the url_href to generate the full path
                                full_url = os.path.normpath(os.path.join(parent_dir, url_href))

                                # check if any element in my_list matches the first 2 characters of text
                                for entry in my_list:
                                    if entry[-2:] == text[:2]:
                                        # write the matching entry to the 'Source Tables(s)' column of df
                                        df.loc[df.index[-1], 'Source Table(s)'] = entry
                                        break  # stop checking for further matches

                                # write the text to the 'Source Column' of the current row of the dataframe df
                                df.loc[df.index[-1], 'Source Column'] = text

                        df = second_last(full_url, df)

        # return the updated dataframe
        return df
