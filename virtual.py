import os
from bs4 import BeautifulSoup
import pandas as pd
from virtual2 import virtual_2
from Virtual3 import virtual_3
from virtual_cor import virtual_cor

def virtual(html_path, user_choice, data_df,q):
    # read the HTML file
    df2 = pd.DataFrame(columns=['Name', 'Long Name', 'Description'])
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

        # find the table tag that follows the "Virtual Elements" anchor tag
        references_anchor = frame2_soup.find('a', {'name': 'VIRTUAL ELEMENTS'})
        references_anchor1 = frame2_soup.find('a', {'name': 'VIRTUAL CONSTANTS'})
        if references_anchor is not None and references_anchor1 is not None:
            virtual_function_tables = None
            for sibling in references_anchor.next_siblings:
                if sibling == references_anchor1:
                    break
                if hasattr(sibling, 'name') and sibling.name == 'table':
                    virtual_function_tables = sibling
                    break
            if virtual_function_tables:
                # extract data from the table
                sys_short_dict = {}
                while not q.empty():
                    link_text = q.get()

                    rows = virtual_function_tables.find_all('tr')[1:]  # start from second row
                    data = []

                    for row in rows:

                        cols = row.find_all('td')

                        user_defined_func = cols[0].text.strip()
                        if  link_text == user_defined_func:

                            url = cols[0].find('a').get('href')

                            dir_path = '/'.join(html_path.split('/')[:-1])

                            # Replace the last path component with user_choice and append the modified url
                            url = dir_path + '/' + url.split('/')[-1]
                            sys_short = virtual_cor(url)

                            if sys_short in sys_short_dict:
                                continue  # Skip to the next iteration if the sys_short already exists in the dictionary

                            sys_short_dict[sys_short] = True



                            Longnamevs=cols[0].text.strip()
                            description_vs=cols[1].text.strip()
                            length_vs=cols[2].text.strip()
                            decimals_vs=cols[3].text.strip()
                            type_vs=cols[4].text.strip()
                            rule_vs=cols[5].text.strip()
                            data_element_vs = cols[6].text.strip()

                            if user_choice =="REITMPLD":
                                    data_df=virtual_3(url,Longnamevs,description_vs,length_vs,decimals_vs,type_vs,rule_vs,data_df,data_element_vs)
                            else:
                                    data_df = virtual_2(url, Longnamevs, description_vs, length_vs, decimals_vs, type_vs,
                                                rule_vs, data_df,data_element_vs)
                            break






        else:
            print("Required anchor tags not found.")
    else:
        print(" Second frame not found.")
    return data_df
