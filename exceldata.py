import os
from bs4 import BeautifulSoup
import pandas as pd

def extract_data(url, df,my_list,url_text):
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

            # get the data rows for the required columns
            required_ths = ["System Name:", "Data Type:", "Default Value:"]
            data_rows = []
            allow_null_values = ""
            default_value = ""
            for tr in general_table.find_all('tr'):
                th = tr.find('th')
                if th and th.text.strip() in required_ths:
                    if th.text.strip() == 'System Name:':
                        td = tr.find('td')
                        if td is not None:
                            target_column = td.text.strip()
                    elif th.text.strip() == 'Data Type:':
                        td = tr.find('td')
                        if td is not None:
                            data_type = td.text.strip()
                            # extract text and integer values separately
                            text_value = data_type.split('(')[0]
                            int_value = data_type.split('(')[-1].split(')')[0] if len(data_type.split('(')) > 1 else ''


                            data_rows.append([target_column,url_text, text_value, int_value])

                    elif th.text.strip() == 'Default Value:':
                        td = tr.find('td')
                        if td is not None:
                            default_value = td.text.strip()

            # append allow_null_values and default_value to the last row in data_rows
            if data_rows:
                last_row = data_rows[-1]
                last_row.extend([ default_value])

            # create a Pandas dataframe from the data
            new_df = pd.DataFrame(data_rows, columns=['Target Columns','Target SQL Column Name', 'Data Type1', 'Length/Precision',
                                                  'Default Value1'])



            # append the new rows of data to the input dataframe
            df = pd.concat([df, new_df], ignore_index=True)


            return df

