import urllib
import urllib.request
import gzip

def download_and_extract(file_name):
    base_url = 'https://datasets.imdbws.com/'
    url = base_url + file_name + '.gz'
    with urllib.request.urlopen(url) as response:
        # Decompress file
        with gzip.GzipFile(fileobj=response) as uncompressed:
            file_content = uncompressed.read()
        # write to file in binary mode 'wb'
        with open(file_name, 'wb') as f:
            f.write(file_content)

datasets = ['title.basics.tsv']

for file in datasets:
    download_and_extract(file)