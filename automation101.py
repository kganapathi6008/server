import os
from urllib.parse import urljoin
import pandas as pd
from bs4 import BeautifulSoup
import requests
from collect_data import collect_data
from virtual import virtual
from user_def import user_def
from source_table import source_table
from header import header
from business_rules import business_rules
from constants import constants
from parameter import parameter
from virtual_order1 import virtual_order1
from join1 import join_1
from auto102 import ma_desc
from indexes import indexes
from business_rules3 import business_rules3
from cdcList import cdcList
from source_tables import source_tables

def get_urls(html_paths,folder_path,fileUrl):
    all_options = []
    all_urls = []


    # read the HTML files
    for html_path in html_paths:
        with open(html_path, 'rb') as f:
            html_bytes = f.read()
        html = html_bytes.decode('utf-16')
        soup = BeautifulSoup(html, 'html.parser')

        # find the second frame tag
        frame2 = soup.find_all('frame')[1]

        if frame2 is not None:
            # get the src attribute of the second frame tag
            frame2_src = frame2['src']

            # read the HTML file pointed to by the src attribute
            with open(os.path.join(os.path.dirname(html_path), frame2_src), 'rb') as f:
                frame2_bytes = f.read()

            # decode the HTML file using utf-8 encoding
            frame2_html = frame2_bytes.decode('utf-16')

            # create a BeautifulSoup object from the HTML in the second frame
            frame2_soup = BeautifulSoup(frame2_html, 'html.parser')

            # navigate to the body tag in the HTML of the second frame
            body = frame2_soup.find('body')

            if body is not None:
                # find the first table tag after the a tag with name=References
                references_a = body.find('a', {'name': 'REFERENCES'})
                if references_a is not None:
                    table = references_a.find_next('table')
                    if table is not None:
                        # find all the a tags in the table that have a class attribute of "NAV"
                        table_rows = references_a.find_all('tr')[1:]




                        nav_links = table.find_all('a', {'class': 'NAV'})


                        options = [nav_link.text for nav_link in nav_links]
                        urls = [urljoin(os.path.dirname(frame2_src), nav_link['href']) for nav_link in nav_links]
                        urls_text = [nav_link.contents[0] for nav_link in nav_links]
                        # add the options and URLs to the master lists
                        all_options += options
                        all_urls += urls





                    else:
                        print(f'No table tag found after the a tag with name=References in {html_path}.')
                else:
                    print(f'No a tag found with name=References in {html_path}.')
            else:
                print(f'No body tag found in the second frame of {html_path}.')
        else:
            print('No frame tag found in the HTML.')






    for user_choice in (all_options):
        join_list_final = []


        new_df1_user_def = pd.DataFrame(
            columns=['', 'User Defined Function', 'Description1', 'Function Return Type',
                         'Description2', 'Required', 'DataType', 'Col', 'Table', 'Expr', 'Const',
                         'Values'])
        data_df = pd.DataFrame(
            columns=['', 'Name', 'Long Name', 'Description',
                         'Length', 'Decimals', 'Type', 'Rule Y/N', 'Structured Rules', 'Data Element'])
        data_const = pd.DataFrame(
            columns=['', 'Name', 'Length', 'Data Type', 'Value', 'Data Element'])
        data_para = pd.DataFrame(
            columns=['', 'Name', 'Description', 'Type', 'Length', 'Decimals'])
        data_index = pd.DataFrame(
            columns=['', 'Target Table', 'Index Table', 'Index Name', 'Key Fields', 'Sequence'])

        # initialize empty lists to store options and URLs from each HTML file

        cdc_list = []

        url = all_urls[all_options.index(user_choice)]
        url = '/'.join(fileUrl.split('/')) + '/data_aq/' + url



        my_list = source_table(url)

        data = []
        data = header(url, my_list, user_choice)

        join_list_final = join_1(url, join_list_final)
        res_map_des = ma_desc(url)
        header_list, data_list = business_rules(url)
        header_list, data_list = business_rules3(url, header_list, data_list)
        df_user_final = user_def(url, new_df1_user_def)
        q = virtual_order1(url, user_choice, data_df)
        dfdata = virtual(url, user_choice, data_df, q)
        data_para = parameter(url, data_para)
        data_const = constants(url, data_const)

        ylist = cdcList(url)
        dataframes1,headingsxx = source_tables(url)
        output_path=collect_data(url, user_choice, my_list, data, df_user_final, dfdata, folder_path, join_list_final,
                         res_map_des, header_list, data_list, data_const, data_para, data_index, ylist,dataframes1,headingsxx)




