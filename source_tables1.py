import os
from bs4 import BeautifulSoup
import pandas as pd
import openpyxl
from openpyxl import Workbook
from source_tables2 import source_tables2
import xlsxwriter
from openpyxl import load_workbook


def source_tables1(html_path, heading):
    # read the HTML file
    df_source = pd.DataFrame(
        columns=[ 'Source Columns', 'Source SQL Column Name'])




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
        references_anchor = frame2_soup.find('a', {'name': 'FIELDS'})
        if references_anchor is not None:
            references_table = references_anchor.find_next('table')

            if references_table is not None:
                # extract data from the table
                rows = references_table.find_all('tr')[1:]  # start from second row
                rows_list = []
                for row in rows:
                    cols = row.find_all('td')
                    if len(cols) >= 1:
                        source_table_name = cols[0].text.strip()
                        dir_path=html_path
                        dir_path = os.path.dirname(html_path)


                        source_table_link = cols[0].find('a').get('href')
                        source_table_link = source_table_link.lstrip("./")
                        source_link = os.path.join(dir_path,source_table_link)
                        source_sql = cols[0].text.strip()

                        df_source=source_tables2(source_link,source_sql,df_source)




                    #writer.save()

                            # Write the dataframes to the Excel file
                            #with pd.ExcelWriter(output_path, engine='xlsxwriter') as writer:


                                # Write df_source to the second sheet starting from the second row
                                #df_source.to_excel(writer, sheet_name='Sheet2', startrow=end, index=False, header=True)
                            #end = start + df_source.shape[0]



                return df_source
