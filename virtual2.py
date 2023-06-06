import os
from bs4 import BeautifulSoup
import pandas as pd

def virtual_2(html_path,Longnamevs,description_vs,length_vs,decimals_vs,type_vs,rule_vs,data_df,data_element_vs):
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
        needed =[]
        required_ths = ["System Name:"]
        # find the table tag that follows the "USER DEFINED FUNCTIONS" anchor tag
        references_anchor = frame2_soup.find('a', {'name': 'RULES'})

        general_anchor = frame2_soup.find('a', {'name': 'GENERAL'})
        general_anchor1 = frame2_soup.find('a', {'name': 'EXPRESSIONS'})
        if general_anchor is not None:
            general_table = general_anchor.find_next('table')
            for tr in general_table.find_all('tr'):
                th = tr.find('th')
                if th and th.text.strip() in required_ths:
                    if th.text.strip() == 'System Name:':
                        td = tr.find('td')
                        if td is not None:
                            needed = td.text.strip()

        if references_anchor is not None:
            references_table = references_anchor.find_next('table')

            if references_table is not None:

            # extract data from the table
                rows = references_table.find_all('tr')[1:]  # start from second row
                data = []
                for row in rows:
                    cols = row.find_all('td')
                    if len(cols) >= 1:
                        data.append(cols[0].text.strip())
                        data.append(cols[1].text.strip())
                        data.append(cols[2].text.strip())
                        data.append(cols[3].text.strip())
                # Use list comprehension to remove empty strings
                cleaned_data = [x for x in data if x != '']

                # Concatenate remaining strings with spaces between them
                result = ' '.join(cleaned_data)
                new_row = { 'Name': needed,
                                'Long Name': Longnamevs, 'Description': description_vs, 'Length':length_vs ,
                                'Decimals':decimals_vs , 'Type':type_vs , 'Rule Y/N':rule_vs,'Structured Rules':result,'Data Element':data_element_vs }
                data_df = pd.concat([data_df, pd.DataFrame(new_row, index=[0])])
            else:
                references_table1 = general_anchor1.find_next('table')

                if references_table1 is not None:

                    # extract data from the table
                    rows = references_table1.find_all('tr')[1:]  # start from second row
                    data = []
                    for row in rows:
                        cols = row.find_all('td')
                        if len(cols) >= 1:
                            data.append(cols[0].text.strip())

                            data.append(cols[1].text.strip())

                    cleaned_data = [x for x in data if x != '']

                    # Concatenate remaining strings with spaces between them
                    result ='"' + ' '.join(cleaned_data)


                    new_row = { 'Name': needed,
                               'Long Name': Longnamevs, 'Description': description_vs, 'Length': length_vs,
                               'Decimals': decimals_vs, 'Type': type_vs, 'Rule Y/N': rule_vs,
                               'Structured Rules': result,'Data Element':data_element_vs}

                    data_df = pd.concat([data_df, pd.DataFrame(new_row, index=[0])])
        if references_table is None and references_table1 is None:
                new_row = {'Name': needed,
                           'Long Name': Longnamevs, 'Description': description_vs, 'Length': length_vs,
                           'Decimals': decimals_vs, 'Type': type_vs, 'Rule Y/N': rule_vs,
                           'Structured Rules':'', 'Data Element': data_element_vs}

                data_df = pd.concat([data_df, pd.DataFrame(new_row, index=[0])])





        return(data_df)
