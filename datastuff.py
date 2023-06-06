import os
from bs4 import BeautifulSoup
import pandas as pd
from exceldata import extract_data
from last_section import last_section
def datastuff(url,df,target_table,my_list,user_choice):
    html_path = url

    # Read the HTML file
    with open(html_path, 'rb') as f:
        html_bytes = f.read()

    # Decode the HTML file using utf-16 encoding
    html = html_bytes.decode('utf-16')

    # Create a BeautifulSoup object from the HTML
    soup = BeautifulSoup(html, 'html.parser')

    # Find the second frame tag
    frame2 = soup.find_all('frame')[1]

    if frame2 is not None:
        # Get the src attribute of the second frame tag
        frame2_src = frame2['src']

        # Read the HTML file pointed to by the src attribute
        with open(os.path.join(os.path.dirname(html_path), frame2_src), 'rb') as f:
            frame2_bytes = f.read()

        # Decode the HTML file using utf-16 encoding
        frame2_html = frame2_bytes.decode('utf-16')

        # Create a BeautifulSoup object from the HTML in the second frame
        frame2_soup = BeautifulSoup(frame2_html, 'html.parser')
        # Find the table tag that follows the "References" anchor tag
        references_anchor = frame2_soup.find('a', {'name': 'DataElements'})
        references_anchor1 = frame2_soup.find('a', {'name': 'Dimensions'})
        pk=''

        if references_anchor is not None:
            references_table = references_anchor.find_next('table')

            # Find all the rows in the table, starting from the second row
            table_rows = references_table.find_all('tr')[1:]


            accumulate = ""

            # Loop over each row in the table
            for row in table_rows:
                cells = row.find_all('td')

                # Extract the URL from the first column of the row
                nav_link = cells[0].find('a', {'class': 'NAV'})

                if nav_link:
                    nav_url = os.path.join(os.path.dirname(html_path), nav_link['href'])
                    nav_url = f"{os.path.abspath(nav_url)}"

                    # Extract the text from the seventh column of the row
                    text = cells[6].text.strip()
                    url_text = cells[0].text.strip()
                    if references_anchor1 is not None:
                        references_table1 = references_anchor1.find_next('table')

                        # Find all the rows in the table, starting from the second row
                        table_rows1 = references_table1.find_all('tr')[1:]
                        # Look for the row where the URL matches nav_link
                        for row1 in table_rows1:
                            cells1 = row1.find_all('td')
                            url_cell = cells1[1].find('a', {'class': 'NAV'})
                            if url_cell == nav_link:
                                # Extract the text from the first column of that row
                                pk = cells1[0].text.strip()
                                pk = str(int(pk) // 10)


                                break
                            else:
                                pk = " "


                    # Accumulate the text from each row
                    accumulate = text

                    # Extract data and update DataFrame as before
                    df = extract_data(nav_url, df, my_list,url_text)
                    df.loc[df.index[-1], 'Target Table'] = target_table

                    df.loc[df.index[-1],'Accumulate']= accumulate
                    df.loc[df.index[-1], 'PK/Nullable'] = pk

                    df = last_section(nav_url, df, my_list,user_choice)



        else:
            print('No "References" anchor tag found.')

    else:
        print('No second frame tag found in the HTML.')



    return df

