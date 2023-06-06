import os
from bs4 import BeautifulSoup
from datastuff import datastuff
import pandas as pd
from combinePdf import combine
from indexes import indexes
from sql_table import sql_table
from push import push

def collect_data(url_collect,user_choice,my_list,data,df_user_final,dfdata,folder_path,join_list_final,res_map_des,header_list,data_list,data_const,data_para,data_index,ylist,dataframes1,headingsxx):


    # set the path to the HTML file
    html_path = url_collect
    df = pd.DataFrame(
        columns=['Target Table', 'Target Columns','Target SQL Column Name', 'Data Type1', 'Length/Precision', 'PK/Nullable','Accumulate', 'Default Value1',' ',
                 'Source Table(s)', 'Source Column','Source SQL Column Name', 'Data Type2', 'Length/Precision2', 'Transformation Logic',
                 'Error Handling rules (if any)','Push Table Name1','Push Table Columns1','Push Table Name2','Push Table Columns2','Push Table Name3','Push Table Columns3'])
    df1 = pd.DataFrame(
        columns=['', '', '', '','', '',
                 '', '', '', '', '',
                 ''])
    push_def = pd.DataFrame(
        columns=['', 'Name', 'Remote Table', 'Remote Schema', 'Push Database Name'])
    # read the HTML file
    with open(html_path, 'rb') as f:
        html_bytes = f.read()

    # decode the HTML file using utf-16 encoding
    html = html_bytes.decode('utf-16')

    # create a BeautifulSoup object from the HTML
    soup = BeautifulSoup(html, 'html.parser')
    list_list=[]
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

        # find the table tag that follows the "References" anchor tag
        references_anchor = frame2_soup.find('a', {'name': 'REGISTERED DATA SETS'})
        if references_anchor is not None:
            references_table = references_anchor.find_next('table')

            # find all the URLs of class "NAV" in the table
            nav_urls = references_table.find_all('a', {'class': 'NAV'})

            # count the URLs and call the nextup function with each URL as a parameter
            count = 0

            for url in nav_urls:
                url_href = url['href'].replace('-RDS-', '')
                new_href=url_href.lstrip("./").replace("RDS-", "")
                new_href = new_href.rstrip(".htm")

                list_list.append(new_href)


                full_url = html_path.rsplit("/", 4)[0] +"/data_mgt/data_sets/" + url_href.lstrip("./").replace("RDS-", "")

                count += 1
                # extract the last part of the URL and put it in the "Target Table" column
                target_table = os.path.splitext(os.path.basename(full_url))[0]

                df=datastuff(full_url,df,target_table,my_list,user_choice)


                data_index=indexes(full_url,data_index)
                df=sql_table(df,html_path)

                push_def,df = push(full_url, push_def,df,target_table)

            # Iterate over the values in the 11th column
            for index, value in df.iloc[:, 10].items():
                # Check if the value is a string
                if isinstance(value, str):
                    # Check if the value starts with "Z1VE"
                    if value.startswith("Z1VE"):
                        # Remove the prefix "Z1" from the value
                        df.iloc[index, 10] = value[2:]
                    # Check if the value starts with "Z1"
                    elif value.startswith("Z1"):
                        # Remove the entire value from the 11th column
                        df.iloc[index, 11] = ''
                        df.iloc[index, 10] = value[2:]
                        # or df.iloc[index, 10] = np.nan
                    # If the value doesn't start with "Z1" or "Z1VE", keep it as it is







        else:
            print('No "References" anchor tag found.')
    else:
        print('No second frame tag found in the HTML.')


    output_path=combine(df, df1,folder_path,user_choice,data,list_list,df_user_final,dfdata,my_list,join_list_final,res_map_des,header_list,data_list,data_const,data_para,data_index,ylist,push_def,dataframes1,headingsxx)
    return output_path




