from bs4 import BeautifulSoup
import os


def ma_desc(url):
    # set the path to the HTML file
    html_path =url

    # read the HTML file
    with open(html_path, 'rb') as f:
        html_bytes = f.read()

    # decode the HTML file using utf-16 encoding
    html = html_bytes.decode('utf-16')

    # create a BeautifulSoup object from the HTML
    soup = BeautifulSoup(html, 'html.parser')

    # find the first frame tag
    frame = soup.find_all('frame')[0]

    if frame is not None:
        # get the src attribute of the first frame tag
        frame_src = frame['src']

        # read the HTML file pointed to by the src attribute
        with open(os.path.join(os.path.dirname(html_path), frame_src), 'rb') as f:
            frame_bytes = f.read()

        # decode the HTML file using utf-16 encoding
        frame_html = frame_bytes.decode('utf-16')

        # create a BeautifulSoup object from the HTML in the first frame
        frame_soup = BeautifulSoup(frame_html, 'html.parser')

        # find all table tags in the HTML of the first frame
        tables = frame_soup.find_all('table')

        # print the data of the first table found
        table = tables[0]

        for row in table.find_all('tr'):
            row_data = [cell.text.strip() for cell in row.find_all('td')]
            if len(row_data) > 1:
                result = row_data[1].split("\n - ")[1]


        return result



