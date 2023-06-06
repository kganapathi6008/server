import os
from bs4 import BeautifulSoup
import pandas as pd


def second_last(url, df):
    # set the path to the HTML file
    html_path = url

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

        # find the table tag that follows the "GENERAL" anchor tag
        general_anchor = frame2_soup.find('a', {'name': 'GENERAL'})
        if general_anchor is not None:
            general_table = general_anchor.find_next('table')
            dec_value=0

            dat_type=''
            len_update=0


            # get the data rows for the required columns
            required_ths = ["Data Type:", "Length:", "Decimals:"]
            data_rows = []
            allow_null_values = ""
            default_value = ""
            for tr in general_table.find_all('tr'):
                th = tr.find('th')
                if th and th.text.strip() in required_ths:
                    if th.text.strip() == 'Data Type:':
                        td = tr.find('td')
                        if td is not None:
                            dat_type = td.text.strip()
                    elif th.text.strip() == 'Length:':
                        td = tr.find('td')
                        if td is not None:
                            len_update = td.text.strip()
                    elif th.text.strip() == 'Decimals:':
                        td = tr.find('td')
                        if td is not None:
                            dec_value = td.text.strip()

                # write the text to the 'Data Type2' and 'Length/Precision2' columns of the current row of the dataframe df
                df.loc[df.index[-1], 'Data Type2'] = dat_type
                if dec_value == 0 or dec_value is None:


                    df.loc[df.index[-1], 'Length/Precision2'] = str(len_update)

                elif dec_value != 0 and dec_value is not None:
                    df.loc[df.index[-1], 'Length/Precision2'] = f"{len_update}.{dec_value}".rstrip('.')





    return df
