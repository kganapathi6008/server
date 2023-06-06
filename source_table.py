import os
from bs4 import BeautifulSoup

def source_table(url):
    #print(f"Collecting data from file: {url}")

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

        # find the table tag that follows the "TABLES" anchor tag
        tables_anchor = frame2_soup.find('a', {'name': 'TABLES'})

        if tables_anchor is not None:
            # find the first table after the "TABLES" anchor tag
            tables_table = tables_anchor.find_next('table')

            # initialize an empty list to hold the extracted text
            my_list = []

            # iterate over all <tr> elements starting from the second
            for tr_element in tables_table.find_all('tr')[1:]:
                # find the first <td> element in the current <tr> and extract its text
                td_element = tr_element.find('td')
                text = td_element.text.strip()

                # append the extracted text to the list
                my_list.append(text)


            return my_list
    else:
        print("Error: could not find frame2")
