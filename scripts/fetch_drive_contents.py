import configparser
from jinja2 import Template
import gdown
import os
from bs4 import BeautifulSoup
import re
from urllib.parse import urlparse, parse_qs

GDOWN_OUTPUT_PATH = "content"

'''
Returns a relative path from src_path to dest_path
'''
def relative_path(src_path: str, dest_path: str) -> str:
    src_split = os.path.normpath(src_path).split(os.path.sep)
    dest_split = os.path.normpath(dest_path).split(os.path.sep)

    for a, b in zip(src_split, dest_split):
        if a == b:
            src_split.remove(a)
            dest_split.remove(b)
    
    path_parts = ['.']
    path_parts.extend(['..']*(len(src_split) - 1))
    path_parts.extend(dest_split)

    return os.path.join(*path_parts)

# Makes the exported .HTML a little better for web design
# (centers content, etc.)
'''
Makes the exported .HTML a little better for the web. Currently, this function:
* Adds some html to <head>
* Cleans up links (removes Google trackers, etc.)
* Fixes inter-site hyperlinks
'''
def rework_HTML(html_path: str, id_dict: dict[str, str], template_path: str, config_path: str) -> None:
    # Load HTML into bs4
    with open(html_path, 'r') as file:
        html_content = file.read()
    soup = BeautifulSoup(html_content, 'html.parser')

    # Read template and config
    with open(template_path, 'r') as f:
        style_template = Template(f.read())
    config = configparser.ConfigParser()
    config.read(config_path)
    template_data = dict(config.items('LAYOUT'))

    # Append <head> with the filled template
    head = soup.find('head')
    head.append(BeautifulSoup(style_template.render(template_data), 'html.parser'))
    
    # General link cleanup
    links = soup.find_all('a')
    for link in links:
        parsed_url = urlparse(link['href'])
        link['href'] = parse_qs(parsed_url.query).get('q', [None])[0]

    # Fix hyperlinks
    # Does this count as parsing HTML with regex? lmao
    pattern = r'/d/([a-zA-Z0-9_-]+)' # Matches document ids
    links = soup.find_all('a', href=re.compile(pattern))
    for link in links:
        match = re.search(pattern, link['href']) # This should always match (inefficient)
        document_id = match.group(1)
        if document_id in id_dict:
            link['href'] = relative_path(html_path, id_dict[document_id])
    
    # Write to output path
    with open(html_path, 'w', encoding='utf-8') as file:
        if 'true' in config['GENERAL']['PrettifyHTML'].lower():
            file.write(soup.prettify())
        else:
            file.write(str(soup))

# Read settings from config file
drive_folder_path = ''
with open('LINK_TO_DRIVE_FOLDER', 'r') as f:
    drive_folder_path = f.readline().strip()

if len(drive_folder_path) > 10:
    # Pull list of files using gdown
    file_list = gdown.download_folder(drive_folder_path, output=GDOWN_OUTPUT_PATH, skip_download=True)

    # gdown.download_folder() returns None if it it fails to retreive folder contents
    if file_list is not None:
        id_dict = {}

        for to_download in file_list:
            # Ensure local directory structure exists
            root_dir = os.path.split(to_download.local_path)[0]
            if not os.path.exists(root_dir):
                os.makedirs(root_dir)

            html_path = to_download.local_path + '.html'
            gdown.download(id=to_download.id,
                        output=html_path,
                        format="html")

            id_dict[to_download.id] = html_path

        print("Fixing up HTML...")
        for to_download in file_list:
            html_path = to_download.local_path + '.html'
            rework_HTML(html_path,
                        id_dict,
                        'templates/style_mod.jinja',
                        'CONFIG.ini')
    else:
        print("gdown failed to download the folder!")
else:
    print('Drive folder not present in config!')