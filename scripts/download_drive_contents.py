import yaml
import gdown
import os
from bs4 import BeautifulSoup
import re

GDOWN_OUTPUT_PATH = "content"

# Read settings from YAML config file
with open("_config.yml") as stream:
    try:
        config = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)
        print('Error loading YAML! aborting...')
        exit()

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
def rework_HTML(html_path: str, id_dict: dict[str, str]) -> None:
    with open(html_path, 'r') as file:
        html_content = file.read()

    soup = BeautifulSoup(html_content, 'html.parser')
    elements = soup.find_all(class_='doc-content')
    for element in elements:
        element['style'] = 'margin: auto; width: 50%;'
    
    # Fix hyperlinks!

    # Does this count as parsing HTML with regex? lmao
    pattern = r'/d/([a-zA-Z0-9_-]+)' # Matches document ids
    links = soup.find_all('a', href=re.compile(pattern))
    for link in links:
        match = re.search(pattern, link['href']) # This should always match (inefficient)
        document_id = match.group(1)
        if document_id in id_dict:
            link['href'] = relative_path(html_path, id_dict[document_id])

    with open(html_path, 'w', encoding='utf-8') as file:
        file.write(soup.prettify())

# Pull list of files using gdown
file_list = gdown.download_folder(config['drive_folder_path'], output=GDOWN_OUTPUT_PATH, skip_download=True)
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
    rework_HTML(html_path, id_dict)