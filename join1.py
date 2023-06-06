import os
from bs4 import BeautifulSoup
from join_list2 import join_list2




def join_1(url_collect,join_list_final):



    # set the path to the HTML file
    html_path = url_collect

    # read the HTML file
    with open(html_path, 'rb') as f:
        html_bytes = f.read()

    # decode the HTML file using utf-16 encoding
    html = html_bytes.decode('utf-16')

    # create a BeautifulSoup object from the HTML
    soup = BeautifulSoup(html, 'html.parser')
    list_list = []

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
        references_anchor = frame2_soup.find('a', {'name': 'TABLES'})
        if references_anchor is not None:
            references_table = references_anchor.find_next('table')
            # Find all the rows in the table, starting from the third row
            for tr_element in references_table.find_all('tr')[2:]:
                # find the first <td> element in the current <tr> and extract its text
                td_element = tr_element.find('td')
                # find the first <a> element in the <td> and get the href attribute
                url = td_element.find('a')['href']

                # get the directory path of the html file
                dir_path = os.path.dirname(html_path)

                # create the full URL by joining the directory path and the url
                full_url = os.path.join(dir_path, url.lstrip("./"))

                # replace "RDS-" and ".htm" with empty strings to get the final URL
                full_url = full_url.replace("RDS-", "").rstrip(".htm") + ".htm"

                # call the join_list2 function for the url
                join_list_final=join_list2(full_url,join_list_final)
        else:
            print('No "References" anchor tag found.')
    else:
        print('No second frame tag found in the HTML.')
    return join_list_final

