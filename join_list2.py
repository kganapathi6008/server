import os
from bs4 import BeautifulSoup





def join_list2(url,join_list_final):


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

        # find the table tag that follows the "References" anchor tag
        references_anchor = frame2_soup.find('a', {'name': 'READ'})

        if references_anchor is not None:
            # find the next table after the "References" anchor tag
            references_table = references_anchor.find_next('table')
            if references_table is not None:

                next_references_table = references_table.find_next('table')

                # if the second table exists, print all the text in it
                if next_references_table is not None:

                    tr_tags = next_references_table.find_all('tr')

                    for i in range(1, len(tr_tags)):  # iterate through all rows except the first one
                        td_tags = tr_tags[i].find_all('td')
                        if len(td_tags) > 2:
                            # extract the data from the second and third td tags
                            data = td_tags[1].text.strip() + "=" + td_tags[2].text.strip().split("/")[-1]
                            if "'" not in td_tags[2].text.strip():
                                join_list_final.append(data)



                    return join_list_final