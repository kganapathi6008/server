import os
from bs4 import BeautifulSoup
import pandas as pd
def constants2(url,data_const,leg_th,data_type,data_elm):
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
        sys_name=''
        value_1=''
        general_anchor = frame2_soup.find('a', {'name': 'GENERAL'})
        if general_anchor is not None:
            general_table = general_anchor.find_next('table')
            if general_table is not None and len(general_table.find_all('tr')) == 1:
                general_table=general_table.find_next('table')

            # get the data rows for the required columns
            required_ths = ["System Name:", "Value:"]
            data_rows = []
            allow_null_values = ""
            default_value = ""
            for tr in general_table.find_all('tr'):
                th = tr.find('th')
                if th and th.text.strip() in required_ths:
                    if th.text.strip() == 'System Name:':
                        td = tr.find('td')
                        if td is not None:
                            sys_name = td.text.strip()
                    elif th.text.strip() == 'Value:':
                        td = tr.find('td')
                        if td is not None:
                            value_1 = td.text.strip()
                    else:
                        print("required field not found")

        else:
            print("General anchor not found")
        #if sys_name is not None and value_1 is not None:

        new_row = {'Name': sys_name,
                   'Data Type': data_type, 'Length': leg_th, 'Value': value_1, 'Data Element': data_elm}

        data_const = pd.concat([data_const, pd.DataFrame(new_row, index=[0])])






        return data_const
        #print(sys_name)
        #print(value_1)


