import os
from bs4 import BeautifulSoup
import pandas as pd

def user_def_2(html_path, data, user_defined_func, funcret):
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
        references_anchor = frame2_soup.find('a', {'name': 'PARAMETERS'})
        general_anchor = frame2_soup.find('a', {'name': 'GENERAL'})
        if general_anchor is not None:
            general_table = general_anchor.find_next('table')

            # get the data rows for the required columns
            required_ths = ["Description:"]
            data_rows = []
            allow_null_values = ""
            default_value = ""
            length = ""
            for tr in general_table.find_all('tr'):
                th = tr.find('th')
                if th and th.text.strip() in required_ths:
                    if th.text.strip() == 'Description:':
                        td = tr.find('td')
                        if td is not None:
                            description1 = td.text.strip()


        if references_anchor is not None:
            references_table = references_anchor.find_next('table')

            if references_table is not None:
                # extract data from the table
                rows = references_table.find_all('tr')[1:]  # start from second row
                rows_list = []
                for row in rows:
                    cols = row.find_all('td')
                    if len(cols) >= 1:
                        description2 = cols[0].text.strip()
                        required = cols[1].text.strip()
                        Data_Type = cols[2].text.strip()


                        Col = cols[3].text.strip()
                        Table = cols[4].text.strip()
                        Expr = cols[5].text.strip()
                        Const = cols[6].text.strip()
                        Values = cols[7].text.strip()

                        # create a dictionary with the row data
                        row_dict = {'':'','User Defined Function': user_defined_func, 'Description1': description1,
                                    'Function Return Type': funcret, 'Description2': description2, 'Required': required,
                                    'Data Type': Data_Type, 'Col': Col, 'Table': Table, 'Expr': Expr, 'Const': Const,
                                    'Values': Values}
                        rows_list.append(row_dict)

                # check if the DataFrame is empty or not
                if len(data) == 0:
                    # if the DataFrame is empty, create it from the list of rows
                    data = pd.DataFrame(rows_list)





                else:
                    # if the DataFrame is not empty, concatenate the new rows to it
                    new_data = pd.DataFrame(rows_list)
                    data = pd.concat([data, new_data], ignore_index=True)






            else:
                print("No table found")
        else:
            print("No anchor tag found")

    else:
        print("No second frame tag found")


    return data
