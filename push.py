import os
from bs4 import BeautifulSoup
import pandas as pd
from push2 import push2

def push(url,push_def,df,target_table):
    html_path = url
    count=1

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
        references_anchor1 = frame2_soup.find('a', {'name': 'PushTables'})
        references_anchor2 = frame2_soup.find('a', {'name': 'DataSetViews'})

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
                            name_txt = cols[0].text.strip()
                            name_url = cols[0].find('a').get('href')
                            name_url1 = html_path.rsplit("/", 1)[0] + "/" + name_url.lstrip("./")
                            remote_table_txt = cols[1].text.strip()
                            remote_schema_txt= cols[2].text.strip()

                            push_dbname_txt= cols[3].text.strip()

                            df,count=push2(name_url1,name_txt,df,count,target_table)
                            count+=1
                        new_row = {'Name': name_txt,
                           'Remote Table': remote_table_txt, 'Remote Schema': remote_schema_txt, 'Push Database Name': push_dbname_txt}
                        push_def = pd.concat([push_def, pd.DataFrame(new_row, index=[0])])
        return push_def,df