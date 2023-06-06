import os
from bs4 import BeautifulSoup
from business_rules2 import business_rules_2
import pandas as pd

def business_rules(url_collect):
    header_list = []
    data_list = []


    # set the path to the HTML file
    html_path = url_collect

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
                new_href = url_href.lstrip("./").replace("RDS-", "")
                new_href = new_href.rstrip(".htm")
                list_list.append(new_href)
                full_url = '/'.join(html_path.split('/')[:-1]) + '/' + url_href.lstrip('./')

                count += 1
                header_list, data_list=business_rules_2(full_url,header_list,data_list)




        else:
            print('No "References" anchor tag found.')
    else:
        print('No second frame tag found in the HTML.')
    for i, header in enumerate(header_list):
        if header.startswith('RDS-'):
            header_list[i] = header[4:]

    return header_list, data_list